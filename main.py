#!/usr/bin/env python3
"""
BGMI Warrior Bot by IBR - Premium Edition
Entry point for the Telegram bot application
"""
import asyncio
import logging
import os
import signal
import sys
from datetime import datetime

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telebot.async_telebot import AsyncTeleBot

from action_service import ActionService
from config import load_config
from database import Database
from command_handlers import CommandHandlers
from middlewares import setup_middlewares

# Setup directories
os.makedirs("bot_logs", exist_ok=True)

# Load configuration
config = load_config()

# Configure logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create logger
logger = logging.getLogger('bgmi_warrior_bot')

# Add console handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

# Initialize bot
bot = AsyncTeleBot(config.TOKEN)

# Create scheduler
scheduler = AsyncIOScheduler(timezone=pytz.utc)

async def main():
    """Main entry point for the application"""
    try:
        logger.info("Starting BGMI Warrior Bot by IBR - Premium Edition")
        
        # Initialize services
        db = Database(config)
        await db.initialize()  # Await the initialization
        action_service = ActionService(config.ACTION_BINARY_PATH)
        
        # Apply middlewares
        setup_middlewares(bot, db, config)
        
        # Initialize command handlers
        handlers = CommandHandlers(bot, db, action_service, config, scheduler)
        
        # Start scheduler
        scheduler.start()
        
        # Schedule periodic tasks
        scheduler.add_job(
            db.clear_expired_users,
            'interval',
            minutes=15,
            id='clear_expired_users'
        )
        
        # Run the bot
        logger.info("Bot is running. Press CTRL+C to stop.")
        await bot.polling(non_stop=True, timeout=60)
        
    except Exception as e:
        logger.critical(f"Critical error: {str(e)}", exc_info=True)
        return 1
    finally:
        # Clean shutdown
        await action_service.stop_all_actions()
        scheduler.shutdown()
        logger.info("Bot has been stopped")
    
    return 0

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Received shutdown signal, exiting...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the main function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)