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

    # PostgreSQL
    DATABASE_URL: str = "postgresql://aiinpocket:aiinpocket_secure_password@postgres:5432/aiinpocket"

    # 網站設定
    SITE_URL: str = "https://aiinpocket.com"
    FRONTEND_PATH: str = "/app/frontend"

    # 彩蛋優惠碼設定
    EASTER_EGG_PROMO_CODE: str = "AIINPOCKET2025"
    EASTER_EGG_DISCOUNT: int = 20

    # Email 設定
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "AiInPocket <noreply@aiinpocket.com>"

    # Webhook 設定
    WEBHOOK_URL: str = ""  # 聯絡表單提交後的 webhook URL

    # Redis 設定
    REDIS_URL: str = "redis://redis:6379/0"

    # 生成網站設定
    PREVIEW_API_LIMIT: int = 30
    GENERATED_SITES_PATH: str = "/app/generated_sites"
    DOWNLOAD_BASE_URL: str = "https://aiinpocket.com/download"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        """將 CORS 來源字串轉換為列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# 全域設定實例
settings = Settings()
