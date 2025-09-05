"""
Configuration file for The Empathy Engine
Customize settings here for different environments
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for The Empathy Engine"""
    
    # Server settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Audio settings
    AUDIO_FORMAT = "wav"
    AUDIO_CLEANUP_HOURS = int(os.getenv("AUDIO_CLEANUP_HOURS", "24"))
    TEMP_AUDIO_DIR = "temp_audio"
    
    # TTS settings
    DEFAULT_RATE = 150  # Words per minute
    DEFAULT_VOLUME = 0.8
    DEFAULT_PITCH = 1.0
    
    # Emotion detection settings
    EMOTION_CONFIDENCE_THRESHOLD = 0.3
    USE_HUGGING_FACE = os.getenv("USE_HUGGING_FACE", "True").lower() == "true"
    
    # Vocal parameter ranges
    RATE_RANGE = (0.5, 2.0)  # Min and max rate multipliers
    PITCH_RANGE = (0.5, 2.0)  # Min and max pitch multipliers
    VOLUME_RANGE = (0.1, 1.0)  # Min and max volume
    
    # Emotion mappings (can be customized) - More human-like ranges
    EMOTION_MAPPINGS = {
        "joy": {
            "rate": 1.1,      # Slightly faster (10% increase)
            "pitch": 1.05,    # Slightly higher pitch (5% increase)
            "volume": 0.9,    # Slightly louder
            "description": "Happy, enthusiastic"
        },
        "sadness": {
            "rate": 0.9,      # Slightly slower (10% decrease)
            "pitch": 0.95,    # Slightly lower pitch (5% decrease)
            "volume": 0.8,    # Quieter
            "description": "Somber, melancholic"
        },
        "anger": {
            "rate": 1.05,     # Slightly faster (5% increase)
            "pitch": 1.02,    # Slightly higher pitch (2% increase)
            "volume": 1.0,    # Full volume
            "description": "Intense, forceful"
        },
        "fear": {
            "rate": 1.15,     # Moderately faster (15% increase)
            "pitch": 1.08,    # Moderately higher pitch (8% increase)
            "volume": 0.85,   # Slightly quieter
            "description": "Anxious, nervous"
        },
        "surprise": {
            "rate": 1.08,     # Slightly faster (8% increase)
            "pitch": 1.1,     # Higher pitch (10% increase)
            "volume": 0.9,    # Slightly louder
            "description": "Excited, astonished"
        },
        "disgust": {
            "rate": 0.95,     # Slightly slower (5% decrease)
            "pitch": 0.98,    # Slightly lower pitch (2% decrease)
            "volume": 0.85,   # Quieter
            "description": "Contemptuous, dismissive"
        },
        "neutral": {
            "rate": 1.0,      # Normal speed
            "pitch": 1.0,     # Normal pitch
            "volume": 0.8,    # Normal volume
            "description": "Calm, professional"
        }
    }
    
    # API settings
    API_TITLE = "The Empathy Engine"
    API_DESCRIPTION = "AI-powered TTS with emotional voice modulation"
    API_VERSION = "1.0.0"
    
    # CORS settings
    CORS_ORIGINS = ["*"]  # In production, specify actual origins
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    @classmethod
    def get_emotion_mapping(cls, emotion: str) -> Dict[str, Any]:
        """Get emotion mapping with fallback to neutral"""
        return cls.EMOTION_MAPPINGS.get(emotion, cls.EMOTION_MAPPINGS["neutral"])
    
    @classmethod
    def validate_intensity(cls, intensity: float) -> float:
        """Validate and clamp intensity value"""
        return max(0.1, min(2.0, intensity))
    
    @classmethod
    def validate_vocal_parameter(cls, param_name: str, value: float) -> float:
        """Validate vocal parameter values"""
        if param_name == "rate":
            return max(cls.RATE_RANGE[0], min(cls.RATE_RANGE[1], value))
        elif param_name == "pitch":
            return max(cls.PITCH_RANGE[0], min(cls.PITCH_RANGE[1], value))
        elif param_name == "volume":
            return max(cls.VOLUME_RANGE[0], min(cls.VOLUME_RANGE[1], value))
        else:
            return value

# Development configuration
class DevelopmentConfig(Config):
    """Development-specific configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"

# Production configuration  
class ProductionConfig(Config):
    """Production-specific configuration"""
    DEBUG = False
    LOG_LEVEL = "INFO"
    CORS_ORIGINS = ["https://yourdomain.com"]  # Update with actual domain

# Configuration selection
def get_config():
    """Get configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig()

# Export the active configuration
config = get_config()

