from pydantic_settings import BaseSettings
from typing import Optional, Dict, List

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://username:password@localhost:5432/ai_seo_platform"
    database_url_test: str = "sqlite:///./test.db"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret: str = "your-jwt-secret-change-in-production"
    
    # AI APIs
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Ollama settings (local development only)
    ollama_base_url: str = "http://host.docker.internal:11434"  # For Docker to reach host
    ollama_default_model: str = "llama3.2:3b"  # Default model for general content
    use_ollama_local_only: bool = True  # Only use Ollama in local development
    
    # Ollama model selection by content type
    ollama_models: Dict[str, str] = {
        # General content models
        "default": "llama3.2:3b",           # Best all-around model (clean output)
        "fast": "llama3.2:3b",              # Fastest for simple content
        "professional": "phi3:3.8b",        # Microsoft model for professional content
        
        # Content-specific models
        "blog_post": "phi3:3.8b",           # Professional content
        "social_media": "llama3.2:3b",      # Fast for short posts
        "technical": "phi3:3.8b",           # For technical content
        "creative": "llama3.2:3b",          # For creative/marketing content
        
        # Quality levels
        "high_quality": "llama3.1:70b",     # Highest quality (requires lots of RAM)
        "balanced": "llama3.1:8b",          # Good balance of speed/quality
        "quick": "llama3.2:3b",            # Fastest response
    }
    
    # Model capabilities and recommendations
    ollama_model_info: Dict[str, Dict[str, str]] = {
        "llama3.1:8b": {
            "size": "~4.7GB",
            "speed": "Medium",
            "quality": "High", 
            "best_for": "General content, blogs, professional writing",
            "description": "Meta's flagship model - excellent all-rounder"
        },
        "llama3.2:3b": {
            "size": "~2GB", 
            "speed": "Fast",
            "quality": "Good",
            "best_for": "Social media, quick content, development testing",
            "description": "Smaller, faster version for quick tasks"
        },
        "llama3.1:70b": {
            "size": "~35GB",
            "speed": "Slow", 
            "quality": "Excellent",
            "best_for": "High-quality content, complex analysis, production",
            "description": "Highest quality but requires lots of RAM"
        },
        "deepseek-r1:1.5b": {
            "size": "~1.1GB",
            "speed": "Medium",
            "quality": "Good (with reasoning)",
            "best_for": "Analysis, research, step-by-step content", 
            "description": "Reasoning model - shows thinking process"
        },
        "codellama:7b": {
            "size": "~3.8GB",
            "speed": "Medium", 
            "quality": "High",
            "best_for": "Technical content, code examples, documentation",
            "description": "Specialized for code and technical writing"
        },
        "qwen2.5:7b": {
            "size": "~4.4GB",
            "speed": "Medium",
            "quality": "High",
            "best_for": "Multilingual content, direct responses",
            "description": "Excellent for clean, direct content generation"
        }
    }
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # CORS
    cors_origins: Optional[str] = None
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        if self.cors_origins:
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return []
    
    # Social Platform APIs (for future)
    linkedin_client_id: Optional[str] = None
    linkedin_client_secret: Optional[str] = None
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env file

settings = Settings()