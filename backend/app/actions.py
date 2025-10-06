"""
頁面操作動作定義
AI 可以執行的網頁操作
"""
from typing import Dict, Optional, List
from pydantic import BaseModel


class Action(BaseModel):
    """操作基類"""
    type: str
    target: Optional[str] = None
    targets: Optional[List[str]] = None
    data: Optional[Dict] = None


class ActionHandler:
    """操作處理器 - 根據使用者意圖生成對應的網頁操作"""

    @staticmethod
    def navigate_to_page(page: str) -> Dict:
        """
        導航到指定頁面

        Args:
            page: 頁面名稱 (portfolio, contact, tech-stack, about, home)

        Returns:
            操作字典
        """
        page_mapping = {
            "portfolio": "/portfolio.html",
            "作品集": "/portfolio.html",
            "專案": "/portfolio.html",
            "contact": "/contact.html",
            "聯絡": "/contact.html",
            "聯絡我們": "/contact.html",
            "tech": "/tech-stack.html",
            "tech-stack": "/tech-stack.html",
            "技術": "/tech-stack.html",
            "技術棧": "/tech-stack.html",
            "about": "/about.html",
            "關於": "/about.html",
            "關於我們": "/about.html",
            "團隊": "/about.html",
            "home": "/index.html",
            "首頁": "/index.html",
        }

        target = page_mapping.get(page.lower(), "/index.html")

        return {
            "type": "navigate",
            "target": target
        }

    @staticmethod
    def scroll_to_section(section_id: str) -> Dict:
        """
        滾動到指定區塊

        Args:
            section_id: 區塊 ID

        Returns:
            操作字典
        """
        return {
            "type": "scroll",
            "target": section_id
        }

    @staticmethod
    def highlight_elements(element_ids: List[str]) -> Dict:
        """
        高亮顯示指定元素

        Args:
            element_ids: 元素 ID 列表

        Returns:
            操作字典
        """
        return {
            "type": "highlight",
            "targets": element_ids
        }

    @staticmethod
    def show_modal(content: str) -> Dict:
        """
        顯示彈窗訊息

        Args:
            content: 彈窗內容

        Returns:
            操作字典
        """
        return {
            "type": "showModal",
            "data": {
                "content": content
            }
        }

    @staticmethod
    def filter_portfolio(category: str) -> Dict:
        """
        篩選作品集

        Args:
            category: 類別 (ai, cloud, devops, all)

        Returns:
            操作字典
        """
        return {
            "type": "filterContent",
            "target": "portfolio",
            "data": {
                "category": category
            }
        }


class IntentClassifier:
    """意圖分類器 - 判斷使用者的意圖並生成對應動作"""

    def __init__(self):
        self.action_handler = ActionHandler()

    def classify_and_execute(self, user_message: str) -> Optional[Dict]:
        """
        根據使用者訊息分類意圖並生成動作

        Args:
            user_message: 使用者訊息

        Returns:
            操作字典或 None
        """
        msg = user_message.lower()

        # 導航意圖
        if any(keyword in msg for keyword in ["作品", "專案", "portfolio", "案例"]):
            return self.action_handler.navigate_to_page("portfolio")

        if any(keyword in msg for keyword in ["聯絡", "contact", "email", "信箱", "聯繫"]):
            return self.action_handler.navigate_to_page("contact")

        if any(keyword in msg for keyword in ["技術", "tech", "工具", "technology"]):
            return self.action_handler.navigate_to_page("tech")

        if any(keyword in msg for keyword in ["關於", "about", "團隊", "公司", "我們"]):
            return self.action_handler.navigate_to_page("about")

        if any(keyword in msg for keyword in ["首頁", "home", "主頁", "回到"]):
            return self.action_handler.navigate_to_page("home")

        # 作品集篩選意圖
        if "ai" in msg and ("作品" in msg or "專案" in msg):
            return {
                "type": "navigate",
                "target": "/portfolio.html",
                "filter": "ai"
            }

        if ("雲端" in msg or "cloud" in msg) and ("作品" in msg or "專案" in msg):
            return {
                "type": "navigate",
                "target": "/portfolio.html",
                "filter": "cloud"
            }

        if ("devops" in msg or "自動化" in msg) and ("作品" in msg or "專案" in msg):
            return {
                "type": "navigate",
                "target": "/portfolio.html",
                "filter": "devops"
            }

        # 沒有明確的導航意圖
        return None

    def generate_response_with_action(self, user_message: str) -> tuple:
        """
        生成回應文字和動作

        Args:
            user_message: 使用者訊息

        Returns:
            (回應文字, 動作字典)
        """
        msg = user_message.lower()
        action = self.classify_and_execute(user_message)

        # 生成對應的回應文字
        if action:
            if action["target"] == "/portfolio.html":
                response = "好的！讓我帶你去看我們的作品集"
            elif action["target"] == "/contact.html":
                response = "沒問題！我會幫你跳轉到聯絡頁面"
            elif action["target"] == "/tech-stack.html":
                response = "讓我為你展示我們的技術棧"
            elif action["target"] == "/about.html":
                response = "帶你了解 AiInPocket 團隊！"
            elif action["target"] == "/index.html":
                response = "回到首頁！"
            else:
                response = "讓我幫你導航到相關頁面"
        else:
            # 沒有明確動作時的通用回應
            if "你好" in msg or "hello" in msg or "hi" in msg:
                response = "你好！很高興為你服務。我可以幫你瀏覽網站、介紹我們的服務，或是回答任何問題。"
                action = None
            elif "服務" in msg or "做什麼" in msg:
                response = "我們提供三大核心服務：\n\n1. AI 解決方案 - 深度學習、NLP、智能自動化\n2. 雲端架構 - 可擴展、高可用的雲端方案\n3. DevOps 工程 - CI/CD、基礎設施即代碼\n\n想了解更多嗎？"
                action = None
            elif "價格" in msg or "費用" in msg or "收費" in msg:
                response = "我們提供彈性的計費方式，包括專案制、時數制、或長期技術顧問合約。建議您透過聯絡表單告訴我們您的需求，我們會提供最適合的報價方案。"
                action = self.action_handler.navigate_to_page("contact")
            else:
                response = f'我收到你的訊息了：「{user_message}」\n\n你可以試試問我：\n• "帶我去看作品集"\n• "我想聯絡你們"\n• "介紹一下技術棧"\n• "告訴我關於你們"'
                action = None

        return response, action
