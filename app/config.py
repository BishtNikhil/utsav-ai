import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()

class AppConfig(BaseModel):
    app_name: str = "UtsavAI"
    app_version: str = "1.0.0"
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    port: int = int(os.getenv("PORT", "8080"))
    host: str = os.getenv("HOST", "0.0.0.0")
    debug: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

    @property
    def has_gemini_key(self) -> bool:
        return bool(self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key_here")

config = AppConfig()
