"""
AI 對話處理模組
整合 OpenAI API 或其他 LLM
"""
import os
from typing import Dict, Optional
from openai import OpenAI
from .config import settings
from .actions import IntentClassifier


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
        self.system_prompt = """你是 AiInPocket (口袋智慧) 的 AI 助手。

公司簡介：
- AiInPocket 是一家專注於 AI 解決方案、雲端架構和 DevOps 工程的科技公司
- 使命：將最先進的技術以最簡潔的方式交付到客戶手中
- 口號：讓智慧觸手可及

核心服務：
1. AI 解決方案
   - 深度學習、自然語言處理、電腦視覺
   - 客製化 AI 模型訓練
   - LLM 應用整合
   - 技術：Python, TensorFlow, PyTorch, OpenAI

2. 雲端架構
   - 雲原生架構設計
   - 容器化與編排 (Kubernetes)
   - 無伺服器架構
   - 技術：AWS, Azure, GCP, Docker

3. DevOps 工程
   - CI/CD 自動化部署
   - 基礎設施即代碼 (Terraform)
   - 監控與日誌系統
   - 技術：Jenkins, GitLab CI, Prometheus, Grafana

你的任務：
1. 友善、專業地回答使用者問題
2. 引導使用者瀏覽網站相關頁面
3. 介紹公司服務與技術能力
4. 回應時要簡潔有力，使用 emoji 增加親和力
5. 當使用者想查看特定內容時，告知他們你會帶他們前往相關頁面

重要：回答要簡短（2-3 句話），並使用繁體中文。
"""

    async def process_message(
        self,
        message: str,
        session_id: str,
        conversation_history: Optional[list] = None
    ) -> Dict:
        """
        處理使用者訊息並生成回應

        Args:
            message: 使用者訊息
            session_id: 會話 ID
            conversation_history: 對話歷史

        Returns:
            包含 reply 和 action 的字典
        """
        # 首先使用意圖分類器判斷是否有明確動作
        response_text, action = self.intent_classifier.generate_response_with_action(message)

        # 如果有 OpenAI 客戶端且訊息比較複雜，使用 GPT 生成更好的回應
        if self.client and len(message) > 20:
            try:
                response_text = await self._get_openai_response(message, conversation_history)
            except Exception as e:
                print(f"OpenAI API error: {e}")
                # 發生錯誤時使用備用回應
                pass

        return {
            "reply": response_text,
            "action": action
        }

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
