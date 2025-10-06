"""
RAG (Retrieval-Augmented Generation) 系統
使用向量搜尋找到最相關的頁面
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from openai import OpenAI
from typing import List, Dict, Optional
from .database import PageContent, SessionLocal
from .html_parser import HTMLParser
from .config import settings


class RAGSystem:
    """RAG 向量搜尋系統"""

    def __init__(self):
        self.openai_client = None
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
            try:
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                print("[OK] RAG System initialized with OpenAI embeddings")
            except Exception as e:
                print(f"[WARN] RAG System initialized without OpenAI: {e}")
        else:
            print("[WARN] RAG System initialized without OpenAI API key")

    def create_embedding(self, text: str) -> Optional[List[float]]:
        """
        使用 OpenAI 建立文字的向量表示

        Args:
            text: 要轉換的文字

        Returns:
            1536 維的向量列表
        """
        if not self.openai_client:
            return None

        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"[ERROR] Failed to create embedding: {e}")
            return None

    def index_page(self, page_data: Dict, db: Session) -> bool:
        """
        為單個頁面建立索引

        Args:
            page_data: 頁面資料字典
            db: 資料庫 session

        Returns:
            是否成功
        """
        try:
            # 組合文字用於生成向量
            text_for_embedding = f"{page_data['title']} {page_data['description']} {page_data['content']}"

            # 建立向量
            embedding = self.create_embedding(text_for_embedding)
            if not embedding:
                print(f"[WARN] Skipping {page_data['url_path']} - no embedding")
                return False

            # 檢查是否已存在
            existing = db.query(PageContent).filter(
                PageContent.url_path == page_data['url_path']
            ).first()

            if existing:
                # 更新現有記錄
                existing.title = page_data['title']
                existing.description = page_data['description']
                existing.content = page_data['content']
                existing.keywords = page_data['keywords']
                existing.embedding = embedding
                print(f"[UPDATE] Updated index for: {page_data['url_path']}")
            else:
                # 建立新記錄
                page = PageContent(
                    url_path=page_data['url_path'],
                    title=page_data['title'],
                    description=page_data['description'],
                    content=page_data['content'],
                    keywords=page_data['keywords'],
                    embedding=embedding
                )
                db.add(page)
                print(f"[CREATE] Created index for: {page_data['url_path']}")

            db.commit()
            return True

        except Exception as e:
            print(f"[ERROR] Failed to index page {page_data.get('url_path')}: {e}")
            db.rollback()
            return False

    def index_all_pages(self) -> int:
        """
        索引所有頁面

        Returns:
            成功索引的頁面數量
        """
        print("\n" + "="*50)
        print("[RAG] Starting to index all pages...")
        print("="*50)

        # 解析所有 HTML
        parser = HTMLParser(settings.FRONTEND_PATH)
        pages = parser.parse_all_pages()

        if not pages:
            print("[WARN] No pages found to index")
            return 0

        # 建立索引
        db = SessionLocal()
        success_count = 0

        try:
            for page_data in pages:
                if self.index_page(page_data, db):
                    success_count += 1

            print("\n" + "="*50)
            print(f"[RAG] Indexed {success_count}/{len(pages)} pages successfully")
            print("="*50 + "\n")

        finally:
            db.close()

        return success_count

    def search_similar_pages(
        self,
        query: str,
        db: Session,
        limit: int = 3
    ) -> List[PageContent]:
        """
        搜尋與查詢最相似的頁面

        Args:
            query: 使用者查詢
            db: 資料庫 session
            limit: 返回結果數量

        Returns:
            相似頁面列表
        """
        if not self.openai_client:
            print("[WARN] No OpenAI client, using fallback search")
            return self._fallback_search(query, db, limit)

        try:
            # 建立查詢向量
            query_embedding = self.create_embedding(query)
            if not query_embedding:
                return self._fallback_search(query, db, limit)

            # 使用 pgvector 的 cosine distance 搜尋
            # <-> 是 pgvector 的 cosine distance 運算符
            results = db.query(PageContent).order_by(
                PageContent.embedding.cosine_distance(query_embedding)
            ).limit(limit).all()

            if results:
                print(f"[RAG] Found {len(results)} similar pages for query: '{query}'")
                for i, page in enumerate(results, 1):
                    print(f"  {i}. {page.url_path} - {page.title}")

            return results

        except Exception as e:
            print(f"[ERROR] Vector search failed: {e}")
            return self._fallback_search(query, db, limit)

    def _fallback_search(
        self,
        query: str,
        db: Session,
        limit: int = 3
    ) -> List[PageContent]:
        """
        備用搜尋方法（不使用向量，用關鍵字匹配）
        """
        query_lower = query.lower()

        try:
            # 簡單的關鍵字匹配
            results = db.query(PageContent).filter(
                (PageContent.title.ilike(f"%{query_lower}%")) |
                (PageContent.description.ilike(f"%{query_lower}%")) |
                (PageContent.content.ilike(f"%{query_lower}%")) |
                (PageContent.keywords.ilike(f"%{query_lower}%"))
            ).limit(limit).all()

            print(f"[FALLBACK] Found {len(results)} pages using keyword search")
            return results

        except Exception as e:
            print(f"[ERROR] Fallback search failed: {e}")
            return []

    def get_page_info(self, url_path: str, db: Session) -> Optional[PageContent]:
        """獲取特定頁面資訊"""
        return db.query(PageContent).filter(
            PageContent.url_path == url_path
        ).first()


# 全域 RAG 系統實例
rag_system = RAGSystem()
