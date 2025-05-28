"""
Asynchronous database layer for the BGMI Warrior Bot by IBR.
Uses Motor for async MongoDB operations.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any

import motor.motor_asyncio
import pymongo
import pytz
from bson import ObjectId

from config import BotConfig
from models import UserAction, UserProfile, UserStatus

logger = logging.getLogger('bgmi_warrior_bot.database')


class Database:
    """Asynchronous MongoDB database manager"""
    
    def __init__(self, config: BotConfig):
        """Initialize database connection"""
        self.client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_URI)
        self.db = self.client[config.DATABASE_NAME]
        self.actions = self.db[config.COLLECTION_NAME]
        self.users = self.db['users']
        self.logs = self.db['logs']
        self._timezone = pytz.timezone(config.TIMEZONE)
        # Don't call _ensure_indexes() directly here, it should be awaited
        
    async def initialize(self):
        """Initialize database and ensure indexes."""
        await self._ensure_indexes()
        logger.info("Database initialized and indexes created")
        
    async def _ensure_indexes(self):
        """Ensure necessary indexes exist for performance"""
        await self.actions.create_index([("user_id", pymongo.ASCENDING)])
        await self.actions.create_index([("timestamp", pymongo.DESCENDING)])
        await self.users.create_index([("user_id", pymongo.ASCENDING)], unique=True)
        await self.logs.create_index([("timestamp", pymongo.DESCENDING)])
        logger.info("Database indexes created successfully")
    
    async def get_user_language(self, user_id: int, default: str = "en") -> str:
        """Get user's preferred language"""
        user = await self.get_user_profile(user_id)
        if user:
            return user.language
        return default

    async def set_user_language(self, user_id: int, language: str) -> bool:
        """Set user's preferred language"""
        user = await self.get_user_profile(user_id)
        if user:
            user.language = language
            return await self.save_user_profile(user)
        else:
            # Create new user profile if it doesn't exist
            user = UserProfile(user_id=user_id, language=language)
            return await self.save_user_profile(user)
    async def get_user_profile(self, user_id: int) -> Optional[UserProfile]:
        """Get user profile by user ID"""
        user_data = await self.users.find_one({"user_id": user_id})
        if not user_data:
            return None
        return UserProfile(**user_data)
    
    async def save_user_profile(self, profile: UserProfile) -> bool:
        """Save or update user profile"""
        user_dict = profile.dict()
        result = await self.users.update_one(
            {"user_id": profile.user_id},
            {"$set": user_dict},
            upsert=True
        )
        return result.acknowledged
    
    async def authorize_user(self, user_id: int, expire_time: datetime,
                             username: Optional[str] = None) -> bool:
        """Authorize a user with expiration time"""
        try:
            profile = await self.get_user_profile(user_id) or UserProfile(
                user_id=user_id,
                username=username
            )
            profile.status = UserStatus.AUTHORIZED
            profile.expire_time = expire_time
            
            return await self.save_user_profile(profile)
        except Exception as e:
            logger.error(f"Error authorizing user {user_id}: {str(e)}")
            return False
    
    async def save_action(self, action: UserAction) -> bool:
        """Save a user action"""
        try:
            action_dict = action.dict()
            result = await self.actions.insert_one(action_dict)
            return result.acknowledged
        except Exception as e:
            logger.error(f"Error saving action: {str(e)}")
            return False
    
    async def get_user_actions(self, user_id: int, limit: int = 5) -> List[UserAction]:
        """Get most recent user actions"""
        cursor = self.actions.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit)
        
        actions = []
        async for doc in cursor:
            actions.append(UserAction(**doc))
        
        return actions
    
    async def get_today_action_count(self, user_id: int) -> int:
        """Get count of actions for today"""
        now = datetime.now(self._timezone)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_utc = today.astimezone(pytz.utc)
        
        count = await self.actions.count_documents({
            "user_id": user_id,
            "timestamp": {"$gte": today_utc}
        })
        
        return count
    
    async def increment_usage_count(self, user_id: int) -> int:
        """Increment usage count for user"""
        now = datetime.now(self._timezone)
        today_str = now.strftime('%Y-%m-%d')
        
        result = await self.users.update_one(
            {"user_id": user_id},
            {
                "$inc": {f"usage_count.{today_str}": 1},
                "$setOnInsert": {"user_id": user_id, "status": "regular"}
            },
            upsert=True
        )
        
        if result.acknowledged:
            user = await self.users.find_one({"user_id": user_id})
            return user.get("usage_count", {}).get(today_str, 0)
        
        return 0
    
    async def clear_expired_users(self) -> int:
        """Update status of expired users"""
        now = datetime.now(pytz.utc)
        result = await self.users.update_many(
            {
                "status": "authorized",
                "expire_time": {"$lte": now}
            },
            {"$set": {"status": "expired"}}
        )
        
        return result.modified_count
    
    async def get_all_users(self) -> List[UserProfile]:
        """Get all users"""
        cursor = self.users.find({})
        users = []
        
        async for doc in cursor:
            users.append(UserProfile(**doc))
            
        return users
    
    async def get_active_users_count(self) -> int:
        """Get count of active users (used the bot in the last 24h)"""
        yesterday = datetime.now(pytz.utc) - timedelta(days=1)
        
        pipeline = [
            {"$match": {"timestamp": {"$gte": yesterday}}},
            {"$group": {"_id": "$user_id"}},
            {"$count": "active_users"}
        ]
        
        result = await self.actions.aggregate(pipeline).to_list(1)
        if result and result[0].get("active_users"):
            return result[0]["active_users"]
        return 0
        
    async def log_activity(self, user_id: int, action_type: str, details: Dict[str, Any]) -> bool:
        """Log user activity"""
        try:
            log_entry = {
                "user_id": user_id,
                "action_type": action_type,
                "details": details,
                "timestamp": datetime.now(pytz.utc)
            }
            
            result = await self.logs.insert_one(log_entry)
            return result.acknowledged
        except Exception as e:
            logger.error(f"Error logging activity: {str(e)}")
            return False
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        now = datetime.now(pytz.utc)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        authorized_users = await self.users.count_documents({"status": "authorized"})
        today_actions = await self.actions.count_documents({"timestamp": {"$gte": today}})
        total_actions = await self.actions.count_documents({})
        total_users = await self.users.count_documents({})
        
        # Get actions per day for the last 7 days
        seven_days_ago = now - timedelta(days=7)
        pipeline = [
            {"$match": {"timestamp": {"$gte": seven_days_ago}}},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}
                    },
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        daily_actions = await self.actions.aggregate(pipeline).to_list(7)
        
        return {
            "authorized_users": authorized_users,
            "today_actions": today_actions,
            "total_actions": total_actions,
            "total_users": total_users,
            "daily_actions": {item["_id"]: item["count"] for item in daily_actions}
        }