"""
ZIP 打包系統
將生成的網站打包成 ZIP 檔案供使用者下載
"""
import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional
from .config import settings


class ZipBuilder:
    """ZIP 打包器"""

    def __init__(self):
        self.generated_sites_path = Path(settings.GENERATED_SITES_PATH)
        self.generated_sites_path.mkdir(parents=True, exist_ok=True)

    def create_website_package(
        self,
        site_id: str,
        html_content: str,
        user_data: dict,
        with_api_key: bool = False
    ) -> str:
        """
        建立網站打包檔案

        Args:
            site_id: 網站 ID
            html_content: 生成的 HTML 內容
            user_data: 使用者資料
            with_api_key: 是否包含使用者自己的 API key（下載版）

        Returns:
            ZIP 檔案路徑
        """
        # 建立臨時資料夾
        site_dir = self.generated_sites_path / site_id
        site_dir.mkdir(parents=True, exist_ok=True)

        try:
            # 1. 儲存主要 HTML
            index_path = site_dir / "index.html"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # 2. 建立 AI 聊天機器人 JS
            self._create_ai_chat_js(site_dir, site_id, with_api_key)

            # 3. 建立 .env 範例檔案（下載版）
            if with_api_key:
                self._create_env_template(site_dir)

            # 4. 建立 README.md
            self._create_readme(site_dir, user_data, with_api_key)

            # 5. 複製必要的資源檔案（如果有）
            self._copy_assets(site_dir)

            # 6. 打包成 ZIP
            zip_path = self.generated_sites_path / f"{site_id}.zip"
            self._create_zip(site_dir, zip_path)

            return str(zip_path)

        except Exception as e:
            print(f"[ERROR] Failed to create package: {e}")
            raise
        finally:
            # 清理臨時資料夾（保留 ZIP）
            if site_dir.exists():
                shutil.rmtree(site_dir, ignore_errors=True)

    def _create_ai_chat_js(self, site_dir: Path, site_id: str, with_api_key: bool):
        """建立 AI 聊天機器人 JavaScript"""

        if with_api_key:
            # 下載版：讓使用者自己填入 API key
            js_content = f"""/**
 * AI 聊天機器人
 * 請在 .env 檔案中設定您的 OPENAI_API_KEY
 */

// ===== 配置 =====
const CONFIG = {{
    apiKey: '', // 請從 .env 檔案讀取或直接填入您的 OpenAI API Key
    apiEndpoint: 'https://api.openai.com/v1/chat/completions',
    model: 'gpt-4',
    siteId: '{site_id}',
    usageLimit: null // 下載版無使用限制
}};

// ===== 主要功能 =====
class AIChatBot {{
    constructor() {{
        this.messages = [];
        this.init();
    }}

    init() {{
        this.createChatUI();
        this.attachEventListeners();
    }}

    createChatUI() {{
        const container = document.getElementById('ai-chat-container');
        if (!container) return;

        container.innerHTML = `
            <div id="ai-chat-widget" class="ai-chat-widget">
                <button id="chat-toggle" class="chat-toggle-btn">
                    <span>💬</span>
                </button>
                <div id="chat-window" class="chat-window" style="display: none;">
                    <div class="chat-header">
                        <h3>AI 助手</h3>
                        <button id="chat-close">&times;</button>
                    </div>
                    <div id="chat-messages" class="chat-messages"></div>
                    <div class="chat-input-area">
                        <input type="text" id="chat-input" placeholder="輸入訊息..." />
                        <button id="chat-send">發送</button>
                    </div>
                </div>
            </div>
            <style>
                .ai-chat-widget {{
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 9999;
                }}
                .chat-toggle-btn {{
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    color: white;
                    font-size: 28px;
                    cursor: pointer;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    transition: transform 0.3s;
                }}
                .chat-toggle-btn:hover {{
                    transform: scale(1.1);
                }}
                .chat-window {{
                    position: absolute;
                    bottom: 80px;
                    right: 0;
                    width: 350px;
                    height: 500px;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                }}
                .chat-header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                .chat-header h3 {{
                    margin: 0;
                    font-size: 16px;
                }}
                #chat-close {{
                    background: none;
                    border: none;
                    color: white;
                    font-size: 24px;
                    cursor: pointer;
                }}
                .chat-messages {{
                    flex: 1;
                    overflow-y: auto;
                    padding: 15px;
                    background: #f5f5f5;
                }}
                .chat-input-area {{
                    display: flex;
                    padding: 10px;
                    border-top: 1px solid #ddd;
                    background: white;
                }}
                #chat-input {{
                    flex: 1;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 20px;
                    outline: none;
                }}
                #chat-send {{
                    margin-left: 10px;
                    padding: 10px 20px;
                    background: #667eea;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    cursor: pointer;
                }}
                .message {{
                    margin-bottom: 10px;
                    padding: 10px;
                    border-radius: 10px;
                    max-width: 80%;
                }}
                .user-message {{
                    background: #667eea;
                    color: white;
                    margin-left: auto;
                }}
                .bot-message {{
                    background: white;
                }}
            </style>
        `;
    }}

    attachEventListeners() {{
        const toggleBtn = document.getElementById('chat-toggle');
        const closeBtn = document.getElementById('chat-close');
        const sendBtn = document.getElementById('chat-send');
        const input = document.getElementById('chat-input');
        const chatWindow = document.getElementById('chat-window');

        toggleBtn?.addEventListener('click', () => {{
            chatWindow.style.display = chatWindow.style.display === 'none' ? 'flex' : 'none';
        }});

        closeBtn?.addEventListener('click', () => {{
            chatWindow.style.display = 'none';
        }});

        sendBtn?.addEventListener('click', () => this.sendMessage());
        input?.addEventListener('keypress', (e) => {{
            if (e.key === 'Enter') this.sendMessage();
        }});
    }}

    async sendMessage() {{
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        if (!message) return;

        // 檢查 API Key
        if (!CONFIG.apiKey) {{
            alert('請先在 .env 檔案中設定您的 OPENAI_API_KEY');
            return;
        }}

        // 顯示使用者訊息
        this.addMessage(message, 'user');
        input.value = '';

        // 呼叫 OpenAI API
        try {{
            const response = await fetch(CONFIG.apiEndpoint, {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${{CONFIG.apiKey}}`
                }},
                body: JSON.stringify({{
                    model: CONFIG.model,
                    messages: [
                        ...this.messages,
                        {{ role: 'user', content: message }}
                    ],
                    max_tokens: 500,
                    temperature: 0.7
                }})
            }});

            const data = await response.json();
            const reply = data.choices[0].message.content;

            this.messages.push({{ role: 'user', content: message }});
            this.messages.push({{ role: 'assistant', content: reply }});

            this.addMessage(reply, 'bot');
        }} catch (error) {{
            console.error('AI Error:', error);
            this.addMessage('抱歉，發生錯誤。請檢查您的 API Key 設定。', 'bot');
        }}
    }}

    addMessage(text, type) {{
        const messagesDiv = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${{type}}-message`;
        messageDiv.textContent = text;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }}
}}

// 初始化
document.addEventListener('DOMContentLoaded', () => {{
    new AIChatBot();
}});
"""
        else:
            # 預覽版：使用平台 API key，有 30 次限制
            js_content = f"""/**
 * AI 聊天機器人 (預覽版)
 * 使用平台 API key，限用 30 次
 */

// ===== 配置 =====
const CONFIG = {{
    apiEndpoint: '{settings.SITE_URL}/api/chat-preview',
    siteId: '{site_id}',
    usageLimit: {settings.PREVIEW_API_LIMIT}
}};

// ===== 主要功能 =====
class AIChatBot {{
    constructor() {{
        this.messages = [];
        this.usageCount = this.getUsageCount();
        this.init();
    }}

    init() {{
        this.createChatUI();
        this.attachEventListeners();
        this.updateUsageDisplay();
    }}

    getUsageCount() {{
        const stored = localStorage.getItem(`chat_usage_${{CONFIG.siteId}}`);
        return stored ? parseInt(stored) : 0;
    }}

    incrementUsage() {{
        this.usageCount++;
        localStorage.setItem(`chat_usage_${{CONFIG.siteId}}`, this.usageCount);
        this.updateUsageDisplay();
    }}

    updateUsageDisplay() {{
        const remaining = CONFIG.usageLimit - this.usageCount;
        const usageEl = document.getElementById('usage-count');
        if (usageEl) {{
            usageEl.textContent = `剩餘 ${{remaining}} 次`;
            if (remaining <= 5) {{
                usageEl.style.color = '#ff4444';
            }}
        }}
    }}

    createChatUI() {{
        const container = document.getElementById('ai-chat-container');
        if (!container) return;

        container.innerHTML = `
            <div id="ai-chat-widget" class="ai-chat-widget">
                <button id="chat-toggle" class="chat-toggle-btn">
                    <span>💬</span>
                </button>
                <div id="chat-window" class="chat-window" style="display: none;">
                    <div class="chat-header">
                        <h3>AI 助手 <span id="usage-count" style="font-size: 12px;"></span></h3>
                        <button id="chat-close">&times;</button>
                    </div>
                    <div id="chat-messages" class="chat-messages"></div>
                    <div class="chat-input-area">
                        <input type="text" id="chat-input" placeholder="輸入訊息..." />
                        <button id="chat-send">發送</button>
                    </div>
                </div>
            </div>
            <style>
                .ai-chat-widget {{
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 9999;
                }}
                .chat-toggle-btn {{
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    color: white;
                    font-size: 28px;
                    cursor: pointer;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    transition: transform 0.3s;
                }}
                .chat-toggle-btn:hover {{
                    transform: scale(1.1);
                }}
                .chat-window {{
                    position: absolute;
                    bottom: 80px;
                    right: 0;
                    width: 350px;
                    height: 500px;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                }}
                .chat-header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                .chat-header h3 {{
                    margin: 0;
                    font-size: 16px;
                    display: flex;
                    flex-direction: column;
                    gap: 4px;
                }}
                #chat-close {{
                    background: none;
                    border: none;
                    color: white;
                    font-size: 24px;
                    cursor: pointer;
                }}
                .chat-messages {{
                    flex: 1;
                    overflow-y: auto;
                    padding: 15px;
                    background: #f5f5f5;
                }}
                .chat-input-area {{
                    display: flex;
                    padding: 10px;
                    border-top: 1px solid #ddd;
                    background: white;
                }}
                #chat-input {{
                    flex: 1;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 20px;
                    outline: none;
                }}
                #chat-send {{
                    margin-left: 10px;
                    padding: 10px 20px;
                    background: #667eea;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    cursor: pointer;
                }}
                .message {{
                    margin-bottom: 10px;
                    padding: 10px;
                    border-radius: 10px;
                    max-width: 80%;
                    word-wrap: break-word;
                }}
                .user-message {{
                    background: #667eea;
                    color: white;
                    margin-left: auto;
                }}
                .bot-message {{
                    background: white;
                }}
            </style>
        `;
    }}

    attachEventListeners() {{
        const toggleBtn = document.getElementById('chat-toggle');
        const closeBtn = document.getElementById('chat-close');
        const sendBtn = document.getElementById('chat-send');
        const input = document.getElementById('chat-input');
        const chatWindow = document.getElementById('chat-window');

        toggleBtn?.addEventListener('click', () => {{
            chatWindow.style.display = chatWindow.style.display === 'none' ? 'flex' : 'none';
        }});

        closeBtn?.addEventListener('click', () => {{
            chatWindow.style.display = 'none';
        }});

        sendBtn?.addEventListener('click', () => this.sendMessage());
        input?.addEventListener('keypress', (e) => {{
            if (e.key === 'Enter') this.sendMessage();
        }});
    }}

    async sendMessage() {{
        // 檢查使用次數
        if (this.usageCount >= CONFIG.usageLimit) {{
            alert('試用次數已用完！請下載完整版並使用您自己的 API Key。');
            return;
        }}

        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        if (!message) return;

        // 顯示使用者訊息
        this.addMessage(message, 'user');
        input.value = '';

        // 呼叫平台 API
        try {{
            const response = await fetch(CONFIG.apiEndpoint, {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{
                    site_id: CONFIG.siteId,
                    message: message,
                    history: this.messages
                }})
            }});

            const data = await response.json();

            if (data.error) {{
                throw new Error(data.error);
            }}

            const reply = data.reply;
            this.messages.push({{ role: 'user', content: message }});
            this.messages.push({{ role: 'assistant', content: reply }});

            this.addMessage(reply, 'bot');
            this.incrementUsage();

        }} catch (error) {{
            console.error('AI Error:', error);
            this.addMessage('抱歉，發生錯誤。請稍後再試。', 'bot');
        }}
    }}

    addMessage(text, type) {{
        const messagesDiv = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${{type}}-message`;
        messageDiv.textContent = text;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }}
}}

// 初始化
document.addEventListener('DOMContentLoaded', () => {{
    new AIChatBot();
}});
"""

        js_path = site_dir / "ai-chat.js"
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)

    def _create_env_template(self, site_dir: Path):
        """建立 .env 範例檔案"""
        env_content = """# OpenAI API Configuration
# 請在此填入您的 OpenAI API Key
# 取得 API Key：https://platform.openai.com/api-keys

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# 網站設定
SITE_NAME=Your Website Name
"""
        env_path = site_dir / ".env.example"
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)

    def _create_readme(self, site_dir: Path, user_data: dict, with_api_key: bool):
        """建立 README.md"""
        company_name = user_data.get("company_name", "Your Company")

        readme_content = f"""# {company_name} - AI 生成網站

此網站由 AiInPocket AI 網站生成器自動建立。

## 📁 檔案說明

- `index.html` - 主要網頁檔案
- `ai-chat.js` - AI 聊天機器人功能
"""

        if with_api_key:
            readme_content += """- `.env.example` - 環境變數範例檔案

## 🚀 如何使用

### 1. 設定 API Key

複製 `.env.example` 為 `.env`：
```bash
cp .env.example .env
```

編輯 `.env` 檔案，填入您的 OpenAI API Key：
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 2. 啟動網站

您可以使用任何靜態網站伺服器：

**方法 1: 使用 Python**
```bash
python -m http.server 8000
```

**方法 2: 使用 Node.js**
```bash
npx http-server
```

**方法 3: 使用 VS Code**
安裝 "Live Server" 擴充套件，右鍵點擊 index.html 選擇 "Open with Live Server"

### 3. 訪問網站

開啟瀏覽器，訪問 http://localhost:8000

## 💬 AI 聊天機器人

網站已整合 AI 聊天機器人功能。確保您已設定 API Key 後：
- 點擊右下角的聊天圖示
- 輸入問題即可與 AI 對話
- AI 會根據網站內容回答訪客的問題

## 📝 自訂網站

您可以直接編輯 `index.html` 來修改網站內容。所有樣式都在 `<style>` 標籤中。

## 🔒 安全建議

- **切勿**將包含真實 API Key 的 `.env` 檔案提交到 Git
- **切勿**在前端程式碼中直接暴露 API Key
- 考慮使用後端代理來保護您的 API Key

## 📧 技術支援

如有任何問題，請聯繫：
- Email: support@aiinpocket.com
- 網站: https://aiinpocket.com
"""
        else:
            readme_content += """
## 🎯 試用版說明

此為預覽版網站，AI 聊天機器人限用 30 次。

### 如何獲得完整版？

1. 回到生成頁面
2. 點擊「下載完整版」
3. 設定您自己的 OpenAI API Key
4. 無使用次數限制！

## 💬 AI 聊天機器人

- 點擊右下角的聊天圖示
- 輸入問題即可與 AI 對話
- 試用版限用 30 次

## 📧 聯絡我們

Email: support@aiinpocket.com
網站: https://aiinpocket.com
"""

        readme_content += f"""
---

© 2025 AiInPocket. Generated by AI Website Generator.
Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        readme_path = site_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)

    def _copy_assets(self, site_dir: Path):
        """複製必要的資源檔案"""
        # 未來可以在這裡複製圖片、字體等資源
        pass

    def _create_zip(self, source_dir: Path, zip_path: Path):
        """建立 ZIP 檔案"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(source_dir)
                    zipf.write(file_path, arcname)

    def get_download_url(self, site_id: str) -> str:
        """獲取下載 URL"""
        return f"{settings.DOWNLOAD_BASE_URL}/{site_id}.zip"


# 全域實例
zip_builder = ZipBuilder()
