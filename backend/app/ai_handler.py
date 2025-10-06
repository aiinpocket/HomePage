"""
AI 對話處理模組
整合 OpenAI API 或其他 LLM + RAG 系統
"""
import os
from typing import Dict, Optional
from openai import OpenAI
from .config import settings
from .actions import IntentClassifier
from .database import SessionLocal


class AIHandler:
    """AI 對話處理器"""

    def __init__(self):
        self.client = None
        self.intent_classifier = IntentClassifier()

        # 初始化 OpenAI 客戶端（如果有 API Key）
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.model = settings.OPENAI_MODEL
                print(f"[OK] OpenAI client initialized with model: {self.model}")
            except Exception as e:
                print(f"[WARN] Failed to initialize OpenAI client: {e}")
                self.client = None
        else:
            print("[WARN] No valid OpenAI API key found, using fallback responses")

        # 系統提示詞
        self.system_prompt = """你是 AiInPocket (口袋智慧) 網站的智能導引助手。

你的職責與限制：
1. 你是一個網站導引員，只能回答關於本網站內容的問題
2. 本網站包含以下頁面：
   - 首頁：公司簡介與核心服務概覽
   - 作品集：過往專案案例展示
   - 技術棧：使用的技術與工具
   - 關於我們：團隊介紹與公司文化
   - 聯絡我們：聯絡方式與表單
   - AI 生成器：AI 網頁生成工具

3. 當使用者提問時：
   - 如果問題與網站內容相關，簡潔回答並引導至對應頁面
   - 如果問題超出網站範圍，禮貌告知「這個問題超出我的職責範圍，我只能協助您瀏覽本網站的內容」
   - 然後主動說明：「本網站提供以下資訊：公司服務、作品案例、技術能力、團隊介紹、聯絡方式等，有什麼我可以幫您找的嗎？」

4. 回應原則：
   - 簡潔專業，2-3 句話內完成
   - 繁體中文
   - 不要回答程式設計、技術諮詢、通用知識等問題
   - 專注於網站導覽

範例：
使用者：「你們的 AI 服務有哪些？」
你：「我們提供 AI 解決方案，包括深度學習、NLP、電腦視覺等。詳細資訊在首頁的核心服務區，讓我帶您過去！」

使用者：「Python 要怎麼學？」
你：「抱歉，這個問題超出我的職責範圍。我只能協助您瀏覽本網站的內容。本網站提供公司服務、作品案例、技術能力、團隊介紹等資訊，有什麼我可以幫您找的嗎？」
"""

    async def process_message(
        self,
        message: str,
        session_id: str,
        conversation_history: Optional[list] = None
    ) -> Dict:
        """
        處理使用者訊息並生成回應（使用 RAG 系統）

        Args:
            message: 使用者訊息
            session_id: 會話 ID
            conversation_history: 對話歷史

        Returns:
            包含 reply 和 action 的字典
        """
        # 使用 RAG 系統搜尋相關頁面
        action = None
        response_text = ""

        try:
            from .rag_system import rag_system

            db = SessionLocal()
            try:
                # 搜尋最相關的頁面
                similar_pages = rag_system.search_similar_pages(message, db, limit=3)

                if similar_pages:
                    # 找到最相關的頁面
                    best_match = similar_pages[0]

                    # 生成動作
                    action = {
                        "type": "navigate",
                        "target": best_match.url_path
                    }

                    # 生成回應文字
                    if self.client and len(message) > 10:
                        # 使用 GPT 生成個性化回應
                        context = f"使用者問：{message}\n最相關的頁面是：{best_match.title}\n頁面描述：{best_match.description}"
                        response_text = await self._get_openai_response_with_context(message, context, conversation_history)
                    else:
                        # 使用預設回應
                        response_text = f"我找到了相關的頁面：{best_match.title}，讓我帶你過去看看！"

                else:
                    # 沒找到相關頁面，使用舊的意圖分類器
                    response_text, action = self.intent_classifier.generate_response_with_action(message)

            finally:
                db.close()

        except Exception as e:
            print(f"RAG system error: {e}")
            # RAG 失敗時使用備用方案
            response_text, action = self.intent_classifier.generate_response_with_action(message)

        return {
            "reply": response_text,
            "action": action
        }

    async def _get_openai_response_with_context(
        self,
        message: str,
        context: str,
        conversation_history: Optional[list] = None
    ) -> str:
        """
        使用 OpenAI API 生成回應（帶有 RAG 上下文）

        Args:
            message: 使用者訊息
            context: RAG 提供的上下文
            conversation_history: 對話歷史

        Returns:
            AI 生成的回應
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"參考資訊：{context}"}
        ]

        # 添加歷史對話（最多保留最近 5 輪）
        if conversation_history:
            messages.extend(conversation_history[-10:])

        # 添加當前訊息
        messages.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=200,
                temperature=0.7,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise

    async def _get_openai_response(
        self,
        message: str,
        conversation_history: Optional[list] = None
    ) -> str:
        """
        使用 OpenAI API 生成回應

        Args:
            message: 使用者訊息
            conversation_history: 對話歷史

        Returns:
            AI 生成的回應
        """
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        # 添加歷史對話（最多保留最近 5 輪）
        if conversation_history:
            messages.extend(conversation_history[-10:])

        # 添加當前訊息
        messages.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=300,
                temperature=0.7,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise

    def get_health_status(self) -> Dict:
        """
        獲取 AI 服務健康狀態

        Returns:
            健康狀態字典
        """
        return {
            "status": "healthy",
            "openai_enabled": self.client is not None,
            "model": self.model if self.client else "fallback",
        }


# 全域 AI 處理器實例
ai_handler = AIHandler()
