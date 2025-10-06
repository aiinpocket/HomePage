"""
Email 通知服務
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import settings


class EmailService:
    """Email 發送服務"""

    async def send_generation_complete_email(
        self,
        recipient_email: str,
        site_id: str,
        company_name: str,
        preview_url: str,
        download_url: str
    ):
        """發送網站生成完成通知"""

        subject = f"🎉 您的網站已生成完成 - {company_name}"

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .button {{ display: inline-block; padding: 15px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 10px 5px; }}
        .info-box {{ background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 網站生成完成！</h1>
            <p>您的專屬網站已經準備就緒</p>
        </div>
        <div class="content">
            <h2>親愛的 {company_name}，</h2>
            <p>您的網站已經成功生成！我們很高興能為您打造這個專屬網站。</p>

            <div class="info-box">
                <h3>📱 立即預覽</h3>
                <p>網站 ID: <code>{site_id}</code></p>
                <p>預覽網址: <a href="{preview_url}">{preview_url}</a></p>
                <p><small>⚠️ 預覽版 AI 聊天機器人限用 30 次</small></p>
            </div>

            <div class="info-box">
                <h3>📦 下載完整版</h3>
                <p>下載後可使用您自己的 OpenAI API Key，無使用次數限制！</p>
                <p>下載網址: <a href="{download_url}">{download_url}</a></p>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{preview_url}" class="button">立即預覽網站</a>
                <a href="{download_url}" class="button" style="background: #10b981;">下載完整版</a>
            </div>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">

            <h3>💡 接下來可以做什麼？</h3>
            <ul>
                <li>預覽並測試網站功能</li>
                <li>下載完整版並設定您的 API Key</li>
                <li>自訂網站內容和樣式</li>
                <li>部署到您的網域</li>
            </ul>

            <p style="margin-top: 30px;">
                <strong>需要協助？</strong><br>
                Email: support@aiinpocket.com<br>
                網站: https://aiinpocket.com
            </p>

            <p style="color: #666; font-size: 14px; margin-top: 30px;">
                © 2025 AiInPocket. 由 AI 網站生成器自動建立。
            </p>
        </div>
    </div>
</body>
</html>
"""

        await self._send_email(recipient_email, subject, html_body)

    async def _send_email(self, to_email: str, subject: str, html_body: str):
        """實際發送 email"""

        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            print(f"[WARN] SMTP not configured, email not sent to {to_email}")
            print(f"[INFO] Subject: {subject}")
            return

        try:
            message = MIMEMultipart('alternative')
            message['From'] = settings.SMTP_FROM
            message['To'] = to_email
            message['Subject'] = subject

            html_part = MIMEText(html_body, 'html', 'utf-8')
            message.attach(html_part)

            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=True
            )

            print(f"[OK] Email sent to {to_email}")

        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")


# 全域實例
email_service = EmailService()
