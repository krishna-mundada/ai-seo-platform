from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import api_router

app = FastAPI(
    title="AI SEO Platform",
    description="AI-powered SEO and marketing automation platform",
    version="0.1.0",
)

# Configure CORS
# Configure allowed origins
allowed_origins = [
    "http://localhost:3000",  # React dev server (alternative port)
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://localhost:8080",  # Alternative frontend ports
    "http://127.0.0.1:8080",
]

# Add production origins if configured
if hasattr(settings, 'CORS_ORIGINS') and settings.CORS_ORIGINS:
    allowed_origins.extend(settings.CORS_ORIGINS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI SEO Platform API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}