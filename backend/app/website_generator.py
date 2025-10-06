"""
AI 網站生成引擎
使用 GPT-4 根據使用者需求和模板風格生成完整網站
"""
import os
import json
from typing import Dict, Optional, List
from openai import OpenAI
from .config import settings
from .template_styles import get_template_by_id, TEMPLATE_STYLES


class WebsiteGenerator:
    """AI 網站生成器"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.base_system_prompt = """你是一個專業的網頁設計師和前端開發者。
你的任務是根據使用者提供的資訊和選擇的風格，生成完整的、美觀的、響應式的 HTML 網站。

重要要求：
1. 生成完整的 HTML 檔案，包含 <!DOCTYPE html> 和所有必要標籤
2. 所有 CSS 必須內嵌在 <style> 標籤中
3. 必須包含響應式設計 (@media queries)
4. 顏色配置必須符合指定的風格
5. 必須包含導航列、Hero Section、內容區塊、Footer
6. 使用語義化 HTML5 標籤
7. 確保可訪問性 (accessibility)
8. 不要包含任何 emoji，除非使用者的內容中包含
9. 確保字體、排版、間距都符合現代網頁設計標準
10. 必須包含 AI 聊天機器人的整合點 (預留 div#ai-chat-container)
"""

    async def generate_website(
        self,
        template_id: str,
        user_data: Dict,
        custom_style: Optional[Dict] = None
    ) -> str:
        """
        生成完整網站 HTML

        Args:
            template_id: 模板 ID
            user_data: 使用者提供的資料 (公司名稱、描述、聯絡方式等)
            custom_style: 自訂風格 (如果使用者上傳圖片或文字描述)

        Returns:
            完整的 HTML 字串
        """
        # 獲取模板資訊
        template = get_template_by_id(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")

        # 建立 prompt
        prompt = self._build_generation_prompt(template, user_data, custom_style)

        # 使用 GPT-4 生成
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.base_system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )

            html_content = response.choices[0].message.content

            # 後處理：確保 HTML 完整性
            html_content = self._post_process_html(html_content, user_data)

            return html_content

        except Exception as e:
            print(f"[ERROR] Failed to generate website: {e}")
            # 返回備用模板
            return self._generate_fallback_template(template, user_data)

    def _build_generation_prompt(
        self,
        template: Dict,
        user_data: Dict,
        custom_style: Optional[Dict] = None
    ) -> str:
        """建立生成 prompt"""

        company_name = user_data.get("company_name", "My Company")
        tagline = user_data.get("tagline", "")
        description = user_data.get("description", "")
        services = user_data.get("services", [])
        contact_email = user_data.get("contact_email", "contact@example.com")
        contact_phone = user_data.get("contact_phone", "")
        portfolio_items = user_data.get("portfolio", [])

        prompt = f"""請生成一個完整的單頁網站 (Single Page Website)。

**公司資訊：**
- 公司/品牌名稱：{company_name}
- 標語：{tagline if tagline else '（使用你認為合適的標語）'}
- 公司描述：{description if description else '（根據風格創建合適的描述）'}

**聯絡資訊：**
- Email：{contact_email}
- 電話：{contact_phone if contact_phone else '（可選）'}

"""

        # 加入服務列表
        if services:
            prompt += f"**提供的服務：**\n"
            for i, service in enumerate(services, 1):
                prompt += f"{i}. {service}\n"
            prompt += "\n"

        # 加入作品集
        if portfolio_items:
            prompt += f"**作品集項目：**\n"
            for i, item in enumerate(portfolio_items, 1):
                prompt += f"{i}. {item.get('title', f'作品 {i}')}\n"
                if item.get('description'):
                    prompt += f"   描述：{item['description']}\n"
            prompt += "\n"

        # 加入風格指引
        if custom_style:
            prompt += f"**自訂風格要求：**\n"
            prompt += f"{custom_style.get('description', '')}\n\n"
            if custom_style.get('colors'):
                prompt += f"配色：{custom_style['colors']}\n"
        else:
            prompt += f"""**風格指引：**
- 模板風格：{template['name']}
- 風格描述：{template['description']}
- 風格關鍵字：{', '.join(template.get('style_keywords', []))}

**配色方案：**
- 主色：{template['colors']['primary']}
- 次要色：{template['colors']['secondary']}
- 強調色：{template['colors']['accent']}
- 背景色：{template['colors']['background']}
- 文字色：{template['colors']['text']}

**字體：**
- 標題字體：{template['fonts']['heading']}
- 內文字體：{template['fonts']['body']}
"""

        prompt += """

**網站結構要求：**
1. 導航列 (固定在頂部，包含 Logo 和導航連結)
2. Hero Section (大標題、副標題、CTA 按鈕)
3. 關於/服務區塊 (展示公司介紹或服務)
4. 作品集/產品展示區塊 (如果有提供)
5. 特色/優勢區塊 (3-4 個特色點)
6. 聯絡資訊 Footer

**技術要求：**
- 使用現代 CSS (Flexbox/Grid)
- 響應式設計 (手機、平板、桌面)
- 平滑滾動和過渡效果
- 漂亮的懸停效果
- 在 Footer 前加入一個 <div id="ai-chat-container"></div> 用於 AI 聊天機器人

請直接返回完整的 HTML 程式碼，不要包含任何解釋文字。
"""

        return prompt

    def _post_process_html(self, html: str, user_data: Dict) -> str:
        """後處理 HTML，確保完整性"""

        # 移除 markdown 程式碼區塊標記（如果有）
        html = html.replace("```html", "").replace("```", "")

        # 確保有 <!DOCTYPE html>
        if not html.strip().startswith("<!DOCTYPE"):
            html = "<!DOCTYPE html>\n" + html

        # 確保有 AI 聊天機器人容器
        if "ai-chat-container" not in html:
            # 在 </body> 前加入
            html = html.replace(
                "</body>",
                '<div id="ai-chat-container"></div>\n</body>'
            )

        # 確保有 meta viewport
        if "viewport" not in html:
            html = html.replace(
                "<head>",
                '<head>\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
            )

        return html

    def _generate_fallback_template(self, template: Dict, user_data: Dict) -> str:
        """生成備用模板（當 API 失敗時）"""

        company_name = user_data.get("company_name", "My Company")
        tagline = user_data.get("tagline", "Welcome to our website")
        contact_email = user_data.get("contact_email", "contact@example.com")

        colors = template.get("colors", {})
        primary = colors.get("primary", "#0077BE")
        secondary = colors.get("secondary", "#FF6B35")
        background = colors.get("background", "#FFFFFF")
        text_color = colors.get("text", "#333333")

        return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: {text_color};
            background: {background};
        }}
        nav {{
            background: {primary};
            color: white;
            padding: 1rem 5%;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }}
        .hero {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 6rem 5% 3rem;
            background: linear-gradient(135deg, {primary}, {secondary});
            color: white;
        }}
        .hero h1 {{ font-size: 3rem; margin-bottom: 1rem; }}
        .hero p {{ font-size: 1.3rem; margin-bottom: 2rem; }}
        .btn {{
            display: inline-block;
            padding: 1rem 2rem;
            background: {secondary};
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: transform 0.3s;
        }}
        .btn:hover {{ transform: translateY(-3px); }}
        footer {{
            background: {primary};
            color: white;
            text-align: center;
            padding: 2rem 5%;
        }}
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <nav>
        <h1>{company_name}</h1>
    </nav>
    <section class="hero">
        <div>
            <h1>{company_name}</h1>
            <p>{tagline}</p>
            <a href="#contact" class="btn">聯絡我們</a>
        </div>
    </section>
    <footer id="contact">
        <p>© 2025 {company_name}. All rights reserved.</p>
        <p>Email: {contact_email}</p>
    </footer>
    <div id="ai-chat-container"></div>
</body>
</html>"""

    async def analyze_image_style(self, image_base64: str, description: str = "") -> Dict:
        """
        使用 GPT-4 Vision 分析圖片風格

        Args:
            image_base64: Base64 編碼的圖片
            description: 使用者文字描述

        Returns:
            風格分析結果 (配色、字體建議等)
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized")

        try:
            messages = [
                {
                    "role": "system",
                    "content": "你是一個專業的視覺設計師。分析圖片的視覺風格，提取配色方案、設計風格、氛圍等資訊。"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""請分析這張圖片的視覺風格，並提供網站設計建議。

{f'使用者描述：{description}' if description else ''}

請以 JSON 格式返回：
{{
    "colors": {{
        "primary": "主色 HEX 碼",
        "secondary": "次要色 HEX 碼",
        "accent": "強調色 HEX 碼",
        "background": "背景色 HEX 碼",
        "text": "文字色 HEX 碼"
    }},
    "style": "風格描述（現代、復古、極簡等）",
    "mood": "氛圍描述（溫暖、冷靜、活力等）",
    "fonts": {{
        "heading": "建議的標題字體",
        "body": "建議的內文字體"
    }},
    "keywords": ["關鍵字1", "關鍵字2", "關鍵字3"]
}}"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]

            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=messages,
                max_tokens=1000
            )

            result_text = response.choices[0].message.content

            # 解析 JSON
            import re
            json_match = re.search(r'\{[\s\S]*\}', result_text)
            if json_match:
                style_data = json.loads(json_match.group())
                return style_data
            else:
                raise ValueError("Failed to parse style data from response")

        except Exception as e:
            print(f"[ERROR] Failed to analyze image: {e}")
            # 返回預設風格
            return {
                "colors": {
                    "primary": "#0077BE",
                    "secondary": "#FF6B35",
                    "accent": "#FFD93D",
                    "background": "#FFFFFF",
                    "text": "#333333"
                },
                "style": "現代簡約",
                "mood": "專業友善",
                "fonts": {
                    "heading": "Arial, sans-serif",
                    "body": "Helvetica, sans-serif"
                },
                "keywords": ["現代", "簡潔", "專業"]
            }

    async def update_website(
        self,
        current_html: str,
        instruction: str,
        modifications: Dict
    ) -> str:
        """
        更新現有網站 (增量更新而非完全重新生成)

        Args:
            current_html: 當前的 HTML 內容
            instruction: 使用者的修改指令 (自然語言)
            modifications: 結構化的修改資料

        Returns:
            更新後的 HTML 內容
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized")

        try:
            prompt = f"""你是一個專業的網頁設計師。請根據使用者的指令更新以下 HTML。

**使用者指令：**
{instruction}

**結構化修改資料：**
{json.dumps(modifications, ensure_ascii=False, indent=2)}

**當前 HTML：**
```html
{current_html}
```

**重要要求：**
1. 只修改必要的部分，保留其他內容不變
2. 保持 HTML 結構完整性
3. 確保修改後的網站仍然美觀且響應式
4. 如果修改顏色，要確保配色協調
5. 如果修改文字，要保持語氣和風格一致
6. 返回完整的 HTML 檔案

請直接返回修改後的完整 HTML，不要包含任何解釋或註解。"""

            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.base_system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # 降低溫度以確保一致性
                max_tokens=4000
            )

            updated_html = response.choices[0].message.content

            # 後處理
            updated_html = self._post_process_html(updated_html, {})

            return updated_html

        except Exception as e:
            print(f"[ERROR] Failed to update website: {e}")
            raise


# 全域生成器實例
website_generator = WebsiteGenerator()
