# AI SEO Platform - Setup Guide

A comprehensive guide for setting up and running the AI SEO Platform locally.

## 📋 Prerequisites

Before starting, ensure you have the following installed:

- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Python 3.11+** - [Download here](https://python.org/)
- **PostgreSQL** - [Download here](https://postgresql.org/) or use Docker
- **Git** - [Download here](https://git-scm.com/)

### Optional but Recommended:
- **pnpm** - Faster package manager for Node.js: `npm install -g pnpm`
- **Docker & Docker Compose** - For easier database setup

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-seo-platform.git
cd ai-seo-platform
```

### 2. Install Dependencies

#### Frontend Dependencies:
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies using pnpm (recommended)
pnpm install

# Alternative: using npm
npm install
```

#### Backend Dependencies:
```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Database Setup

#### Option A: Using Docker (Recommended)
```bash
# Start PostgreSQL using Docker
docker run --name postgres-ai-seo \
  -e POSTGRES_DB=ai_seo_platform \
  -e POSTGRES_USER=username \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -d postgres:15
```

#### Option B: Local PostgreSQL
```bash
# Create database
createdb ai_seo_platform
```

#### Run Database Migrations:
```bash
# Make sure you're in the backend directory with venv activated
cd backend
source venv/bin/activate  # if not already activated

# Run migrations
alembic upgrade head

# Seed initial data (industries)
python scripts/seed_industries.py
```

### 4. Environment Configuration

```bash
# Copy environment example
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

Required environment variables:
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/ai_seo_platform

# Security
SECRET_KEY=your-super-secret-key-change-in-production
JWT_SECRET=your-jwt-secret-change-in-production

# AI Services (at least one required)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional - Ollama for local development
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_DEFAULT_MODEL=llama3.2:3b
```

### 5. Start the Application

#### Terminal 1 - Backend:
```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start the FastAPI server with logs
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
```

#### Terminal 2 - Frontend:
```bash
cd frontend

# Start the Vite development server
pnpm dev
```

You should see output like:
```
VITE v5.4.10  ready in 114 ms
➜  Local:   http://localhost:5173/
➜  Network: http://192.168.x.x:5173/
```

### 6. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432 (PostgreSQL)

## 🔧 Development Setup

### VSCode Configuration

#### Recommended Extensions:
1. **Python** - Microsoft Python extension
2. **Pylance** - Advanced Python IntelliSense
3. **TypeScript and JavaScript Language Features** - Built-in
4. **ES7+ React/Redux/React-Native snippets**
5. **Prettier** - Code formatter
6. **ESLint** - JavaScript/TypeScript linting

#### Python Interpreter Setup:
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Python: Select Interpreter"
3. Choose your virtual environment: `./backend/venv/bin/python`

#### TypeScript Setup:
VSCode should auto-detect the TypeScript configuration in the frontend directory.

### Viewing Backend Logs

#### Development Logs:
Backend logs appear in the terminal where you ran `uvicorn`:
```
INFO:     127.0.0.1:54321 - "GET /api/v1/content HTTP/1.1" 200 OK
INFO:     127.0.0.1:54322 - "POST /api/v1/businesses HTTP/1.1" 201 Created
ERROR:    Database connection failed
```

#### Detailed Logging:
```bash
# For more verbose logging
uvicorn app.main:app --reload --log-level debug
```

#### Custom Logging:
Add debug prints to your code:
```python
# In your Python code
print("Debug: Processing request...")
import logging
logging.info("Custom log message")
```

### Running Tests

#### Backend Tests:
```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/api/endpoints/test_businesses.py

# Run with extra verbose output and stop on first failure
pytest -xvs
```

#### Frontend Tests (when implemented):
```bash
cd frontend
pnpm test
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Python Module Not Found
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt

# If still issues, try recreating venv
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Node Modules Issues
```bash
cd frontend

# Clear cache and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Or with npm
rm -rf node_modules package-lock.json
npm install
```

#### 3. Database Connection Issues
```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# Check if database exists
psql -h localhost -p 5432 -U username -l

# For testing, use SQLite instead
DATABASE_URL=sqlite:///./test.db
```

#### 4. Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --reload --port 8001
```

#### 5. Migration Issues
```bash
# Check migration status
alembic current

# Reset database (WARNING: destroys data)
alembic downgrade base
alembic upgrade head

# Create new migration if schema changed
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

#### 6. VSCode Python Path Issues
1. Open Command Palette (`Ctrl+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose the interpreter in your virtual environment
4. Restart VSCode if needed

### Environment-Specific Issues

#### macOS:
```bash
# If you get SSL certificate errors
/Applications/Python\ 3.x/Install\ Certificates.command

# If PostgreSQL installation issues
brew install postgresql
brew services start postgresql
```

#### Windows:
```bash
# Use Command Prompt or PowerShell, not Git Bash for Python commands
# Activate virtual environment:
venv\Scripts\activate

# If permission errors
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Linux:
```bash
# Install system dependencies if needed
sudo apt-get update
sudo apt-get install python3-venv python3-pip postgresql postgresql-contrib

# If permission issues with PostgreSQL
sudo -u postgres createuser --interactive
sudo -u postgres createdb ai_seo_platform
```

## 🔄 Development Workflow

### Making Changes

1. **Backend changes**: Server auto-reloads with `--reload` flag
2. **Frontend changes**: Vite hot-reloads automatically
3. **Database schema changes**: Create and run migrations

### Adding New Dependencies

#### Backend:
```bash
cd backend
source venv/bin/activate

# Install new package
pip install package-name

# Update requirements
pip freeze > requirements.txt
```

#### Frontend:
```bash
cd frontend

# Add new package
pnpm add package-name

# Add dev dependency
pnpm add -D package-name
```

### Database Migrations

```bash
# Create new migration after model changes
alembic revision --autogenerate -m "Add new table"

# Apply migration
alembic upgrade head

# Check current migration
alembic current

# Rollback if needed
alembic downgrade -1
```

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://react.dev/
- **Mantine UI Components**: https://mantine.dev/
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/
- **Alembic Migrations**: https://alembic.sqlalchemy.org/
- **pytest Testing**: https://pytest.org/

## 🆘 Getting Help

If you encounter issues not covered in this guide:

1. Check the application logs in both terminals
2. Verify all environment variables are set correctly
3. Ensure all services (database, backend, frontend) are running
4. Check the GitHub issues for similar problems
5. Review the API documentation at http://localhost:8000/docs

## 🔐 Production Deployment

For production deployment:

1. Use environment-specific `.env` files
2. Set up proper database with connection pooling
3. Use a production WSGI server like Gunicorn
4. Set up reverse proxy with Nginx
5. Configure proper logging and monitoring
6. Use Docker containers for consistency

This setup guide should get you up and running with the AI SEO Platform. Happy coding! 🚀