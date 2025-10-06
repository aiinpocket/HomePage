# AI Website Generator

A full-stack web application that generates professional single-page websites using AI technology in under 30 seconds.

**Why AI/LLM is Essential:** Unlike traditional website builders with static templates, this system uses Large Language Models (GPT-4, Claude, etc.) to create fully customized, content-rich websites. The AI analyzes your business description, extracts styles from reference images, and generates tailored designs with appropriate color schemes, layouts, and compelling copy.

## Key Features

- **AI-Powered Generation** - LLM creates custom websites, not just templates
- **Image Style Analysis** - Upload reference images, AI extracts color palettes and design styles (GPT-4 Vision)
- **Incremental Updates** - Modify websites with natural language commands without full regeneration
- **25+ Template Styles** - Starting points across various industries
- **Multi-LLM Support** - Works with OpenAI, Claude, Gemini, or local models via Ollama
- **Real-time Preview & Download** - See changes instantly
- **Docker Deployment** - One-command setup

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- PostgreSQL (with pgvector)
- Redis
- OpenAI API (optional)
- Docker & Docker Compose

### Frontend
- HTML5/CSS3/JavaScript
- Responsive design
- No framework dependencies

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/onepageweb.git
cd onepageweb
```

2. Set up environment variables:
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your preferred LLM provider (see [LLM Configuration Guide](LLM_CONFIGURATION.md)):

**Option A: OpenAI (Default)**
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4
```

**Option B: Anthropic Claude**
```env
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

**Option C: Local Ollama (No API key needed)**
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

See `LLM_CONFIGURATION.md` for all supported providers and detailed setup instructions.

3. Start the application:
```bash
docker-compose up --build -d
```

4. Access the application:
- Generator: http://localhost:8000/generator
- API Documentation: http://localhost:8001/docs

## Project Structure

```
onepageweb/
├── frontend/
│   ├── corporate/       # Corporate website (optional, can be removed)
│   ├── generator/       # AI website generator (main application)
│   └── shared/          # Shared CSS/JS resources
├── backend/             # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── website_generator.py
│   │   ├── models.py
│   │   └── ...
│   └── requirements.txt
├── docker/              # Docker configurations
│   ├── nginx/
│   └── backend/
├── docker-compose.yml
├── README.md
├── LLM_CONFIGURATION.md # LLM provider setup guide
└── MAINTENANCE.md       # System maintenance guide
```

## Configuration

### LLM Provider Setup

This application supports multiple LLM providers. See [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md) for detailed setup instructions for:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3)
- Google (Gemini Pro)
- Ollama (Local LLMs)
- Azure OpenAI

### General Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| OPENAI_API_KEY | OpenAI API key for AI features | - |
| OPENAI_MODEL | OpenAI model to use | gpt-4 |
| DATABASE_URL | PostgreSQL connection string | - |
| REDIS_URL | Redis connection string | - |
| CORS_ORIGINS | Allowed CORS origins | localhost:8000 |

### Timezone

All services are configured to use **Asia/Taipei (UTC+8)** timezone by default. Modify `docker-compose.yml` to change:

```yaml
environment:
  TZ: Your/Timezone
```

## API Endpoints

### Generate Website
```http
POST /api/generate
Content-Type: application/json

{
  "company_name": "My Company",
  "industry": "Technology",
  "style": "modern",
  "description": "A brief description"
}
```

### Preview Website
```http
GET /api/preview/{access_token}
```

### Download Website
```http
GET /api/download/{access_token}
```

For complete API documentation, visit http://localhost:8001/docs

## Development

### Running Locally (without Docker)

1. Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

2. Frontend:
```bash
cd frontend
python -m http.server 8000
```

### Database Migrations

```bash
docker-compose exec backend alembic upgrade head
```

## Customization

### Removing Corporate Website

If you only need the generator, remove the `corporate/` directory:

```bash
rm -rf frontend/corporate
```

Update `frontend/index.html` to redirect directly to the generator.

### Adding Template Styles

Edit `backend/app/template_styles.py` to add new website templates.

## Security Notes

- Change default database passwords in `docker-compose.yml`
- Use strong API keys in production
- Enable HTTPS for production deployment
- Review CORS settings for production use

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome. Please read CONTRIBUTING.md for guidelines.

## Support

For issues and questions, please use the GitHub issue tracker.

## Deployment

### Production Deployment

1. Update production environment variables
2. Configure reverse proxy (nginx/Caddy)
3. Enable SSL/TLS certificates
4. Set up backup for PostgreSQL data
5. Configure monitoring and logging

### Docker Production Build

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Container fails to start
```bash
docker-compose logs backend
docker-compose logs postgres
```

### Database connection issues
Check PostgreSQL container status and connection string in `.env`

### API not responding
Verify backend container is running: `docker ps`

## Acknowledgments

Built with modern web technologies and AI capabilities to democratize website creation.
