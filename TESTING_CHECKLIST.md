# Testing Checklist

## Pre-Deployment Tests

### 1. Frontend Tests (Corporate Website)

#### Navigation
- [ ] Logo 點擊回首頁
- [ ] 所有導航連結正常 (首頁、作品集、技術棧、關於我們、聯絡我們、AI 生成器)
- [ ] 手機版選單展開/收合
- [ ] 滾動時導航列樣式變化

#### 首頁 (/corporate/index.html)
- [ ] Hero 區塊顯示正常
- [ ] 浮動元素動畫
- [ ] 服務卡片顯示
- [ ] 數據計數器動畫
- [ ] CTA 按鈕連結正確

#### 作品集 (/corporate/portfolio.html)
- [ ] 專案卡片顯示
- [ ] 篩選按鈕功能 (All, AI, Cloud, DevOps)
- [ ] 卡片淡入動畫

#### 技術棧 (/corporate/tech-stack.html)
- [ ] 技術分類顯示
- [ ] 技術項目完整
- [ ] 無 emoji 殘留

#### 關於我們 (/corporate/about.html)
- [ ] 團隊介紹顯示
- [ ] 公司文化展示
- [ ] 無 emoji 殘留

#### 聯絡我們 (/corporate/contact.html)
- [ ] 表單欄位正常
- [ ] 表單驗證
- [ ] 提交功能 (可以先測試前端驗證)

#### 彩蛋功能
- [ ] Logo hover 顯示委託資訊
- [ ] 鍵盤輸入 "aiinpocket" 觸發彩蛋
- [ ] Konami Code (↑↑↓↓←→←→BA)
- [ ] 彈窗關閉功能

#### Footer
- [ ] 動態年份顯示 (2025)
- [ ] 連結正常

### 2. Frontend Tests (AI Generator)

#### Generator UI (/generator/index.html)
- [ ] 步驟進度條顯示
- [ ] 模板選擇卡片
- [ ] 圖片上傳功能
  - [ ] 點擊上傳
  - [ ] 拖放上傳
  - [ ] 檔案大小驗證 (5MB)
  - [ ] 檔案類型驗證
  - [ ] 圖片預覽
- [ ] 表單輸入
  - [ ] 公司名稱
  - [ ] 描述
  - [ ] 服務項目動態新增
  - [ ] 聯絡資訊
- [ ] 生成按鈕
- [ ] 預覽顯示
- [ ] 下載按鈕

### 3. Backend API Tests

#### Health Check
```bash
curl http://localhost:8001/api/health
```
Expected: `{"status": "healthy", "timestamp": "..."}`

#### Image Analysis (GPT-4 Vision)
```bash
curl -X POST http://localhost:8001/api/analyze-image \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "base64_string", "description": "modern website"}'
```
Expected: Color palette, style, mood, fonts, keywords

#### Website Generation
```bash
curl -X POST http://localhost:8001/api/generate-website \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "modern-tech",
    "user_data": {
      "company_name": "Test Company",
      "description": "Test description"
    },
    "contact_email": "test@example.com"
  }'
```
Expected: site_id, preview_url, download_url

#### Website Update
```bash
curl -X POST http://localhost:8001/api/update-website \
  -H "Content-Type: application/json" \
  -d '{
    "site_id": "test-site-id",
    "modifications": {},
    "instruction": "Change primary color to blue"
  }'
```
Expected: Updated preview_url

#### AI Chat Navigation
```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "帶我去看作品集",
    "session_id": "test-session"
  }'
```
Expected: Reply + navigation action to /corporate/portfolio.html

### 4. Database Tests

#### Check Tables Created
```bash
docker-compose exec postgres psql -U aiinpocket -d aiinpocket -c "\dt"
```
Expected: users, projects, page_content tables

#### Check pgvector Extension
```bash
docker-compose exec postgres psql -U aiinpocket -d aiinpocket -c "\dx"
```
Expected: vector extension listed

#### Check RAG Indexed Pages
```bash
docker-compose exec postgres psql -U aiinpocket -d aiinpocket -c "SELECT url_path, title FROM page_content;"
```
Expected: 
- /index.html
- /corporate/index.html
- /corporate/portfolio.html
- /corporate/tech-stack.html
- /corporate/about.html
- /corporate/contact.html
- /generator/index.html

### 5. Dynamic RAG Tests

#### Add New Page
1. Create `frontend/corporate/test-page.html`:
```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <title>Test Page - AiInPocket</title>
    <meta name="description" content="This is a test page">
</head>
<body>
    <main>
        <h1>Test Page</h1>
        <p>This page should be automatically indexed.</p>
    </main>
</body>
</html>
```

2. Restart backend:
```bash
docker-compose restart backend
```

3. Check logs:
```bash
docker-compose logs backend | grep "test-page"
```
Expected: "[CREATE] Created index for: /corporate/test-page.html"

4. Test AI navigation:
```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "帶我去 test page", "session_id": "test"}'
```
Expected: Navigation to /corporate/test-page.html

5. Cleanup:
```bash
rm frontend/corporate/test-page.html
docker-compose restart backend
```

### 6. Static Website Generation Tests

#### Generate Website
1. Use generator UI to create a website
2. Download ZIP file
3. Extract and verify contents:
   - [ ] index.html (complete website)
   - [ ] ai-chat.js (optional AI chat)
   - [ ] README.md (instructions)
   - [ ] No database files
   - [ ] No backend code

4. Open index.html in browser:
   - [ ] Website displays correctly
   - [ ] All styles applied
   - [ ] Responsive design works
   - [ ] No broken links

### 7. Docker Tests

#### Volume Persistence
```bash
# Stop containers
docker-compose down

# Start again
docker-compose up -d

# Check data persists
docker-compose exec postgres psql -U aiinpocket -d aiinpocket -c "SELECT COUNT(*) FROM page_content;"
```
Expected: Same number of pages as before

#### Timezone
```bash
docker-compose exec backend date
docker-compose exec postgres date
```
Expected: Both show Asia/Taipei timezone

### 8. Performance Tests

#### Page Load Speed
- [ ] Corporate pages load < 2s
- [ ] Generator page loads < 2s
- [ ] API responses < 500ms

#### Memory Usage
```bash
docker stats --no-stream
```
Expected: All containers < 512MB

## Post-Deployment Checklist

- [ ] All tests pass
- [ ] No console errors in browser
- [ ] No emoji in any file
- [ ] Documentation is accurate
- [ ] .env.example is complete
- [ ] README is clear
- [ ] Git commit message is descriptive
- [ ] All files are committed

## Known Limitations

1. AI features require OpenAI API key (or alternative LLM)
2. Image analysis requires GPT-4 Vision access
3. Email delivery requires SMTP configuration
4. Generated websites are static (no backend needed for deployment)

## Success Criteria

✅ All frontend pages work without errors
✅ AI navigation finds all corporate pages dynamically
✅ Website generation creates valid static HTML
✅ Database auto-initializes on first run
✅ Docker volumes persist data
✅ No hardcoded page lists in RAG system
✅ Corporate folder can be safely removed for OSS deployment
