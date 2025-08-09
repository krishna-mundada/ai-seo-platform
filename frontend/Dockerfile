# Frontend Dockerfile for React + Vite
FROM node:18-alpine

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S reactjs -u 1001
RUN chown -R reactjs:nodejs /app
USER reactjs

EXPOSE 3000

# Development command (can be overridden)
CMD ["pnpm", "dev", "--host", "0.0.0.0"]