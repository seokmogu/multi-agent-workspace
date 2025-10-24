# Frontend Application

> Next.js 14 + shadcn/ui frontend for Company Research Platform

## Quick Start

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Update .env.local with your backend API URL
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Project Structure

```
.
├── app/                    # Next.js 14 App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── dashboard/         # Dashboard
│   ├── research/new/      # New research
│   └── api/               # API routes
│
├── components/
│   ├── ui/                # shadcn/ui components
│   └── ...                # Custom components
│
├── lib/
│   ├── api.ts             # Backend API client
│   ├── utils.ts           # Utilities
│   └── types.ts           # TypeScript types
│
└── styles/
    └── globals.css        # Global styles
```

## Features

- ✅ Next.js 14 App Router
- ✅ TypeScript
- ✅ Tailwind CSS
- ✅ shadcn/ui components
- ✅ React Query for data fetching
- ✅ Fully responsive
- ✅ Production-ready

## Available Scripts

```bash
npm run dev        # Start development server
npm run build      # Build for production
npm run start      # Start production server
npm run lint       # Run ESLint
npm run type-check # Check TypeScript types
```

## Adding shadcn/ui Components

```bash
# Add a component
npx shadcn-ui@latest add dialog

# Or use the helper script
bash ../scripts/add-component.sh dialog
```

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Or connect your Git repository in Vercel dashboard for automatic deployments.

### Docker

```bash
# Build
docker build -t frontend:latest .

# Run
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=https://api.yourcompany.com \
  frontend:latest
```

## Customization

### Colors

Edit `tailwind.config.ts`:

```typescript
colors: {
  primary: '#your-color',
  // ...
}
```

### Fonts

Update `app/layout.tsx`:

```typescript
import { YourFont } from 'next/font/google'

const yourFont = YourFont({ subsets: ['latin'] })
```

## Documentation

- [Next.js 14 Docs](https://nextjs.org/docs)
- [shadcn/ui Docs](https://ui.shadcn.com)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [React Query Docs](https://tanstack.com/query)

## License

MIT
