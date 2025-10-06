# AiInPocket 部署指南

## 專案資訊

- **網站**: https://aiinpocket.com
- **聯絡信箱**: help@aiinpocket.com
- **專案名稱**: AiInPocket (口袋智慧)

## 已完成項目

### ✓ 功能開發
- [x] 5 個完整頁面（首頁、作品集、技術棧、關於我們、聯絡）
- [x] 科幻視覺設計（淡藍色 × 蘋果綠）
- [x] 粒子背景動畫系統
- [x] 隱藏彩蛋系統
- [x] AI 聊天機器人（前端 + 後端）
- [x] 響應式設計

### ✓ 後端 API
- [x] Python FastAPI 後端
- [x] OpenAI GPT-4 整合
- [x] 意圖分類與頁面操作
- [x] CORS 配置
- [x] 健康檢查端點

### ✓ Docker 容器化
- [x] 前端 Nginx 容器
- [x] 後端 Python 容器
- [x] Docker Compose 編排
- [x] 環境變數管理

### ✓ 代碼優化
- [x] 移除所有 emoji（看起來更專業）
- [x] 更新域名配置
- [x] 更新聯絡信箱

## 本地開發

### 啟動容器

```bash
# Windows
docker-compose up -d --build

# 查看狀態
docker-compose ps

# 查看日誌
docker-compose logs -f

# 停止容器
docker-compose down
```

### 訪問地址

- **前端**: http://localhost:8080
- **後端 API**: http://localhost:8000
- **API 文檔**: http://localhost:8000/docs

## 生產環境部署

### 1. 環境變數設定

確保 `backend/.env` 包含：

```env
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4
CORS_ORIGINS=https://aiinpocket.com,http://aiinpocket.com
APP_NAME=AiInPocket
APP_VERSION=1.0.0
DEBUG=False
```

### 2. 建議的部署架構

```
┌─────────────────┐
│   CloudFlare    │  ← HTTPS, CDN, DDoS Protection
│  (DNS + CDN)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Nginx Proxy   │  ← SSL Termination, Reverse Proxy
│  (VPS/Cloud)    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│Frontend│ │Backend │  ← Docker Containers
│ :8080  │ │ :8000  │
└────────┘ └────────┘
```

### 3. Nginx 配置範例（生產環境）

```nginx
server {
    listen 443 ssl http2;
    server_name aiinpocket.com www.aiinpocket.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # 前端
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 後端 API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name aiinpocket.com www.aiinpocket.com;
    return 301 https://$server_name$request_uri;
}
```

### 4. 部署步驟

```bash
# 1. 複製專案到伺服器
scp -r onepageweb/ user@server:/var/www/

# 2. SSH 登入伺服器
ssh user@server

# 3. 進入專案目錄
cd /var/www/onepageweb

# 4. 設定環境變數
cp backend/.env.example backend/.env
nano backend/.env  # 編輯設定

# 5. 啟動容器
docker-compose up -d --build

# 6. 檢查狀態
docker-compose ps
docker-compose logs -f
```

### 5. SSL 證書

使用 Let's Encrypt 免費 SSL：

```bash
# 安裝 certbot
apt install certbot python3-certbot-nginx

# 取得證書
certbot --nginx -d aiinpocket.com -d www.aiinpocket.com

# 自動更新
certbot renew --dry-run
```

## 監控與維護

### 健康檢查

```bash
# 檢查 API 健康狀態
curl https://aiinpocket.com/api/health

# 預期回應
{
  "status": "healthy",
  "app_name": "AiInPocket",
  "version": "1.0.0",
  "ai_status": {
    "status": "healthy",
    "openai_enabled": true,
    "model": "gpt-4"
  }
}
```

### 日誌管理

```bash
# 查看實時日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f backend
docker-compose logs -f frontend

# 清理舊日誌
docker-compose logs --tail=100 > logs.txt
```

### 備份

```bash
# 備份環境變數
cp backend/.env backend/.env.backup

# 備份整個專案
tar -czf aiinpocket-backup-$(date +%Y%m%d).tar.gz onepageweb/
```

## 性能優化建議

### 1. 前端優化
- 啟用 Gzip 壓縮（已在 nginx.conf 中配置）
- 設定靜態資源快取
- 使用 CDN 加速靜態資源

### 2. 後端優化
- 使用 Redis 快取 AI 回應
- 限制 API 請求頻率（Rate Limiting）
- 設定連接池

### 3. 資料庫（如需要）
- 使用 PostgreSQL 儲存對話歷史
- 定期清理過期會話

## 安全建議

1. **API Key 管理**
   - 絕不提交 `.env` 到版本控制
   - 使用環境變數或密鑰管理服務

2. **CORS 設定**
   - 只允許信任的域名
   - 定期檢查 CORS 配置

3. **更新與補丁**
   - 定期更新 Docker 映像
   - 監控安全漏洞

4. **防火牆**
   - 只開放必要的端口（80, 443）
   - 限制後端 API 端口（8000）僅內部訪問

## 故障排除

### 容器無法啟動

```bash
# 查看錯誤日誌
docker-compose logs backend

# 重新構建
docker-compose down
docker-compose up -d --build
```

### OpenAI API 錯誤

```bash
# 檢查 API Key
docker exec aiinpocket-backend cat .env | grep OPENAI

# 測試 API
docker exec aiinpocket-backend python -c "from openai import OpenAI; print('OK')"
```

### CORS 錯誤

檢查 `backend/.env` 中的 `CORS_ORIGINS` 是否包含正確的域名。

## 聯絡資訊

- **技術支援**: help@aiinpocket.com
- **網站**: https://aiinpocket.com

---

最後更新: 2024-10-06
