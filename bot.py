#!/usr/bin/env python3
"""
BGMI Warrior Bot by IBR - Premium Edition
An advanced Telegram bot for BGMI players with DDoS protection capabilities.
"""
import asyncio
import logging
import os
import re
import signal
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any

import pytz
import telebot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, validator
from telebot.async_telebot import AsyncTeleBot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    CallbackQuery
)

# Load environment variables from .env file
load_dotenv()

# Configure logging with more detailed format
logging.basicConfig(
    filename='bot_logs/warrior_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create logger
logger = logging.getLogger('bgmi_warrior_bot')

# Add console handler with a specific format
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)