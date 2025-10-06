# AI Website Generator - Feature Overview

## Core Features

### 1. AI-Powered Website Generation

The website generator uses LLM (GPT-4, Claude, etc.) to create professional single-page websites in under 30 seconds.

**Why LLM is Essential:**
- **Intelligent Design**: AI analyzes your business description and generates appropriate layouts, color schemes, and content structure
- **Style Adaptation**: Creates designs that match your industry and brand personality
- **Content Generation**: Writes compelling copy based on minimal input
- **Custom Styling**: Generates CSS that perfectly matches your vision

**Without LLM:** You would only get pre-made static templates with placeholder text.

**With LLM:** You get fully customized, content-rich websites tailored to your specific needs.

### 2. Image-Based Style Analysis (GPT-4 Vision)

Upload a reference image and AI will:
- Extract color palette
- Identify design style (modern, vintage, minimalist, etc.)
- Recommend fonts
- Detect mood and atmosphere
- Apply these insights to your website

**API Endpoint:** `POST /api/analyze-image`

**Example:**
```json
{
  "image_base64": "data:image/jpeg;base64,...",
  "description": "I like this coffee shop's aesthetic"
}
```

**Response:**
```json
{
  "colors": {
    "primary": "#8B4513",
    "secondary": "#DEB887",
    "accent": "#CD853F"
  },
  "style": "Warm and rustic",
  "mood": "Cozy and inviting",
  "fonts": {
    "heading": "Playfair Display",
    "body": "Lato"
  },
  "keywords": ["coffee", "rustic", "warm", "artisan"]
}
```

### 3. Text-Based Style Description

Describe your desired style in natural language:

```
"Create a website with a futuristic tech vibe, 
using dark backgrounds with neon accents. 
Think cyberpunk meets Silicon Valley."
```

The AI will interpret this and generate appropriate:
- Color schemes
- Typography choices
- Layout styles
- Visual elements

### 4. Incremental Website Updates

Don't like something? Update it without regenerating the entire website.

**API Endpoint:** `POST /api/update-website`

**Example:**
```json
{
  "site_id": "abc-123",
  "modifications": {
    "section": "hero",
    "new_title": "Transform Your Business with AI"
  },
  "instruction": "Change the main headline and make the primary color dark blue"
}
```

**Benefits:**
- Faster iterations
- Preserves existing content
- Targeted changes
- Cost-effective (fewer tokens used)

### 5. 25+ Template Styles

Pre-designed templates for various industries:
- Technology & SaaS
- Creative & Design
- Business & Consulting
- E-commerce
- Portfolio
- Restaurant & Hospitality
- Health & Wellness
- Education
- And more...

Each template is fully customizable through AI.

## Complete Workflow

```
1. Choose Style
   ├─ Select template
   ├─ Upload reference image (optional)
   └─ Describe desired style (optional)
   
2. Provide Information
   ├─ Company name
   ├─ Description
   ├─ Services
   └─ Contact info
   
3. AI Generation
   ├─ GPT-4 analyzes input
   ├─ Generates HTML + CSS
   └─ Creates preview

4. Preview & Edit
   ├─ View live preview
   ├─ Request changes via natural language
   └─ AI applies incremental updates
   
5. Download
   ├─ Get complete website package
   ├─ Includes HTML, CSS, assets
   └─ Ready to deploy
```

## API Endpoints

### Generation
- `POST /api/generate-website` - Generate new website
- `POST /api/analyze-image` - Analyze image style
- `POST /api/update-website` - Update existing website

### Access
- `GET /api/preview/{site_id}` - Preview generated website
- `GET /api/download/{site_id}` - Download website package

### Chat Assistant
- `POST /api/chat` - AI navigation assistant
- `POST /api/chat-preview` - Preview-specific chat

## LLM Provider Support

The system works with multiple LLM providers:

| Provider | Best For | Setup Required |
|----------|----------|----------------|
| OpenAI GPT-4 | Highest quality | API key |
| Anthropic Claude | Excellent reasoning | API key |
| Google Gemini | Free tier available | API key |
| Ollama | Local, privacy-focused | Local installation |

See [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md) for setup instructions.

## Why LLM is Critical

### Without LLM:
- Static templates only
- Manual customization required
- Generic placeholder content
- No style adaptation
- No image analysis
- No intelligent updates

### With LLM:
- Fully customized designs
- AI-generated content
- Intelligent color schemes
- Style extraction from images
- Natural language updates
- Context-aware modifications

## Technical Implementation

### Image Analysis Flow
```
User uploads image
    ↓
Frontend converts to base64
    ↓
API sends to GPT-4 Vision
    ↓
AI analyzes visual style
    ↓
Returns color palette + recommendations
    ↓
Applied to website generation
```

### Update Flow
```
User requests change
    ↓
Frontend sends instruction + site_id
    ↓
Backend loads current HTML
    ↓
AI applies targeted modifications
    ↓
Saves updated HTML
    ↓
User sees updated preview
```

## Cost Optimization

- **Generation**: ~4000 tokens per website
- **Image Analysis**: ~1000 tokens per image
- **Updates**: ~500-1500 tokens per update

**Estimated Costs (GPT-4):**
- Website generation: ~$0.20
- Image analysis: ~$0.05
- Update: ~$0.03

Using GPT-3.5-turbo reduces costs by 90%.

## Future Enhancements

- [ ] Multi-page website support
- [ ] Real-time collaborative editing
- [ ] A/B testing variants
- [ ] SEO optimization suggestions
- [ ] Accessibility compliance checking
- [ ] Mobile app preview
- [ ] Version history & rollback
- [ ] Template marketplace

## Getting Started

1. Set up environment variables (see [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md))
2. Start Docker containers: `docker-compose up -d`
3. Access generator: http://localhost:8000/generator
4. Upload reference image or describe your style
5. Fill in business information
6. Generate and preview
7. Request changes as needed
8. Download final package

---

For detailed API documentation, visit http://localhost:8001/docs
