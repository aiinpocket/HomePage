"""
使用量追蹤系統
使用 Redis 追蹤每個生成網站的 API 使用次數
"""
import redis
from typing import Optional
from .config import settings


class UsageTracker:
    """API 使用量追蹤器"""

    def __init__(self):
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True
            )
            # 測試連接
            self.redis_client.ping()
            print("[OK] Redis connection established")
        except Exception as e:
            print(f"[ERROR] Redis connection failed: {e}")
            self.redis_client = None

    def get_usage(self, site_id: str) -> int:
        """
        獲取網站的 API 使用次數

        Args:
            site_id: 網站 ID

        Returns:
            使用次數
        """
        if not self.redis_client:
            return 0

        try:
            key = f"usage:{site_id}"
            count = self.redis_client.get(key)
            return int(count) if count else 0
        except Exception as e:
            print(f"[ERROR] Failed to get usage: {e}")
            return 0

    def increment_usage(self, site_id: str) -> int:
        """
        增加網站的 API 使用次數

        Args:
            site_id: 網站 ID

        Returns:
            新的使用次數
        """
        if not self.redis_client:
            return 0

        try:
            key = f"usage:{site_id}"
            count = self.redis_client.incr(key)

            # 設定 30 天過期（預防 key 永久存在）
            if count == 1:
                self.redis_client.expire(key, 30 * 24 * 60 * 60)

            return count
        except Exception as e:
            print(f"[ERROR] Failed to increment usage: {e}")
            return 0

    def check_limit(self, site_id: str) -> bool:
        """
        檢查是否超過使用限制

        Args:
            site_id: 網站 ID

        Returns:
            是否可以繼續使用（True = 可以，False = 超限）
        """
        current_usage = self.get_usage(site_id)
        return current_usage < settings.PREVIEW_API_LIMIT

    def reset_usage(self, site_id: str) -> bool:
        """
        重置網站的使用次數（管理功能）

        Args:
            site_id: 網站 ID

        Returns:
            是否成功
        """
        if not self.redis_client:
            return False

        try:
            key = f"usage:{site_id}"
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to reset usage: {e}")
            return False

    def get_all_stats(self) -> dict:
        """獲取所有網站的使用統計"""
        if not self.redis_client:
            return {}

        try:
            stats = {}
            for key in self.redis_client.scan_iter("usage:*"):
                site_id = key.replace("usage:", "")
                count = self.redis_client.get(key)
                stats[site_id] = int(count) if count else 0
            return stats
        except Exception as e:
            print(f"[ERROR] Failed to get stats: {e}")
            return {}


# 全域追蹤器實例
usage_tracker = UsageTracker()
