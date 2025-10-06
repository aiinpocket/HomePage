# AiInPocket 快速開始指南

## 🚀 5 分鐘快速啟動

### 方法 1：使用 Docker（推薦）

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### 方法 2：本地開發

#### 1. 啟動前端

```bash
cd frontend
python -m http.server 3000
```

訪問 http://localhost:3000

#### 2. 啟動後端（可選）

```bash
cd backend
pip install -r requirements.txt

# 複製環境變數檔案
cp .env.example .env

# 編輯 .env 並設定你的 OPENAI_API_KEY（可選）

# 啟動後端
uvicorn app.main:app --reload --port 8000
```

訪問 http://localhost:8000/docs 查看 API 文檔

## 📋 前置需求

### Docker 方式
- Docker
- Docker Compose

### 本地開發方式
- Python 3.11+
- 任何 HTTP 伺服器（如 Python http.server, Node.js http-server 等）

## 🎯 功能測試清單

### ✅ 前端測試

1. **粒子背景動畫**
   - 打開首頁，應該看到淡藍色與蘋果綠的粒子動畫
   - 滑鼠移動時，粒子會躲避游標

2. **導航功能**
   - 點擊導航列各項目，應該能正確跳轉
   - 手機版：點擊漢堡選單應能展開/收起

3. **隱藏彩蛋**
   - **Logo hover**: 滑鼠移到左上角 Logo，會顯示委託資訊框
   - **鍵盤輸入**: 在頁面上輸入 "pocket"（不在輸入框中），會觸發彩蛋
   - **點擊粒子**: 點擊背景粒子會有爆炸效果
   - **Konami Code**: 輸入 ↑↑↓↓←→←→BA（方向鍵+字母鍵）

4. **作品集篩選**
   - 進入作品集頁面
   - 點擊篩選按鈕（全部/AI/雲端/DevOps）
   - 卡片應該會動態顯示/隱藏

5. **聯絡表單**
   - 填寫聯絡表單
   - 提交後應該顯示成功訊息

### ✅ AI 聊天機器人測試

1. **基本對話**
   - 點擊右下角的 🤖 按鈕
   - 聊天視窗應該彈出並顯示歡迎訊息

2. **快速動作**
   - 點擊快速按鈕（查看作品集、聯絡我們等）
   - 應該會自動填入訊息並觸發對應動作

3. **頁面導航**
   試試這些訊息：
   - "帶我去看作品集"
   - "我想聯絡你們"
   - "介紹一下技術棧"
   - "告訴我關於你們"

   每個訊息都應該：
   - 顯示 AI 回應
   - 自動跳轉到對應頁面

4. **對話歷史**
   - 發送多條訊息
   - 歷史對話應該保留
   - 滾動應該自動到底部

### ✅ 後端 API 測試

如果你啟動了後端：

1. **健康檢查**
   ```bash
   curl http://localhost:8000/api/health
   ```

   應該返回系統狀態

2. **聊天 API**
   ```bash
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -d '{
       "message": "帶我去看作品集",
       "session_id": "test123"
     }'
   ```

   應該返回包含 `reply` 和 `action` 的 JSON

3. **API 文檔**
   訪問 http://localhost:8000/docs
   應該看到 Swagger UI 介面

## 🔧 設定 OpenAI API（可選）

1. 編輯 `backend/.env`：
   ```env
   OPENAI_API_KEY=sk-your-actual-api-key-here
   OPENAI_MODEL=gpt-4
   ```

2. 重啟後端容器：
   ```bash
   docker-compose restart backend
   ```

3. 測試對話，應該會得到更智能的回應

**注意**: 沒有 API Key 也能正常運行，系統會使用內建的規則式回應。

## 🐛 故障排除

### Docker 容器無法啟動

```bash
# 查看錯誤日誌
docker-compose logs backend
docker-compose logs frontend

# 完全重建
docker-compose down
docker-compose up --build --force-recreate
```

### 前端無法訪問

- 確認端口 80 沒有被占用
- 嘗試使用其他端口：`docker-compose.yml` 中修改 `80:80` 為 `8080:80`

### 後端 API 連接失敗

- 檢查後端是否在運行：`docker ps`
- 查看 Nginx 配置是否正確代理到後端
- 檢查瀏覽器控制台的網路請求

### AI 回應異常

- 確認 `backend/.env` 中的 API Key 是否正確
- 查看後端日誌：`docker-compose logs -f backend`
- 沒有 API Key 時，系統會使用備用回應

## 📚 更多資訊

- 完整文檔：查看 `README.md`
- 開發指南：查看 `CLAUDE.md`
- API 文檔：http://localhost:8000/docs（後端運行時）

## 🎉 享受 AiInPocket！

如果一切正常，你應該能看到：
- ✅ 科幻風格的粒子背景
- ✅ 流暢的頁面導航
- ✅ 互動式 AI 聊天機器人
- ✅ 各種隱藏彩蛋

有問題嗎？檢查控制台日誌或查看文檔！
