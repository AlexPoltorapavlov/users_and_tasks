"""Configuration module for the application.

This module handles loading environment variables and provides
a Config class to access application configuration settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class holding application settings.
    
    Attributes:
        DATABASE_URL (str): Database connection URL from environment variables
        JWT_SECRET_KEY (str): Secret key for JWT token generation and validation
    """
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

config = Config