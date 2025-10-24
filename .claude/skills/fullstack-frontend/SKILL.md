---
name: fullstack-frontend
description: Production-ready Next.js 14 + shadcn/ui frontend builder. Use this skill when building web UI for backend APIs. Supports TypeScript, Tailwind CSS, App Router, API integration, and Vercel deployment.
license: MIT
---

# Fullstack Frontend Skill

Build production-ready Next.js 14 frontend applications with shadcn/ui, TypeScript, and Tailwind CSS.

## Purpose

This skill provides a complete Next.js 14 frontend template for building web interfaces that connect to backend APIs (FastAPI, Express, etc.). It includes:

- **Next.js 14 App Router** - Modern file-based routing with Server/Client Components
- **shadcn/ui** - Beautiful, accessible UI components built on Radix UI and Tailwind CSS
- **TypeScript** - Type-safe development
- **React Query** - Powerful data fetching and caching
- **Production-ready** - Optimized for deployment on Vercel, AWS, or any platform

## When to Use This Skill

Use this skill when:

- Building a web UI for an existing backend API
- Creating admin dashboards, SaaS applications, or internal tools
- Need a production-quality frontend quickly
- Want a clean, customizable foundation that follows modern best practices

**Examples:**
- "Create a frontend for the company research backend"
- "Build a dashboard to view research results"
- "Add a web UI for the coordinator API"

## How to Use

### Step 1: Copy Template to Project

```bash
cp -r .claude/skills/fullstack-frontend/assets/nextjs-template ./frontend
cd frontend
```

### Step 2: Run Setup Script

```bash
bash ../.claude/skills/fullstack-frontend/scripts/setup-frontend.sh
```

This will:
- Install npm dependencies
- Initialize shadcn/ui
- Set up the development environment

### Step 3: Configure Environment Variables

```bash
cp .env.example .env.local
```

Edit `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000  # Your backend API URL
```

### Step 4: Start Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000

### Step 5: Customize for Your Use Case

The template provides a foundation. Customize it by:

1. **Modify Pages** - Update `app/page.tsx`, `app/dashboard/page.tsx`, etc.
2. **Add Components** - Create new components in `components/`
3. **Update API Integration** - Modify `lib/api.ts` to match your backend endpoints
4. **Add shadcn/ui Components** - Use `bash scripts/add-component.sh <component-name>`
5. **Customize Styles** - Edit `tailwind.config.ts` for colors, fonts, etc.

## Template Structure

```
nextjs-template/
├── app/                          # Pages (Next.js 14 App Router)
│   ├── layout.tsx               # Root layout with providers
│   ├── page.tsx                 # Home/landing page
│   ├── dashboard/               # Dashboard page
│   ├── research/new/            # Research execution page
│   └── api/research/            # API proxy routes
│
├── components/
│   ├── ui/                      # shadcn/ui components (button, card, etc.)
│   ├── research-form.tsx        # Custom: Research execution form
│   ├── result-viewer.tsx        # Custom: Display JSON results
│   ├── history-table.tsx        # Custom: History table with search
│   └── stats-card.tsx           # Custom: Statistics cards
│
├── lib/
│   ├── api.ts                   # Backend API client (fetch wrapper)
│   ├── utils.ts                 # Utility functions (cn, etc.)
│   └── types.ts                 # TypeScript type definitions
│
├── styles/
│   └── globals.css              # Global styles and Tailwind imports
│
├── package.json                 # Dependencies
├── tsconfig.json                # TypeScript configuration
├── next.config.mjs              # Next.js configuration
├── tailwind.config.ts           # Tailwind CSS configuration
└── components.json              # shadcn/ui configuration
```

## Key Features

### 1. Pre-built Pages

- **Home Page** (`/`) - Landing page with quick start
- **Dashboard** (`/dashboard`) - Statistics and recent activity
- **New Research** (`/research/new`) - Execute new research tasks
- **History** (`/history`) - View past results with search/filter

### 2. Custom Components

- **ResearchForm** - Real-time progress, error handling, schema selection
- **ResultViewer** - Pretty JSON display with download options
- **HistoryTable** - Sortable, searchable, paginated table
- **StatsCard** - Display metrics (throughput, success rate, cost)

### 3. Backend Integration

The `lib/api.ts` file provides a clean interface for backend communication:

```typescript
// Example usage in components
import { startResearch, getResearchStatus } from '@/lib/api'

const result = await startResearch({
  company_name: "Anthropic",
  extraction_schema: {...}
})
```

CORS is handled automatically via Next.js API routes if needed.

### 4. Customization-Ready

**Design System** - Easily customize via `tailwind.config.ts`:
```typescript
colors: {
  primary: '#your-brand-color',
  secondary: '#your-secondary-color'
}
```

**Components** - All shadcn/ui components are copied to your project, so you can modify them freely.

## Bundled Resources

### assets/nextjs-template/

Complete, ready-to-use Next.js 14 project template. Copy this to your project root as `frontend/` and customize as needed.

### references/

Detailed guides for advanced topics:

- **nextjs-14-guide.md** - Next.js 14 App Router, Server Components, data fetching
- **shadcn-ui-usage.md** - Adding/customizing components, theming, variants
- **api-integration.md** - Connecting to FastAPI/Express, WebSocket, error handling
- **deployment.md** - Deploying to Vercel, AWS, Nginx

Load these references when users need deeper guidance on specific topics.

### scripts/

- **setup-frontend.sh** - Automated setup (npm install, shadcn init)
- **add-component.sh** - Helper to add shadcn/ui components

Execute these scripts to streamline the development workflow.

## Design Philosophy

The template provides a **clean, neutral, professional design** that works immediately but is easy to customize:

- **Colors**: Blue primary, gray neutrals (easily changed)
- **Typography**: System font stack (customize with Pretendard, Geist, etc.)
- **Layout**: Simple top navigation + main content
- **Responsive**: Mobile-first, works on all screen sizes

This allows immediate use while giving complete freedom for branding and customization later.

## Production Readiness

The template includes production best practices:

- ✅ **TypeScript** - Type safety throughout
- ✅ **Error Handling** - Graceful error states and user feedback
- ✅ **Loading States** - Skeleton loaders and spinners
- ✅ **Accessibility** - Semantic HTML, ARIA labels, keyboard navigation
- ✅ **SEO** - Proper meta tags and OpenGraph
- ✅ **Performance** - Code splitting, image optimization, caching
- ✅ **Security** - Environment variables, CSP headers

## Deployment

### Vercel (Recommended)

```bash
vercel deploy
```

See `references/deployment.md` for detailed instructions.

### Other Platforms

The template works on any Node.js hosting:
- AWS Amplify
- Netlify
- Railway
- Docker (via `npm run build && npm run start`)

## Next Steps

After setting up the template:

1. **Test the connection** - Verify backend API is accessible
2. **Customize branding** - Update colors, fonts, logos
3. **Add features** - Implement your specific functionality
4. **Deploy** - Push to production

For detailed guidance on any topic, refer to the `references/` documentation or ask for specific help.

## Example Workflows

### Add a New Page

```bash
# Create new page
touch app/settings/page.tsx

# Add navigation link in layout.tsx
```

### Add a shadcn/ui Component

```bash
bash scripts/add-component.sh dialog
# Component added to components/ui/dialog.tsx
```

### Customize Theme

```typescript
// tailwind.config.ts
theme: {
  extend: {
    colors: {
      primary: '#6366f1',  // Indigo
      secondary: '#10b981'  // Emerald
    }
  }
}
```

## Troubleshooting

**Issue: Backend API not connecting**
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
- Verify backend is running
- Check CORS settings if needed

**Issue: shadcn/ui component not found**
- Run `bash scripts/add-component.sh <component-name>`
- Check `components.json` configuration

**Issue: Build errors**
- Run `npm install` to ensure all dependencies are installed
- Check TypeScript errors with `npm run type-check`

For more help, refer to `references/` documentation.

---

**Created**: 2025-10-24
**Version**: 1.0.0
**Compatible with**: Next.js 14+, React 18+, Node.js 18+
