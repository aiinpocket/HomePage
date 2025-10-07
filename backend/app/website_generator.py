"""
AI 網站生成引擎
使用 GPT-4 根據使用者需求和模板風格生成完整網站
"""
import os
import json
from typing import Dict, Optional, List
from openai import OpenAI
from .config import settings
from .template_styles import get_template_by_id, TEMPLATE_STYLES
from .translation_service import translation_service


class WebsiteGenerator:
    """AI 網站生成器"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.base_system_prompt = """你是全球最頂尖的網頁設計大師，曾為 Apple、Stripe、Linear、Vercel 等頂級科技公司打造震撼人心的官網。你的作品多次獲得 Awwwards、CSS Design Awards 年度大獎。

## 核心使命
創造**視覺震撼、內容豐富、技術精湛、獨一無二**的一頁式網站，品質必須**遠超 WordPress 模板**，達到頂級設計工作室的水準。

## 創意原則（最重要）
**每個網站都必須是獨特的作品，不是套用模板**

1. **深入理解品牌**：根據公司名稱、服務內容、目標受眾，創造符合品牌個性的設計
2. **配色創新**：不要照抄參考配色，要根據品牌調性創造獨特的色彩方案
3. **佈局創意**：在遵循基本結構的前提下，創造獨特的視覺佈局和動線
4. **內容深度**：根據客戶資訊撰寫有深度、有溫度的文案，不要空洞或模板化
5. **視覺差異化**：即使是相同風格方向，也要創造視覺上的差異化
6. **細節用心**：在 hover 效果、動畫、裝飾元素上展現創意

**禁止規則**：
- 禁止照抄參考配色（必須調整或創造新配色）
- 禁止使用模板化的空洞文案（必須根據品牌撰寫）
- 禁止千篇一律的佈局（在基本結構上創新）
- 禁止相同的視覺元素（每個網站應有獨特的視覺語言）

## 設計標竿參考
- **Apple.com**: 超大留白、精緻字體排印、流暢動畫
- **Stripe.com**: 漸層魔法、玻璃擬態、專業配色
- **Linear.app**: 極簡主義、精準對齊、優雅過渡
- **Vercel.com**: 深色模式、科技感、微妙光影
- **Airbnb.com**: 溫暖色調、人性化、卡片設計

---

# 完整網站結構（8-10 個 Section）

## 1. 導航列 (Navigation Bar)
```css
必須實現:
- position: fixed; top: 0; z-index: 9999;
- 玻璃擬態: background: rgba(255,255,255,0.8); backdrop-filter: blur(20px) saturate(180%);
- 滾動時增加陰影: box-shadow: 0 4px 30px rgba(0,0,0,0.1);
- Logo + 導航連結（關於、服務、作品、聯絡）+ CTA 按鈕
- 平滑過渡: transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
- 手機版: 純 CSS 漢堡選單（使用 checkbox hack）

視覺要求:
- 高度: 70-80px (desktop), 60px (mobile)
- Logo 字體: 24-28px, 粗體 700-900
- 導航文字: 14-16px, 間距 30-40px
- CTA 按鈕: 漸層背景, 圓角 8-12px, padding: 10px 24px
- hover 效果: 文字顏色變化 + 底部出現 2px 下劃線
```

## 2. Hero Section（首屏震撼區）
```css
尺寸與佈局:
- height: 100vh; (完整視窗高度)
- display: flex; align-items: center; justify-content: center;
- text-align: center; (或 left 對齊搭配圖片)
- padding: 0 80px; (確保兩側留白)

背景效果（選其一，根據模板風格）:
選項 A - 複雜漸層:
  background: linear-gradient(135deg,
    rgba(99,102,241,0.1) 0%,
    rgba(168,85,247,0.1) 50%,
    rgba(236,72,153,0.1) 100%);

選項 B - 動態網格:
  background-image:
    linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px);
  background-size: 50px 50px;

選項 C - 光暈效果:
  background: radial-gradient(circle at 30% 20%,
    rgba(primary-color, 0.2) 0%,
    transparent 50%);

內容結構（必須全部包含）:
1. 主標題 (H1)
   - font-size: 72-96px (desktop), 40-48px (mobile)
   - font-weight: 900
   - line-height: 1.1
   - letter-spacing: -0.02em
   - 可選: 文字漸層效果
     background: linear-gradient(135deg, color1, color2);
     -webkit-background-clip: text;
     -webkit-text-fill-color: transparent;

2. 副標題 / 標語 (H2 或 P)
   - font-size: 24-32px (desktop), 18-24px (mobile)
   - font-weight: 400-500
   - opacity: 0.8
   - margin-top: 20px

3. 描述段落 (P)
   - font-size: 18-20px
   - line-height: 1.7
   - max-width: 600px; (限制寬度提升可讀性)
   - margin: 30px auto;

4. CTA 按鈕組（2-3 個按鈕）
   主按鈕 CSS:
   .hero-cta-primary {
     font-size: 18px;
     padding: 16px 40px;
     background: linear-gradient(135deg, color1, color2);
     color: white;
     border: none;
     border-radius: 12px;
     box-shadow: 0 10px 40px rgba(primary-color, 0.3);
     cursor: pointer;
     transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
   }
   .hero-cta-primary:hover {
     transform: translateY(-3px) scale(1.02);
     box-shadow: 0 15px 60px rgba(primary-color, 0.4);
   }

   次按鈕 CSS:
   .hero-cta-secondary {
     font-size: 18px;
     padding: 16px 40px;
     background: transparent;
     color: primary-color;
     border: 2px solid primary-color;
     border-radius: 12px;
     margin-left: 20px;
   }

5. 向下滾動提示（箭頭動畫）
   使用純 CSS 繪製:
   .scroll-indicator {
     position: absolute;
     bottom: 40px;
     left: 50%;
     transform: translateX(-50%);
     width: 30px;
     height: 50px;
     border: 2px solid rgba(0,0,0,0.2);
     border-radius: 25px;
   }
   .scroll-indicator::before {
     content: '';
     position: absolute;
     top: 10px;
     left: 50%;
     transform: translateX(-50%);
     width: 6px;
     height: 6px;
     background: rgba(0,0,0,0.4);
     border-radius: 50%;
     animation: scroll 2s infinite;
   }
   @keyframes scroll {
     0%, 20% { transform: translateX(-50%) translateY(0); opacity: 1; }
     100% { transform: translateX(-50%) translateY(20px); opacity: 0; }
   }
```

## 3. 📊 關於/介紹區 (About Section)
```css
佈局:
- 左右分欄 (60% 文字 + 40% 視覺元素)
- 或居中對齊純文字佈局
- padding: 120px 80px;
- background: linear-gradient(180deg, white 0%, #fafafa 100%);

內容必須包含:
1. Section 標題
   - font-size: 48-56px
   - font-weight: 700
   - margin-bottom: 30px
   - 可添加裝飾線:
     .section-title::before {
       content: '';
       display: block;
       width: 60px;
       height: 4px;
       background: linear-gradient(90deg, color1, color2);
       margin-bottom: 20px;
       border-radius: 2px;
     }

2. 詳細介紹文字 (2-4 段落)
   - font-size: 18px
   - line-height: 1.8
   - color: #374151
   - 每段至少 80-120 字
   - 使用具體內容，不要空洞描述

3. 統計數據展示 (Stats Cards)
   佈局: display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px;

   每個卡片包含:
   .stat-card {
     text-align: center;
     padding: 40px 30px;
     background: white;
     border-radius: 16px;
     box-shadow: 0 4px 20px rgba(0,0,0,0.08);
     transition: transform 0.3s ease;
   }
   .stat-card:hover {
     transform: translateY(-8px);
   }
   .stat-number {
     font-size: 56px;
     font-weight: 900;
     color: primary-color;
     line-height: 1;
   }
   .stat-label {
     font-size: 16px;
     color: #6b7280;
     margin-top: 10px;
   }

   範例數據:
   - "500+" 滿意客戶
   - "10 年" 專業經驗
   - "98%" 客戶滿意度
   - "24/7" 全天候服務
```

## 4. 💼 服務/功能展示區 (Services)
```css
佈局:
- display: grid;
- grid-template-columns: repeat(3, 1fr); (desktop)
- grid-template-columns: repeat(2, 1fr); (tablet)
- grid-template-columns: 1fr; (mobile)
- gap: 40px;
- padding: 120px 80px;

每個服務卡片必須包含:
.service-card {
  background: white;
  padding: 50px 40px;
  border-radius: 20px;
  border: 1px solid rgba(0,0,0,0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

/* 懸停時的背景光暈 */
.service-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, primary-color 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
}
.service-card:hover::before {
  opacity: 0.05;
}

.service-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 20px 60px rgba(0,0,0,0.12);
  border-color: primary-color;
}

卡片內容結構:
1. 圖示區域 (Icon)
   .service-icon {
     width: 80px;
     height: 80px;
     background: linear-gradient(135deg, color1, color2);
     border-radius: 16px;
     display: flex;
     align-items: center;
     justify-content: center;
     font-size: 36px;
     margin-bottom: 30px;
     box-shadow: 0 8px 24px rgba(primary-color, 0.25);
   }
   內容: 使用 Unicode 符號 (圖示或符號) 或 CSS 繪製圖形

2. 服務標題
   - font-size: 24-28px
   - font-weight: 700
   - margin-bottom: 15px

3. 服務描述
   - font-size: 16px
   - line-height: 1.7
   - color: #6b7280
   - 至少 60-80 字的詳細說明

4. 了解更多連結
   .service-link {
     display: inline-flex;
     align-items: center;
     color: primary-color;
     font-weight: 600;
     margin-top: 20px;
     transition: gap 0.3s ease;
   }
   .service-link:hover {
     gap: 8px; /* 箭頭向右移動效果 */
   }
   .service-link::after {
     content: '→';
     margin-left: 8px;
   }

內容要求:
- 至少 4-6 個服務項目
- 每個服務描述具體且專業
- 使用行業相關術語
```

## 5. 🖼️ 作品集/案例展示 (Portfolio)
```css
如果用戶提供了作品集，必須創建精美展示區:

佈局選項 A - 網格佈局:
.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  padding: 120px 80px;
}

佈局選項 B - Masonry 瀑布流效果:
.portfolio-grid {
  columns: 3;
  column-gap: 30px;
}
.portfolio-item {
  break-inside: avoid;
  margin-bottom: 30px;
}

每個作品項目:
.portfolio-item {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.portfolio-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  aspect-ratio: 4/3;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.portfolio-item:hover .portfolio-image {
  transform: scale(1.08);
}

/* 覆蓋層效果 */
.portfolio-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg,
    transparent 0%,
    rgba(0,0,0,0.3) 40%,
    rgba(0,0,0,0.9) 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 40px;
}

.portfolio-item:hover .portfolio-overlay {
  opacity: 1;
}

.portfolio-title {
  color: white;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 10px;
  transform: translateY(20px);
  transition: transform 0.4s ease;
}

.portfolio-item:hover .portfolio-title {
  transform: translateY(0);
}

.portfolio-description {
  color: rgba(255,255,255,0.9);
  font-size: 14px;
  line-height: 1.6;
  transform: translateY(20px);
  transition: transform 0.4s 0.1s ease;
}

.portfolio-item:hover .portfolio-description {
  transform: translateY(0);
}
```

## 6. 客戶見證 (Testimonials)
```css
必須添加此區塊以增加可信度:

.testimonials-section {
  padding: 120px 80px;
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
}

佈局:
.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

每個見證卡片:
.testimonial-card {
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.08);
  position: relative;
}

/* 引號裝飾 */
.testimonial-card::before {
  content: '"';
  position: absolute;
  top: -20px;
  left: 30px;
  font-size: 120px;
  color: rgba(primary-color, 0.1);
  font-family: Georgia, serif;
  line-height: 1;
}

.testimonial-stars {
  color: #fbbf24;
  font-size: 20px;
  margin-bottom: 20px;
}

.testimonial-text {
  font-size: 16px;
  line-height: 1.8;
  color: #374151;
  font-style: italic;
  margin-bottom: 30px;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 15px;
}

.author-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, color1, color2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 20px;
}

.author-info {
  flex: 1;
}

.author-name {
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 4px;
}

.author-role {
  font-size: 14px;
  color: #6b7280;
}

範例內容（自行創作類似的見證，不要用 Lorem Ipsum）:
- "與他們合作讓我們的業績成長了 300%，專業、高效、值得信賴！"
- "設計品質超出預期，客戶反饋極佳，強烈推薦給所有企業！"
- "從諮詢到交付都非常專業，是我們長期合作的最佳夥伴。"
```

## 7. 📈 特色/優勢展示 (Features/Why Choose Us)
```css
此區塊展示核心競爭力:

.features-section {
  padding: 120px 80px;
  background: white;
}

/* 交錯佈局 (Staggered Layout) */
.feature-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 80px;
  align-items: center;
  margin-bottom: 100px;
}

.feature-row:nth-child(even) .feature-content {
  order: 2;
}

.feature-visual {
  width: 100%;
  height: 400px;
  background: linear-gradient(135deg, color1, color2);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 80px;
  position: relative;
  overflow: hidden;
}

/* 添加裝飾性圖形 */
.feature-visual::before {
  content: '';
  position: absolute;
  width: 300px;
  height: 300px;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  top: -100px;
  right: -100px;
}

.feature-content h3 {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 20px;
}

.feature-content p {
  font-size: 18px;
  line-height: 1.8;
  color: #4b5563;
  margin-bottom: 30px;
}

.feature-benefits {
  list-style: none;
  padding: 0;
}

.feature-benefits li {
  padding-left: 30px;
  position: relative;
  margin-bottom: 15px;
  font-size: 16px;
  color: #374151;
}

.feature-benefits li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: primary-color;
  font-weight: 900;
  font-size: 18px;
}
```

## 8. 行動呼籲區 (CTA Section)
```css
位於 Footer 之前，最後一次轉化機會:

.cta-section {
  padding: 150px 80px;
  background: linear-gradient(135deg, primary-color 0%, secondary-color 100%);
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* 背景裝飾 */
.cta-section::before {
  content: '';
  position: absolute;
  width: 600px;
  height: 600px;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  top: -300px;
  right: -200px;
}

.cta-section::after {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  background: rgba(255,255,255,0.05);
  border-radius: 50%;
  bottom: -200px;
  left: -100px;
}

.cta-content {
  position: relative;
  z-index: 1;
}

.cta-title {
  font-size: 56px;
  font-weight: 900;
  color: white;
  margin-bottom: 25px;
  line-height: 1.2;
}

.cta-subtitle {
  font-size: 24px;
  color: rgba(255,255,255,0.9);
  margin-bottom: 50px;
}

.cta-button {
  font-size: 20px;
  padding: 20px 60px;
  background: white;
  color: primary-color;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  cursor: pointer;
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 15px 60px rgba(0,0,0,0.3);
}

.cta-note {
  font-size: 16px;
  color: rgba(255,255,255,0.8);
  margin-top: 30px;
}
```

## 9. Footer（豐富完整）
```css
.footer {
  background: #0a0e27; /* 深色背景 */
  color: rgba(255,255,255,0.8);
  padding: 80px 80px 40px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 60px;
  margin-bottom: 60px;
}

/* 公司資訊欄 */
.footer-brand {
  max-width: 350px;
}

.footer-logo {
  font-size: 28px;
  font-weight: 900;
  color: white;
  margin-bottom: 20px;
}

.footer-description {
  font-size: 14px;
  line-height: 1.8;
  margin-bottom: 30px;
}

.footer-social {
  display: flex;
  gap: 15px;
}

.social-icon {
  width: 40px;
  height: 40px;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.social-icon:hover {
  background: primary-color;
  transform: translateY(-3px);
}

/* 快速連結欄 */
.footer-links h4 {
  color: white;
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 20px;
}

.footer-links ul {
  list-style: none;
  padding: 0;
}

.footer-links li {
  margin-bottom: 12px;
}

.footer-links a {
  color: rgba(255,255,255,0.7);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s ease;
  display: inline-block;
}

.footer-links a:hover {
  color: white;
  transform: translateX(5px);
}

/* 版權區 */
.footer-bottom {
  padding-top: 30px;
  border-top: 1px solid rgba(255,255,255,0.1);
  text-align: center;
  font-size: 14px;
  color: rgba(255,255,255,0.5);
}
```

---

# 全局 CSS 設計系統

## CSS Variables（必須在 :root 定義）
```css
:root {
  /* 主色系 */
  --primary: [從模板獲取];
  --secondary: [從模板獲取];
  --accent: [從模板獲取];

  /* 中性色 */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;

  /* 語義色 */
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
  --info: #3b82f6;

  /* 字體 */
  --font-heading: [從模板獲取], -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-body: [從模板獲取], -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

  /* 間距 */
  --spacing-xs: 8px;
  --spacing-sm: 16px;
  --spacing-md: 24px;
  --spacing-lg: 40px;
  --spacing-xl: 64px;
  --spacing-2xl: 96px;
  --spacing-3xl: 128px;

  /* 陰影 */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 40px rgba(0,0,0,0.12);
  --shadow-xl: 0 20px 60px rgba(0,0,0,0.15);

  /* 圓角 */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;

  /* 過渡 */
  --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
```

## 基礎樣式重置
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
  font-size: 16px;
}

body {
  font-family: var(--font-body);
  color: var(--gray-900);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

a {
  text-decoration: none;
  color: inherit;
  transition: var(--transition-base);
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}

button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  outline: none;
}

section {
  position: relative;
  overflow: hidden;
}
```

## 通用工具類
```css
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 80px;
}

@media (max-width: 1199px) {
  .container {
    padding: 0 40px;
  }
}

@media (max-width: 767px) {
  .container {
    padding: 0 20px;
  }
}

.section-title {
  font-size: 48px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 60px;
}

@media (max-width: 767px) {
  .section-title {
    font-size: 32px;
    margin-bottom: 40px;
  }
}
```

---

# 響應式設計（嚴格執行）

## 斷點策略
```css
/* Desktop First Approach */

/* Desktop: 1200px+ */
預設樣式

/* Tablet: 768px - 1199px */
@media (max-width: 1199px) {
  - Font sizes 減少 15-20%
  - Padding/Margin 減少 25-30%
  - Grid columns 從 3 欄改為 2 欄
  - Hero 高度從 100vh 改為 80vh
}

/* Mobile: < 768px */
@media (max-width: 767px) {
  - Font sizes 減少 30-40%
  - Padding/Margin 減少 40-50%
  - 所有 Grid 改為單欄
  - Hero 高度從 100vh 改為 auto（min-height: 100vh）
  - 導航列顯示漢堡選單
  - 隱藏裝飾性元素
  - 按鈕改為 full-width
}
```

## 手機版導航選單（純 CSS 實現）
```css
.hamburger {
  display: none;
  flex-direction: column;
  gap: 6px;
  cursor: pointer;
}

.hamburger span {
  width: 25px;
  height: 3px;
  background: currentColor;
  border-radius: 3px;
  transition: var(--transition-base);
}

.nav-checkbox {
  display: none;
}

@media (max-width: 767px) {
  .hamburger {
    display: flex;
  }

  .nav-links {
    position: fixed;
    top: 70px;
    left: 0;
    width: 100%;
    height: calc(100vh - 70px);
    background: white;
    flex-direction: column;
    padding: 40px;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .nav-checkbox:checked ~ .nav-links {
    transform: translateX(0);
  }

  .nav-checkbox:checked ~ .hamburger span:nth-child(1) {
    transform: rotate(45deg) translate(8px, 8px);
  }

  .nav-checkbox:checked ~ .hamburger span:nth-child(2) {
    opacity: 0;
  }

  .nav-checkbox:checked ~ .hamburger span:nth-child(3) {
    transform: rotate(-45deg) translate(7px, -6px);
  }
}
```

---

# 絕對禁止事項

**禁止使用 Lorem Ipsum** - 所有內容必須根據用戶資料創作真實、專業的文案
**禁止空洞描述** - 每個 section 必須有實質內容（至少 100 字）
**禁止單調背景** - 必須使用漸層、圖案或層次效果
**禁止忽略 hover 效果** - 所有互動元素必須有精緻的 hover 動畫
**禁止外部資源** - 所有 CSS 必須內嵌，不可引用外部檔案
**禁止使用 JavaScript** - 除了預留的 `<div id="ai-chat-container"></div>`
**禁止忽略響應式** - 必須完美支持 Desktop / Tablet / Mobile
**禁止小字體** - body 最小 16px，標題至少 48px (desktop)
**禁止擁擠排版** - section 間距至少 100px，內容要有呼吸感

---

# 品質檢查清單

在生成前，確保每一項都達成：

Hero section 達 100vh，視覺震撼
至少 8-10 個完整 section
每個 section 內容豐富（150+ 字或 5+ 視覺元素）
所有按鈕、卡片、連結都有精緻 hover 效果
完整的響應式設計（三種斷點都完美）
配色和諧，漸層運用精準
字體層次分明（至少 6 種字體大小）
充足的留白和呼吸感（section padding 80-120px）
Footer 資訊完整且結構化（4 欄位）
整體視覺品質**遠超 WordPress 模板**
包含客戶見證區塊（增加可信度）
包含統計數據展示（增加說服力）
包含 CTA 行動呼籲區（提升轉化）
所有圖片使用正確的佔位符格式
預留 `<div id="ai-chat-container"></div>` 在 </body> 之前

---

# 最終目標

**創造一個讓客戶驚嘆的網站**，品質必須達到：
- 視覺設計：媲美 Awwwards 獲獎作品
- 內容深度：超越 WordPress 高級主題
- 技術品質：符合 Web 開發最佳實踐
- 用戶體驗：流暢、直覺、令人愉悅

請全力以赴，創作一個「年度最佳設計」級別的作品！
"""

    async def generate_website(
        self,
        template_id: str,
        user_data: Dict,
        custom_style: Optional[Dict] = None,
        languages: List[str] = ["zh-TW", "en", "ja"],
        image_keys: Optional[List[str]] = None
    ) -> str:
        """
        生成完整網站 HTML（支援多語言和圖片佔位符）

        Args:
            template_id: 模板 ID
            user_data: 使用者提供的資料 (公司名稱、描述、聯絡方式等)
            custom_style: 自訂風格 (如果使用者上傳圖片或文字描述)
            languages: 支援的語言列表
            image_keys: 圖片鍵值列表（用於生成佔位符）

        Returns:
            完整的 HTML 字串（包含圖片佔位符如 {{ logo }}, {{ portfolio1 }} 等）
        """
        # 獲取模板資訊（如果模板不存在，使用通用模板）
        template = get_template_by_id(template_id)
        if not template:
            print(f"[WARN] Template {template_id} not found, using generic template")
            # 創建一個通用模板
            template = {
                "id": template_id,
                "name": template_id.replace('-', ' ').title(),
                "category": "generic",
                "description": f"Generic template for {template_id}",
                "colors": {
                    "primary": "#667eea",
                    "secondary": "#764ba2",
                    "accent": "#f093fb",
                    "background": "#0a0e27",
                    "text": "#ffffff"
                },
                "fonts": {
                    "heading": "Arial, sans-serif",
                    "body": "Helvetica, sans-serif"
                },
                "style_keywords": ["modern", "professional", "clean"]
            }

        # 建立 prompt
        prompt = self._build_generation_prompt(template, user_data, custom_style)

        # 使用 GPT-4 生成
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",  # 使用 GPT-4 Turbo (最新版本，支持128K上下文)
                messages=[
                    {"role": "system", "content": self.base_system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.85,  # 提高創造力，讓每個網站更獨特
                max_tokens=4096  # gpt-4-turbo 最大支援 4096 completion tokens
            )

            html_content = response.choices[0].message.content

            # 後處理：確保 HTML 完整性
            html_content = self._post_process_html(html_content, user_data)

            return html_content

        except Exception as e:
            print(f"[ERROR] Failed to generate website: {e}")
            # 返回備用模板
            return self._generate_fallback_template(template, user_data)

    def _build_generation_prompt(
        self,
        template: Dict,
        user_data: Dict,
        custom_style: Optional[Dict] = None
    ) -> str:
        """建立生成 prompt"""

        company_name = user_data.get("company_name", "My Company")
        tagline = user_data.get("tagline", "")
        description = user_data.get("description", "")
        services = user_data.get("services", [])
        contact_email = user_data.get("contact_email", "contact@example.com")
        contact_phone = user_data.get("contact_phone", "")
        portfolio_items = user_data.get("portfolio", [])

        prompt = f"""# 網站生成任務

請為以下客戶打造一個**獨一無二**的專業、現代化的單頁式網站 (Single Page Website)。

## 客戶資訊分析

### 品牌識別
- **公司/品牌名稱**: {company_name}
- **品牌標語**: {tagline if tagline else '請根據公司性質創作一句簡潔有力、符合品牌調性的標語'}
- **公司介紹**: {description if description else '請深入分析公司名稱和服務內容，撰寫 2-3 句有深度、有溫度的公司介紹'}

### 聯絡方式
- **Email**: {contact_email}
- **電話**: {contact_phone if contact_phone else '不提供'}

### 設計策略（請深入思考）
在開始設計前，請先分析：
1. **品牌個性**：從公司名稱和服務內容，推測品牌的個性特質（專業/親切/創新/傳統等）
2. **目標受眾**：這個品牌最可能服務的客戶類型是什麼？
3. **配色靈感**：根據品牌個性和目標受眾，什麼樣的配色最能傳達品牌價值？
4. **視覺風格**：應該使用什麼樣的視覺語言來吸引目標受眾？
5. **內容調性**：文案應該是正式專業、還是輕鬆親切？

**然後根據以上分析，創造一個完全獨特的設計方案。**

"""

        # 加入服務列表
        if services:
            prompt += f"### 核心服務/產品\n"
            for i, service in enumerate(services, 1):
                prompt += f"{i}. **{service}**\n"
            prompt += "\n"

        # 加入作品集
        if portfolio_items:
            prompt += f"### 作品集/案例展示\n"
            for i, item in enumerate(portfolio_items, 1):
                prompt += f"{i}. **{item.get('title', f'專案 {i}')}**\n"
                if item.get('description'):
                    prompt += f"   - 描述: {item['description']}\n"
                if item.get('image'):
                    prompt += f"   - 圖片: `{item['image']}`\n"
            prompt += "\n"

        # 加入外部連結
        external_links = user_data.get("external_links", [])
        if external_links:
            prompt += f"### 社交媒體與外部連結\n"
            prompt += "請在網站中適當位置（例如 Header、Footer 或聯絡區塊）加入以下社交媒體連結圖示：\n\n"
            for link in external_links:
                link_name = link.get('name', 'External Link')
                link_url = link.get('url', '#')
                prompt += f"- **{link_name}**: {link_url}\n"
            prompt += "\n請使用適當的圖示（可用 SVG 或 emoji）並確保連結在新視窗開啟（target=\"_blank\" rel=\"noopener noreferrer\"）\n\n"

        # 加入風格指引
        if custom_style or template.get('id') == 'custom':
            prompt += f"## 客製化風格要求\n\n"
            if custom_style:
                prompt += f"{custom_style.get('description', '')}\n\n"
                if custom_style.get('colors'):
                    prompt += f"**特殊配色**: {custom_style['colors']}\n\n"
            else:
                prompt += "請根據品牌名稱和服務內容，創造一個獨特、專業且符合品牌調性的設計風格。\n\n"

            prompt += """請自由發揮創意，設計一個：
- **視覺風格**: 現代、專業、引人入勝
- **色彩配置**: 和諧、有層次、符合品牌調性
- **字體系統**: 清晰易讀、層次分明
- **整體氛圍**: 專業、可信、令人印象深刻

"""
        elif template.get('colors') and template.get('fonts'):
            prompt += f"""## 設計風格指南

### 風格定位
- **風格方向**: {template['name']} ({template['id']})
- **設計理念**: {template['description']}
- **風格關鍵字**: {', '.join(template.get('style_keywords', []))}
- **目標氛圍**: 專業、現代、引人入勝

### 配色參考（請根據品牌調性自由發揮，創造獨特配色）
以下配色僅供參考，請根據客戶的品牌名稱、服務內容、目標受眾，創造更合適的配色方案：

參考色系：
- 主色調參考: {template['colors']['primary']} (可調整色相、飽和度、明度)
- 次要色參考: {template['colors']['secondary']} (可調整或選擇互補色)
- 強調色參考: {template['colors']['accent']} (可選擇對比色或漸層)
- 背景色參考: {template['colors']['background']} (可調整深淺或加入紋理)
- 文字色參考: {template['colors']['text']} (確保對比度符合 WCAG 標準)

**重要提示**：
- 請勿照抄參考配色，要根據品牌調性創造獨特的配色方案
- 可以使用漸層、陰影、透明度來豐富視覺層次
- 確保配色和諧、符合品牌個性
- 每個網站都應該有獨特的視覺識別

### 字體系統（請選擇最適合的字體）
- **標題字體建議**: {template['fonts']['heading']} (或其他更適合品牌的字體)
- **內文字體建議**: {template['fonts']['body']} (或其他更易讀的字體)
- 可以根據品牌調性選擇更合適的字體組合

"""

        prompt += """
## 網站結構規範

### 必要區塊 (按順序)

1. **導航列 (Navigation Bar)**
   - 固定於頂部 (position: fixed)
   - 包含品牌 Logo/名稱
   - 導航連結 (關於、服務、作品集、聯絡)
   - 玻璃擬態效果 (backdrop-filter: blur)

2. **Hero Section (首屏)**
   - 高度: 100vh 或至少 80vh
   - 包含元素:
     * 主標題 (公司名稱，超大字體)
     * 副標題 (品牌標語，吸引人)
     * 主要 CTA 按鈕 (「立即聯繫」「了解更多」等)
   - 背景: 漸層或動態效果
   - 視覺重點: 震撼、吸睛

3. **關於/服務展示區**
   - 公司介紹段落
   - 服務列表以精美卡片呈現
   - 每個服務: Icon + 標題 + 簡介
   - Grid 或 Flexbox 佈局
   - 懸停時卡片上浮效果

4. **作品集區塊** (如有提供)
   - 展示作品/案例
   - 圖片使用 `<img src="{{ portfolio0 }}" alt="...">` 格式
   - object-fit: cover 確保比例
   - 懸停時放大或顯示詳情

5. **特色/優勢區塊**
   - 3-4 個核心優勢
   - 數據化呈現（如適用）
   - 簡潔有力的文案

6. **Footer (頁尾)**
   - 聯絡資訊 (Email, 電話)
   - 版權宣告
   - 社交媒體連結（可選）
   - 深色背景，與主體區分

### 特殊整合點
- 在 `</body>` 結束前加入: `<div id="ai-chat-container"></div>`

## 品質檢查清單

### 視覺設計
- [ ] 配色和諧，符合品牌調性
- [ ] 排版精緻，視覺層次清晰
- [ ] 適當留白，不擁擠
- [ ] 動畫流暢，不過度

### 響應式設計
- [ ] Desktop (1200px+): 多欄佈局，內容豐富
- [ ] Tablet (768-1199px): 適當調整，維持美感
- [ ] Mobile (<768px): 單欄堆疊，觸控友善

### 技術實現
- [ ] 純 HTML + 內嵌 CSS
- [ ] 語義化標籤
- [ ] 無障礙優化
- [ ] 載入性能佳

---

**請直接輸出完整的 HTML 程式碼，不要包含任何解釋或註解。從 `<!DOCTYPE html>` 開始，到 `</html>` 結束。**
"""

        return prompt

    def _post_process_html(self, html: str, user_data: Dict) -> str:
        """後處理 HTML，確保完整性"""

        # 移除 markdown 程式碼區塊標記（如果有）
        html = html.replace("```html", "").replace("```", "")

        # 確保有 <!DOCTYPE html>
        if not html.strip().startswith("<!DOCTYPE"):
            html = "<!DOCTYPE html>\n" + html

        # 確保有 AI 聊天機器人容器
        if "ai-chat-container" not in html:
            # 在 </body> 前加入
            html = html.replace(
                "</body>",
                '<div id="ai-chat-container"></div>\n</body>'
            )

        # 確保有 meta viewport
        if "viewport" not in html:
            html = html.replace(
                "<head>",
                '<head>\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
            )

        return html

    def _generate_fallback_template(self, template: Dict, user_data: Dict) -> str:
        """生成備用模板（當 API 失敗時）"""

        company_name = user_data.get("company_name", "My Company")
        tagline = user_data.get("tagline", "Welcome to our website")
        contact_email = user_data.get("contact_email", "contact@example.com")

        # 處理客製化模板（colors 可能是 None）
        colors = template.get("colors") if template.get("colors") else {}
        primary = colors.get("primary", "#0077BE") if colors else "#0077BE"
        secondary = colors.get("secondary", "#FF6B35") if colors else "#FF6B35"
        background = colors.get("background", "#FFFFFF") if colors else "#FFFFFF"
        text_color = colors.get("text", "#333333") if colors else "#333333"

        return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: {text_color};
            background: {background};
        }}
        nav {{
            background: {primary};
            color: white;
            padding: 1rem 5%;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }}
        .hero {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 6rem 5% 3rem;
            background: linear-gradient(135deg, {primary}, {secondary});
            color: white;
        }}
        .hero h1 {{ font-size: 3rem; margin-bottom: 1rem; }}
        .hero p {{ font-size: 1.3rem; margin-bottom: 2rem; }}
        .btn {{
            display: inline-block;
            padding: 1rem 2rem;
            background: {secondary};
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: transform 0.3s;
        }}
        .btn:hover {{ transform: translateY(-3px); }}
        footer {{
            background: {primary};
            color: white;
            text-align: center;
            padding: 2rem 5%;
        }}
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <nav>
        <h1>{company_name}</h1>
    </nav>
    <section class="hero">
        <div>
            <h1>{company_name}</h1>
            <p>{tagline}</p>
            <a href="#contact" class="btn">聯絡我們</a>
        </div>
    </section>
    <footer id="contact">
        <p>© 2025 {company_name}. All rights reserved.</p>
        <p>Email: {contact_email}</p>
    </footer>
    <div id="ai-chat-container"></div>
</body>
</html>"""

    async def analyze_image_style(self, image_base64: str, description: str = "") -> Dict:
        """
        使用 GPT-4 Vision 分析圖片風格

        Args:
            image_base64: Base64 編碼的圖片
            description: 使用者文字描述

        Returns:
            風格分析結果 (配色、字體建議等)
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized")

        try:
            messages = [
                {
                    "role": "system",
                    "content": "你是一個專業的視覺設計師。分析圖片的視覺風格，提取配色方案、設計風格、氛圍等資訊。"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""請分析這張圖片的視覺風格，並提供網站設計建議。

{f'使用者描述：{description}' if description else ''}

請以 JSON 格式返回：
{{
    "colors": {{
        "primary": "主色 HEX 碼",
        "secondary": "次要色 HEX 碼",
        "accent": "強調色 HEX 碼",
        "background": "背景色 HEX 碼",
        "text": "文字色 HEX 碼"
    }},
    "style": "風格描述（現代、復古、極簡等）",
    "mood": "氛圍描述（溫暖、冷靜、活力等）",
    "fonts": {{
        "heading": "建議的標題字體",
        "body": "建議的內文字體"
    }},
    "keywords": ["關鍵字1", "關鍵字2", "關鍵字3"]
}}"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]

            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=messages,
                max_tokens=1000
            )

            result_text = response.choices[0].message.content

            # 解析 JSON
            import re
            json_match = re.search(r'\{[\s\S]*\}', result_text)
            if json_match:
                style_data = json.loads(json_match.group())
                return style_data
            else:
                raise ValueError("Failed to parse style data from response")

        except Exception as e:
            print(f"[ERROR] Failed to analyze image: {e}")
            # 返回預設風格
            return {
                "colors": {
                    "primary": "#0077BE",
                    "secondary": "#FF6B35",
                    "accent": "#FFD93D",
                    "background": "#FFFFFF",
                    "text": "#333333"
                },
                "style": "現代簡約",
                "mood": "專業友善",
                "fonts": {
                    "heading": "Arial, sans-serif",
                    "body": "Helvetica, sans-serif"
                },
                "keywords": ["現代", "簡潔", "專業"]
            }

    async def update_website(
        self,
        current_html: str,
        instruction: str,
        modifications: Dict
    ) -> str:
        """
        更新現有網站 (增量更新而非完全重新生成)

        Args:
            current_html: 當前的 HTML 內容
            instruction: 使用者的修改指令 (自然語言)
            modifications: 結構化的修改資料

        Returns:
            更新後的 HTML 內容
        """
        if not self.client:
            raise ValueError("OpenAI client not initialized")

        try:
            prompt = f"""你是一個專業的網頁設計師。請根據使用者的指令更新以下 HTML。

**使用者指令：**
{instruction}

**結構化修改資料：**
{json.dumps(modifications, ensure_ascii=False, indent=2)}

**當前 HTML：**
```html
{current_html}
```

**重要要求：**
1. 只修改必要的部分，保留其他內容不變
2. 保持 HTML 結構完整性
3. 確保修改後的網站仍然美觀且響應式
4. 如果修改顏色，要確保配色協調
5. 如果修改文字，要保持語氣和風格一致
6. 返回完整的 HTML 檔案

請直接返回修改後的完整 HTML，不要包含任何解釋或註解。"""

            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.base_system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # 降低溫度以確保一致性
                max_tokens=4000
            )

            updated_html = response.choices[0].message.content

            # 後處理
            updated_html = self._post_process_html(updated_html, {})

            return updated_html

        except Exception as e:
            print(f"[ERROR] Failed to update website: {e}")
            raise


# 全域生成器實例
website_generator = WebsiteGenerator()
