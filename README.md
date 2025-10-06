# AiInPocket (口袋智慧)

充滿 AI 與科幻色彩的公司形象網站，配備智能聊天機器人助手

## 🚀 功能特色

- **科幻視覺設計** - 淡藍色 × 蘋果綠配色，粒子動畫背景
- **AI 聊天機器人** - 智能助手可直接操作網頁，引導使用者瀏覽
- **隱藏彩蛋** - Logo hover、鍵盤輸入、Konami Code 等互動彩蛋
- **前後端分離** - 安全的 API Key 管理
- **Docker 容器化** - 一鍵部署

## 📁 專案結構

```
onepageweb/
├── frontend/          # 前端靜態網站
├── backend/           # Python FastAPI 後端
├── docker/            # Docker 配置
└── docker-compose.yml # 容器編排
```

## 🛠️ 技術棧

### 前端
- HTML5 / CSS3 / JavaScript
- 粒子動畫系統
- 響應式設計

### 後端
- Python 3.11
- FastAPI
- OpenAI API / 其他 LLM
- Uvicorn

### 部署
- Docker & Docker Compose
- Nginx

## 🏃 快速開始

### 開發模式

```bash
# 前端開發
cd frontend
python -m http.server 3000

# 後端開發
cd backend
pip install -r requirements.txt
cp .env.example .env  # 配置 API Key
uvicorn app.main:app --reload --port 8000
```

### Docker 部署

```bash
# 建立並啟動所有容器
docker-compose up --build

# 背景執行
docker-compose up -d

# 停止容器
docker-compose down
```

訪問：
- 生產環境: https://aiinpocket.com
- 本地前端: http://localhost:8080
- 後端 API: http://localhost:8000
- API 文檔: http://localhost:8000/docs

## 🎮 隱藏彩蛋

1. **Logo hover** - 滑鼠移到右上角 Logo 顯示委託資訊
2. **鍵盤輸入 "pocket"** - 觸發特殊動畫效果
3. **點擊粒子** - 背景粒子互動
4. **Konami Code** (↑↑↓↓←→←→BA) - 開啟開發者彩蛋

## 🤖 AI 機器人使用範例

使用者可以這樣詢問：
- "帶我去看作品集"
- "我想聯絡你們"
- "介紹一下你們的技術棧"
- "顯示關於我們的資訊"

AI 會自動執行對應的頁面操作。

## ⚙️ 環境變數配置

複製 `backend/.env.example` 到 `backend/.env`，設定：

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4
CORS_ORIGINS=http://localhost:80,http://localhost:3000
```

## 📝 授權

MIT License

## 👨‍💻 開發者

AiInPocket Team - 讓智慧觸手可及
