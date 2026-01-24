"""
FastAPI 主程式（精簡版）
AiInPocket 官網 API - 彩蛋與聯絡表單
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging

from .config import settings
from .easter_eggs import easter_egg_system

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ========================================
# Pydantic 模型
# ========================================

class ContactRequest(BaseModel):
    """聯絡表單請求模型"""
    name: str
    email: str
    company: Optional[str] = None
    service: str
    message: str
    language: str = 'zh-TW'


class ContactResponse(BaseModel):
    """聯絡表單回應模型"""
    success: bool
    message: str
    timestamp: str


class HealthResponse(BaseModel):
    """健康檢查回應模型"""
    status: str
    app_name: str
    version: str
    timestamp: str


# ========================================
# FastAPI 應用
# ========================================

app = FastAPI(
    title=settings.APP_NAME,
    description="AiInPocket 官網 API - 彩蛋與聯絡表單",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# API 端點
# ========================================

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now().isoformat()
    }


# ========================================
# 彩蛋 API
# ========================================

@app.post("/api/easter-egg/{egg_type}", tags=["Easter Egg"])
async def trigger_easter_egg(egg_type: str):
    """
    觸發彩蛋並獲取優惠碼

    Args:
        egg_type: 彩蛋類型 (konami, click_logo_10, secret_url, inspect_element, explorer)
    """
    result = easter_egg_system.validate_easter_egg(egg_type)

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="彩蛋不存在")


@app.get("/api/promo/{promo_code}", tags=["Easter Egg"])
async def validate_promo_code(promo_code: str):
    """驗證優惠碼"""
    result = easter_egg_system.get_promo_info(promo_code)
    return result


@app.get("/secret-garden", tags=["Easter Egg"])
async def secret_garden():
    """隱藏彩蛋頁面"""
    result = easter_egg_system.validate_easter_egg("secret_url")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <title>Secret Garden | AiInPocket</title>
        <style>
            body {{
                background: linear-gradient(135deg, #0a0e27 0%, #1a1e3f 100%);
                color: #fff;
                font-family: 'Segoe UI', sans-serif;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0;
            }}
            .container {{
                text-align: center;
                padding: 2rem;
            }}
            h1 {{
                background: linear-gradient(135deg, #87CEEB, #7FFF00);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 3rem;
            }}
            .promo {{
                background: rgba(127, 255, 0, 0.1);
                border: 2px solid #7FFF00;
                padding: 2rem;
                border-radius: 15px;
                margin-top: 2rem;
            }}
            .code {{
                font-size: 2rem;
                font-family: monospace;
                color: #7FFF00;
                letter-spacing: 3px;
            }}
            a {{
                color: #87CEEB;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the Secret Garden</h1>
            <p>你發現了隱藏的秘密花園！</p>
            <div class="promo">
                <p>恭喜獲得優惠碼：</p>
                <p class="code">{result['promo_code']}</p>
                <p>{result['discount']}% OFF</p>
            </div>
            <p style="margin-top: 2rem;">
                <a href="/corporate/index.html">← 返回首頁</a>
            </p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# ========================================
# 聯絡表單 API
# ========================================

@app.post("/api/contact", response_model=ContactResponse, tags=["Contact"])
async def submit_contact_form(request: ContactRequest):
    """
    提交聯絡表單
    """
    try:
        # 記錄聯絡表單提交
        logger.info(f"Contact form submitted: {request.name} <{request.email}>")

        # TODO: 實作 Email 發送或 Webhook 通知
        # 目前先回傳成功訊息

        return {
            "success": True,
            "message": "感謝您的來信！我們會盡快回覆您。",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Contact form error: {e}")
        raise HTTPException(status_code=500, detail="提交失敗，請稍後再試")


# ========================================
# 啟動
# ========================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
