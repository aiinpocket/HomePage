# LLM Provider Configuration Guide

This application supports multiple LLM providers. You can choose the one that best fits your needs.

## Supported Providers

1. **OpenAI** (GPT-4, GPT-3.5-turbo)
2. **Anthropic** (Claude 3)
3. **Google** (Gemini Pro)
4. **Ollama** (Local LLMs)
5. **Azure OpenAI**

## Quick Setup

### Option 1: OpenAI (Default)

1. Get API key from https://platform.openai.com/api-keys

2. Edit `backend/.env`:
```env
OPENAI_API_KEY=sk-...your-key-here
OPENAI_MODEL=gpt-4
```

**Available Models:**
- `gpt-4` - Most capable, higher cost
- `gpt-4-turbo` - Faster, cost-effective
- `gpt-3.5-turbo` - Fast, economical

### Option 2: Anthropic Claude

1. Get API key from https://console.anthropic.com/

2. Edit `backend/.env`:
```env
# Comment out OpenAI
# OPENAI_API_KEY=...

# Enable Anthropic
ANTHROPIC_API_KEY=sk-ant-...your-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

3. Update `backend/app/ai_handler.py` to use Anthropic client

**Available Models:**
- `claude-3-opus-20240229` - Most capable
- `claude-3-sonnet-20240229` - Balanced
- `claude-3-haiku-20240307` - Fast and economical

### Option 3: Google Gemini

1. Get API key from https://makersuite.google.com/app/apikey

2. Edit `backend/.env`:
```env
# Comment out OpenAI
# OPENAI_API_KEY=...

# Enable Gemini
GOOGLE_API_KEY=...your-key-here
GEMINI_MODEL=gemini-pro
```

3. Update `backend/app/ai_handler.py` to use Google's SDK

**Available Models:**
- `gemini-pro` - Text generation
- `gemini-pro-vision` - Multimodal (text + images)

### Option 4: Local LLM with Ollama

Perfect for development, testing, or privacy-sensitive environments.

1. Install Ollama: https://ollama.ai/

2. Pull a model:
```bash
ollama pull llama2
# or
ollama pull mistral
ollama pull codellama
```

3. Edit `backend/.env`:
```env
# Comment out OpenAI
# OPENAI_API_KEY=...

# Enable Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

4. Update `backend/app/ai_handler.py` to use Ollama API

**Available Models:**
- `llama2` - General purpose
- `mistral` - High quality, efficient
- `codellama` - Code-focused
- `phi` - Small, fast

### Option 5: Azure OpenAI

For enterprise deployments using Azure.

1. Create Azure OpenAI resource in Azure Portal

2. Deploy a model (e.g., gpt-4)

3. Edit `backend/.env`:
```env
# Comment out OpenAI
# OPENAI_API_KEY=...

# Enable Azure OpenAI
AZURE_OPENAI_API_KEY=...your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-gpt4-deployment
AZURE_API_VERSION=2024-02-15-preview
```

4. Update `backend/app/ai_handler.py` to use Azure OpenAI client

## Implementation Guide

### Modifying ai_handler.py

To switch LLM providers, update `backend/app/ai_handler.py`:

```python
from typing import Optional
import os

class AIHandler:
    def __init__(self):
        # Detect which provider is configured
        if os.getenv("ANTHROPIC_API_KEY"):
            self.provider = "anthropic"
            from anthropic import Anthropic
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
            
        elif os.getenv("GOOGLE_API_KEY"):
            self.provider = "google"
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.model = os.getenv("GEMINI_MODEL", "gemini-pro")
            self.client = genai.GenerativeModel(self.model)
            
        elif os.getenv("OLLAMA_BASE_URL"):
            self.provider = "ollama"
            from ollama import Client
            self.client = Client(host=os.getenv("OLLAMA_BASE_URL"))
            self.model = os.getenv("OLLAMA_MODEL", "llama2")
            
        elif os.getenv("AZURE_OPENAI_API_KEY"):
            self.provider = "azure"
            from openai import AzureOpenAI
            self.client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_version=os.getenv("AZURE_API_VERSION")
            )
            self.model = os.getenv("AZURE_OPENAI_DEPLOYMENT")
            
        else:
            # Default to OpenAI
            self.provider = "openai"
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-4")
```

## Cost Comparison

| Provider | Model | Cost (per 1M tokens) | Speed | Quality |
|----------|-------|---------------------|-------|---------|
| OpenAI | GPT-4 | $30 input / $60 output | Medium | Excellent |
| OpenAI | GPT-3.5-turbo | $0.50 / $1.50 | Fast | Good |
| Anthropic | Claude-3-Opus | $15 / $75 | Medium | Excellent |
| Anthropic | Claude-3-Sonnet | $3 / $15 | Fast | Very Good |
| Google | Gemini Pro | Free tier available | Fast | Very Good |
| Ollama | Local | Free | Varies | Good |

## No LLM Mode

The application can run without any LLM provider:

```env
# Comment out all LLM configurations
# OPENAI_API_KEY=...
# ANTHROPIC_API_KEY=...
# etc.

# Disable AI chat
ENABLE_AI_CHAT=False
```

The website generator will still work using pre-defined templates, but the AI chat assistant will be disabled.

## Testing Your Configuration

After configuration, test with:

```bash
# Start the application
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Test API
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test"}'
```

## Troubleshooting

### API Key Invalid
- Verify key is correct and has not expired
- Check for extra spaces or newlines in `.env`
- Ensure billing is enabled for the provider

### Model Not Available
- Verify model name matches provider's documentation
- Some models require special access or waitlist approval
- Check regional availability

### Connection Timeout
- For local Ollama, ensure service is running: `ollama serve`
- For Azure, verify endpoint URL and firewall rules
- Check network connectivity

## Security Best Practices

1. Never commit `.env` to version control
2. Use environment-specific configurations
3. Rotate API keys regularly
4. Monitor usage and set billing alerts
5. Use least-privilege API keys when available

## Further Reading

- OpenAI: https://platform.openai.com/docs
- Anthropic: https://docs.anthropic.com/
- Google AI: https://ai.google.dev/docs
- Ollama: https://github.com/ollama/ollama
- Azure OpenAI: https://learn.microsoft.com/azure/ai-services/openai/
