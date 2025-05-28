"""
Utility functions for the BGMI Warrior Bot by IBR.
"""
import ipaddress
import random
import re
from datetime import datetime, timedelta
from typing import Dict, Optional

import pytz
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def is_valid_ip(ip: str) -> bool:
    """Validate IP address format"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_port(port: int) -> bool:
    """Validate port number"""
    return 1 <= port <= 65535

def is_valid_duration(duration: int) -> bool:
    """Validate duration"""
    return 1 <= duration <= 600

def format_time_remaining(seconds: int) -> str:
    """Format seconds into human-readable time"""
    if seconds < 60:
        return f"{seconds}s"
    
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {seconds}s"
    
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m {seconds}s"

def get_random_duration() -> int:
    """Get random duration for auto mode"""
    return random.randint(80, 240)

def create_user_markup(user_id: int, username: str = None) -> Dict:
    """Create a user information object"""
    return {
        'user_id': user_id,
        'username': username or "Unknown",
        'active_since': datetime.now(pytz.utc)
    }

def parse_duration_string(duration_str: str, base_time: datetime) -> Optional[datetime]:
    """Parse duration string and return expiration time"""
    time_match = re.match(r"(\d+)([dhm])", duration_str)
    if time_match:
        value, unit = time_match.groups()
        value = int(value)
        if unit == 'h':
            return base_time + timedelta(hours=value)
        elif unit == 'd':
            return base_time + timedelta(days=value)
        elif unit == 'm':
            return base_time + timedelta(days=30 * value)
    elif duration_str == 'permanent':
        return base_time + timedelta(days=365*100)
        
    return None

def create_main_keyboard() -> ReplyKeyboardMarkup:
    """Create the main keyboard markup"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton('Manual Mode'), KeyboardButton('Auto Mode'))
    markup.row(KeyboardButton('/help'), KeyboardButton('/usage'))
    markup.row(KeyboardButton('/ping'), KeyboardButton('/history'))
    return markup

def sanitize_text(text: str) -> str:
    """Sanitize text for security"""
    # Remove potentially dangerous characters
    return re.sub(r'[^\w\s\.\-:,]', '', text).strip()