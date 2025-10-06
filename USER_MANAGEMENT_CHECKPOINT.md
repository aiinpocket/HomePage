# 使用者管理系統實作 Checkpoint

**日期:** 2025-10-06
**狀態:** Part 2/3 完成，Part 3 待實作
**Git Commits:**
- `fbe9a93` - Part 1: Authentication foundation
- `d11fe1d` - Part 2: VIP system and usage tracking

---

## ✅ 已完成功能 (Part 1-2)

### 1. 資料庫 Schema

#### User 模型
```python
- email (唯一，索引)
- vip_level (0=免費, 1=基礎, 2=專業, 3=企業)
- max_projects (預設 5，可依 VIP 調整)
- total_projects_created (統計)
- can_create_project(db) -> bool
- get_remaining_projects(db) -> int
- upgrade_vip(level) -> void
```

#### Project 模型
```python
- user_id (外鍵)
- project_name (使用者自訂名稱)
- template_id (使用的模板)
- form_data (JSON 格式完整表單資料)
- site_id (生成的網站 ID)
- status (draft/generating/completed/failed)
- is_deleted (軟刪除)
```

#### OTPToken 模型
```python
- user_id (外鍵)
- token (6 位數字)
- expires_at (10 分鐘)
- is_used (使用後失效)
- is_valid() -> bool
- mark_as_used() -> void
```

#### SiteUsage 模型
```python
- site_id (綁定網站 UUID，非 email)
- api_calls_count (目前使用次數)
- max_api_calls (預設 30)
- increment_usage() -> int
- is_quota_exceeded() -> bool
- get_remaining_calls() -> int
```

### 2. 後端服務

#### AuthService (`auth_service.py`)
```python
- get_or_create_user(db, email) -> User
- send_otp(db, email) -> (bool, str)
- verify_otp(db, email, otp_code) -> (bool, user_id, str)
- create_session_token(user_id) -> str
```

#### UsageTrackerPG (`usage_tracker_pg.py`)
```python
- get_or_create_usage(db, site_id) -> SiteUsage
- get_usage(db, site_id) -> int
- increment_usage(db, site_id) -> int
- check_limit(db, site_id) -> bool
- get_remaining_calls(db, site_id) -> int
- reset_usage(db, site_id) -> bool
- get_usage_stats(db, site_id) -> Dict
```

#### EmailService 擴充
```python
- send_otp_email(email, otp_code, expires_minutes=10)
  * 科幻風格郵件模板
  * 6 位數字大字顯示
  * 安全提示
```

---

## 🚧 待實作功能 (Part 3)

### 1. 後端 API 端點

需要在 `main.py` 添加以下 API：

#### 認證 API
```python
@app.post("/api/auth/send-otp")
async def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    """
    發送一次性密碼到 email

    Request: { "email": "user@example.com" }
    Response: { "success": true, "message": "驗證碼已發送" }
    """
    pass

@app.post("/api/auth/verify-otp")
async def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    """
    驗證 OTP 並登入

    Request: { "email": "user@example.com", "otp_code": "123456" }
    Response: {
        "success": true,
        "user_id": "uuid",
        "session_token": "token",
        "user_info": {
            "email": "...",
            "vip_level": 0,
            "max_projects": 5,
            "remaining_projects": 3
        }
    }
    """
    pass

@app.post("/api/auth/logout")
async def logout():
    """登出（清除前端 session）"""
    pass
```

#### 專案管理 API
```python
@app.get("/api/projects")
async def list_projects(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)  # 需實作 auth middleware
):
    """
    取得使用者所有專案列表

    Response: {
        "projects": [
            {
                "id": "uuid",
                "project_name": "我的網站",
                "template_id": "modern-tech",
                "status": "completed",
                "created_at": "2025-10-06T...",
                "preview_url": "...",
                "thumbnail": "..." # 可選
            },
            ...
        ],
        "total": 10,
        "remaining_quota": 3
    }
    """
    pass

@app.get("/api/projects/{project_id}")
async def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    取得特定專案的完整資料（用於編輯）

    Response: {
        "id": "uuid",
        "project_name": "我的網站",
        "template_id": "modern-tech",
        "form_data": {
            # 完整的表單資料，可直接填回表單
            "company_name": "...",
            "services": [...],
            ...
        },
        "site_id": "uuid",
        "preview_url": "...",
        "download_url": "..."
    }
    """
    pass

@app.post("/api/projects")
async def save_project(
    request: SaveProjectRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    儲存新專案（在生成前或生成後都可以）

    Request: {
        "project_name": "我的網站",
        "template_id": "modern-tech",
        "form_data": { ... }
    }

    Response: {
        "project_id": "uuid",
        "message": "專案已儲存"
    }
    """
    pass

@app.put("/api/projects/{project_id}")
async def update_project(
    project_id: str,
    request: UpdateProjectRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    更新專案（修改名稱或表單資料）

    Request: {
        "project_name": "新名稱",
        "form_data": { ... }
    }
    """
    pass

@app.delete("/api/projects/{project_id}")
async def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """軟刪除專案"""
    pass

@app.post("/api/projects/{project_id}/regenerate")
async def regenerate_project(
    project_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    重新生成專案（使用已儲存的 form_data）
    """
    pass
```

#### 使用統計 API
```python
@app.get("/api/usage/{site_id}")
async def get_usage_stats(site_id: str, db: Session = Depends(get_db)):
    """
    取得網站使用統計（公開，不需登入）

    Response: {
        "site_id": "uuid",
        "api_calls_count": 15,
        "max_api_calls": 30,
        "remaining_calls": 15,
        "is_quota_exceeded": false
    }
    """
    pass
```

### 2. 前端 UI 實作

需要在 `generator.html` 添加：

#### 登入按鈕和彈窗
```html
<!-- 在導航列添加登入按鈕 -->
<nav class="navbar">
    <!-- 原有內容 -->
    <button id="login-btn" class="nav-cta">
        <span id="user-email" style="display:none;"></span>
        <span id="login-text">登入</span>
    </button>
</nav>

<!-- 登入彈窗 -->
<div id="login-modal" class="modal">
    <div class="modal-content">
        <h2>使用 Email 登入</h2>
        <p>登入後可以儲存和管理您的作品</p>

        <!-- 步驟 1: 輸入 Email -->
        <div id="step-email" class="login-step active">
            <input type="email" id="login-email" placeholder="your@email.com">
            <button onclick="sendOTP()">發送驗證碼</button>
            <p class="hint">無需註冊，直接使用 Email 登入</p>
        </div>

        <!-- 步驟 2: 輸入 OTP -->
        <div id="step-otp" class="login-step">
            <p>驗證碼已發送到 <strong id="email-display"></strong></p>
            <input type="text" id="otp-code" maxlength="6" placeholder="6位數驗證碼">
            <button onclick="verifyOTP()">驗證並登入</button>
            <p class="hint">驗證碼 10 分鐘內有效，僅能使用一次</p>
            <button class="link-btn" onclick="resendOTP()">重新發送驗證碼</button>
        </div>
    </div>
</div>
```

#### 作品歷史列表
```html
<!-- 在 generator.html 添加「我的作品」按鈕 -->
<button id="my-projects-btn" onclick="showMyProjects()" style="display:none;">
    我的作品 (3/5)
</button>

<!-- 我的作品彈窗 -->
<div id="projects-modal" class="modal">
    <div class="modal-content large">
        <h2>我的作品</h2>
        <div class="projects-grid" id="projects-list">
            <!-- 動態生成作品卡片 -->
        </div>
    </div>
</div>

<!-- 作品卡片模板 -->
<template id="project-card-template">
    <div class="project-card">
        <div class="project-thumbnail">
            <img src="placeholder.jpg" alt="Website Preview">
        </div>
        <div class="project-info">
            <h3 class="project-name">我的網站</h3>
            <p class="project-date">2025-10-06</p>
            <p class="project-template">使用模板：現代科技</p>
        </div>
        <div class="project-actions">
            <button class="btn-load" onclick="loadProject('uuid')">載入編輯</button>
            <button class="btn-preview" onclick="window.open('preview_url')">預覽</button>
            <button class="btn-delete" onclick="deleteProject('uuid')">刪除</button>
        </div>
    </div>
</template>
```

#### JavaScript 功能
```javascript
// 全域變數
let currentUser = null;
let sessionToken = null;
let currentProjectId = null; // 如果是編輯模式

// 登入相關
async function sendOTP() {
    const email = document.getElementById('login-email').value;
    // 呼叫 /api/auth/send-otp
    // 切換到 OTP 輸入步驟
}

async function verifyOTP() {
    const email = document.getElementById('login-email').value;
    const otp = document.getElementById('otp-code').value;
    // 呼叫 /api/auth/verify-otp
    // 儲存 sessionToken 和 user_info 到 localStorage
    // 更新 UI 顯示使用者資訊
    // 載入使用者的專案列表
}

async function logout() {
    localStorage.removeItem('sessionToken');
    localStorage.removeItem('userInfo');
    currentUser = null;
    sessionToken = null;
    // 更新 UI
}

// 專案管理
async function loadMyProjects() {
    // 呼叫 /api/projects
    // 顯示專案列表
}

async function loadProject(projectId) {
    // 呼叫 /api/projects/{projectId}
    // 取得 form_data
    // 填回表單各欄位
    // 設定為編輯模式
    currentProjectId = projectId;
}

async function saveCurrentProject() {
    const formData = collectFormData();

    if (currentProjectId) {
        // 更新現有專案
        await fetch(`/api/projects/${currentProjectId}`, {
            method: 'PUT',
            body: JSON.stringify({
                project_name: document.getElementById('project-name').value,
                form_data: formData
            })
        });
    } else {
        // 建立新專案
        await fetch('/api/projects', {
            method: 'POST',
            body: JSON.stringify({
                project_name: '新專案',
                template_id: selectedStyle,
                form_data: formData
            })
        });
    }
}

async function deleteProject(projectId) {
    if (confirm('確定要刪除此專案？')) {
        await fetch(`/api/projects/${projectId}`, {
            method: 'DELETE'
        });
        loadMyProjects(); // 重新載入列表
    }
}

// 修改生成流程
async function generateWebsite() {
    // ... 原有驗證 ...

    const formData = collectFormData();

    // 如果已登入，先儲存專案
    if (sessionToken) {
        await saveCurrentProject();
    }

    // 呼叫生成 API
    const response = await fetch('/api/generate-website', {
        method: 'POST',
        body: JSON.stringify(formData)
    });

    // 如果已登入，更新專案的 site_id 和 URLs
    if (sessionToken && currentProjectId) {
        await fetch(`/api/projects/${currentProjectId}`, {
            method: 'PUT',
            body: JSON.stringify({
                site_id: result.site_id,
                preview_url: result.preview_url,
                download_url: result.download_url,
                status: 'completed'
            })
        });
    }
}

// 頁面載入時檢查登入狀態
document.addEventListener('DOMContentLoaded', () => {
    const saved = localStorage.getItem('userInfo');
    if (saved) {
        currentUser = JSON.parse(saved);
        sessionToken = localStorage.getItem('sessionToken');
        updateUIForLoggedInUser();
    }
});
```

### 3. CSS 樣式

```css
/* 登入彈窗 */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(10, 14, 39, 0.95);
    z-index: 1001;
    align-items: center;
    justify-content: center;
}

.modal.show {
    display: flex;
}

.modal-content {
    background: var(--card-bg);
    border: 2px solid var(--primary-blue);
    border-radius: var(--radius-lg);
    padding: 3rem;
    max-width: 500px;
    width: 90%;
}

.modal-content.large {
    max-width: 1200px;
}

.login-step {
    display: none;
}

.login-step.active {
    display: block;
}

/* 作品卡片 */
.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.project-card {
    background: var(--card-bg);
    border: 1px solid rgba(135, 206, 235, 0.2);
    border-radius: var(--radius-md);
    overflow: hidden;
    transition: var(--transition);
}

.project-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px var(--glow-blue);
}

.project-thumbnail {
    width: 100%;
    height: 200px;
    background: rgba(135, 206, 235, 0.1);
    overflow: hidden;
}

.project-thumbnail img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.project-info {
    padding: 1.5rem;
}

.project-actions {
    display: flex;
    gap: 0.5rem;
    padding: 1rem 1.5rem;
    border-top: 1px solid rgba(135, 206, 235, 0.2);
}
```

---

## 📝 實作順序建議

### Phase 1: 後端 API（1-2 小時）
1. 在 `main.py` 添加所有 API 端點
2. 實作 Pydantic models for requests/responses
3. 實作 authentication middleware
4. 測試所有 API（使用 Postman 或 /docs）

### Phase 2: 前端登入 UI（1 小時）
1. 添加登入彈窗 HTML
2. 實作 sendOTP() 和 verifyOTP()
3. 實作 session 管理（localStorage）
4. 更新 UI 顯示登入狀態

### Phase 3: 專案管理 UI（1-2 小時）
1. 添加「我的作品」按鈕和彈窗
2. 實作專案列表顯示
3. 實作載入專案功能（填回表單）
4. 實作刪除專案功能
5. 修改生成流程整合專案儲存

### Phase 4: 測試（30 分鐘）
1. 測試完整登入流程
2. 測試專案建立和載入
3. 測試編輯和重新生成
4. 測試 VIP 限制和試用次數

---

## 🔑 關鍵設計決策

### 1. **登入非強制**
- 未登入使用者可以直接使用生成器
- 登入後才能儲存和管理作品
- UI 顯示「登入以儲存作品」提示

### 2. **試用次數綁定 site_id**
- 每個生成的網站有獨立的 30 次試用
- 使用 PostgreSQL 儲存，永久保留
- 與使用者無關，即使未登入也有限制

### 3. **專案數量綁定 email**
- 免費使用者：5 個專案
- 基礎 VIP：15 個
- 專業 VIP：50 個
- 企業 VIP：999 個（近乎無限）

### 4. **專案儲存時機**
- 可以在生成前儲存（草稿）
- 可以在生成後自動儲存
- 可以載入後編輯再重新生成

### 5. **安全性**
- OTP 10 分鐘過期
- OTP 使用後立即失效
- Session token 儲存在 localStorage
- 每次重要操作驗證 session

---

## 📊 資料庫遷移

首次部署時執行：

```python
# backend/app/main.py - startup event
@app.on_event("startup")
async def startup_event():
    # ... 原有程式碼 ...

    # 建立新的資料表
    from .database import init_db
    init_db()
```

---

## 🧪 測試案例

### 認證流程
1. 發送 OTP 到新 email → 建立使用者
2. 驗證 OTP → 登入成功
3. 使用過的 OTP → 驗證失敗
4. 過期的 OTP → 驗證失敗
5. 重新發送 OTP → 舊的失效

### 專案管理
1. 建立 5 個專案 → 成功
2. 建立第 6 個專案 → 失敗（超過限制）
3. 刪除 1 個專案 → 成功
4. 再建立 1 個專案 → 成功
5. 升級到 VIP 1 → 限制變成 15
6. 載入專案 → 表單填回資料
7. 修改並重新生成 → 更新專案

### 試用次數
1. 新網站 site_id → 30 次可用
2. 呼叫 29 次 → 剩餘 1 次
3. 呼叫第 30 次 → 剩餘 0 次
4. 呼叫第 31 次 → 拒絕（超過限制）
5. Redis 重啟 → 次數仍然保留（PostgreSQL）

---

## 🎯 下一步行動

選擇以下任一方案：

**方案 A: 由 Claude 繼續完成**
- 實作所有後端 API
- 實作所有前端 UI
- 整合測試

**方案 B: 團隊接手實作**
- 使用本文檔作為實作指南
- 參考 Part 1-2 的程式碼風格
- 有問題可以詢問 Claude

**方案 C: 分階段實作**
- 先完成後端 API（2 小時）
- 測試 API 功能正常
- 再完成前端 UI（2 小時）
- 最後整合測試（30 分鐘）

---

**Checkpoint 建立:** 2025-10-06
**完成度:** 40% (資料庫和服務層完成，API 和 UI 待實作)
