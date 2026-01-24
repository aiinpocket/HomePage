"""
配置管理模組（精簡版）
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """應用配置"""

    # CORS 設定
    CORS_ORIGINS: str = "https://aiinpocket.com,http://localhost:80,http://localhost:3000"

    # 應用設定
    APP_NAME: str = "AiInPocket"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False

    # 網站設定
    SITE_URL: str = "https://aiinpocket.com"

    # 彩蛋優惠碼設定
    EASTER_EGG_PROMO_CODE: str = "AIINPOCKET2025"
    EASTER_EGG_DISCOUNT: int = 20
    EXPLORER_PROMO_CODE: str = "EXPLORER2025"
    EXPLORER_DISCOUNT: int = 15

    # Email 設定（聯絡表單用）
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "AiInPocket <noreply@aiinpocket.com>"

    # Webhook 設定
    WEBHOOK_URL: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        """將 CORS 來源字串轉換為列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# 全域設定實例
settings = Settings()
