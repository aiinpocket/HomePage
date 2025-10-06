"""
資料庫設定和模型
使用 PostgreSQL + pgvector 實作 RAG 系統
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# 建立資料庫引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# 建立 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 匯入模型（放在這裡避免循環匯入）
from .models import Base, User, Project, OTPToken, PageContent


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
