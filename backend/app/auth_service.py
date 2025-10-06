"""
使用者認證服務
處理 Email 登入和一次性密碼（OTP）
"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, Tuple
import logging

from .models import User, OTPToken
from .email_service import email_service

logger = logging.getLogger(__name__)


class AuthService:
    """認證服務類別"""

    @staticmethod
    def get_or_create_user(db: Session, email: str) -> User:
        """
        取得或建立使用者

        Args:
            db: 資料庫 session
            email: 使用者 email

        Returns:
            User 物件
        """
        # 查詢使用者
        user = db.query(User).filter(User.email == email).first()

        if not user:
            # 建立新使用者
            user = User(email=email)
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created new user: {email}")

        return user

    @staticmethod
    async def send_otp(db: Session, email: str) -> Tuple[bool, str]:
        """
        發送一次性密碼到使用者信箱

        Args:
            db: 資料庫 session
            email: 使用者 email

        Returns:
            (成功與否, 訊息)
        """
        try:
            # 取得或建立使用者
            user = AuthService.get_or_create_user(db, email)

            # 使舊的未使用密碼失效（設為已使用）
            old_tokens = db.query(OTPToken).filter(
                OTPToken.user_id == user.id,
                OTPToken.is_used == False,
                OTPToken.expires_at > datetime.utcnow()
            ).all()

            for token in old_tokens:
                token.mark_as_used()

            # 生成新的一次性密碼
            otp_token = OTPToken.generate_token()
            expires_at = datetime.utcnow() + timedelta(minutes=10)  # 10 分鐘有效

            # 儲存到資料庫
            new_token = OTPToken(
                user_id=user.id,
                token=otp_token,
                expires_at=expires_at
            )
            db.add(new_token)
            db.commit()

            logger.info(f"Generated OTP for user: {email}")

            # 發送 Email
            try:
                await email_service.send_otp_email(
                    recipient_email=email,
                    otp_code=otp_token,
                    expires_minutes=10
                )
                logger.info(f"OTP email sent to: {email}")
                return True, "驗證碼已發送到您的信箱"
            except Exception as email_error:
                logger.error(f"Failed to send OTP email: {email_error}")
                # 即使 Email 發送失敗，密碼仍然有效（開發環境可以從 log 看到）
                logger.info(f"OTP Code (for dev): {otp_token}")
                return True, f"驗證碼已生成（開發模式）: {otp_token}"

        except Exception as e:
            logger.error(f"Error sending OTP: {e}")
            return False, "發送驗證碼失敗，請稍後再試"

    @staticmethod
    def verify_otp(db: Session, email: str, otp_code: str) -> Tuple[bool, Optional[str], str]:
        """
        驗證一次性密碼

        Args:
            db: 資料庫 session
            email: 使用者 email
            otp_code: 一次性密碼

        Returns:
            (驗證成功與否, 使用者 ID, 訊息)
        """
        try:
            # 查詢使用者
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return False, None, "使用者不存在"

            # 查詢密碼
            token = db.query(OTPToken).filter(
                OTPToken.user_id == user.id,
                OTPToken.token == otp_code,
                OTPToken.is_used == False
            ).first()

            if not token:
                return False, None, "驗證碼無效"

            # 檢查是否過期
            if not token.is_valid():
                return False, None, "驗證碼已過期或已使用"

            # 標記為已使用
            token.mark_as_used()
            db.commit()

            logger.info(f"OTP verified successfully for user: {email}")
            return True, user.id, "驗證成功"

        except Exception as e:
            logger.error(f"Error verifying OTP: {e}")
            return False, None, "驗證失敗，請稍後再試"

    @staticmethod
    def create_session_token(user_id: str) -> str:
        """
        建立 session token（簡單的 JWT 或隨機 token）

        Args:
            user_id: 使用者 ID

        Returns:
            session token
        """
        import secrets
        import hashlib

        # 生成隨機 token
        random_data = f"{user_id}:{datetime.utcnow().isoformat()}:{secrets.token_urlsafe(32)}"
        token = hashlib.sha256(random_data.encode()).hexdigest()

        return token


# 全域認證服務實例
auth_service = AuthService()
