# Dynamic AI Navigation System

## Overview

The AI navigation assistant automatically discovers and indexes all website pages without hardcoded configuration. When you add new pages to the `frontend/corporate/` directory, the system will automatically:

1. Discover the new HTML files on startup
2. Parse content, titles, and descriptions
3. Create vector embeddings for semantic search
4. Enable AI-guided navigation to new pages

**No code changes required when adding new pages!**

## How It Works

### 1. Automatic Page Discovery

The `HTMLParser` recursively scans all subdirectories in `frontend/`:

```python
# backend/app/html_parser.py
def get_all_html_files(self) -> List[Path]:
    # Uses rglob to recursively find all .html files
    html_files = list(self.frontend_path.rglob("*.html"))

    # Excludes: node_modules, dist, build, .git, samples
    # Includes: corporate/, generator/, and all subdirectories
```

**Discovered Paths:**
```
/index.html                    # Root landing page
/corporate/index.html          # Corporate homepage
/corporate/portfolio.html      # Your portfolio
/corporate/tech-stack.html     # Your tech stack
/corporate/about.html          # About page
/corporate/contact.html        # Contact page
/generator/index.html          # AI generator
```

### 2. Content Extraction

For each HTML file, the system extracts:

- **Title**: From `<title>` tag or `<h1>`
- **Description**: From `<meta name="description">`
- **Keywords**: From `<meta name="keywords">`
- **Main Content**: All text from `<main>` or `<body>` (excluding nav, footer, scripts)

Example extracted data:
```python
{
    'url_path': '/corporate/portfolio.html',
    'title': '作品集 - AiInPocket',
    'description': 'AiInPocket 過往專案案例展示',
    'content': 'AI 智能客服系統 為企業打造...',
    'keywords': 'AI, portfolio, projects'
}
```

### 3. Vector Embeddings & RAG

The system creates semantic embeddings using OpenAI's `text-embedding-ada-002`:

```python
# Combines title + description + content
text = f"{title} {description} {content}"

# Creates 1536-dimensional vector
embedding = openai.embeddings.create(
    model="text-embedding-ada-002",
    input=text
)

# Stores in PostgreSQL with pgvector
```

**Storage in Database:**
```sql
CREATE TABLE page_content (
    id SERIAL PRIMARY KEY,
    url_path VARCHAR(255) UNIQUE,
    title VARCHAR(500),
    description TEXT,
    content TEXT,
    keywords TEXT,
    embedding vector(1536)  -- pgvector extension
);
```

### 4. Semantic Search

When a user asks a question, the AI finds the most relevant page:

```python
# User: "我想看你們的作品"
query_embedding = create_embedding("我想看你們的作品")

# pgvector cosine similarity search
results = db.query(PageContent).order_by(
    PageContent.embedding.cosine_distance(query_embedding)
).limit(3).all()

# Returns: /corporate/portfolio.html (highest similarity)
```

### 5. AI-Guided Navigation

The AI assistant then:
1. Responds with context about the page
2. Triggers navigation action to the page

```json
{
  "reply": "我找到了相關的頁面：作品集，讓我帶你過去看看！",
  "action": {
    "type": "navigate",
    "target": "/corporate/portfolio.html"
  }
}
```

## Initialization Flow

```
Server Startup
    ↓
Initialize Database
    ↓
HTMLParser scans frontend/
    ├─ corporate/*.html  ✓
    ├─ generator/*.html  ✓
    └─ samples/*.html    ✗ (excluded)
    ↓
For each HTML file:
    ├─ Extract title, desc, content
    ├─ Create embedding vector
    └─ Store in PostgreSQL
    ↓
RAG System Ready
    ↓
AI can navigate to ANY page
```

## Adding New Pages

### Example: Adding a Blog

1. **Create the HTML file:**
```bash
# Create new page
touch frontend/corporate/blog.html
```

2. **Add standard metadata:**
```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>部落格 - AiInPocket</title>
    <meta name="description" content="AiInPocket 技術文章與產業見解">
    <meta name="keywords" content="blog, AI, technology, insights">
    <!-- rest of head -->
</head>
<body>
    <main>
        <h1>技術部落格</h1>
        <p>分享 AI 與雲端技術的最新見解...</p>
        <!-- content -->
    </main>
</body>
</html>
```

3. **Restart the server:**
```bash
docker-compose restart backend
```

4. **Automatic indexing:**
```
[INFO] Found 8 HTML files (excluded 2 files)
[OK] Parsed: /corporate/blog.html - 部落格 - AiInPocket
[CREATE] Created index for: /corporate/blog.html
[RAG] Indexed 8/8 pages successfully
```

5. **Test navigation:**
```
User: "帶我去看部落格"
AI: "我找到了相關的頁面：部落格，讓我帶你過去看看！"
Action: Navigate to /corporate/blog.html
```

**That's it! No code changes needed.**

## Architecture Components

### HTMLParser (html_parser.py)
- Recursively scans `frontend/` directory
- Parses HTML content
- Extracts metadata
- Excludes unwanted directories

### RAGSystem (rag_system.py)
- Creates embeddings via OpenAI API
- Stores in PostgreSQL with pgvector
- Performs semantic similarity search
- Fallback to keyword search if no API

### AI Handler (ai_handler.py)
- Receives user queries
- Searches RAG system for relevant pages
- Generates natural language responses
- Triggers navigation actions

### Database (models.py)
- `PageContent` model with pgvector
- Automatic migration on startup
- Persistent semantic index

## Fallback Mode

If OpenAI API is not available, the system uses keyword-based search:

```python
# Keyword matching (without embeddings)
results = db.query(PageContent).filter(
    (PageContent.title.ilike(f"%{query}%")) |
    (PageContent.description.ilike(f"%{query}%")) |
    (PageContent.content.ilike(f"%{query}%"))
).limit(3).all()
```

This ensures the AI assistant works even without API keys.

## Monitoring & Debugging

### Check indexed pages:
```bash
docker-compose exec backend python -c "
from app.rag_system import rag_system
from app.database import SessionLocal

db = SessionLocal()
pages = db.query(PageContent).all()
for page in pages:
    print(f'{page.url_path} - {page.title}')
"
```

### Re-index pages:
```bash
docker-compose exec backend python -c "
from app.rag_system import rag_system
count = rag_system.index_all_pages()
print(f'Indexed {count} pages')
"
```

### Test search:
```bash
docker-compose exec backend python -c "
from app.rag_system import rag_system
from app.database import SessionLocal

db = SessionLocal()
results = rag_system.search_similar_pages('作品集', db, limit=3)
for r in results:
    print(f'{r.url_path} - {r.title}')
"
```

## Performance Considerations

- **Embedding Cost**: ~$0.0001 per page (one-time)
- **Search Speed**: <50ms with pgvector index
- **Memory**: ~6KB per page (embedding)
- **Re-indexing**: Only on server restart or manual trigger

## Best Practices

1. **Use semantic HTML** - Clear `<title>`, `<meta description>`, `<h1>`
2. **Add keywords** - `<meta name="keywords">` helps fallback search
3. **Meaningful content** - AI learns from actual text, not Lorem Ipsum
4. **Logical structure** - Use `<main>`, `<section>`, `<article>` tags
5. **Exclude samples** - Put example/demo files in `samples/` directory

## Security Notes

- RAG system only indexes files in `frontend/` directory
- Sensitive directories (`.git`, `node_modules`) are automatically excluded
- Generated sites in `generated_sites/` are not indexed
- No user input is stored in embeddings

---

**Summary:** The AI navigation system is fully dynamic. Just add HTML files to `frontend/corporate/` and restart the server. The AI will automatically discover, index, and navigate to your new pages without any code changes!
