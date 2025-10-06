"""
配置管理模組
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """應用配置"""

    # OpenAI 設定
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"

    # CORS 設定
    CORS_ORIGINS: str = "http://localhost:80,http://localhost:3000"

    # 應用設定
    APP_NAME: str = "AiInPocket"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        """將 CORS 來源字串轉換為列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# 全域設定實例
settings = Settings()
