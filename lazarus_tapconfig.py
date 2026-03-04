"""
Project Lazarus Tap Configuration Module
Centralized configuration management with environment-based settings.
Architectural Rationale: Decouples configuration from code, enables environment-specific 
settings (dev/staging/prod), and provides type safety for critical parameters.
"""

import os
import logging
from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings with validation and defaults."""
    
    # Firebase Configuration
    firebase_credentials_path: str = Field(
        default="./firebase-credentials.json",
        description="Path to Firebase service account credentials"
    )
    firestore_collection_prefix: str = Field(
        default="lazarus_tap",
        description="Prefix for Firestore collections"
    )
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_debug: bool = Field(default=False, env="API_DEBUG")
    cors_origins: list = Field(
        default=["http://localhost:3000", "https://lazarus-tap.com"],
        description="Allowed CORS origins"
    )
    
    # Security Configuration
    jwt_secret_key: str = Field(
        default=os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-prod"),
        env="JWT_SECRET_KEY"
    )
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=30)
    
    # Ethereum Configuration
    web3_provider_url: str = Field(
        default=os.getenv("WEB3_PROVIDER_URL", "https://mainnet.infura.io/v3/your-infura-key"),
        env="WEB3_PROVIDER_URL"
    )
    subscription_contract_address: Optional[str] = Field(
        default=os.getenv("SUBSCRIPTION_CONTRACT_ADDRESS"),
        env="SUBSCRIPTION_CONTRACT_ADDRESS"
    )
    
    # Telemetry Configuration
    telemetry_update_interval_seconds: int = Field(default=5)
    delayed_feed_buffer_minutes: int = Field(default=5)
    
    # Tier Pricing (in ETH)
    tier_pricing: Dict[str, float] = Field(
        default={
            "tier_1": 0.0,      # Free tier
            "tier_2": 0.1,      # 0.1 ETH/month
            "tier_3": 1.0       # 1 ETH/month
        }
    )
    
    # Logging Configuration
    log_level: str = Field(default="INFO")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @validator("jwt_secret_key")
    def validate_jwt_secret_key(cls, v):
        if v == "dev-secret-key-change-in-prod":
            logging.warning("Using default JWT secret key - CHANGE IN PRODUCTION!")
        return v
    
    @validator("web3_provider_url")
    def validate_web3_provider(cls, v):
        if "your-infura-key" in v:
            logging.warning("Using placeholder Infura key - REPLACE WITH ACTUAL KEY!")
        return v

# Global settings instance
settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format=settings.log_format
)
logger = logging.getLogger(__name__)