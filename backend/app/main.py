"""
FastAPI 主程式
AiInPocket AI 聊天機器人後端 API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
import uvicorn
from datetime import datetime
import uuid
import logging
from pathlib import Path

from .config import settings
from .ai_handler import ai_handler
from .easter_eggs import easter_egg_system
from .website_generator import website_generator
from .zip_builder import zip_builder
from .email_service import email_service
from .usage_tracker import usage_tracker

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ========================================
# Pydantic 模型
# ========================================

class ChatRequest(BaseModel):
    """聊天請求模型"""
    message: str
    session_id: str
    conversation_history: Optional[list] = None


class ChatResponse(BaseModel):
    """聊天回應模型"""
    reply: str
    action: Optional[Dict] = None
    timestamp: str


class HealthResponse(BaseModel):
    """健康檢查回應模型"""
    status: str
    app_name: str
    version: str
    timestamp: str
    ai_status: Dict


class PortfolioItem(BaseModel):
    """作品集項目"""
    title: str
    description: Optional[str] = None


class GenerateWebsiteRequest(BaseModel):
    """生成網站請求模型"""
    template_id: str
    user_data: Dict
    contact_email: str


class GenerateWebsiteResponse(BaseModel):
    """生成網站回應模型"""
    site_id: str
    preview_url: str
    download_url: str
    timestamp: str


class AnalyzeImageRequest(BaseModel):
    """分析圖片請求模型"""
    image_base64: str
    description: Optional[str] = ""


class AnalyzeImageResponse(BaseModel):
    """分析圖片回應模型"""
    colors: Dict
    style: str
    mood: str
    fonts: Dict
    keywords: List[str]


class ChatPreviewRequest(BaseModel):
    """預覽版聊天請求模型"""
    site_id: str
    message: str
    history: Optional[List[Dict]] = None


class ChatPreviewResponse(BaseModel):
    """預覽版聊天回應模型"""
    reply: str
    usage_count: int
    remaining: int
    timestamp: str


# ========================================
# FastAPI 應用初始化
# ========================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AiInPocket AI 聊天機器人 API",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS 中間件設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# 會話存儲（簡單的記憶體儲存）
# ========================================

sessions: Dict[str, list] = {}


def get_session_history(session_id: str) -> list:
    """獲取會話歷史"""
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]


def add_to_session_history(session_id: str, role: str, content: str):
    """添加訊息到會話歷史"""
    if session_id not in sessions:
        sessions[session_id] = []

    sessions[session_id].append({
        "role": role,
        "content": content
    })

    # 只保留最近 20 條訊息
    if len(sessions[session_id]) > 20:
        sessions[session_id] = sessions[session_id][-20:]


# ========================================
# API 路由
# ========================================

@app.get("/", tags=["Root"])
async def root():
    """根路徑 - API 資訊"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "AiInPocket AI 聊天機器人 API",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """健康檢查端點"""
    ai_status = ai_handler.get_health_status()

    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        timestamp=datetime.now().isoformat(),
        ai_status=ai_status
    )


@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    聊天端點 - 處理使用者訊息並返回 AI 回應

    Args:
        request: 聊天請求（包含訊息、會話 ID 和歷史）

    Returns:
        ChatResponse: 包含回應文字、動作和時間戳
    """
    try:
        # 獲取會話歷史
        history = get_session_history(request.session_id)

        # 處理訊息
        result = await ai_handler.process_message(
            message=request.message,
            session_id=request.session_id,
            conversation_history=history
        )

        # 更新會話歷史
        add_to_session_history(request.session_id, "user", request.message)
        add_to_session_history(request.session_id, "assistant", result["reply"])

        # 返回回應
        return ChatResponse(
            reply=result["reply"],
            action=result["action"],
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"處理訊息時發生錯誤：{str(e)}"
        )


@app.delete("/api/session/{session_id}", tags=["Session"])
async def clear_session(session_id: str):
    """清除指定會話的歷史記錄"""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"Session {session_id} cleared successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@app.get("/api/sessions", tags=["Session"])
async def list_sessions():
    """列出所有活躍會話（僅用於開發/除錯）"""
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Not available in production")

    return {
        "total_sessions": len(sessions),
        "session_ids": list(sessions.keys())
    }


# ========================================
# 網站生成 API
# ========================================

@app.post("/api/generate-website", response_model=GenerateWebsiteResponse, tags=["Website Generation"])
async def generate_website(request: GenerateWebsiteRequest):
    """
    生成網站

    Args:
        request: 生成網站請求（包含模板 ID、使用者資料和聯絡 email）

    Returns:
        GenerateWebsiteResponse: 包含 site_id、預覽 URL 和下載 URL
    """
    try:
        logger.info(f"Starting website generation with template: {request.template_id}")

        # 1. 生成網站 HTML
        html_content = await website_generator.generate_website(
            template_id=request.template_id,
            user_data=request.user_data
        )

        # 2. 生成唯一的 site_id
        site_id = str(uuid.uuid4())
        logger.info(f"Generated site_id: {site_id}")

        # 3. 建立兩個版本的 ZIP
        # 預覽版（使用平台 API key，有限制）
        preview_zip = zip_builder.create_website_package(
            site_id=site_id,
            html_content=html_content,
            user_data=request.user_data,
            with_api_key=False
        )
        logger.info(f"Preview package created: {preview_zip}")

        # 下載版（需要使用者自己的 API key，無限制）
        download_zip = zip_builder.create_website_package(
            site_id=f"{site_id}_full",
            html_content=html_content,
            user_data=request.user_data,
            with_api_key=True
        )
        logger.info(f"Download package created: {download_zip}")

        # 4. 建立 URL
        preview_url = f"{settings.SITE_URL}/api/preview/{site_id}"
        download_url = f"{settings.SITE_URL}/api/download/{site_id}"

        # 5. 發送 email 通知
        try:
            await email_service.send_generation_complete_email(
                recipient_email=request.contact_email,
                site_id=site_id,
                company_name=request.user_data.get("company_name", "Your Company"),
                preview_url=preview_url,
                download_url=download_url
            )
            logger.info(f"Email sent to: {request.contact_email}")
        except Exception as email_error:
            logger.error(f"Failed to send email: {email_error}")
            # 不要因為 email 失敗而中斷整個流程

        # 6. 返回結果
        return GenerateWebsiteResponse(
            site_id=site_id,
            preview_url=preview_url,
            download_url=download_url,
            timestamp=datetime.now().isoformat()
        )

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error generating website: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"生成網站時發生錯誤：{str(e)}"
        )


@app.post("/api/analyze-image", response_model=AnalyzeImageResponse, tags=["Website Generation"])
async def analyze_image(request: AnalyzeImageRequest):
    """
    分析上傳的圖片風格

    Args:
        request: 包含 base64 編碼的圖片和文字描述

    Returns:
        AnalyzeImageResponse: 風格分析結果（配色、字體建議等）
    """
    try:
        logger.info("Starting image style analysis")

        # 使用 GPT-4 Vision 分析圖片
        style_data = await website_generator.analyze_image_style(
            image_base64=request.image_base64,
            description=request.description
        )

        logger.info(f"Image analysis complete: {style_data.get('style', 'N/A')}")

        return AnalyzeImageResponse(
            colors=style_data.get("colors", {}),
            style=style_data.get("style", ""),
            mood=style_data.get("mood", ""),
            fonts=style_data.get("fonts", {}),
            keywords=style_data.get("keywords", [])
        )

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error analyzing image: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"分析圖片時發生錯誤：{str(e)}"
        )


@app.post("/api/chat-preview", response_model=ChatPreviewResponse, tags=["Website Generation"])
async def chat_preview(request: ChatPreviewRequest):
    """
    預覽版聊天機器人

    Args:
        request: 包含 site_id、訊息和歷史

    Returns:
        ChatPreviewResponse: AI 回應和使用量資訊
    """
    try:
        logger.info(f"Chat preview request for site: {request.site_id}")

        # 1. 檢查使用次數
        if not usage_tracker.check_limit(request.site_id):
            current_usage = usage_tracker.get_usage(request.site_id)
            logger.warning(f"Usage limit exceeded for site: {request.site_id}")
            raise HTTPException(
                status_code=429,
                detail=f"試用次數已用完（{current_usage}/{settings.PREVIEW_API_LIMIT}）。請下載完整版並使用您自己的 API Key。"
            )

        # 2. 處理訊息
        history = request.history or []
        result = await ai_handler.process_message(
            message=request.message,
            session_id=request.site_id,
            conversation_history=history
        )

        # 3. 增加使用次數
        new_usage = usage_tracker.increment_usage(request.site_id)
        remaining = settings.PREVIEW_API_LIMIT - new_usage

        logger.info(f"Chat response sent. Usage: {new_usage}/{settings.PREVIEW_API_LIMIT}")

        # 4. 返回回應
        return ChatPreviewResponse(
            reply=result["reply"],
            usage_count=new_usage,
            remaining=remaining,
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat preview: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"處理訊息時發生錯誤：{str(e)}"
        )


@app.get("/api/preview/{site_id}", response_class=HTMLResponse, tags=["Website Generation"])
async def preview_website(site_id: str):
    """
    預覽網站

    Args:
        site_id: 網站 ID

    Returns:
        HTML 內容
    """
    try:
        logger.info(f"Preview request for site: {site_id}")

        # 從 generated_sites 資料夾讀取 ZIP 並解壓
        generated_sites_path = Path(settings.GENERATED_SITES_PATH)
        zip_path = generated_sites_path / f"{site_id}.zip"

        if not zip_path.exists():
            logger.warning(f"Site not found: {site_id}")
            raise HTTPException(status_code=404, detail="網站不存在")

        # 解壓並讀取 index.html
        import zipfile
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            index_path = Path(temp_dir) / "index.html"
            if not index_path.exists():
                raise HTTPException(status_code=500, detail="網站檔案損壞")

            html_content = index_path.read_text(encoding='utf-8')

            # 注入 ai-chat.js
            js_path = Path(temp_dir) / "ai-chat.js"
            if js_path.exists():
                js_content = js_path.read_text(encoding='utf-8')
                html_content = html_content.replace(
                    '</body>',
                    f'<script>{js_content}</script>\n</body>'
                )

            return HTMLResponse(content=html_content)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving preview: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"載入預覽時發生錯誤：{str(e)}"
        )


@app.get("/api/download/{site_id}", tags=["Website Generation"])
async def download_website(site_id: str):
    """
    下載完整版 ZIP

    Args:
        site_id: 網站 ID

    Returns:
        ZIP 檔案
    """
    try:
        logger.info(f"Download request for site: {site_id}")

        # 下載完整版（帶 _full 後綴）
        generated_sites_path = Path(settings.GENERATED_SITES_PATH)
        zip_path = generated_sites_path / f"{site_id}_full.zip"

        if not zip_path.exists():
            logger.warning(f"Download package not found: {site_id}")
            raise HTTPException(status_code=404, detail="下載檔案不存在")

        return FileResponse(
            path=str(zip_path),
            media_type='application/zip',
            filename=f"website_{site_id}.zip"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving download: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"下載檔案時發生錯誤：{str(e)}"
        )


# ========================================
# 彩蛋系統 API
# ========================================

@app.post("/api/easter-egg/{egg_type}", tags=["Easter Egg"])
async def trigger_easter_egg(egg_type: str):
    """
    觸發彩蛋並獲取優惠碼

    Args:
        egg_type: 彩蛋類型 (konami, click_logo_10, secret_url, inspect_element)
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
    return {
        "message": "歡迎來到秘密花園",
        "promo": result
    }


# ========================================
# 啟動事件
# ========================================

@app.on_event("startup")
async def startup_event():
    """應用啟動時執行"""
    print("=" * 50)
    print(f"[START] {settings.APP_NAME} v{settings.APP_VERSION} is starting...")
    print(f"[DEBUG] Debug mode: {settings.DEBUG}")
    print(f"[CORS] CORS origins: {settings.cors_origins_list}")
    print(f"[AI] AI handler initialized")
    print("=" * 50)

    # 初始化資料庫
    try:
        from .database import init_db
        init_db()
    except Exception as e:
        print(f"[ERROR] Failed to initialize database: {e}")

    # 建立 RAG 索引
    try:
        from .rag_system import rag_system
        indexed_count = rag_system.index_all_pages()
        print(f"[RAG] Indexed {indexed_count} pages")
    except Exception as e:
        print(f"[ERROR] Failed to build RAG index: {e}")

    # 生成 sitemap.xml
    try:
        from .sitemap_generator import generate_sitemap
        sitemap_path = generate_sitemap()
        print(f"[SITEMAP] Generated: {sitemap_path}")
    except Exception as e:
        print(f"[ERROR] Failed to generate sitemap: {e}")

    print("=" * 50)
    print("[START] Application startup complete!")
    print("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """應用關閉時執行"""
    print("=" * 50)
    print(f"[STOP] {settings.APP_NAME} is shutting down...")
    print("=" * 50)


# ========================================
# 開發模式運行
# ========================================

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
