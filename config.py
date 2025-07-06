"""
🌟 BGMI Warrior Bot by IBR - Production Configuration 🌟
✨ Complete settings for modern features and premium experience ✨
"""
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BotConfig(BaseModel):
    """Production-ready bot configuration with modern features"""
    
    # Core settings
    TOKEN: str = Field(..., description="Telegram bot token")
    MONGO_URI: str = Field(..., description="MongoDB Connection URI")
    DATABASE_NAME: str = Field("bgmi_warrior_premium", description="Database name")
    COLLECTION_NAME: str = Field("actions", description="MongoDB Collection Name")
    
    # Admin and authorization
    AUTHORIZED_USERS: List[int] = Field(default_factory=list, description="Admin user IDs list")
    
    # Action service settings
    ACTION_BINARY_PATH: str = Field("./action", description="Path to action binary")
    DEFAULT_THREAD_COUNT: int = Field(100, description="Default thread count")
    MAX_THREAD_COUNT: int = Field(500, description="Maximum thread count")
    MIN_THREAD_COUNT: int = Field(50, description="Minimum thread count")
    
    # Rate limiting and premium tiers
    RATE_LIMIT: int = Field(5, description="Daily action limit for groups")
    PREMIUM_RATE_LIMIT: int = Field(50, description="Daily limit for premium users")
    VIP_RATE_LIMIT: int = Field(100, description="Daily limit for VIP users")
    HISTORY_CLEAR_INTERVAL: int = Field(3600, description="Interval in seconds for clearing history")
    
    # Security settings
    BLOCKED_PORTS: List[int] = Field(
        default_factory=lambda: [22, 23, 25, 53, 80, 110, 443, 993, 995, 8700, 20000, 17500, 9031, 20002, 20001],
        description="Blocked port numbers"
    )
    MAX_DURATION: int = Field(600, description="Maximum action duration in seconds")
    MIN_DURATION: int = Field(1, description="Minimum action duration in seconds")
    MAX_BANDWIDTH_MBPS: float = Field(100.0, description="Maximum bandwidth in Mbps")
    
    # Modern UI settings
    DEFAULT_THEME: str = Field("rainbow_neon", description="Default UI theme")
    ENABLE_ANIMATIONS: bool = Field(True, description="Enable UI animations")
    RAINBOW_MODE_DEFAULT: bool = Field(False, description="Default rainbow mode state")
    
    # Feature toggles
    ENABLE_MINI_GAMES: bool = Field(True, description="Enable mini-games")
    ENABLE_ACHIEVEMENTS: bool = Field(True, description="Enable achievement system")
    ENABLE_MUSIC_PLAYER: bool = Field(True, description="Enable music player")
    ENABLE_ANALYTICS: bool = Field(True, description="Enable analytics")
    ENABLE_VOICE_COMMANDS: bool = Field(False, description="Enable voice commands (premium)")
    
    # AI-powered features
    ENABLE_AI_COMMANDS: bool = Field(True, description="Enable AI-powered natural language commands")
    ENABLE_AI_TRANSLATION: bool = Field(True, description="Enable AI-powered language detection and translation")
    ENABLE_AI_RECOMMENDATIONS: bool = Field(True, description="Enable AI-powered smart recommendations")
    ENABLE_AI_BEHAVIOR: bool = Field(True, description="Enable AI user behavior adaptation")

    # Language settings
    DEFAULT_LANGUAGE: str = Field("en", description="Default language")
    SUPPORTED_LANGUAGES: List[str] = Field(
        default_factory=lambda: ["en", "es", "fr", "de", "ru", "zh", "ja", "hi", "ur"],
        description="Supported languages"
    )
    
    # Premium features
    PREMIUM_FEATURES: Dict[str, bool] = Field(
        default_factory=lambda: {
            "unlimited_actions": True,
            "exclusive_themes": True,
            "voice_commands": True,
            "priority_support": True,
            "advanced_analytics": True,
            "private_tournaments": True
        },
        description="Premium feature flags"
    )
    
    # Logging and monitoring
    LOG_FILE: str = Field("bot_logs/warrior_bot.log", description="Log file path")
    LOG_LEVEL: str = Field("INFO", description="Logging level")
    DEBUG_MODE: bool = Field(False, description="Enable debug mode")
    
    # Performance settings
    MAX_CONCURRENT_ACTIONS: int = Field(10, description="Maximum concurrent actions")
    CONNECTION_TIMEOUT: int = Field(30, description="Connection timeout in seconds")
    
    # Timezone
    TIMEZONE: str = Field("Asia/Kolkata", description="Default timezone")
    
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
    
    @validator('AUTHORIZED_USERS')
    def validate_user_ids(cls, v):
        """Validate user ID lists"""
        return [int(uid) for uid in v if str(uid).isdigit()]
    
    @validator('DEFAULT_THEME')
    def validate_theme(cls, v):
        """Validate theme selection"""
        valid_themes = ["rainbow_neon", "dark_galaxy", "fire_storm", "ice_crystal", 
                       "cherry_blossom", "electric_blue", "carnival", "golden_elite"]
        if v not in valid_themes:
            return "rainbow_neon"
        return v
    
    class Config:
        """Pydantic config"""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Available themes configuration
AVAILABLE_THEMES = {
    "rainbow_neon": {
        "name": "🌈 Rainbow Neon",
        "emojis": ["🌈", "✨", "💎", "⚡", "🔥"],
        "style": "cyberpunk"
    },
    "dark_galaxy": {
        "name": "🌌 Dark Galaxy", 
        "emojis": ["🌌", "⭐", "🔮", "🌟", "✨"],
        "style": "space"
    },
    "fire_storm": {
        "name": "🔥 Fire Storm",
        "emojis": ["🔥", "⚡", "💥", "🌋", "💫"],
        "style": "energy"
    },
    "ice_crystal": {
        "name": "❄️ Ice Crystal",
        "emojis": ["❄️", "💎", "🔷", "⭐", "✨"],
        "style": "cool"
    },
    "cherry_blossom": {
        "name": "🌸 Cherry Blossom",
        "emojis": ["🌸", "🌺", "💮", "🎀", "✨"],
        "style": "elegant"
    },
    "electric_blue": {
        "name": "⚡ Electric Blue",
        "emojis": ["⚡", "🔵", "💙", "🌀", "✨"],
        "style": "electric"
    },
    "carnival": {
        "name": "🎪 Carnival",
        "emojis": ["🎪", "🎭", "🎨", "🎊", "✨"],
        "style": "fun"
    },
    "golden_elite": {
        "name": "🏆 Golden Elite",
        "emojis": ["🏆", "👑", "💰", "🌟", "✨"],
        "style": "luxury"
    }
}

# Supported languages with names
SUPPORTED_LANGUAGES = {
    "en": "🇺🇸 English",
    "es": "🇪🇸 Español", 
    "fr": "🇫🇷 Français",
    "de": "🇩🇪 Deutsch",
    "ru": "🇷🇺 Русский",
    "zh": "🇨🇳 中文",
    "ja": "🇯🇵 日本語",
    "hi": "🇮🇳 हिंदी"
}

# Load configuration from environment variables
def load_config() -> BotConfig:
    """Load and validate configuration from environment variables"""
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
        DATABASE_NAME=os.getenv("DATABASE_NAME", "bgmi_warrior_premium"),
        COLLECTION_NAME=os.getenv("COLLECTION_NAME", "actions"),
        RATE_LIMIT=int(os.getenv("RATE_LIMIT", "5")),
        PREMIUM_RATE_LIMIT=int(os.getenv("PREMIUM_RATE_LIMIT", "50")),
        VIP_RATE_LIMIT=int(os.getenv("VIP_RATE_LIMIT", "100")),
        HISTORY_CLEAR_INTERVAL=int(os.getenv("HISTORY_CLEAR_INTERVAL", "3600")),
        AUTHORIZED_USERS=auth_users or [6800732852, 5113311276],
        BLOCKED_PORTS=blocked_ports,
        TIMEZONE=os.getenv("TIMEZONE", "Asia/Kolkata"),
        LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
        LOG_FILE=os.getenv("LOG_FILE", "bot_logs/warrior_bot.log"),
        ACTION_BINARY_PATH=os.getenv("ACTION_BINARY_PATH", "./action"),
        MAX_BANDWIDTH_MBPS=float(os.getenv("MAX_BANDWIDTH_MBPS", "100.0")),
        DEFAULT_THEME=os.getenv("DEFAULT_THEME", "rainbow_neon"),
        ENABLE_ANIMATIONS=os.getenv("ENABLE_ANIMATIONS", "true").lower() == "true",
        RAINBOW_MODE_DEFAULT=os.getenv("RAINBOW_MODE_DEFAULT", "false").lower() == "true",
        ENABLE_MINI_GAMES=os.getenv("ENABLE_MINI_GAMES", "true").lower() == "true",
        ENABLE_ACHIEVEMENTS=os.getenv("ENABLE_ACHIEVEMENTS", "true").lower() == "true",
        ENABLE_MUSIC_PLAYER=os.getenv("ENABLE_MUSIC_PLAYER", "true").lower() == "true",
        ENABLE_ANALYTICS=os.getenv("ENABLE_ANALYTICS", "true").lower() == "true",
        ENABLE_VOICE_COMMANDS=os.getenv("ENABLE_VOICE_COMMANDS", "false").lower() == "true",
        DEFAULT_LANGUAGE=os.getenv("DEFAULT_LANGUAGE", "en"),
        SUPPORTED_LANGUAGES=[lang.strip() for lang in os.getenv("SUPPORTED_LANGUAGES", "en,es,fr,de,ru,zh,ja,hi").split(",")],
        PREMIUM_FEATURES={
            "unlimited_actions": os.getenv("PREMIUM_UNLIMITED_ACTIONS", "true").lower() == "true",
            "exclusive_themes": os.getenv("PREMIUM_EXCLUSIVE_THEMES", "true").lower() == "true",
            "voice_commands": os.getenv("PREMIUM_VOICE_COMMANDS", "true").lower() == "true",
            "priority_support": os.getenv("PREMIUM_PRIORITY_SUPPORT", "true").lower() == "true",
            "advanced_analytics": os.getenv("PREMIUM_ADVANCED_ANALYTICS", "true").lower() == "true",
            "private_tournaments": os.getenv("PREMIUM_PRIVATE_TOURNAMENTS", "true").lower() == "true"
        },
        DEBUG_MODE=os.getenv("DEBUG_MODE", "false").lower() == "true",
        MAX_CONCURRENT_ACTIONS=int(os.getenv("MAX_CONCURRENT_ACTIONS", "10")),
        CONNECTION_TIMEOUT=int(os.getenv("CONNECTION_TIMEOUT", "30")),
        ENABLE_AI_COMMANDS=os.getenv("ENABLE_AI_COMMANDS", "true").lower() == "true",
        ENABLE_AI_TRANSLATION=os.getenv("ENABLE_AI_TRANSLATION", "true").lower() == "true",
        ENABLE_AI_RECOMMENDATIONS=os.getenv("ENABLE_AI_RECOMMENDATIONS", "true").lower() == "true",
        ENABLE_AI_BEHAVIOR=os.getenv("ENABLE_AI_BEHAVIOR", "true").lower() == "true"
    )