"""
使用量追蹤系統（PostgreSQL 版本）
使用 PostgreSQL 持久化追蹤每個生成網站的 API 使用次數
避免 Redis 重啟導致資料遺失
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict
from .models import SiteUsage
from .config import settings


class UsageTrackerPG:
    """API 使用量追蹤器（PostgreSQL 版本）"""

    def get_or_create_usage(self, db: Session, site_id: str) -> SiteUsage:
        """
        獲取或建立網站使用記錄

        Args:
            db: 資料庫 session
            site_id: 網站 ID

        Returns:
            SiteUsage 物件
        """
        usage = db.query(SiteUsage).filter(SiteUsage.site_id == site_id).first()

        if not usage:
            usage = SiteUsage(site_id=site_id)
            db.add(usage)
            db.commit()
            db.refresh(usage)

        return usage

    def get_usage(self, db: Session, site_id: str) -> int:
        """
        獲取網站的 API 使用次數

        Args:
            db: 資料庫 session
            site_id: 網站 ID

        Returns:
            使用次數
        """
        try:
            usage = self.get_or_create_usage(db, site_id)
            return usage.api_calls_count
        except Exception as e:
            print(f"[ERROR] Failed to get usage: {e}")
            return 0

    def increment_usage(self, db: Session, site_id: str) -> int:
        """
        增加網站的 API 使用次數

        Args:
            db: 資料庫 session
            site_id: 網站 ID

        Returns:
            新的使用次數
        """
        try:
            usage = self.get_or_create_usage(db, site_id)
            new_count = usage.increment_usage()
            db.commit()
            return new_count
        except Exception as e:
            print(f"[ERROR] Failed to increment usage: {e}")
            db.rollback()
            return 0

    def check_limit(self, db: Session, site_id: str) -> bool:
        """
        檢查是否超過使用限制

        Args:
            db: 資料庫 session
            site_id: 網站 ID

        Returns:
            是否可以繼續使用（True = 可以，False = 超限）
        """
        try:
            usage = self.get_or_create_usage(db, site_id)
            return not usage.is_quota_exceeded()
        except Exception as e:
            print(f"[ERROR] Failed to check limit: {e}")
            return False

    def get_remaining_calls(self, db: Session, site_id: str) -> int:
        """
        獲取剩餘可用次數

        Args:
            db: 資料庫 session
            site_id: 網站 ID

        Returns:
            剩餘次數
        """
        try:
            usage = self.get_or_create_usage(db, site_id)
            return usage.get_remaining_calls()
        except Exception as e:
            print(f"[ERROR] Failed to get remaining calls: {e}")
            return 0

    def reset_usage(self, db: Session, site_id: str) -> bool:
        """
        重置網站的使用次數（管理功能）

        Args:
            db: 資料庫 session
            site_id: 網站 ID

        Returns:
            是否成功
        """
        try:
            usage = db.query(SiteUsage).filter(SiteUsage.site_id == site_id).first()
            if usage:
                usage.api_calls_count = 0
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"[ERROR] Failed to reset usage: {e}")
            db.rollback()
            return False

    def get_usage_stats(self, db: Session, site_id: str) -> Dict:
        """
        獲取網站的詳細使用統計

        Args:
            db: 資料庫 session
            site_id: 網站 ID

        Returns:
            統計資訊字典
        """
        try:
            usage = self.get_or_create_usage(db, site_id)
            return {
                "site_id": usage.site_id,
                "api_calls_count": usage.api_calls_count,
                "max_api_calls": usage.max_api_calls,
                "remaining_calls": usage.get_remaining_calls(),
                "is_quota_exceeded": usage.is_quota_exceeded(),
                "created_at": usage.created_at.isoformat(),
                "last_used_at": usage.last_used_at.isoformat()
            }
        except Exception as e:
            print(f"[ERROR] Failed to get usage stats: {e}")
            return {}

    def get_all_stats(self, db: Session, limit: int = 100) -> list:
        """
        獲取所有網站的使用統計

        Args:
            db: 資料庫 session
            limit: 返回數量限制

        Returns:
            統計資訊列表
        """
        try:
            usages = db.query(SiteUsage).order_by(
                SiteUsage.last_used_at.desc()
            ).limit(limit).all()

            return [
                {
                    "site_id": usage.site_id,
                    "api_calls_count": usage.api_calls_count,
                    "max_api_calls": usage.max_api_calls,
                    "remaining_calls": usage.get_remaining_calls(),
                    "last_used_at": usage.last_used_at.isoformat()
                }
                for usage in usages
            ]
        except Exception as e:
            print(f"[ERROR] Failed to get all stats: {e}")
            return []


# 全域追蹤器實例（PostgreSQL 版本）
usage_tracker_pg = UsageTrackerPG()
