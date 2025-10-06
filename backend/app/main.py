"""
FastAPI 主程式
AiInPocket AI 聊天機器人後端 API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn
from datetime import datetime

from .config import settings
from .ai_handler import ai_handler
from .easter_eggs import easter_egg_system


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
