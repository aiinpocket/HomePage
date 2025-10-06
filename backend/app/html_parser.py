"""
HTML 內容解析器
從 HTML 檔案中提取標題、描述、內容等資訊
"""
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, List
import re


class HTMLParser:
    """HTML 解析器"""

    def __init__(self, frontend_path: str = "/app/frontend"):
        self.frontend_path = Path(frontend_path)

    def get_all_html_files(self) -> List[Path]:
        """獲取所有 HTML 檔案"""
        if not self.frontend_path.exists():
            print(f"[WARN] Frontend path not found: {self.frontend_path}")
            return []

        html_files = list(self.frontend_path.glob("*.html"))
        print(f"[INFO] Found {len(html_files)} HTML files")
        return html_files

    def parse_html_file(self, file_path: Path) -> Dict:
        """
        解析單個 HTML 檔案

        Returns:
            {
                'url_path': str,
                'title': str,
                'description': str,
                'content': str,
                'keywords': str
            }
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'lxml')

            # 提取 URL 路徑
            url_path = f"/{file_path.name}"

            # 提取標題
            title = ""
            if soup.title:
                title = soup.title.string.strip()
            elif soup.find('h1'):
                title = soup.find('h1').get_text().strip()

            # 提取描述（meta description）
            description = ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                description = meta_desc.get('content').strip()

            # 提取關鍵字
            keywords = ""
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords and meta_keywords.get('content'):
                keywords = meta_keywords.get('content').strip()

            # 提取主要內容
            content = self._extract_main_content(soup)

            return {
                'url_path': url_path,
                'title': title,
                'description': description,
                'content': content,
                'keywords': keywords
            }

        except Exception as e:
            print(f"[ERROR] Failed to parse {file_path}: {e}")
            return None

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        提取頁面主要內容（移除 script, style, nav 等）
        """
        # 移除不需要的標籤
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()

        # 提取 main 或 body 的文字
        main_content = soup.find('main') or soup.find('body')
        if not main_content:
            return ""

        # 獲取所有文字
        text = main_content.get_text(separator=' ', strip=True)

        # 清理多餘空白
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        # 限制長度（避免過長）
        max_length = 5000
        if len(text) > max_length:
            text = text[:max_length] + "..."

        return text

    def parse_all_pages(self) -> List[Dict]:
        """解析所有頁面"""
        html_files = self.get_all_html_files()
        results = []

        for file_path in html_files:
            parsed = self.parse_html_file(file_path)
            if parsed:
                results.append(parsed)
                print(f"[OK] Parsed: {parsed['url_path']} - {parsed['title']}")

        print(f"[INFO] Successfully parsed {len(results)} pages")
        return results


def test_parser():
    """測試解析器"""
    parser = HTMLParser()
    pages = parser.parse_all_pages()

    for page in pages:
        print("\n" + "="*50)
        print(f"URL: {page['url_path']}")
        print(f"Title: {page['title']}")
        print(f"Description: {page['description'][:100] if page['description'] else 'N/A'}")
        print(f"Content length: {len(page['content'])} chars")
        print(f"Keywords: {page['keywords']}")


if __name__ == "__main__":
    test_parser()
