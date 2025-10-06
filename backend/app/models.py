"""
資料庫模型定義
包含使用者、作品、一次性密碼等
"""
from sqlalchemy import Column, String, DateTime, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector
from datetime import datetime, timedelta
import uuid

Base = declarative_base()


class User(Base):
    """使用者模型"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 關聯
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    otp_tokens = relationship("OTPToken", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"


class Project(Base):
    """網站生成專案模型"""
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    # 專案基本資訊
    project_name = Column(String(255), nullable=False)  # 專案名稱（使用者可自訂）
    template_id = Column(String(50), nullable=False)    # 使用的模板 ID

    # 表單資料（JSON 格式儲存）
    form_data = Column(Text, nullable=False)  # 儲存完整的表單資料（JSON）

    # 生成結果
    site_id = Column(String(36), unique=True, index=True)  # 生成的網站 ID
    preview_url = Column(String(500))
    download_url = Column(String(500))

    # 狀態
    status = Column(String(20), default="draft")  # draft, generating, completed, failed
    is_deleted = Column(Boolean, default=False)   # 軟刪除標記

    # 時間戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    generated_at = Column(DateTime, nullable=True)  # 實際生成時間

    # 關聯
    user = relationship("User", back_populates="projects")

    def __repr__(self):
        return f"<Project {self.project_name} ({self.id})>"


class OTPToken(Base):
    """一次性密碼（One-Time Password）模型"""
    __tablename__ = "otp_tokens"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    # 密碼資訊
    token = Column(String(6), nullable=False, index=True)  # 6 位數字密碼

    # 狀態
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)

    # 時間限制
    expires_at = Column(DateTime, nullable=False)  # 過期時間（10 分鐘）
    created_at = Column(DateTime, default=datetime.utcnow)

    # 關聯
    user = relationship("User", back_populates="otp_tokens")

    def is_valid(self):
        """檢查密碼是否有效"""
        if self.is_used:
            return False
        if datetime.utcnow() > self.expires_at:
            return False
        return True

    def mark_as_used(self):
        """標記為已使用"""
        self.is_used = True
        self.used_at = datetime.utcnow()

    @staticmethod
    def generate_token():
        """生成 6 位數字密碼"""
        import random
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

    def __repr__(self):
        return f"<OTPToken {self.token} (used={self.is_used})>"


class PageContent(Base):
    """頁面內容表 - 儲存網頁內容和向量（用於 RAG 系統）"""
    __tablename__ = "page_contents"

    id = Column(Integer, primary_key=True, index=True)
    url_path = Column(String, unique=True, index=True)  # 例如: /index.html
    title = Column(String)  # 頁面標題
    description = Column(Text)  # 頁面描述
    content = Column(Text)  # 頁面主要內容（純文字）
    keywords = Column(Text)  # 關鍵字（逗號分隔）

    # 向量欄位 - OpenAI embeddings 是 1536 維
    embedding = Column(Vector(1536))

    # 元數據
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PageContent(url_path='{self.url_path}', title='{self.title}')>"
