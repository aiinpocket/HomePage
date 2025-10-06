# 安全性強化方案

**日期:** 2025-10-06
**目標:** 防止資料外洩、專案隔離、URL 安全

---

## 安全問題分析

### 當前風險

1. **可預測的 URL**
   - 目前使用 UUID: `/api/preview/{uuid}`
   - UUID 雖然難猜，但仍有規律
   - 可能被暴力嘗試

2. **專案資料可見性**
   - 未登入使用者的專案是否需要保護？
   - 如何防止他人存取專案資料？

3. **檔案存取控制**
   - generated_sites 目錄直接可讀？
   - 需要驗證機制

---

## 解決方案

### 1. URL 安全強化

#### 方案 A: 加密 Token（推薦）

```python
import secrets
import hashlib
from datetime import datetime

def generate_secure_token() -> str:
    """生成安全的隨機 token"""
    timestamp = str(datetime.utcnow().timestamp())
    random_bytes = secrets.token_bytes(32)
    combined = f"{timestamp}:{random_bytes.hex()}"

    # SHA-256 hash
    token = hashlib.sha256(combined.encode()).hexdigest()
    return token[:32]  # 使用前 32 字元

# 範例輸出: a7f3c8d9e2b4f1a6c8d3e9f2b7a4c1d8
```

**URL 格式:**
- 預覽: `/api/preview/a7f3c8d9e2b4f1a6c8d3e9f2b7a4c1d8`
- 下載: `/api/download/a7f3c8d9e2b4f1a6c8d3e9f2b7a4c1d8`

**優點:**
- 完全不可預測
- 無規律可循
- 防暴力破解

#### 方案 B: 有效期限 Token

```python
# 包含時間戳的加密 token
# 24 小時後自動失效
```

#### 方案 C: 訪問控制（最安全）

```python
# 檢查訪問權限
# - 生成者可以訪問
# - 透過 email 發送的連結可以訪問
# - 其他人無法訪問
```

---

### 2. 專案存取控制

#### 未登入使用者

**策略:** 寬鬆但有保護

1. 可以生成網站（無需登入）
2. 透過 email 收到唯一連結
3. 連結包含安全 token
4. 不儲存到資料庫（或標記為 anonymous）

#### 已登入使用者

**策略:** 嚴格保護

1. 專案儲存到資料庫
2. 必須驗證 user_id
3. 只能存取自己的專案
4. URL token 與 user_id 綁定

---

### 3. 資料庫隔離

#### Project 模型更新

```python
class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)  # 允許 NULL

    # 安全性欄位
    access_token = Column(String(64), unique=True, index=True)  # 訪問 token
    is_public = Column(Boolean, default=False)  # 是否公開
    is_anonymous = Column(Boolean, default=False)  # 匿名專案

    # 訪問控制
    allowed_emails = Column(Text)  # JSON array of allowed emails
    access_count = Column(Integer, default=0)  # 訪問次數
    last_accessed = Column(DateTime)  # 最後訪問時間
```

#### API 訪問驗證

```python
@app.get("/api/preview/{access_token}")
async def preview_website(access_token: str, db: Session = Depends(get_db)):
    # 1. 查找專案
    project = db.query(Project).filter(
        Project.access_token == access_token
    ).first()

    if not project:
        raise HTTPException(404, "Website not found")

    # 2. 檢查是否為公開專案
    if project.is_public:
        return serve_website(project.site_id)

    # 3. 檢查是否為匿名專案（透過 email 連結訪問）
    if project.is_anonymous:
        # 記錄訪問
        project.access_count += 1
        project.last_accessed = datetime.utcnow()
        db.commit()
        return serve_website(project.site_id)

    # 4. 需要驗證使用者身份
    # ... 驗證邏輯
```

---

### 4. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/preview/{token}")
@limiter.limit("10/minute")  # 每分鐘最多 10 次
async def preview_website(token: str):
    # ...
```

---

## 實作優先級

### Phase 1: URL Token 化（高優先）

1. 修改 `website_generator.py`
   - 生成 secure token 而非 UUID
   - 儲存 token 到資料庫

2. 修改 API 端點
   - `/api/preview/{token}`
   - `/api/download/{token}`

3. 更新前端
   - 顯示新格式的 URL

### Phase 2: 專案隔離（中優先）

1. 修改 Project 模型
   - 添加 access_token
   - 添加 is_anonymous
   - 添加訪問控制欄位

2. 實作訪問驗證邏輯

### Phase 3: Rate Limiting（低優先）

1. 安裝 slowapi
2. 配置限流規則

---

## 建議實作方案

### 最小化改動方案（推薦）

**策略:**
1. 保持 UUID 作為 site_id（內部使用）
2. 添加 access_token（外部訪問）
3. URL 使用 access_token，映射到 site_id

**優點:**
- 改動小
- 向後兼容
- 安全性提升

**實作:**
```python
# 生成網站時
site_id = str(uuid.uuid4())  # 內部使用
access_token = generate_secure_token()  # 外部訪問

# 儲存
project.site_id = site_id
project.access_token = access_token

# URL
preview_url = f"/api/preview/{access_token}"
download_url = f"/api/download/{access_token}"

# API 端點
@app.get("/api/preview/{access_token}")
async def preview(access_token: str, db: Session):
    project = db.query(Project).filter(
        Project.access_token == access_token
    ).first()

    if not project:
        raise HTTPException(404)

    return serve_website(project.site_id)
```

---

## 登入策略調整

### 當前策略（過於嚴格）

- 生成網站需要登入？ NO
- 查看專案需要登入？ 視情況

### 建議策略（更友善）

#### 未登入使用者

1. 可以生成網站
2. Email 收到唯一連結（含 access_token）
3. 透過連結可以訪問和下載
4. 不儲存到「我的作品集」

#### 已登入使用者

1. 可以生成網站
2. 自動儲存到「我的作品集」
3. 可以管理、編輯、刪除
4. 可以重新生成

#### 訪問控制

```
未登入生成的網站:
- 透過 email 連結訪問（有 token）
- 不需要登入
- 不會在資料庫顯示

已登入生成的網站:
- 儲存在資料庫
- 需要登入才能在「我的作品集」查看
- 但透過 token 連結仍可直接訪問
```

---

## 文件命名與內容

### 避免 AI 痕跡

1. **移除所有 emoji**
   - 用純文字替代
   - 使用專業術語

2. **專業的 commit message**
   - 不要用: "feat: Add awesome feature"
   - 改用: "Add user authentication system"

3. **文檔風格**
   - 簡潔專業
   - 技術為主
   - 避免過度熱情的語氣

4. **變數命名**
   - 使用慣例命名
   - 避免過於創意的名稱

---

## 下一步

1. 實作 secure token 生成
2. 修改 API 端點使用 token
3. 更新資料庫模型
4. 調整前端顯示
5. 移除所有 emoji
