"""
Configuration module for the BGMI Warrior Bot by IBR.
Uses Pydantic for type validation and dotenv for environment variables.
"""
import os
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BotConfig(BaseModel):
    """Bot configuration model with validation"""
    TOKEN: str = Field(..., description="Telegram Bot Token")
    MONGO_URI: str = Field(..., description="MongoDB Connection URI")
    DATABASE_NAME: str = Field("action", description="MongoDB Database Name")
    COLLECTION_NAME: str = Field("action", description="MongoDB Collection Name")
    RATE_LIMIT: int = Field(5, description="Number of actions per day for non-premium users in groups")
    HISTORY_CLEAR_INTERVAL: int = Field(3600, description="Interval in seconds for clearing history")
    AUTHORIZED_USERS: List[int] = Field(default_factory=list, description="Admin user IDs list")
    BLOCKED_PORTS: List[int] = Field(
        default_factory=lambda: [8700, 20000, 443, 17500, 9031, 20002, 20001],
        description="List of blocked ports"
    )
    TIMEZONE: str = Field("Asia/Kolkata", description="Default timezone")
    LOG_LEVEL: str = Field("INFO", description="Logging level")
    LOG_FILE: str = Field("bot_logs/warrior_bot.log", description="Log file path")
    ACTION_BINARY_PATH: str = Field("./action", description="Path to action binary")
    MAX_BANDWIDTH_MBPS: float = Field(100.0, description="Maximum bandwidth in Mbps")
    
    @validator('TOKEN')
    def token_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Bot token cannot be empty")
        return v
    
    @validator('MONGO_URI')
    def mongo_uri_must_be_valid(cls, v):
        if not v.startswith(('mongodb://', 'mongodb+srv://')):
            raise ValueError("MongoDB URI must start with mongodb:// or mongodb+srv://")
        return v

# Load configuration from environment variables
def load_config() -> BotConfig:
    """Load and validate configuration from environment variables"""
    # Ensure directories exist
    os.makedirs("bot_logs", exist_ok=True)
    
    # Load authorized users from env var as comma-separated list
    auth_users_str = os.getenv("AUTHORIZED_USERS", "")
    auth_users = [int(user.strip()) for user in auth_users_str.split(",") if user.strip().isdigit()]
    
    # Load blocked ports from env var as comma-separated list
    blocked_ports_str = os.getenv("BLOCKED_PORTS", "8700,20000,443,17500,9031,20002,20001")
    blocked_ports = [int(port.strip()) for port in blocked_ports_str.split(",") if port.strip().isdigit()]
    
    return BotConfig(
        TOKEN=os.getenv("BOT_TOKEN", ""),
        MONGO_URI=os.getenv("MONGO_URI", ""),
        DATABASE_NAME=os.getenv("DATABASE_NAME", "action"),
        COLLECTION_NAME=os.getenv("COLLECTION_NAME", "action"),
        RATE_LIMIT=int(os.getenv("RATE_LIMIT", "5")),
        HISTORY_CLEAR_INTERVAL=int(os.getenv("HISTORY_CLEAR_INTERVAL", "3600")),
        AUTHORIZED_USERS=auth_users or [6800732852, 5113311276],
        BLOCKED_PORTS=blocked_ports,
        TIMEZONE=os.getenv("TIMEZONE", "Asia/Kolkata"),
        LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
        LOG_FILE=os.getenv("LOG_FILE", "bot_logs/warrior_bot.log"),
        ACTION_BINARY_PATH=os.getenv("ACTION_BINARY_PATH", "./action"),
        MAX_BANDWIDTH_MBPS=float(os.getenv("MAX_BANDWIDTH_MBPS", "100.0"))
    )