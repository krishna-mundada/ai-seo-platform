# Ollama Setup for AI SEO Platform

This guide shows how to set up Ollama for local AI content generation - perfect for development and testing without API costs!

## Quick Start

### 1. Install Ollama

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from https://ollama.ai/download

### 2. Start Ollama Service

```bash
ollama serve
```

This starts Ollama on `http://localhost:11434` (default port)

### 3. Download a Model

For best results, use Llama 3.1 8B (default in our config):

```bash
# Download the recommended model (2-4GB download)
ollama pull llama3.1:8b

# Alternative smaller model (faster but less capable)
ollama pull llama3.2:3b

# List available models
ollama list
```

### 4. Test AI Content Generation

With Ollama running and a model downloaded, the AI SEO Platform will automatically detect and use it:

```bash
# Test content generation
curl -X POST "http://localhost:8000/api/v1/content/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": 2,
    "content_type": "blog_post",
    "topic": "How AI is revolutionizing small business marketing",
    "keywords": ["AI marketing", "small business", "automation"]
  }'
```

## Model Recommendations

| Model | Size | Use Case | Performance |
|-------|------|----------|-------------|
| `llama3.1:8b` | ~4GB | **Recommended** - Best balance of quality and speed | ⭐⭐⭐⭐⭐ |
| `llama3.2:3b` | ~2GB | Faster, good for simple content | ⭐⭐⭐⭐ |
| `llama3.1:70b` | ~35GB | Highest quality (requires 32GB+ RAM) | ⭐⭐⭐⭐⭐⭐ |
| `codellama:7b` | ~4GB | Good for technical/code content | ⭐⭐⭐⭐ |

## Configuration

The platform automatically detects Ollama. To customize:

```bash
# .env file
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

## Troubleshooting

### Ollama Not Detected
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check logs
docker compose logs api --tail 20
```

### Model Not Found
```bash
# List downloaded models
ollama list

# Download the model if missing
ollama pull llama3.1:8b
```

### Performance Issues
- **Use smaller models** for development: `llama3.2:3b`
- **Increase RAM** if using larger models
- **Use SSD storage** for faster model loading

## Environment-Based AI Selection

### Local Development (ENVIRONMENT=development)
1. **Ollama** (local) - Free, private, fast for development
2. **Mock Content** - Fallback templates

### Deployed Environments (staging/production)
1. **Anthropic Claude** - High quality, paid API
2. **OpenAI GPT** - Good quality, paid API  
3. **Mock Content** - Fallback templates

**Note:** Ollama is automatically disabled in staging/production environments to ensure cloud API usage.

## Benefits of Ollama

✅ **Free** - No API costs  
✅ **Private** - Data stays local  
✅ **Fast** - No network latency  
✅ **Offline** - Works without internet  
✅ **Development-friendly** - Perfect for testing  

## Production Notes

For production, consider:
- Use paid APIs (OpenAI/Anthropic) for highest quality
- Ollama is great for development/testing
- Can run both: Ollama for dev, APIs for production