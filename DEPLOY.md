# AiInPocket 部署指南

## 📋 目錄

- [專案概述](#專案概述)
- [系統需求](#系統需求)
- [快速開始](#快速開始)
- [詳細部署步驟](#詳細部署步驟)
- [生產環境部署](#生產環境部署)
- [故障排除](#故障排除)
- [維護與監控](#維護與監控)

## 專案概述

**AiInPocket** 是一個充滿 AI 與科幻色彩的公司形象網站，配備智能聊天機器人助手和 AI 網站生成器功能。

### 核心功能

1. **AI 聊天機器人** - 智能助手可直接操作網頁，引導使用者瀏覽
2. **AI 網站生成器** - 30 秒內根據使用者需求生成專業網站
3. **25+ 種模板風格** - 涵蓋各行各業的設計風格
4. **隱藏彩蛋系統** - Logo hover、Konami Code 等互動彩蛋
5. **RAG 知識庫** - 基於網站內容的智能問答系統

### 技術棧

**前端：**
- HTML5 / CSS3 / JavaScript (無框架，原生開發)
- 粒子動畫系統 (Canvas)
- 響應式設計

**後端：**
- Python 3.11
- FastAPI (現代化 Web 框架)
- OpenAI GPT-4 (AI 對話與網站生成)
- PostgreSQL + pgvector (向量資料庫)
- Redis (快取與使用量追蹤)

**部署：**
- Docker & Docker Compose
- Nginx (反向代理)

---

## 系統需求

### 開發環境

- **作業系統:** Windows 10/11, macOS, Linux
- **Python:** 3.11 或以上
- **Node.js:** 非必需（前端為純 HTML/CSS/JS）
- **Docker:** 20.10 或以上 (推薦)
- **Docker Compose:** 2.0 或以上

### 生產環境

- **CPU:** 2 核心以上
- **記憶體:** 4GB RAM 以上 (推薦 8GB)
- **硬碟:** 20GB 可用空間
- **網路:** 穩定的網際網路連接 (需要呼叫 OpenAI API)

---

## 快速開始

### 方法一：使用 Docker Compose（推薦）

```bash
# 1. Clone 專案
git clone https://github.com/your-org/onepageweb.git
cd onepageweb

# 2. 設定環境變數
cd backend
cp .env.example .env
nano .env  # 編輯並填入 OPENAI_API_KEY

# 3. 啟動所有服務
docker-compose up -d

# 4. 查看日誌
docker-compose logs -f

# 5. 訪問網站
# 前端: http://localhost:8000
# 後端 API: http://localhost:8001
# API 文檔: http://localhost:8001/docs
```

### 方法二：本地開發

```bash
# 前端開發
cd frontend
python -m http.server 3000
# 訪問 http://localhost:3000

# 後端開發 (新終端)
cd backend
pip install -r requirements.txt
cp .env.example .env
nano .env  # 填入 OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
# API 訪問 http://localhost:8000
```

---

## 詳細部署步驟

### 1. 環境準備

#### 1.1 安裝 Docker

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

**macOS:**
```bash
brew install --cask docker
# 或從官網下載 Docker Desktop: https://www.docker.com/products/docker-desktop
```

**Windows:**
- 下載並安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- 啟用 WSL 2 (Windows Subsystem for Linux 2)

#### 1.2 驗證安裝

```bash
docker --version
docker-compose --version
```

### 2. 取得專案原始碼

```bash
git clone https://github.com/your-org/onepageweb.git
cd onepageweb
```

### 3. 配置環境變數

#### 3.1 後端配置

```bash
cd backend
cp .env.example .env
```

編輯 `.env` 文件：

```env
# ========================================
# OpenAI API 設定 (必填)
# ========================================
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4

# ========================================
# CORS 設定
# ========================================
CORS_ORIGINS=http://localhost:80,http://localhost:3000,http://localhost:8080,https://yourdomain.com

# ========================================
# 應用設定
# ========================================
APP_NAME=AiInPocket
APP_VERSION=1.0.0
DEBUG=True

# ========================================
# PostgreSQL 設定 (Docker 自動配置)
# ========================================
DATABASE_URL=postgresql://aiinpocket:aiinpocket_secure_password@postgres:5432/aiinpocket

# ========================================
# 網站設定
# ========================================
SITE_URL=https://yourdomain.com
FRONTEND_PATH=/app/frontend

# ========================================
# Email 設定 (選填，用於網站生成通知)
# ========================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=AiInPocket <noreply@yourdomain.com>

# ========================================
# Redis 設定 (Docker 自動配置)
# ========================================
REDIS_URL=redis://redis:6379/0

# ========================================
# 生成網站設定
# ========================================
PREVIEW_API_LIMIT=30
GENERATED_SITES_PATH=/app/generated_sites
DOWNLOAD_BASE_URL=https://yourdomain.com/download
```

**重要配置說明：**

1. **OPENAI_API_KEY (必填):**
   - 從 [OpenAI Platform](https://platform.openai.com/api-keys) 取得
   - 確保帳戶有足夠的額度

2. **CORS_ORIGINS:**
   - 生產環境請改為實際的域名
   - 多個來源用逗號分隔

3. **SMTP 設定 (選填):**
   - 如需發送網站生成通知，請配置 SMTP
   - Gmail 需使用[應用程式密碼](https://myaccount.google.com/apppasswords)

### 4. 建立必要目錄

```bash
# 返回專案根目錄
cd ..

# 建立生成網站的存放目錄
mkdir -p backend/generated_sites
```

### 5. 啟動服務

#### 5.1 使用 Docker Compose (推薦)

```bash
# 建立並啟動所有容器
docker-compose up -d --build

# 查看服務狀態
docker-compose ps

# 查看即時日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

#### 5.2 等待服務啟動

```bash
# 檢查後端健康狀態
curl http://localhost:8001/api/health

# 檢查前端
curl http://localhost:8000
```

### 6. 驗證部署

訪問以下 URL 確認服務正常：

- **前端網站:** http://localhost:8000
- **後端 API:** http://localhost:8001/api/health
- **API 文檔:** http://localhost:8001/docs
- **網站生成器:** http://localhost:8000/generator.html

---

## 生產環境部署

### 1. 使用 Nginx 反向代理

#### 1.1 安裝 Nginx

```bash
sudo apt-get install nginx
```

#### 1.2 配置 Nginx

建立 `/etc/nginx/sites-available/aiinpocket` 文件：

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # 前端靜態文件
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 後端 API
    location /api/ {
        proxy_pass http://localhost:8001/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # 超時設定
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

啟用網站：

```bash
sudo ln -s /etc/nginx/sites-available/aiinpocket /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 2. 配置 SSL (Let's Encrypt)

```bash
# 安裝 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 自動配置 SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 測試自動續期
sudo certbot renew --dry-run
```

### 3. 生產環境優化

#### 3.1 修改環境變數

```env
# 關閉除錯模式
DEBUG=False

# 更新 CORS 來源
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# 更新網站 URL
SITE_URL=https://yourdomain.com
```

#### 3.2 增強資料庫安全性

修改 `docker-compose.yml` 中的資料庫密碼：

```yaml
postgres:
  environment:
    POSTGRES_PASSWORD: your-strong-password-here
```

同時更新 `.env` 中的 `DATABASE_URL`：

```env
DATABASE_URL=postgresql://aiinpocket:your-strong-password-here@postgres:5432/aiinpocket
```

#### 3.3 設定自動重啟

```bash
# 確保 Docker 容器自動重啟
docker-compose up -d --force-recreate
```

### 4. 監控與日誌

#### 4.1 查看容器狀態

```bash
docker-compose ps
docker stats
```

#### 4.2 持久化日誌

修改 `docker-compose.yml` 添加日誌配置：

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 故障排除

### 問題 1: Docker 容器無法啟動

**症狀：** `docker-compose up` 失敗

**解決方法：**

```bash
# 查看詳細錯誤
docker-compose logs backend

# 重新建立容器
docker-compose down -v
docker-compose up --build --force-recreate
```

### 問題 2: API 連接失敗

**症狀：** 前端無法連接到後端 API

**解決方法：**

1. 檢查後端容器是否運行：
```bash
docker ps | grep backend
```

2. 檢查後端健康狀態：
```bash
curl http://localhost:8001/api/health
```

3. 查看 Nginx 配置：
```bash
sudo nginx -t
```

### 問題 3: OpenAI API 錯誤

**症狀：** AI 功能無法使用，出現 401 或 429 錯誤

**解決方法：**

1. 驗證 API Key：
```bash
# 檢查環境變數
docker-compose exec backend printenv | grep OPENAI
```

2. 檢查 OpenAI 帳戶額度：
   - 訪問 [OpenAI Platform](https://platform.openai.com/usage)
   - 確認 API Key 有效且有足夠額度

3. 如果是 Rate Limit 問題，可調整 `RATE_LIMIT_PER_MINUTE`

### 問題 4: 資料庫連接失敗

**症狀：** 後端日誌顯示資料庫連接錯誤

**解決方法：**

```bash
# 檢查 PostgreSQL 容器
docker-compose logs postgres

# 重啟資料庫
docker-compose restart postgres

# 進入資料庫檢查
docker-compose exec postgres psql -U aiinpocket -d aiinpocket
```

### 問題 5: 網站生成失敗

**症狀：** 生成網站時出現錯誤

**解決方法：**

1. 檢查 `generated_sites` 目錄權限：
```bash
ls -la backend/generated_sites
chmod 755 backend/generated_sites
```

2. 查看後端詳細日誌：
```bash
docker-compose logs -f backend | grep ERROR
```

3. 確認 GPT-4 可用：
   - OpenAI API 帳戶需要有 GPT-4 存取權限

---

## 維護與監控

### 日常維護

```bash
# 查看容器狀態
docker-compose ps

# 查看資源使用
docker stats

# 清理舊的映像檔
docker system prune -a

# 備份資料庫
docker-compose exec postgres pg_dump -U aiinpocket aiinpocket > backup.sql

# 還原資料庫
docker-compose exec -T postgres psql -U aiinpocket aiinpocket < backup.sql
```

### 更新部署

```bash
# 拉取最新程式碼
git pull origin main

# 重新建立並啟動
docker-compose down
docker-compose up -d --build

# 查看更新後的日誌
docker-compose logs -f
```

### 效能監控

建議使用以下工具監控服務：

- **Prometheus + Grafana** - 系統監控
- **ELK Stack** - 日誌分析
- **Sentry** - 錯誤追蹤
- **Uptime Robot** - 服務可用性監控

---

## 附錄

### A. 端口說明

| 服務 | 內部端口 | 外部端口 | 說明 |
|------|---------|---------|------|
| Frontend (Nginx) | 80 | 8000 | 前端網站 |
| Backend (FastAPI) | 8000 | 8001 | 後端 API |
| PostgreSQL | 5432 | - | 資料庫 (僅內部) |
| Redis | 6379 | - | 快取 (僅內部) |

### B. 環境變數完整列表

請參考 `backend/.env.example` 文件

### C. API 文檔

部署完成後，訪問 `http://your-domain/docs` 查看完整 API 文檔

### D. 支援與聯絡

- **GitHub Issues:** https://github.com/your-org/onepageweb/issues
- **Email:** support@aiinpocket.com
- **文檔:** https://docs.aiinpocket.com

---

## 授權

MIT License - 詳見 LICENSE 文件

---

**部署完成！🎉**

如有任何問題，請參考故障排除章節或聯絡技術支援。
