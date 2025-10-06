"""
AI 翻譯服務
使用 OpenAI API 進行多語言翻譯
"""
from typing import Dict, List
from openai import OpenAI
from .config import settings
import json


class TranslationService:
    """AI 翻譯服務"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    async def translate_content(
        self,
        content: Dict,
        source_lang: str = "zh-TW",
        target_langs: List[str] = ["en", "ja"]
    ) -> Dict[str, Dict]:
        """
        翻譯網站內容到多種語言

        Args:
            content: 原始內容（中文）
            source_lang: 來源語言
            target_langs: 目標語言列表

        Returns:
            翻譯後的內容字典 {language: content}
        """
        if not self.client:
            print("[WARN] OpenAI API Key not set, translation skipped")
            return {source_lang: content}

        translations = {source_lang: content}

        for target_lang in target_langs:
            if target_lang == source_lang:
                continue

            try:
                lang_name = {
                    "en": "English",
                    "ja": "Japanese (日本語)",
                    "zh-TW": "Traditional Chinese (繁體中文)",
                    "zh-CN": "Simplified Chinese (简体中文)",
                    "ko": "Korean (한국어)",
                    "es": "Spanish",
                    "fr": "French",
                    "de": "German"
                }.get(target_lang, target_lang)

                prompt = f"""You are a professional translator. Translate the following website content to {lang_name}.

IMPORTANT RULES:
1. Keep HTML tags unchanged (like <strong>, <br>, etc.)
2. Keep technical terms in English (like "AI", "DevOps", "Cloud", "Python", "Docker", etc.)
3. Preserve the JSON structure exactly
4. Translate naturally, don't translate word by word
5. Keep URLs, email addresses, and code unchanged
6. Maintain the same tone and style

Source content (JSON):
{json.dumps(content, ensure_ascii=False, indent=2)}

Return ONLY the translated JSON without any explanation."""

                response = self.client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional website content translator. Return only valid JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=4000
                )

                translated_text = response.choices[0].message.content.strip()

                # 移除可能的 markdown 代碼塊標記
                if translated_text.startswith("```json"):
                    translated_text = translated_text[7:]
                if translated_text.startswith("```"):
                    translated_text = translated_text[3:]
                if translated_text.endswith("```"):
                    translated_text = translated_text[:-3]

                translated_content = json.loads(translated_text.strip())
                translations[target_lang] = translated_content

                print(f"[OK] Translated to {lang_name}")

            except Exception as e:
                print(f"[ERROR] Translation to {target_lang} failed: {e}")
                # 失敗時使用原始內容
                translations[target_lang] = content

        return translations

    async def generate_i18n_js(self, translations: Dict[str, Dict]) -> str:
        """
        生成 i18n.js 文件內容

        Args:
            translations: 翻譯字典 {language: content}

        Returns:
            i18n.js 文件內容
        """
        i18n_template = """/**
 * 多語言系統 (i18n)
 * 由 AI 自動生成
 */

const translations = """ + json.dumps(translations, ensure_ascii=False, indent=4) + """;

// 當前語言（預設繁體中文）
let currentLanguage = localStorage.getItem('language') || 'zh-TW';

/**
 * 取得翻譯文字
 */
function t(key) {
    const keys = key.split('.');
    let value = translations[currentLanguage];

    for (const k of keys) {
        value = value?.[k];
    }

    return value || key;
}

/**
 * 切換語言
 */
function setLanguage(lang) {
    if (!translations[lang]) {
        console.error(`Language ${lang} not supported`);
        return;
    }

    currentLanguage = lang;
    localStorage.setItem('language', lang);
    updatePageContent();

    // 觸發語言變更事件
    document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
}

/**
 * 取得當前語言
 */
function getCurrentLanguage() {
    return currentLanguage;
}

/**
 * 更新頁面內容
 */
function updatePageContent() {
    // 更新所有帶有 data-i18n 屬性的元素
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = t(key);

        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            element.placeholder = translation;
        } else if (element.tagName === 'SELECT') {
            return;
        } else {
            element.innerHTML = translation;
        }
    });

    // 更新頁面語言屬性
    document.documentElement.lang = currentLanguage;
}

// 頁面載入時初始化
document.addEventListener('DOMContentLoaded', () => {
    updatePageContent();
});
"""
        return i18n_template


# 全域實例
translation_service = TranslationService()
