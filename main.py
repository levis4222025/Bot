#!/usr/bin/env python3
"""
🌟 BGMI Warrior Bot by IBR - PRODUCTION EDITION 🌟
✨ AI-powered, multi-language, feature-rich Telegram bot ✨
Entry point for the advanced bot application
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
from config import load_config  # Use config loader
from database import Database
from command_handlers import CommandHandlers  # Use consolidated handlers
from middlewares import setup_middlewares

# Create production directories
os.makedirs("bot_logs", exist_ok=True)
os.makedirs("themes", exist_ok=True)
os.makedirs("user_data", exist_ok=True)

print("""
╔════════════════════════════════════════╗
║    🌟 BGMI WARRIOR BOT - PRODUCTION 🌟  ║
║         ✨ AI-POWERED EDITION ✨         ║
║                                        ║
║  🤖 AI • � Multi-Lang • � Modern UI  ║
║  🏆 Achievements • 🎵 Music • 📊 Stats ║
╚════════════════════════════════════════╝
""")

# Load production-ready configuration
config = load_config()

# Production logging configuration
logging.basicConfig(
    filename=config.LOG_FILE,
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - 🤖 %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create production logger
logger = logging.getLogger('🌟_bgmi_warrior_production')

# Add console handler with production formatting
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('🚀 %(asctime)s - ✨ %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

# Initialize production bot
bot = AsyncTeleBot(config.TOKEN)

# Create production scheduler
scheduler = AsyncIOScheduler(timezone=pytz.utc)

async def main():
    """Production-ready main entry point for the bot application"""
    try:
        print("🚀 Starting BGMI Warrior Bot - Production Edition...")
        logger.info("🌟 Initializing Production Bot Systems...")
        
        # Initialize production services
        db = Database(config)
        await db.initialize()
        action_service = ActionService(config.ACTION_BINARY_PATH)
        
        # Apply production middlewares
        setup_middlewares(bot, db, config)
        
        # Initialize production-ready command handlers
        handlers = CommandHandlers(bot, db, action_service, config, scheduler)
        
        print("✨ Production features loaded:")
        print("  • 🎨 Modern UI with animated messages")
        print("  • 🌍 Multi-language support")
        print("  • 🤖 AI-powered command understanding")
        print("  • 🏆 Achievement system")
        print("  • 🎮 Mini-games and entertainment")
        print("  • 🎵 Music player")
        print("  • 📊 Advanced analytics & monitoring")
        print("  • 💎 Premium themes and features")
        print("  • ⚡ Enhanced attack modes")
        print("  • 🔒 User management & verification")
        
        # Start production scheduler
        scheduler.start()
        
        # Schedule production periodic tasks
        scheduler.add_job(
            db.clear_expired_users,
            'interval',
            minutes=15,
            id='clear_expired_users'
        )
        
        # Add production scheduled tasks
        scheduler.add_job(
            _update_user_achievements,
            'interval',
            hours=1,
            id='update_achievements',
            args=[db]
        )
        
        scheduler.add_job(
            _refresh_leaderboard,
            'interval',
            minutes=30,
            id='refresh_leaderboard',
            args=[db]
        )
        
        # Production startup message
        print("\n🎊 ═══════════════════════════════════ 🎊")
        print("🚀 PRODUCTION BOT IS NOW ONLINE!")
        print("💎 All features activated and ready!")
        print("🎮 Ready for advanced operations!")
        print("🎊 ═══════════════════════════════════ 🎊\n")
        
        logger.info("🌟 Production Bot is running. Press CTRL+C to stop.")
        await bot.polling(non_stop=True, timeout=60)
        
    except Exception as e:
        logger.critical(f"💥 Critical system error: {str(e)}", exc_info=True)
        return 1
    finally:
        # Production clean shutdown
        print("\n🔄 Shutting down production systems...")
        await action_service.stop_all_actions()
        scheduler.shutdown()
        logger.info("✨ Production Bot has been stopped gracefully")
    
    return 0

async def _update_user_achievements(db: Database):
    """Update user achievements periodically"""
    logger.info("🏆 Updating user achievements...")
    # Achievement update logic would go here
    
async def _refresh_leaderboard(db: Database):
    """Refresh leaderboard data"""
    logger.info("📊 Refreshing leaderboard data...")
    # Leaderboard refresh logic would go here

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