"""
UtsavAI Application Configuration Module.

Manages application runtime parameters, Google Gemini API settings,
and safe environment variable loading adhering to the Zero-Secret Law.
"""

import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()

class AppConfig(BaseModel):
    """
    Immutable application configuration container.
    
    Attributes:
        app_name (str): The official application display name.
        app_version (str): The semver version tag.
        gemini_api_key (str): The Google AI Studio API key (strictly read from env).
        gemini_model (str): The targeted Gemini model identifier.
        port (int): HTTP listen port.
        host (str): HTTP binding host interface.
        debug (bool): Development debug flag.
    """
    app_name: str = Field(default="UtsavAI")
    app_version: str = Field(default="1.0.0")
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = Field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    port: int = Field(default_factory=lambda: int(os.getenv("PORT", "8080")))
    host: str = Field(default_factory=lambda: os.getenv("HOST", "0.0.0.0"))
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "True").lower() in ("true", "1", "yes"))

    @property
    def has_gemini_key(self) -> bool:
        """
        Validates whether a legitimate Gemini API key has been configured.
        
        Returns:
            bool: True if key is set and non-placeholder, False otherwise.
        """
        return bool(self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key_here")

config = AppConfig()
