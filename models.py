"""
Data models for the BGMI Warrior Bot by IBR using Pydantic.
"""
import uuid
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional, Union, Any

import pytz
from pydantic import BaseModel, Field, validator, root_validator


class UserMode(str, Enum):
    """User operation modes"""
    MANUAL = "manual"
    AUTO = "auto"


class UserStatus(str, Enum):
    """User authorization status"""
    AUTHORIZED = "authorized"
    PENDING = "pending" 
    REJECTED = "rejected"
    EXPIRED = "expired"
    REGULAR = "regular"


class UserAction(BaseModel):
    """Model representing a user action"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int
    ip: str
    port: int
    duration: int
    mode: UserMode
    timestamp: datetime = Field(default_factory=lambda: datetime.now(pytz.utc))
    status: str = "completed"
    thread_value: int = 200
    
    @validator('ip')
    def validate_ip(cls, v):
        """Validate IP address format"""
        parts = v.split('.')
        if len(parts) != 4:
            raise ValueError("Invalid IP address format")
        
        for part in parts:
            if not part.isdigit() or int(part) < 0 or int(part) > 255:
                raise ValueError("Invalid IP address format")
        
        return v
    
    @validator('port')
    def validate_port(cls, v):
        """Validate port number"""
        if v < 1 or v > 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v
    
    @validator('duration')
    def validate_duration(cls, v):
        """Validate duration"""
        if v < 1 or v > 600:
            raise ValueError("Duration must be between 1 and 600 seconds")
        return v


class UserProfile(BaseModel):
    """User profile model"""
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: UserStatus = UserStatus.REGULAR
    expire_time: Optional[datetime] = None
    joined_date: datetime = Field(default_factory=lambda: datetime.now(pytz.utc))
    thread_value: int = 200
    language: str = "en"  # Default to English
    preferred_mode: UserMode = UserMode.MANUAL
    usage_count: Dict[str, int] = Field(default_factory=dict)
    
    def is_authorized(self, timezone=pytz.UTC) -> bool:
        """Check if user is authorized and not expired"""
        if self.status != UserStatus.AUTHORIZED:
            return False
            
        if self.expire_time is None:
            return False
            
        now = datetime.now(timezone)
        return now < self.expire_time