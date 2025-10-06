"""
背景任務處理
用於異步網站生成（支援並行處理）
"""
import json
import base64
import os
import zipfile
import asyncio
from io import BytesIO
from datetime import datetime
from typing import Dict, Optional
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore

from .models import Project
from .website_generator import website_generator
from .email_service import email_service
from .config import settings
from .database import SessionLocal
import logging

logger = logging.getLogger(__name__)

# 並行處理配置
# 限制同時處理的任務數（使用 50% CPU，假設 4 核心 = 2 個並行任務）
import multiprocessing
MAX_WORKERS = max(1, multiprocessing.cpu_count() // 2)  # 使用 50% CPU
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
task_semaphore = Semaphore(MAX_WORKERS)  # 限制並發數

logger.info(f"[INIT] Background task executor initialized with {MAX_WORKERS} workers (50% CPU)")


def submit_generation_task(project_id: str):
    """
    提交生成任務到線程池（立即返回，不阻塞）

    Args:
        project_id: 專案 ID
    """
    logger.info(f"[SUBMIT] Submitting generation task for project {project_id}")
    executor.submit(_run_generation_task, project_id)


def _run_generation_task(project_id: str):
    """
    在獨立線程中執行生成任務

    Args:
        project_id: 專案 ID
    """
    with task_semaphore:  # 限制並發數
        logger.info(f"[START] Starting generation for project {project_id}")
        try:
            # 在新的 event loop 中運行異步任務
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(generate_website_async(project_id))
            finally:
                loop.close()
        except Exception as e:
            logger.error(f"[ERROR] Failed to run generation task for {project_id}: {e}", exc_info=True)


async def generate_website_async(project_id: str):
    """
    異步生成網站

    Args:
        project_id: 專案 ID
    """
    # 創建新的 DB session（每個線程獨立）
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            logger.error(f"[ERROR] Project {project_id} not found")
            return

        # 更新狀態為 generating
        project.status = "generating"
        db.commit()

        # 解析表單資料
        form_data = json.loads(project.form_data)

        # 準備使用者資料
        user_data = {
            "company_name": form_data.get("company_name", ""),
            "tagline": form_data.get("tagline", ""),
            "description": form_data.get("description", ""),
            "services": form_data.get("services", []),
            "contact_email": form_data.get("contact_email", ""),
            "contact_phone": form_data.get("contact_phone", ""),
            "portfolio": form_data.get("portfolio", [])
        }

        # 準備圖片鍵值
        image_keys = None
        if project.images_data:
            images = json.loads(project.images_data)
            image_keys = list(images.keys())

        # 生成網站 HTML
        html_content = await website_generator.generate_website(
            template_id=project.template_id,
            user_data=user_data,
            custom_style=None,
            languages=["zh-TW", "en", "ja"],
            image_keys=image_keys
        )

        # 儲存 HTML 內容
        project.html_content = html_content

        # 如果有圖片，處理圖片嵌入
        if project.images_data:
            images = json.loads(project.images_data)
            html_content = embed_images_in_html(html_content, images)
            project.html_content = html_content

        # 生成網站 ID 和 URLs
        if not project.site_id:
            import uuid
            project.site_id = str(uuid.uuid4())

        # 生成一次性下載密碼（6位數字）
        import random
        download_password = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        project.preview_url = f"{settings.SITE_URL}/preview/{project.site_id}"
        project.download_url = f"{settings.SITE_URL}/api/download/{project.site_id}"
        project.download_password = download_password
        project.download_password_used = False

        # 更新狀態為 completed
        project.status = "completed"
        project.generated_at = datetime.utcnow()
        project.error_message = None
        db.commit()

        # 發送完成通知郵件
        await send_completion_email(project, db)

        logger.info(f"[SUCCESS] Website generated successfully for project {project_id}")

    except Exception as e:
        logger.error(f"[ERROR] Failed to generate website for project {project_id}: {e}", exc_info=True)
        try:
            project.status = "failed"
            project.error_message = str(e)
            db.commit()

            # 發送失敗通知郵件
            await send_failure_email(project, db)
        except Exception as email_error:
            logger.error(f"[ERROR] Failed to send failure email: {email_error}")

    finally:
        # 確保關閉 DB session
        db.close()
        logger.info(f"[DONE] Generation task completed for project {project_id}")


def embed_images_in_html(html: str, images: Dict[str, str]) -> str:
    """
    將圖片以 data URI 嵌入到 HTML 中（用於預覽）

    Args:
        html: HTML 內容
        images: {"image_key": "base64_data", ...}

    Returns:
        處理後的 HTML
    """
    for key, base64_data in images.items():
        # 替換圖片引用為 data URI
        placeholder = f"{{{{ {key} }}}}"
        data_uri = f"data:image/jpeg;base64,{base64_data}"
        html = html.replace(placeholder, data_uri)

    return html


async def send_completion_email(project: Project, db: Session):
    """發送生成完成通知郵件"""
    try:
        form_data = json.loads(project.form_data)
        user_email = form_data.get("contact_email")

        if not user_email:
            logger.warning(f"No email found for project {project.id}")
            return

        # 從 project 取得下載密碼
        download_password = project.download_password

        subject = f"✅ 您的網站 \"{project.project_name}\" 已生成完成 - 下載密碼：{download_password}"

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #87CEEB;">🎉 網站生成完成！</h2>

                <p>您好，</p>

                <p>您的網站 <strong>"{project.project_name}"</strong> 已成功生成完成！</p>

                <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">📋 專案資訊</h3>
                    <p><strong>專案名稱：</strong>{project.project_name}</p>
                    <p><strong>使用模板：</strong>{project.template_id}</p>
                    <p><strong>生成時間：</strong>{project.generated_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>

                <div style="margin: 30px 0;">
                    <a href="{project.preview_url}"
                       style="display: inline-block; padding: 12px 24px; background: #87CEEB; color: white; text-decoration: none; border-radius: 5px;">
                        🔍 預覽您的網站
                    </a>
                </div>

                <div style="background: linear-gradient(135deg, #7FFF00, #32CD32); border-radius: 12px; padding: 25px; margin: 30px 0; text-align: center; box-shadow: 0 4px 15px rgba(127, 255, 0, 0.3);">
                    <h3 style="margin-top: 0; color: white; font-size: 1.3em;">🔑 您的下載密碼</h3>
                    <div style="background: white; border-radius: 8px; padding: 20px; margin: 15px 0;">
                        <div style="font-size: 2.5em; font-weight: bold; color: #7FFF00; letter-spacing: 0.3em; font-family: 'Courier New', monospace;">
                            {download_password}
                        </div>
                    </div>
                    <p style="margin: 10px 0 0 0; color: white; font-size: 0.95em;">
                        ⚠️ 此密碼僅可使用一次，請妥善保管
                    </p>
                </div>

                <div style="background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #155724;">📥 如何下載您的網站</h3>
                    <ol style="margin: 10px 0; padding-left: 20px; color: #155724;">
                        <li>前往 <a href="https://aiinpocket.com/generator/dashboard.html" style="color: #155724; font-weight: bold;">我的作品頁面</a></li>
                        <li>使用本信箱登入（若尚未登入）</li>
                        <li>找到您的專案並點擊「📥 下載」按鈕</li>
                        <li>在彈出視窗中輸入上方的 <strong>6位數密碼</strong></li>
                        <li>點擊「確認下載」即可下載 ZIP 檔案</li>
                    </ol>
                    <p style="margin: 10px 0 0 0; color: #856404; background: #fff3cd; padding: 10px; border-radius: 5px;">
                        <strong>💡 提示：</strong>如果忘記密碼或密碼已使用，可在「我的作品」頁面點擊「重新取得密碼」按鈕
                    </p>
                </div>

                <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>💡 下載檔案包含：</strong></p>
                    <ul style="margin: 10px 0;">
                        <li><strong>index.html</strong> - 完整網站檔案（已包含所有樣式和多語言支援）</li>
                        <li><strong>images/</strong> - 所有圖片資源（如有上傳）</li>
                    </ul>
                    <p style="margin: 0;">解壓縮後即可直接部署到任何靜態網站託管服務（GitHub Pages、Netlify、Vercel 等）！</p>
                </div>

                <div style="background: #e7f3ff; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>🔐 安全提示：</strong></p>
                    <ul style="margin: 10px 0;">
                        <li>下載密碼為 <strong>一次性使用</strong>，下載後即失效</li>
                        <li>如需重新下載，請在「我的作品」中點擊「🔄 重新取得密碼」按鈕</li>
                        <li>新密碼將直接顯示在頁面上，無需重新收信</li>
                        <li>請妥善保管您的帳號，避免作品被他人存取</li>
                    </ul>
                </div>

                <p>如有任何問題，請隨時聯繫我們：<a href="mailto:help@aiinpocket.com" style="color: #87CEEB;">help@aiinpocket.com</a></p>

                <p>祝您使用愉快！</p>

                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

                <p style="color: #999; font-size: 12px;">
                    此郵件由 AiInPocket 網站生成器自動發送<br>
                    © 2025 AiInPocket. All rights reserved.
                </p>
            </div>
        </body>
        </html>
        """

        await email_service.send_email(
            to_email=user_email,
            subject=subject,
            body=html_body
        )

        logger.info(f"Completion email sent to {user_email} for project {project.id}")

    except Exception as e:
        logger.error(f"Failed to send completion email: {e}")


async def send_failure_email(project: Project, db: Session):
    """發送生成失敗通知郵件"""
    try:
        form_data = json.loads(project.form_data)
        user_email = form_data.get("contact_email")

        if not user_email:
            logger.warning(f"No email found for project {project.id}")
            return

        subject = f"❌ 網站生成失敗 - {project.project_name}"

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #dc3545;">😔 網站生成失敗</h2>

                <p>您好，</p>

                <p>很抱歉，您的網站 <strong>"{project.project_name}"</strong> 生成過程中遇到錯誤。</p>

                <div style="background: #f8d7da; border-left: 4px solid #dc3545; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>錯誤訊息：</strong></p>
                    <p style="margin: 10px 0; font-family: monospace; font-size: 14px;">{project.error_message}</p>
                </div>

                <p>我們的團隊已收到錯誤通知，將盡快為您處理。</p>

                <p>您也可以：</p>
                <ul>
                    <li>嘗試使用不同的模板重新生成</li>
                    <li>檢查提供的資料是否完整</li>
                    <li>聯繫我們的客服團隊：<a href="mailto:help@aiinpocket.com">help@aiinpocket.com</a></li>
                </ul>

                <p>造成您的不便，敬請見諒。</p>

                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

                <p style="color: #999; font-size: 12px;">
                    此郵件由 AiInPocket 網站生成器自動發送<br>
                    © 2025 AiInPocket. All rights reserved.
                </p>
            </div>
        </body>
        </html>
        """

        await email_service.send_email(
            to_email=user_email,
            subject=subject,
            body=html_body
        )

        logger.info(f"Failure email sent to {user_email} for project {project.id}")

    except Exception as e:
        logger.error(f"Failed to send failure email: {e}")


def create_download_package(project: Project) -> BytesIO:
    """
    創建下載套件（ZIP）
    包含 HTML 和 images 資料夾

    Args:
        project: 專案物件

    Returns:
        ZIP 檔案的 BytesIO
    """
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 添加 HTML 檔案
        html_content = project.html_content

        # 如果有圖片，處理圖片引用並添加圖片檔案
        if project.images_data:
            images = json.loads(project.images_data)

            # 替換 HTML 中的圖片引用為相對路徑
            for key, base64_data in images.items():
                placeholder = f"{{{{ {key} }}}}"
                relative_path = f"./images/{key}.jpg"
                html_content = html_content.replace(placeholder, relative_path)

                # 解碼 base64 並添加到 ZIP
                image_data = base64.b64decode(base64_data)
                zip_file.writestr(f"images/{key}.jpg", image_data)

        # 添加處理後的 HTML
        zip_file.writestr("index.html", html_content)

    zip_buffer.seek(0)
    return zip_buffer
