# AI SEO Platform

A comprehensive AI-powered SEO and marketing automation platform designed for small to medium businesses to automate their digital marketing efforts.

## Features

- **AI Content Generation**: Automated blog posts, social media content, and marketing copy
- **Multi-Platform Publishing**: LinkedIn, Twitter, Facebook, Instagram, Reddit, Quora
- **SEO Optimization**: Keyword research, content optimization, and performance tracking
- **Campaign Management**: Automated marketing campaigns with performance analytics
- **Brand Consistency**: Maintain consistent brand voice across all platforms
- **Performance Analytics**: Track engagement, views, clicks, and ROI

## Tech Stack

### Backend
- **Framework**: Python FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Services**: OpenAI GPT-4, Anthropic Claude, Ollama (local development)
- **Testing**: pytest with comprehensive test coverage
- **Migrations**: Alembic for database schema management

### Frontend  
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: Mantine v7
- **State Management**: TanStack Query (React Query)
- **Styling**: CSS-in-JS with Mantine components

### Development
- **Containerization**: Docker & Docker Compose
- **Package Management**: pnpm (frontend), pip (backend)
- **Database**: PostgreSQL in production, SQLite for tests

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ and pnpm (for frontend development)
- Python 3.11+ (for backend development)

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-seo-platform
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Add your API keys to `.env`:
```bash
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

4. Start the services:
```bash
docker-compose up -d
```

5. Run database migrations:
```bash
docker-compose exec api alembic upgrade head
```

6. Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### Local Development

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up local PostgreSQL database:
```bash
createdb ai_seo_platform
```

4. Update `.env` with your local database URL:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/ai_seo_platform
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the backend server:
```bash
uvicorn app.main:app --reload
```

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
pnpm install
```

3. Start the development server:
```bash
pnpm dev
```

The frontend will be available at http://localhost:5173 and the backend API at http://localhost:8000.

## API Endpoints

### Business Management
- `POST /api/v1/businesses/` - Create business profile
- `GET /api/v1/businesses/` - List all businesses
- `GET /api/v1/businesses/{id}` - Get business details
- `PUT /api/v1/businesses/{id}` - Update business profile
- `DELETE /api/v1/businesses/{id}` - Delete business (CASCADE deletes content)

### Industry Management
- `GET /api/v1/industries/` - List all industries with optional filters
- `GET /api/v1/industries/{id}` - Get industry by ID
- `GET /api/v1/industries/slug/{slug}` - Get industry by slug
- `POST /api/v1/industries/` - Create new industry
- `PUT /api/v1/industries/{id}` - Update industry
- `DELETE /api/v1/industries/{id}` - Delete industry

### Content Generation & Management
- `POST /api/v1/content/generate` - Generate AI content
- `GET /api/v1/content/` - List content with filters
- `GET /api/v1/content/{id}` - Get specific content
- `PUT /api/v1/content/{id}` - Update content
- `DELETE /api/v1/content/{id}` - Delete content
- `PUT /api/v1/content/{id}/approve` - Approve content for publishing
- `PUT /api/v1/content/{id}/draft` - Save content as draft

### AI Suggestions
- `POST /api/v1/suggestions/topics` - Generate AI topic suggestions
- `POST /api/v1/suggestions/keywords` - Generate AI keyword suggestions

## Database Schema

### Core Entities

- **Industries**: Industry categories with metadata (icons, colors, descriptions)
- **Businesses**: Business profiles with brand guidelines and industry relationships
- **Content**: Generated content with SEO metadata, status tracking, and AI generation details
- **Campaigns**: Marketing campaigns with automation settings (future feature)

### Key Features

- **CASCADE DELETE**: Deleting a business automatically removes all related content
- **Content Status Management**: DRAFT → PENDING_APPROVAL → APPROVED → PUBLISHED
- **AI Integration**: Full metadata tracking for AI-generated content
- **SEO Optimization**: Keyword tracking, meta descriptions, and SEO scoring
- **Industry Relationships**: Structured industry data with business associations

## Development

### Project Structure

```
ai-seo-platform/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   └── endpoints/    # Route handlers
│   │   ├── core/            # Core configuration
│   │   ├── db/              # Database setup
│   │   ├── models/          # SQLAlchemy models
│   │   ├── repositories/    # Data access layer
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   ├── alembic/            # Database migrations
│   ├── scripts/            # Utility scripts
│   └── tests/              # Test suite
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── lib/           # Utilities and API client
│   │   ├── pages/         # Page components
│   │   └── main.tsx       # App entry point
│   └── public/            # Static assets
└── docker-compose.yml     # Development environment
```

### Adding New Features

1. Define database models in `app/models/`
2. Create Pydantic schemas in `app/schemas/`
3. Implement repository pattern in `app/repositories/`
4. Add business logic in `app/services/`
5. Create API endpoints in `app/api/endpoints/`
6. Generate and run migrations

### Running Tests

#### Backend Tests
```bash
cd backend
pytest -xvs
```

#### Frontend Tests (when added)
```bash
cd frontend
pnpm test
```

### Test Coverage
The backend includes comprehensive test coverage with:
- Unit tests for repositories and services
- Integration tests for API endpoints
- CASCADE delete functionality tests
- Database consistency tests

## Deployment

The application is designed to be easily deployable to various platforms:

- **Docker**: Use provided Dockerfile and docker-compose.yml
- **Cloud Providers**: AWS, GCP, Azure with container services
- **Platform-as-a-Service**: Heroku, Railway, Render

## Configuration

All configuration is managed through environment variables:

### Required
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Application secret key
- `JWT_SECRET`: JWT signing secret

### AI Services (at least one required)
- `OPENAI_API_KEY`: OpenAI API key for content generation
- `ANTHROPIC_API_KEY`: Anthropic API key for content generation

### Ollama (Local Development)
- `OLLAMA_BASE_URL`: Ollama server URL (default: http://host.docker.internal:11434)
- `OLLAMA_DEFAULT_MODEL`: Default model to use (default: llama3.2:3b)

### Optional
- `ENVIRONMENT`: development/staging/production (default: development)
- `DEBUG`: Enable debug mode (default: True)
- `DATABASE_URL_TEST`: Test database URL (default: sqlite:///./test.db)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is proprietary software. All rights reserved.

## Support

For support and questions, please contact the development team.