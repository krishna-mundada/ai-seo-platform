# AI SEO Platform - Deployment Guide

## 🏗️ Tech Stack

- **Frontend**: React + TypeScript + Vite + Mantine UI
- **Backend**: FastAPI + Python + SQLAlchemy  
- **Database**: Supabase PostgreSQL
- **Authentication**: Clerk
- **Deployment**: Vercel (full-stack serverless)

## 🚀 Production Deployment

This guide covers deploying your AI SEO Platform to production using **Vercel** (full-stack) and **Supabase** (database).

## Prerequisites

- GitHub account with your code repository
- Vercel account ([vercel.com](https://vercel.com))
- Supabase account ([supabase.com](https://supabase.com))
- Clerk account with production keys

## 🎯 Deployment Benefits

- **Serverless**: Auto-scaling, pay-per-request
- **Single Platform**: Both frontend + backend on Vercel
- **PostgreSQL**: Keep existing database schema
- **Global CDN**: Fast worldwide performance
- **Real-time Ready**: Supabase has built-in real-time capabilities

## 📋 Deployment Steps

### 1. Database Setup (Supabase)

#### Create Supabase Project:
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Click "New Project"
3. Choose organization and set project details:
   - **Name**: `ai-seo-platform`
   - **Database Password**: Generate strong password
   - **Region**: Choose closest to your users
4. Wait for project to be created (~2 minutes)
5. Go to **Settings → Database** and copy the connection string

#### Get Database Connection Details:
- **Host**: `db.xxx.supabase.co`
- **Database**: `postgres`
- **Username**: `postgres`
- **Password**: Your chosen password
- **Port**: `5432`

### 2. Full-Stack Deployment (Vercel)

#### Deploy to Vercel:
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect the configuration from `vercel.json`
5. The build will handle both frontend and backend automatically

#### Configure Environment Variables:
In Vercel Dashboard → Project → Settings → Environment Variables:

```bash
# Database (Supabase)
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxx.supabase.co:5432/postgres

# AI API Keys
OPENAI_API_KEY=sk-your_openai_api_key
ANTHROPIC_API_KEY=sk-your_anthropic_api_key

# Security
SECRET_KEY=your-super-secure-secret-key-production
JWT_SECRET=your-jwt-secret-production

# Clerk Authentication
VITE_CLERK_PUBLISHABLE_KEY=pk_test_cmFwaWQtc2hhZC03MC5jbGVyay5hY2NvdW50cy5kZXYk

# Environment
ENVIRONMENT=production
DEBUG=false
```

### 3. Database Migration

After deployment, run migrations:
1. Go to Vercel Dashboard → Project → Functions
2. Find your API function and click "View Function Logs"
3. Or use local migration with production database:

```bash
# Set production DATABASE_URL locally
export DATABASE_URL="postgresql://postgres:password@db.xxx.supabase.co:5432/postgres"

# Run migrations
cd backend
alembic upgrade head
python scripts/seed_industries.py
```

### 5. Clerk Production Setup

1. Go to [Clerk Dashboard](https://dashboard.clerk.com)
2. Create a production instance or update existing
3. Add your production frontend URL to authorized origins
4. Update environment variables with production keys

## 🔧 Production Environment Variables

### Backend (Railway):
```bash
DATABASE_URL=postgresql://...          # Auto-set by Railway
OPENAI_API_KEY=sk-...                 # Your OpenAI API key
ANTHROPIC_API_KEY=sk-...              # Your Anthropic API key
SECRET_KEY=...                        # Strong secret key
JWT_SECRET=...                        # Strong JWT secret
CORS_ORIGINS=https://yourdomain.com   # Your frontend URL
ENVIRONMENT=production
DEBUG=false
```

### Frontend (Vercel):
```bash
VITE_CLERK_PUBLISHABLE_KEY=pk_...     # Your Clerk publishable key
VITE_API_URL=https://your-backend.railway.app  # Your Railway backend URL
```

## ✅ Post-Deployment Checklist

- [ ] Backend health check works: `https://your-backend.railway.app/health`
- [ ] Frontend loads without errors
- [ ] Authentication works (sign up/sign in)
- [ ] Database connections working
- [ ] Content generation works
- [ ] All API endpoints responding correctly

## 🔄 Continuous Deployment

Both Railway and Vercel will automatically redeploy when you push to your main branch:

1. **Code changes** → Push to GitHub
2. **Railway** auto-deploys backend changes
3. **Vercel** auto-deploys frontend changes
4. **Zero downtime** deployments

## 📊 Monitoring & Logs

### Railway:
- **Logs**: Railway Dashboard → Service → Deployments → View Logs
- **Metrics**: Built-in CPU, memory, and network monitoring

### Vercel:
- **Logs**: Vercel Dashboard → Project → Functions tab
- **Analytics**: Built-in performance and usage analytics

## 🐛 Troubleshooting

### Common Issues:

1. **CORS Errors**: Verify `CORS_ORIGINS` environment variable
2. **Database Connection**: Check `DATABASE_URL` format
3. **Build Failures**: Check build logs in Railway/Vercel
4. **API 500 Errors**: Check backend logs for Python errors

### Debug Commands:
```bash
# Check backend health
curl https://your-backend.railway.app/health

# Check frontend API calls (browser dev tools)
# Network tab → XHR requests
```

## 🚀 Going Live

1. **Custom Domain**: Add your domain in Vercel settings
2. **SSL**: Automatically handled by Vercel/Railway
3. **Environment Promotion**: Copy staging vars to production
4. **Monitoring**: Set up alerts for downtime

Your AI SEO Platform is now live and ready for users! 🎉