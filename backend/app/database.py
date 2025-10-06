"""
資料庫設定和模型
使用 PostgreSQL + pgvector 實作 RAG 系統
"""
from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from datetime import datetime
from .config import settings

# 建立資料庫引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# 建立 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 類別
Base = declarative_base()


class PageContent(Base):
    """頁面內容表 - 儲存網頁內容和向量"""
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


def get_db():
    """獲取資料庫 session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化資料庫 - 建立表格和 pgvector 擴展"""
    from sqlalchemy import text

    # 啟用 pgvector 擴展
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    # 建立所有表格
    Base.metadata.create_all(bind=engine)
    print("[DB] Database initialized successfully")


def drop_all_tables():
    """刪除所有表格（僅供開發使用）"""
    Base.metadata.drop_all(bind=engine)
    print("[DB] All tables dropped")
