# AiInPocket - AI 網站生成器

**Demo網站，包含形象官網都是由本專案呈現**
https://aiinpocket.com

**30 秒內使用 AI 生成專業網站**

一個全棧 AI 網站生成平台，讓用戶通過簡單的表單填寫，即可獲得完整、可下載的專業網站。

## ✨ 核心功能

- **AI 自動生成** - 使用 GPT-4/Claude/Gemini 生成完整 HTML
- **25+ 模板風格** - 涵蓋企業、電商、個人品牌等各行業
- **圖片風格分析** - 上傳參考圖片，AI 自動提取設計風格
- **即時預覽** - 生成完成立即查看效果
- **一鍵下載** - ZIP 包含完整網站（HTML + 圖片）
- **會員系統** - 註冊登入，管理所有作品

## 🚀 快速開始

### 系統需求

- Docker & Docker Compose
- 任何 LLM API Key（OpenAI/Claude/Gemini）

### 啟動專案

```bash
# 1. Clone 專案
git clone <repository-url>
cd onepageweb

# 2. 設定環境變數
cp backend/.env.example backend/.env
# 編輯 backend/.env，填入你的 API Key

# 3. 啟動容器
docker-compose up -d

# 4. 訪問網站
# 前端：http://localhost:80
# 後端 API：http://localhost:8000
# API 文檔：http://localhost:8000/docs
```

### Windows 快速啟動

```cmd
start.bat
```

### Linux/Mac 快速啟動

```bash
chmod +x start.sh
./start.sh
```

## 📁 專案結構

```
onepageweb/
├── frontend/              # 前端靜態網站
│   ├── index.html        # 主頁
│   ├── generator/        # AI 生成器頁面
│   │   ├── index.html    # 生成器主頁面
│   │   └── dashboard.html # 我的作品
│   └── corporate/        # 企業頁面
├── backend/              # Python FastAPI 後端
│   ├── app/
│   │   ├── main.py              # 主程式
│   │   ├── website_generator.py # AI 生成核心
│   │   ├── template_styles.py   # 25+ 模板配置
│   │   └── background_tasks.py  # 並行處理（50% CPU）
│   └── requirements.txt
└── docker-compose.yml    # Docker 編排
```

## 🎯 使用流程

### 1. 生成網站

1. 訪問 http://localhost:80/generator/
2. 選擇模板風格（25+ 選項）
3. 填寫公司資訊（名稱、標語、服務等）
4. 填寫聯絡 Email（**必填**）
5. 可選：上傳圖片、作品集
6. 點擊「生成網站」

### 2. 查看作品

1. 點擊「登入」，使用生成時填寫的 Email
2. 進入「我的作品」
3. 查看狀態：
   - ⏳ **生成中** - 等待完成（約 40-50 秒）
   - ✅ **已完成** - 可預覽和下載
   - ❌ **失敗** - 查看錯誤訊息

### 3. 預覽與下載

- **預覽** - 點擊「🔍 預覽」在新視窗查看
- **下載** - 點擊「📥 下載」：
  1. 系統發送 6 位數提取碼到 Email
  2. 輸入提取碼
  3. 下載 ZIP（含 index.html + images/）
  4. 提取碼失效（一次性使用）

## ⚙️ 配置說明

### 環境變數 (backend/.env)

```bash
# === LLM 配置 ===
OPENAI_API_KEY=sk-...           # OpenAI API Key
OPENAI_MODEL=gpt-4              # 使用的模型

# 或使用其他 LLM
ANTHROPIC_API_KEY=sk-ant-...    # Claude
GEMINI_API_KEY=...              # Gemini
OLLAMA_BASE_URL=http://...      # 本地 Ollama

# === 資料庫 ===
DATABASE_URL=postgresql://user:password@db:5432/aiinpocket

# === Email 配置（可選）===
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=noreply@aiinpocket.com

# === 其他 ===
BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:80,http://localhost:3000
```

### LLM 切換

支援多種 LLM，在 `backend/app/config.py` 中配置：

```python
# OpenAI (預設)
LLM_PROVIDER = "openai"
OPENAI_MODEL = "gpt-4"

# Claude
LLM_PROVIDER = "anthropic"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"

# Gemini
LLM_PROVIDER = "gemini"
GEMINI_MODEL = "gemini-1.5-pro"

# 本地 Ollama
LLM_PROVIDER = "ollama"
OLLAMA_MODEL = "llama3"
OLLAMA_BASE_URL = "http://localhost:11434"
```

## 🔧 進階功能

### 並行處理

系統使用 ThreadPoolExecutor 支援並行生成：
- 自動使用 **50% CPU**
- 同時處理多個生成請求
- 每個任務獨立 DB session 和 event loop

### 圖片處理

- 上傳圖片以 base64 儲存在資料庫
- 預覽時嵌入為 data URI
- 下載時轉換為獨立檔案（images/ 資料夾）

### 會員系統

- Email 自動註冊：填寫 Email 即自動創建帳號
- 作品關聯：所有專案自動綁定到 Email
- 專案管理：查看、預覽、下載、刪除

## 📚 更多文檔

- **[DEPLOY.md](./DEPLOY.md)** - 詳細部署指南（生產環境、監控、備份）
- **[CLAUDE.md](./CLAUDE.md)** - Claude Code 開發指引

## 🛠️ 常見問題

### Q: 生成速度可以更快嗎？
A: 主要瓶頸是 LLM API（40-50 秒），可以：
- 使用更快的模型（如 gpt-3.5-turbo）
- 使用本地 Ollama（需高性能 GPU）

### Q: 支援多語言嗎？
A: 預設支援繁體中文、英文、日文三語切換。

### Q: 沒有 Email 伺服器可以用嗎？
A: 可以，Email 功能是可選的。不配置 SMTP 也能正常生成網站，只是無法收到通知和下載碼。

### Q: 如何增加模板？
A: 編輯 `backend/app/template_styles.py`，添加新的模板配置。

### Q: 可以商用嗎？
A: 請確保使用的 LLM API 符合商用授權。OpenAI/Claude/Gemini 皆有商用方案。

## 📞 聯絡我們

- **Website**: https://aiinpocket.com
- **Email**: help@aiinpocket.com

---

**© 2025 AiInPocket. All rights reserved.**
