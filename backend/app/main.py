"""
FastAPI 主程式
AiInPocket AI 聊天機器人後端 API
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
import uvicorn
from datetime import datetime
import uuid
import logging
from pathlib import Path
import json

from .config import settings
from .ai_handler import ai_handler
from .easter_eggs import easter_egg_system
from .website_generator import website_generator
from .zip_builder import zip_builder
from .email_service import email_service
from .usage_tracker import usage_tracker
from .auth_service import auth_service
from .usage_tracker_pg import usage_tracker_pg
from .database import get_db
from .models import User, Project
from sqlalchemy.orm import Session
from fastapi import Depends
from .email_templates import format_email

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
    languages: List[str] = ["zh-TW", "en", "ja"]  # 預設支援三語
    images: Optional[Dict[str, str]] = None  # {"logo": "base64...", "portfolio1": "base64..."}


class GenerateWebsiteResponse(BaseModel):
    """生成網站回應模型"""
    site_id: str
    preview_url: str
    download_url: str
    timestamp: str
    message: Optional[str] = None


class UpdateWebsiteRequest(BaseModel):
    """更新網站請求模型"""
    site_id: str
    modifications: Dict  # {"section": "hero", "changes": {...}}
    instruction: str  # AI 指令,例如 "改成藍色主題" 或 "調整標題文字為..."


class UpdateWebsiteResponse(BaseModel):
    """更新網站回應模型"""
    site_id: str
    preview_url: str
    timestamp: str
    changes_applied: Dict


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


class ContactRequest(BaseModel):
    """聯絡表單請求模型"""
    name: str
    email: str
    company: Optional[str] = None
    service: str  # 'ai', 'cloud', 'devops', 'consulting', 'other'
    message: str
    language: str = 'zh-TW'  # 預設繁體中文


class ContactResponse(BaseModel):
    """聯絡表單回應模型"""
    success: bool
    message: str
    timestamp: str


class SendOTPRequest(BaseModel):
    """發送 OTP 請求模型"""
    email: str


class SendOTPResponse(BaseModel):
    """發送 OTP 回應模型"""
    success: bool
    message: str


class VerifyOTPRequest(BaseModel):
    """驗證 OTP 請求模型"""
    email: str
    otp_code: str


class VerifyOTPResponse(BaseModel):
    """驗證 OTP 回應模型"""
    success: bool
    message: str
    user_id: Optional[str] = None
    session_token: Optional[str] = None
    user_info: Optional[Dict] = None


class SaveProjectRequest(BaseModel):
    """儲存專案請求模型"""
    user_id: str
    project_name: str
    template_id: str
    form_data: Dict
    site_id: Optional[str] = None
    preview_url: Optional[str] = None
    download_url: Optional[str] = None


class UpdateProjectRequest(BaseModel):
    """更新專案請求模型"""
    project_name: Optional[str] = None
    template_id: Optional[str] = None
    form_data: Optional[Dict] = None
    status: Optional[str] = None


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
# 認證 API
# ========================================

@app.post("/api/auth/send-otp", response_model=SendOTPResponse, tags=["Authentication"])
async def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    """
    發送 OTP 到使用者 email

    Args:
        request: 包含 email 的請求
        db: 資料庫 session

    Returns:
        SendOTPResponse: 發送結果
    """
    try:
        logger.info(f"Sending OTP to email: {request.email}")

        success, message = await auth_service.send_otp(db, request.email)

        return SendOTPResponse(
            success=success,
            message=message
        )

    except Exception as e:
        logger.error(f"Error sending OTP: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"發送驗證碼時發生錯誤：{str(e)}"
        )


@app.post("/api/auth/verify-otp", response_model=VerifyOTPResponse, tags=["Authentication"])
async def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    """
    驗證 OTP 並登入

    Args:
        request: 包含 email 和 otp_code 的請求
        db: 資料庫 session

    Returns:
        VerifyOTPResponse: 驗證結果和 session token
    """
    try:
        logger.info(f"Verifying OTP for email: {request.email}")

        success, user_id, message = auth_service.verify_otp(
            db, request.email, request.otp_code
        )

        if not success:
            return VerifyOTPResponse(
                success=False,
                message=message
            )

        # 生成 session token
        session_token = auth_service.create_session_token(user_id)

        # 獲取使用者資訊
        user = db.query(User).filter(User.id == user_id).first()
        user_info = {
            "user_id": user.id,
            "email": user.email,
            "vip_level": user.vip_level,
            "max_projects": user.max_projects,
            "remaining_projects": user.get_remaining_projects(db)
        }

        logger.info(f"User logged in: {user.email}")

        return VerifyOTPResponse(
            success=True,
            message="登入成功",
            user_id=user_id,
            session_token=session_token,
            user_info=user_info
        )

    except Exception as e:
        logger.error(f"Error verifying OTP: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"驗證時發生錯誤：{str(e)}"
        )


@app.post("/api/auth/logout", tags=["Authentication"])
async def logout():
    """
    登出（前端清除 session token）
    """
    return {"success": True, "message": "登出成功"}


# ========================================
# 專案管理 API
# ========================================

@app.get("/api/projects", tags=["Projects"])
async def list_projects(user_id: str, db: Session = Depends(get_db)):
    """
    列出使用者的所有專案

    Args:
        user_id: 使用者 ID
        db: 資料庫 session

    Returns:
        專案列表
    """
    try:
        logger.info(f"Listing projects for user: {user_id}")

        projects = db.query(Project).filter(
            Project.user_id == user_id,
            Project.is_deleted == False
        ).order_by(Project.updated_at.desc()).all()

        project_list = [
            {
                "id": p.id,
                "project_name": p.project_name,
                "template_id": p.template_id,
                "site_id": p.site_id,
                "preview_url": p.preview_url,
                "download_url": p.download_url,
                "status": p.status,
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat()
            }
            for p in projects
        ]

        return {
            "success": True,
            "projects": project_list,
            "total": len(project_list)
        }

    except Exception as e:
        logger.error(f"Error listing projects: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"獲取專案列表時發生錯誤：{str(e)}"
        )


@app.get("/api/projects/{project_id}", tags=["Projects"])
async def get_project(project_id: str, user_id: str, db: Session = Depends(get_db)):
    """
    獲取專案詳細資料（用於編輯）

    Args:
        project_id: 專案 ID
        user_id: 使用者 ID
        db: 資料庫 session

    Returns:
        專案完整資料（包含 form_data）
    """
    try:
        logger.info(f"Getting project: {project_id} for user: {user_id}")

        project = db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == user_id,
            Project.is_deleted == False
        ).first()

        if not project:
            raise HTTPException(status_code=404, detail="專案不存在")

        import json

        return {
            "success": True,
            "project": {
                "id": project.id,
                "project_name": project.project_name,
                "template_id": project.template_id,
                "form_data": json.loads(project.form_data),
                "site_id": project.site_id,
                "preview_url": project.preview_url,
                "download_url": project.download_url,
                "status": project.status,
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat()
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"獲取專案時發生錯誤：{str(e)}"
        )


@app.post("/api/projects", tags=["Projects"])
async def save_project(request: SaveProjectRequest, db: Session = Depends(get_db)):
    """
    儲存新專案

    Args:
        request: 專案資料
        db: 資料庫 session

    Returns:
        儲存結果
    """
    try:
        logger.info(f"Saving project for user: {request.user_id}")

        # 檢查使用者是否存在
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="使用者不存在")

        # 檢查專案數量限制
        if not user.can_create_project(db):
            raise HTTPException(
                status_code=403,
                detail=f"已達專案數量上限（{user.max_projects}個）。請刪除舊專案或升級 VIP。"
            )

        # 建立專案
        import json

        new_project = Project(
            user_id=request.user_id,
            project_name=request.project_name,
            template_id=request.template_id,
            form_data=json.dumps(request.form_data, ensure_ascii=False),
            site_id=request.site_id,
            preview_url=request.preview_url,
            download_url=request.download_url,
            status="draft"
        )

        db.add(new_project)
        user.total_projects_created += 1
        db.commit()
        db.refresh(new_project)

        logger.info(f"Project saved: {new_project.id}")

        return {
            "success": True,
            "message": "專案已儲存",
            "project_id": new_project.id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving project: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"儲存專案時發生錯誤：{str(e)}"
        )


@app.put("/api/projects/{project_id}", tags=["Projects"])
async def update_project(
    project_id: str,
    request: UpdateProjectRequest,
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    更新專案

    Args:
        project_id: 專案 ID
        request: 更新資料
        user_id: 使用者 ID
        db: 資料庫 session

    Returns:
        更新結果
    """
    try:
        logger.info(f"Updating project: {project_id}")

        project = db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == user_id,
            Project.is_deleted == False
        ).first()

        if not project:
            raise HTTPException(status_code=404, detail="專案不存在")

        # 更新欄位
        if request.project_name is not None:
            project.project_name = request.project_name
        if request.template_id is not None:
            project.template_id = request.template_id
        if request.form_data is not None:
            import json
            project.form_data = json.dumps(request.form_data, ensure_ascii=False)
        if request.status is not None:
            project.status = request.status

        db.commit()

        logger.info(f"Project updated: {project_id}")

        return {
            "success": True,
            "message": "專案已更新"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating project: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"更新專案時發生錯誤：{str(e)}"
        )


@app.delete("/api/projects/{project_id}", tags=["Projects"])
async def delete_project(project_id: str, user_id: str, db: Session = Depends(get_db)):
    """
    刪除專案（軟刪除）

    Args:
        project_id: 專案 ID
        user_id: 使用者 ID
        db: 資料庫 session

    Returns:
        刪除結果
    """
    try:
        logger.info(f"Deleting project: {project_id}")

        project = db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == user_id,
            Project.is_deleted == False
        ).first()

        if not project:
            raise HTTPException(status_code=404, detail="專案不存在")

        # 軟刪除
        project.is_deleted = True
        db.commit()

        logger.info(f"Project deleted: {project_id}")

        return {
            "success": True,
            "message": "專案已刪除"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"刪除專案時發生錯誤：{str(e)}"
        )


@app.post("/api/projects/{project_id}/regenerate", tags=["Projects"])
async def regenerate_project(
    project_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    重新生成專案

    Args:
        project_id: 專案 ID
        user_id: 使用者 ID
        db: 資料庫 session

    Returns:
        生成結果
    """
    try:
        logger.info(f"Regenerating project: {project_id}")

        # 獲取專案
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == user_id,
            Project.is_deleted == False
        ).first()

        if not project:
            raise HTTPException(status_code=404, detail="專案不存在")

        # 解析 form_data
        import json
        form_data = json.loads(project.form_data)

        # 重新生成網站
        html_content = await website_generator.generate_website(
            template_id=project.template_id,
            user_data=form_data
        )

        # 生成新的 site_id
        new_site_id = str(uuid.uuid4())

        # 建立 ZIP 檔案
        preview_zip = zip_builder.create_website_package(
            site_id=new_site_id,
            html_content=html_content,
            user_data=form_data,
            with_api_key=False
        )

        download_zip = zip_builder.create_website_package(
            site_id=f"{new_site_id}_full",
            html_content=html_content,
            user_data=form_data,
            with_api_key=True
        )

        # 更新專案
        project.site_id = new_site_id
        project.preview_url = f"{settings.SITE_URL}/api/preview/{new_site_id}"
        project.download_url = f"{settings.SITE_URL}/api/download/{new_site_id}"
        project.status = "completed"
        project.generated_at = datetime.now()

        db.commit()

        logger.info(f"Project regenerated: {project_id} -> {new_site_id}")

        return {
            "success": True,
            "message": "專案已重新生成",
            "site_id": new_site_id,
            "preview_url": project.preview_url,
            "download_url": project.download_url
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error regenerating project: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"重新生成專案時發生錯誤：{str(e)}"
        )


@app.get("/api/usage/{site_id}", tags=["Usage"])
async def get_usage_stats(site_id: str, db: Session = Depends(get_db)):
    """
    獲取網站使用統計

    Args:
        site_id: 網站 ID
        db: 資料庫 session

    Returns:
        使用統計
    """
    try:
        stats = usage_tracker_pg.get_usage_stats(db, site_id)
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Error getting usage stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"獲取使用統計時發生錯誤：{str(e)}"
        )


# ========================================
# 聯絡表單 API
# ========================================

@app.post("/api/contact", response_model=ContactResponse, tags=["Contact"])
async def contact(request: ContactRequest):
    """
    聯絡表單提交

    Args:
        request: 聯絡表單資料（包含語言資訊）

    Returns:
        ContactResponse: 提交結果
    """
    try:
        logger.info(f"Contact form submitted: {request.email} (Language: {request.language})")

        # 格式化 Email 內容（根據語言）
        email_content = format_email(
            template_name='contact_confirmation',
            language=request.language,
            name=request.name,
            service=request.service,
            message=request.message
        )

        # 發送確認 Email 給使用者
        await email_service.send_email(
            to_email=request.email,
            subject=email_content['subject'],
            body=email_content['body']
        )

        # 發送通知 Email 給管理員（使用繁中）
        admin_email = format_email(
            template_name='contact_confirmation',
            language='zh-TW',
            name=request.name,
            service=request.service,
            message=request.message
        )

        await email_service.send_email(
            to_email='help@aiinpocket.com',
            subject=f'[新諮詢] {request.name} - {request.service}',
            body=f"""
收到新的聯絡表單提交：

姓名：{request.name}
Email：{request.email}
公司：{request.company or '未提供'}
服務：{request.service}
語言：{request.language}

訊息：
{request.message}

---
提交時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
        )

        # 發送 Webhook 通知（如果已設定）
        if settings.WEBHOOK_URL:
            try:
                import httpx
                webhook_data = {
                    "event": "contact_form_submission",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "name": request.name,
                        "email": request.email,
                        "company": request.company or "",
                        "service": request.service,
                        "message": request.message,
                        "language": request.language
                    }
                }

                async with httpx.AsyncClient(timeout=10.0) as client:
                    webhook_response = await client.post(
                        settings.WEBHOOK_URL,
                        json=webhook_data,
                        headers={"Content-Type": "application/json; charset=utf-8"}
                    )
                    logger.info(f"Webhook sent successfully: {webhook_response.status_code}")
            except Exception as webhook_error:
                # Webhook 失敗不應影響主流程
                logger.error(f"Failed to send webhook: {webhook_error}")


        # 返回成功訊息（根據語言）
        success_messages = {
            'zh-TW': '感謝您的聯繫！我們會在 24 小時內回覆您。',
            'en': 'Thank you for contacting us! We will respond within 24 hours.',
            'ja': 'お問い合わせありがとうございます！24時間以内に返信いたします。'
        }

        return ContactResponse(
            success=True,
            message=success_messages.get(request.language, success_messages['zh-TW']),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Error in contact endpoint: {e}")

        error_messages = {
            'zh-TW': '提交失敗，請稍後再試或直接發送 Email 至 help@aiinpocket.com',
            'en': 'Submission failed. Please try again later or email us at help@aiinpocket.com',
            'ja': '送信に失敗しました。後でもう一度お試しいただくか、help@aiinpocket.comまでメールでお問い合わせください'
        }

        return ContactResponse(
            success=False,
            message=error_messages.get(request.language, error_messages['zh-TW']),
            timestamp=datetime.now().isoformat()
        )


# ========================================
# 網站生成 API
# ========================================

@app.post("/api/generate-website", response_model=GenerateWebsiteResponse, tags=["Website Generation"])
async def generate_website(
    request: GenerateWebsiteRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    提交網站生成請求（異步處理）

    Args:
        request: 生成網站請求（包含模板 ID、使用者資料、圖片等）
        background_tasks: FastAPI 背景任務
        db: 資料庫 session

    Returns:
        GenerateWebsiteResponse: 包含專案 ID 和狀態訊息
    """
    try:
        logger.info(f"Received website generation request with template: {request.template_id}")

        # 1. 根據 email 查詢或創建使用者
        user_id = None
        contact_email = request.contact_email

        if contact_email:
            # 查詢使用者是否存在
            user = db.query(User).filter(User.email == contact_email).first()

            if not user:
                # 如果使用者不存在，創建新使用者（自動註冊）
                user = User(
                    email=contact_email,
                    vip_level=0,  # 免費用戶
                    max_projects=10,  # 預設上限
                    total_projects_created=0
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                logger.info(f"Auto-created user for email: {contact_email}")

            user_id = user.id

            # 更新專案計數
            user.total_projects_created += 1
            db.commit()

        # 2. 創建專案記錄
        project = Project(
            user_id=user_id,  # 關聯到使用者（通過 email 查詢得到）
            project_name=request.user_data.get("company_name", "未命名專案"),
            template_id=request.template_id,
            form_data=json.dumps(request.user_data, ensure_ascii=False),
            images_data=json.dumps(request.images, ensure_ascii=False) if request.images else None,
            status="pending"
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        logger.info(f"Created project {project.id}, submitting to background task")

        # 2. 提交到背景任務（不傳遞 db session，讓背景任務自己創建）
        from .background_tasks import submit_generation_task
        submit_generation_task(project.id)

        # 3. 立即返回（不等待生成完成）
        return GenerateWebsiteResponse(
            site_id=project.id,
            preview_url="",  # 生成完成後會發送郵件
            download_url="",
            timestamp=datetime.now().isoformat(),
            message="已收到您的請求，網站生成中，完成後將發送 Email 通知您"
        )

    except Exception as e:
        logger.error(f"Error submitting generation request: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"提交請求時發生錯誤：{str(e)}"
        )


@app.post("/api/update-website", response_model=UpdateWebsiteResponse, tags=["Website Generation"])
async def update_website(request: UpdateWebsiteRequest, db: Session = Depends(get_db)):
    """
    更新已生成的網站 (使用 AI 增量更新)

    Args:
        request: 更新網站請求 (site_id, modifications, instruction)
        db: 資料庫 session

    Returns:
        UpdateWebsiteResponse: 更新後的預覽 URL

    Examples:
        修改主題顏色:
        {
            "site_id": "abc-123",
            "modifications": {},
            "instruction": "把主色改成深藍色 #1a365d"
        }

        修改文字內容:
        {
            "site_id": "abc-123",
            "modifications": {"section": "hero", "title": "新標題"},
            "instruction": "更新首頁大標題"
        }
    """
    try:
        logger.info(f"Updating website: {request.site_id}")

        # 1. 從資料庫讀取專案
        project = db.query(Project).filter(Project.id == request.site_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="專案不存在")

        if not project.html_content:
            raise HTTPException(status_code=400, detail="網站內容不存在，無法更新")

        # 2. 使用 AI 進行增量更新
        updated_html = await website_generator.update_website(
            current_html=project.html_content,
            instruction=request.instruction,
            modifications=request.modifications
        )

        # 3. 保存更新後的 HTML 到資料庫
        project.html_content = updated_html
        project.updated_at = datetime.utcnow()
        db.commit()

        logger.info(f"Website updated successfully: {request.site_id}")

        # 4. 返回結果
        return UpdateWebsiteResponse(
            site_id=request.site_id,
            preview_url=f"/api/preview/{request.site_id}",
            timestamp=datetime.now().isoformat(),
            changes_applied=request.modifications
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating website: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"更新網站時發生錯誤：{str(e)}"
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
async def preview_website(site_id: str, db: Session = Depends(get_db)):
    """
    預覽網站（圖片以 data URI 嵌入）

    Args:
        site_id: 專案/網站 ID
        db: 資料庫 session

    Returns:
        HTML 內容
    """
    try:
        logger.info(f"Preview request for site: {site_id}")

        # 從資料庫取得專案
        project = db.query(Project).filter(Project.id == site_id).first()

        if not project:
            logger.warning(f"Project not found: {site_id}")
            raise HTTPException(status_code=404, detail="專案不存在")

        if project.status == "pending":
            return HTMLResponse(content="""
                <!DOCTYPE html>
                <html lang="zh-TW">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>生成中...</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            min-height: 100vh;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            text-align: center;
                        }
                        .container { padding: 2rem; }
                        .spinner {
                            border: 4px solid rgba(255, 255, 255, 0.3);
                            border-top: 4px solid white;
                            border-radius: 50%;
                            width: 50px;
                            height: 50px;
                            animation: spin 1s linear infinite;
                            margin: 0 auto 1rem;
                        }
                        @keyframes spin {
                            0% { transform: rotate(0deg); }
                            100% { transform: rotate(360deg); }
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="spinner"></div>
                        <h2>🚀 網站生成中...</h2>
                        <p>我們正在為您生成專屬網站，完成後將發送 Email 通知您</p>
                    </div>
                </body>
                </html>
            """)

        if project.status == "failed":
            return HTMLResponse(content=f"""
                <!DOCTYPE html>
                <html lang="zh-TW">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>生成失敗</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            min-height: 100vh;
                            background: #f8d7da;
                            color: #721c24;
                            text-align: center;
                        }}
                        .container {{ padding: 2rem; max-width: 600px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>😔 網站生成失敗</h2>
                        <p>錯誤訊息：{project.error_message}</p>
                        <p>請聯繫客服或嘗試重新生成</p>
                    </div>
                </body>
                </html>
            """)

        if not project.html_content:
            raise HTTPException(status_code=500, detail="網站內容不存在")

        # 返回 HTML（圖片已經嵌入為 data URI）
        return HTMLResponse(content=project.html_content)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving preview: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"載入預覽時發生錯誤：{str(e)}"
        )


@app.post("/api/regenerate-download-password/{project_id}", tags=["Website Generation"])
async def regenerate_download_password(project_id: str, db: Session = Depends(get_db)):
    """
    重新生成下載密碼並發送郵件給使用者

    Args:
        project_id: 專案 ID
        db: 資料庫 session

    Returns:
        成功訊息
    """
    try:
        project = db.query(Project).filter(Project.id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="專案不存在")

        # 取得使用者 email
        user = db.query(User).filter(User.id == project.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="使用者不存在")

        # 生成新密碼
        import random
        new_password = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        project.download_password = new_password
        project.download_password_used = False
        db.commit()

        logger.info(f"Download password regenerated for project: {project_id}")

        # 發送下載密碼郵件
        try:
            await email_service.send_download_password_email(user.email, project.project_name, new_password, project.site_id)
            logger.info(f"Download password email sent to: {user.email}")
        except Exception as email_error:
            logger.error(f"Failed to send download password email: {email_error}")
            # 即使郵件發送失敗，也要告知使用者密碼（開發模式）
            logger.warning(f"[DEV MODE] Download password for {user.email}: {new_password}")

        return {
            "success": True,
            "message": "下載密碼已發送到您的信箱"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error regenerating password: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"重新生成密碼時發生錯誤：{str(e)}"
        )


@app.get("/api/download/{site_id}", tags=["Website Generation"])
async def download_website(site_id: str, password: str, db: Session = Depends(get_db)):
    """
    下載完整版 ZIP（需要一次性密碼）

    Args:
        site_id: 專案/網站 ID
        password: 一次性下載密碼
        db: 資料庫 session

    Returns:
        ZIP 檔案
    """
    try:
        logger.info(f"Download request for site: {site_id}")

        # 從資料庫取得專案
        project = db.query(Project).filter(Project.id == site_id).first()

        if not project:
            logger.warning(f"Project not found: {site_id}")
            raise HTTPException(status_code=404, detail="專案不存在")

        if project.status != "completed":
            raise HTTPException(
                status_code=400,
                detail=f"專案尚未完成生成，目前狀態：{project.status}"
            )

        # 驗證下載密碼
        if not project.download_password:
            raise HTTPException(status_code=400, detail="此專案未設定下載密碼")

        if project.download_password_used:
            raise HTTPException(
                status_code=403,
                detail="下載密碼已使用過，請聯繫客服重新取得密碼"
            )

        if project.download_password != password:
            raise HTTPException(status_code=403, detail="下載密碼錯誤")

        # 標記密碼已使用
        project.download_password_used = True
        db.commit()

        logger.info(f"Download password validated for site: {site_id}")

        # 生成下載套件
        from .background_tasks import create_download_package
        zip_buffer = create_download_package(project)

        # 返回 ZIP 檔案
        return StreamingResponse(
            zip_buffer,
            media_type='application/zip',
            headers={
                'Content-Disposition': f'attachment; filename="website_{project.project_name}.zip"'
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving download: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"下載檔案時發生錯誤：{str(e)}"
        )


@app.get("/preview/{site_id}", tags=["Website Generation"])
async def preview_website(site_id: str, db: Session = Depends(get_db)):
    """
    預覽生成的網站（返回 HTML）

    Args:
        site_id: 專案/網站 ID
        db: 資料庫 session

    Returns:
        HTML 內容
    """
    try:
        logger.info(f"Preview request for site: {site_id}")

        # 從資料庫取得專案
        project = db.query(Project).filter(Project.site_id == site_id).first()

        if not project:
            # 也嘗試使用 project.id 查找
            project = db.query(Project).filter(Project.id == site_id).first()

        if not project:
            logger.warning(f"Project not found: {site_id}")
            raise HTTPException(status_code=404, detail="專案不存在")

        if project.status == "failed":
            raise HTTPException(
                status_code=400,
                detail=f"網站生成失敗：{project.error_message or '未知錯誤'}"
            )

        if project.status != "completed":
            # 返回生成中的頁面
            return HTMLResponse(content=f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>網站生成中...</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #0a0e27, #1a1f3a);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }}
        .container {{
            text-align: center;
            padding: 2rem;
        }}
        .spinner {{
            border: 4px solid rgba(135, 206, 235, 0.3);
            border-top: 4px solid #87CEEB;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
            margin: 0 auto 2rem;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        h1 {{ color: #7FFF00; }}
        p {{ color: #87CEEB; font-size: 1.2rem; }}
    </style>
    <script>
        setTimeout(() => location.reload(), 5000);
    </script>
</head>
<body>
    <div class="container">
        <div class="spinner"></div>
        <h1>🚀 網站生成中...</h1>
        <p>狀態：{project.status}</p>
        <p>頁面將每 5 秒自動重新整理</p>
    </div>
</body>
</html>
            """)

        # 返回完成的 HTML
        if not project.html_content:
            raise HTTPException(status_code=500, detail="HTML 內容不存在")

        return HTMLResponse(content=project.html_content)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving preview: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"預覽網站時發生錯誤：{str(e)}"
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
