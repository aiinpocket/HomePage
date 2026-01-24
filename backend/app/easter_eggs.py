"""
彩蛋系統 - 隱藏優惠碼
"""
from typing import Dict, Optional
from .config import settings


class EasterEggSystem:
    """彩蛋管理系統"""

    def __init__(self):
        self.promo_code = settings.EASTER_EGG_PROMO_CODE
        self.discount = settings.EASTER_EGG_DISCOUNT
        self.explorer_code = settings.EXPLORER_PROMO_CODE
        self.explorer_discount = settings.EXPLORER_DISCOUNT

        # 定義多個彩蛋觸發方式
        self.easter_eggs = {
            "konami": {
                "code": "UP_UP_DOWN_DOWN_LEFT_RIGHT_LEFT_RIGHT_B_A",
                "hint": "經典遊戲祕技",
                "reward": self.promo_code,
                "discount": self.discount
            },
            "click_logo_10": {
                "code": "LOGO_CLICK_10",
                "hint": "點擊 Logo 10 次",
                "reward": self.promo_code,
                "discount": self.discount
            },
            "secret_url": {
                "code": "SECRET_PATH",
                "hint": "訪問 /secret-garden",
                "reward": self.promo_code,
                "discount": self.discount
            },
            "inspect_element": {
                "code": "INSPECT_COMMENT",
                "hint": "檢視原始碼中的註解",
                "reward": self.promo_code,
                "discount": self.discount
            },
            "explorer": {
                "code": "VISIT_ALL_PAGES",
                "hint": "瀏覽全部 6 個頁面",
                "reward": self.explorer_code,
                "discount": self.explorer_discount
            }
        }

    def validate_easter_egg(self, egg_type: str) -> Optional[Dict]:
        """
        驗證彩蛋是否正確觸發

        Args:
            egg_type: 彩蛋類型

        Returns:
            包含優惠碼資訊的字典，或 None
        """
        if egg_type not in self.easter_eggs:
            return None

        egg = self.easter_eggs[egg_type]
        discount = egg.get("discount", self.discount)

        return {
            "success": True,
            "promo_code": egg["reward"],
            "discount": discount,
            "message": f"恭喜發現彩蛋！獲得優惠碼：{egg['reward']}（{discount}% OFF）"
        }

    def get_promo_info(self, promo_code: str) -> Optional[Dict]:
        """
        查詢優惠碼資訊

        Args:
            promo_code: 優惠碼

        Returns:
            優惠碼資訊或 None
        """
        # 檢查主要優惠碼
        if promo_code == self.promo_code:
            return {
                "valid": True,
                "code": promo_code,
                "discount": self.discount,
                "description": f"AiInPocket 服務 {self.discount}% OFF"
            }

        # 檢查探索家優惠碼
        if promo_code == self.explorer_code:
            return {
                "valid": True,
                "code": promo_code,
                "discount": self.explorer_discount,
                "description": f"探索家專屬優惠 {self.explorer_discount}% OFF"
            }

        return {
            "valid": False,
            "message": "優惠碼無效或已過期"
        }


# 全域彩蛋系統實例
easter_egg_system = EasterEggSystem()
