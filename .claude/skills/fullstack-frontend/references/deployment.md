# Deployment Guide

This guide covers deploying the Next.js frontend to production.

## Vercel (Recommended)

Vercel is the easiest deployment option for Next.js applications.

### Prerequisites

- GitHub/GitLab/Bitbucket account
- Vercel account (free tier available)

### Deployment Steps

1. **Push to Git Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to https://vercel.com
   - Click "New Project"
   - Import your repository
   - Vercel auto-detects Next.js

3. **Configure Environment Variables**
   - In Vercel dashboard → Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = `https://your-backend-api.com`
   - Add any other required variables

4. **Deploy**
   - Click "Deploy"
   - Wait 1-2 minutes
   - Your app is live!

### Auto-Deployment

Every push to `main` branch automatically deploys to production.

For staging environments:
- Create a `staging` branch
- Vercel creates a preview deployment
- Each PR gets its own preview URL

### Custom Domain

1. Vercel dashboard → Settings → Domains
2. Add your domain (e.g., `app.yourcompany.com`)
3. Update DNS records as instructed
4. SSL certificate is automatically provisioned

## AWS Amplify

Great option if you're already using AWS.

### Deployment Steps

1. **Install Amplify CLI**
   ```bash
   npm install -g @aws-amplify/cli
   amplify configure
   ```

2. **Initialize Amplify**
   ```bash
   amplify init
   ```

3. **Add Hosting**
   ```bash
   amplify add hosting
   # Choose "Hosting with Amplify Console"
   ```

4. **Deploy**
   ```bash
   amplify publish
   ```

### Environment Variables

Set in Amplify Console → App Settings → Environment Variables

## Docker Deployment

For self-hosted or Kubernetes deployments.

### Dockerfile

Create `Dockerfile` in frontend directory:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

### Build and Run

```bash
# Build
docker build -t frontend:latest .

# Run
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=https://api.yourcompany.com \
  frontend:latest
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
```

## Nginx Deployment

For traditional server deployment.

### Build for Production

```bash
npm run build
npm run start  # Runs on port 3000
```

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/yourapp
server {
    listen 80;
    server_name app.yourcompany.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### PM2 Process Manager

```bash
# Install PM2
npm install -g pm2

# Start app
pm2 start npm --name "frontend" -- start

# Save process list
pm2 save

# Auto-start on reboot
pm2 startup
```

## Environment-Specific Configuration

### Production Environment Variables

```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.yourcompany.com
NODE_ENV=production
```

### Build Optimization

In `next.config.mjs`:

```javascript
const nextConfig = {
  // Output standalone for Docker
  output: 'standalone',

  // Compress images
  images: {
    formats: ['image/avif', 'image/webp'],
  },

  // Enable SWC minification
  swcMinify: true,
}
```

## Performance Optimization

### 1. Enable Caching

```javascript
// next.config.mjs
async headers() {
  return [
    {
      source: '/static/(.*)',
      headers: [
        {
          key: 'Cache-Control',
          value: 'public, max-age=31536000, immutable',
        },
      ],
    },
  ]
}
```

### 2. Image Optimization

Use Next.js `<Image>` component:

```typescript
import Image from 'next/image'

<Image
  src="/logo.png"
  width={200}
  height={100}
  alt="Logo"
  priority
/>
```

### 3. Code Splitting

Lazy load heavy components:

```typescript
import dynamic from 'next/dynamic'

const HeavyChart = dynamic(() => import('@/components/heavy-chart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false
})
```

## Monitoring

### Vercel Analytics

Built-in for Vercel deployments. View in dashboard.

### Sentry Error Tracking

```bash
npm install @sentry/nextjs
npx @sentry/wizard -i nextjs
```

### Custom Logging

```typescript
// lib/logger.ts
export function logError(error: Error, context?: any) {
  if (process.env.NODE_ENV === 'production') {
    // Send to logging service
    console.error(error, context)
  } else {
    console.error(error, context)
  }
}
```

## Security

### 1. Content Security Policy

```javascript
// next.config.mjs
async headers() {
  return [
    {
      source: '/(.*)',
      headers: [
        {
          key: 'Content-Security-Policy',
          value: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline';"
        },
      ],
    },
  ]
}
```

### 2. Environment Variables

Never commit `.env.local` or expose sensitive keys client-side.

Only use `NEXT_PUBLIC_` prefix for non-sensitive values.

### 3. API Rate Limiting

Implement on backend, but also throttle on frontend:

```typescript
import { debounce } from 'lodash'

const debouncedSearch = debounce(async (query) => {
  await searchAPI(query)
}, 500)
```

## Troubleshooting

**Issue: Build fails with "out of memory"**
```bash
NODE_OPTIONS="--max-old-space-size=4096" npm run build
```

**Issue: Environment variables not working**
- Ensure `NEXT_PUBLIC_` prefix for client-side
- Restart dev server after changes
- Check Vercel dashboard settings

**Issue: Images not loading in production**
- Configure `next.config.mjs` image domains
- Use Next.js `<Image>` component
- Check public/ directory

## Best Practices

1. ✅ Use environment variables for all config
2. ✅ Enable analytics and error tracking
3. ✅ Set up staging environment
4. ✅ Use CDN for static assets
5. ✅ Implement proper caching headers
6. ✅ Monitor performance metrics
7. ✅ Keep dependencies updated
8. ✅ Test builds locally before deploying

## Resources

- [Next.js Deployment Docs](https://nextjs.org/docs/deployment)
- [Vercel Docs](https://vercel.com/docs)
- [AWS Amplify Hosting](https://docs.amplify.aws/guides/hosting/nextjs/q/platform/js/)
