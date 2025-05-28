"""
Middlewares for the BGMI Warrior Bot.
Includes request logging, rate limiting, and authorization checks.
"""
import logging
import time
from datetime import datetime
from typing import Callable, Dict, List, Optional, Set, Any

import pytz
from telebot import TeleBot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, Update

from config import BotConfig
from database import Database

logger = logging.getLogger('bgmi_warrior_bot.middleware')

def setup_middlewares(bot: AsyncTeleBot, db: Database, config: BotConfig):
    """Set up all middlewares for the bot"""
    # Register middlewares
    bot.setup_middleware(LoggingMiddleware(config.TIMEZONE))
    bot.setup_middleware(RateLimitMiddleware(db, config))
    bot.setup_middleware(AuthorizationMiddleware(db, config))

class LoggingMiddleware:
    """Middleware for logging all incoming messages"""
    
    def __init__(self, timezone: str):
        self.timezone = pytz.timezone(timezone)
        # Add this line to specify which update types to process
        self.update_types = ['message', 'edited_message', 'callback_query']
        
    async def pre_process(self, message: Message, data: Dict):
        """Log incoming message before processing"""
        user_id = message.from_user.id if message.from_user else "Unknown"
        username = message.from_user.username or "Unknown"
        chat_id = message.chat.id if message.chat else "Unknown"
        chat_type = message.chat.type if message.chat else "Unknown"
        
        logger.info(
            f"Received message from user {user_id} (@{username}) "
            f"in chat {chat_id} ({chat_type}): {message.text}"
        )
        
        # Add processing start time for performance tracking
        data['process_start'] = time.time()
        
        return True
    
    async def post_process(self, message: Message, data: Dict, exception: Optional[Exception] = None):
        """Log after message processing"""
        if 'process_start' in data:
            process_time = time.time() - data['process_start']
            logger.info(f"Message processed in {process_time:.3f} seconds")
        
        if exception:
            logger.error(f"Error processing message: {str(exception)}", exc_info=True)

class RateLimitMiddleware:
    """Middleware for rate limiting users in group chats"""
    
    def __init__(self, db: Database, config: BotConfig):
        self.db = db
        self.config = config
        self.exempt_commands = {'start', 'help', 'auth', 'usage', 'ping'}
        # Add this line to specify which update types to process
        self.update_types = ['message']
        
    async def pre_process(self, message: Message, data: Dict):
        """Check if user has exceeded rate limit"""
        # Skip rate limiting for exempt commands
        if message.text and message.text.startswith('/'):
            command = message.text.split()[0][1:].split('@')[0]
            if command in self.exempt_commands:
                return True
        
        user_id = message.from_user.id
        chat_type = message.chat.type
        
        # Skip rate limiting for private chats and admin users
        if chat_type == 'private' or user_id in self.config.AUTHORIZED_USERS:
            return True
        
        # Check if user is authorized (premium)
        user = await self.db.get_user_profile(user_id)
        if user and user.is_authorized(pytz.timezone(self.config.TIMEZONE)):
            return True
        
        # Check rate limit for group chats
        if chat_type in ('group', 'supergroup'):
            today_count = await self.db.get_today_action_count(user_id)
            
            if today_count >= self.config.RATE_LIMIT:
                await message.bot.reply_to(
                    message,
                    f"⛔ *Ammo Depleted!* You've fired {self.config.RATE_LIMIT} strikes today in this group!\n\n"
                    "🎯 *Go Warlord:* `/auth` in private for unlimited frags!",
                    parse_mode='Markdown'
                )
                return False
        
        return True

class AuthorizationMiddleware:
    """Middleware for checking user authorization"""
    
    def __init__(self, db: Database, config: BotConfig):
        self.db = db
        self.config = config
        self.public_commands = {'start', 'help', 'auth', 'ping'}
        # Add this line to specify which update types to process
        self.update_types = ['message', 'callback_query']
        
    async def pre_process(self, message: Any, data: Dict):
        """Check if user is authorized for restricted commands"""
        # Handle different types of updates
        if hasattr(message, 'data') and message.data:  # Callback query
            user_id = message.from_user.id
            # Admin users are always authorized for callbacks
            if user_id in self.config.AUTHORIZED_USERS:
                data['is_admin'] = True
                return True
            return True  # Allow all callbacks for now, we'll check permissions when handling
            
        # Regular message
        if not hasattr(message, 'text'):
            return True
            
        # Allow public commands for everyone
        if message.text and message.text.startswith('/'):
            command = message.text.split()[0][1:].split('@')[0]
            if command in self.public_commands:
                return True
        
        user_id = message.from_user.id
        chat_type = message.chat.type
        
        # Admin users are always authorized
        if user_id in self.config.AUTHORIZED_USERS:
            data['is_admin'] = True
            return True
        
        # For private chats, check authorization for non-public commands
        if chat_type == 'private':
            # Only check authorization for commands that aren't public
            if message.text and message.text.startswith('/'):
                command = message.text.split()[0][1:].split('@')[0]
                if command not in self.public_commands:
                    user = await self.db.get_user_profile(user_id)
                    if not user or not user.is_authorized(pytz.timezone(self.config.TIMEZONE)):
                        await message.bot.reply_to(
                            message,
                            "🚫 *Warlord Pass Needed!* Drop `/auth` to unlock!",
                            parse_mode='Markdown'
                        )
                        return False
        
        # For DDoS actions in private chat, check authorization
        if chat_type == 'private' and message.text and not message.text.startswith('/'):
            user = await self.db.get_user_profile(user_id)
            if not user or not user.is_authorized(pytz.timezone(self.config.TIMEZONE)):
                await message.bot.reply_to(
                    message,
                    "🚫 *Warlord Squad Only!* Drop `/auth` to join the fray! 🔥\n\n"
                    "*Built by Ibr, the BGMI Beast!*",
                    parse_mode='Markdown'
                )
                return False
        
        return True