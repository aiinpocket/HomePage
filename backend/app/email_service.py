"""
Email 通知服務
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import settings


class EmailService:
    """Email 發送服務"""

    async def send_otp_email(
        self,
        recipient_email: str,
        otp_code: str,
        expires_minutes: int = 10
    ):
        """發送一次性密碼（OTP）郵件"""

        subject = "🔐 AiInPocket 登入驗證碼"

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #87CEEB, #7FFF00); color: #0a0e27; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .otp-code {{ background: #0a0e27; color: #7FFF00; font-size: 32px; font-weight: bold; letter-spacing: 8px; padding: 20px; text-align: center; border-radius: 10px; margin: 30px 0; font-family: 'Courier New', monospace; }}
        .warning {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0; }}
        .info-box {{ background: white; padding: 20px; border-left: 4px solid #87CEEB; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 登入驗證碼</h1>
            <p>AiInPocket 口袋智慧</p>
        </div>
        <div class="content">
            <h2>您好！</h2>
            <p>您正在嘗試登入 AiInPocket 網站生成器。請使用以下驗證碼完成登入：</p>

            <div class="otp-code">
                {otp_code}
            </div>

            <div class="warning">
                <strong>⏰ 重要提示：</strong>
                <ul style="margin: 10px 0;">
                    <li>此驗證碼將在 <strong>{expires_minutes} 分鐘</strong>後失效</li>
                    <li>此驗證碼 <strong>僅能使用一次</strong></li>
                    <li>請勿分享此驗證碼給任何人</li>
                </ul>
            </div>

            <div class="info-box">
                <h3>🛡️ 安全性說明</h3>
                <p>我們使用一次性密碼（OTP）來保護您的帳號安全：</p>
                <ul>
                    <li>每次登入都需要新的驗證碼</li>
                    <li>驗證碼使用後立即失效</li>
                    <li>保護您的作品不被他人竊取</li>
                </ul>
            </div>

            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">

            <p><strong>如果您沒有嘗試登入，請忽略此郵件。</strong></p>

            <p style="margin-top: 30px;">
                <strong>需要協助？</strong><br>
                Email: support@aiinpocket.com<br>
                網站: https://aiinpocket.com
            </p>

            <p style="color: #666; font-size: 14px; margin-top: 30px;">
                © 2025 AiInPocket. 讓智慧觸手可及。
            </p>
        </div>
    </div>
</body>
</html>
"""

        await self._send_email(recipient_email, subject, html_body)

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

    async def send_email(self, to_email: str, subject: str, body: str):
        """
        通用的 Email 發送方法

        Args:
            to_email: 收件人 Email
            subject: 郵件主旨
            body: 郵件內容（純文字或 HTML）
        """
        # 如果 body 看起來像 HTML，直接使用，否則包裝成簡單的 HTML
        if '<html' in body.lower() or '<body' in body.lower():
            html_body = body
        else:
            # 簡單的文字包裝成 HTML
            html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 10px; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            {body}
        </div>
    </div>
</body>
</html>
"""
        await self._send_email(to_email, subject, html_body)

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
