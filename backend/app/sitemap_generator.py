"""
Sitemap.xml 自動生成器
"""
from datetime import datetime
from pathlib import Path
from typing import List
from .config import settings
from .html_parser import HTMLParser


class SitemapGenerator:
    """Sitemap 生成器"""

    def __init__(self, site_url: str = None, frontend_path: str = None):
        self.site_url = site_url or settings.SITE_URL
        self.frontend_path = Path(frontend_path or settings.FRONTEND_PATH)

    def generate_sitemap(self) -> str:
        """
        生成 sitemap.xml 內容

        Returns:
            XML 字符串
        """
        parser = HTMLParser(str(self.frontend_path))
        html_files = parser.get_all_html_files()

        # 生成 URL 列表
        urls = []
        for file_path in html_files:
            # 使用相對於 frontend 的路徑
            try:
                relative_path = file_path.relative_to(self.frontend_path)
                url_path = f"/{relative_path.as_posix()}"
            except ValueError:
                url_path = f"/{file_path.name}"

            # 設定優先級
            priority = self._get_priority(url_path)

            # 設定更新頻率
            changefreq = self._get_changefreq(url_path)

            urls.append({
                'loc': f"{self.site_url}{url_path}",
                'lastmod': datetime.now().strftime('%Y-%m-%d'),
                'changefreq': changefreq,
                'priority': priority
            })

        # 生成 XML
        xml_content = self._build_xml(urls)
        return xml_content

    def _get_priority(self, url_path: str) -> str:
        """獲取頁面優先級 (支援子目錄路徑)"""
        # 根目錄首頁
        if url_path in ['/index.html', '/corporate/index.html']:
            return '1.0'
        # 生成器首頁
        elif url_path == '/generator/index.html':
            return '1.0'
        # 重要頁面
        elif any(page in url_path for page in ['portfolio', 'contact', 'generator']):
            return '0.9'
        # 一般頁面
        elif any(page in url_path for page in ['about', 'tech-stack']):
            return '0.8'
        else:
            return '0.7'

    def _get_changefreq(self, url_path: str) -> str:
        """獲取頁面更新頻率 (支援子目錄路徑)"""
        # 首頁和生成器更新頻繁
        if 'index.html' in url_path or 'generator' in url_path:
            return 'weekly'
        # 作品集和技術棧每月更新
        elif any(page in url_path for page in ['portfolio', 'tech-stack']):
            return 'monthly'
        # 其他頁面較少更新
        else:
            return 'yearly'

    def _build_xml(self, urls: List[dict]) -> str:
        """建立 XML 內容"""
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]

        for url in urls:
            xml_lines.extend([
                '  <url>',
                f'    <loc>{url["loc"]}</loc>',
                f'    <lastmod>{url["lastmod"]}</lastmod>',
                f'    <changefreq>{url["changefreq"]}</changefreq>',
                f'    <priority>{url["priority"]}</priority>',
                '  </url>'
            ])

        xml_lines.append('</urlset>')
        return '\n'.join(xml_lines)

    def save_sitemap(self, output_path: str = None):
        """
        保存 sitemap.xml 到檔案

        Args:
            output_path: 輸出路徑，預設為 frontend/sitemap.xml
        """
        if output_path is None:
            output_path = self.frontend_path / "sitemap.xml"
        else:
            output_path = Path(output_path)

        xml_content = self.generate_sitemap()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)

        print(f"[OK] Sitemap saved to: {output_path}")
        return str(output_path)


def generate_sitemap():
    """快速生成 sitemap"""
    generator = SitemapGenerator()
    return generator.save_sitemap()


if __name__ == "__main__":
    generate_sitemap()
