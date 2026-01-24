# AiInPocket 官方網站

**公司官網**

https://aiinpocket.com

## 專案結構

```
HomePage/
├── frontend/              # 前端靜態網站
│   ├── index.html        # 入口頁面（重定向至官網）
│   ├── corporate/        # 公司官網
│   │   ├── index.html    # 首頁
│   │   ├── about.html    # 關於我們
│   │   ├── contact.html  # 聯絡我們
│   │   ├── portfolio.html # 作品集
│   │   ├── tech-stack.html # 技術棧
│   │   └── privacy.html  # 隱私政策
│   ├── shared/           # 共用資源
│   │   ├── css/          # 樣式表
│   │   └── js/           # JavaScript
│   ├── js/               # 頁面專用 JS
│   └── css/              # 頁面專用 CSS
└── README.md
```

## 快速開始

這是一個純靜態網站，只需將 `frontend/` 目錄部署到任何靜態網站伺服器即可。

### 本機測試

```bash
# 使用 Python 內建伺服器
cd frontend
python -m http.server 8080
# 訪問 http://localhost:8080

# 或使用 Node.js serve
npx serve frontend
```

### 部署

將 `frontend/` 目錄部署至：
- GitHub Pages
- Cloudflare Pages
- Vercel
- Netlify
- 或任何靜態網站伺服器

## 聯絡我們

- **Website**: https://aiinpocket.com
- **Email**: help@aiinpocket.com

---

**© 2025 AiInPocket. All rights reserved.**
