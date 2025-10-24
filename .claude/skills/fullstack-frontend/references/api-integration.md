# API Integration Guide

This guide covers how to connect the Next.js frontend to your FastAPI backend.

## Backend Setup

The template is configured to connect to a FastAPI backend running on `localhost:8000`.

### Environment Variables

Set your backend URL in `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production:
```bash
NEXT_PUBLIC_API_URL=https://api.yourcompany.com
```

## API Client (`lib/api.ts`)

The `lib/api.ts` file provides a clean interface for all backend communication.

### Basic Usage

```typescript
import { startResearch, getStats } from '@/lib/api'

// Start research
const result = await startResearch({
  company_name: "Anthropic",
  extraction_schema: mySchema,
  user_context: "Focus on AI products",
  max_iterations: 2
})

// Get statistics
const stats = await getStats()
```

### Error Handling

All API functions throw an `ApiError` with status code and message:

```typescript
try {
  const result = await startResearch(request)
} catch (error) {
  if (error instanceof ApiError) {
    console.error(`API Error ${error.status}: ${error.message}`)
  }
}
```

## React Query Integration

The template uses `@tanstack/react-query` for server state management.

### Basic Query

```typescript
'use client'

import { useQuery } from '@tanstack/react-query'
import { getStats } from '@/lib/api'

function StatsComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['stats'],
    queryFn: getStats,
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return <div>Total Jobs: {data.total_jobs}</div>
}
```

### Mutation (POST/PUT/DELETE)

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { startResearch } from '@/lib/api'

function ResearchForm() {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: startResearch,
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['research-history'] })
    },
  })

  const handleSubmit = (data) => {
    mutation.mutate(data)
  }

  return (
    <button
      onClick={() => handleSubmit(formData)}
      disabled={mutation.isPending}
    >
      {mutation.isPending ? 'Loading...' : 'Start Research'}
    </button>
  )
}
```

## WebSocket for Real-Time Updates

For real-time progress updates during research:

```typescript
import { connectWebSocket } from '@/lib/api'
import { useEffect, useState } from 'react'

function ResearchProgress({ jobId }: { jobId: string }) {
  const [progress, setProgress] = useState<any>(null)

  useEffect(() => {
    const ws = connectWebSocket(jobId, (data) => {
      setProgress(data)
    })

    return () => ws.close()
  }, [jobId])

  return <div>Progress: {progress?.percentage}%</div>
}
```

## CORS Configuration

### Development

Next.js API routes handle CORS automatically via `next.config.mjs`:

```javascript
async headers() {
  return [
    {
      source: '/api/:path*',
      headers: [
        { key: 'Access-Control-Allow-Origin', value: '*' },
        { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
      ],
    },
  ]
}
```

### Production

Configure CORS on your backend:

```python
# FastAPI backend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## API Proxying

You can proxy API requests through Next.js to avoid CORS issues:

### Method 1: Next.js API Routes

```typescript
// app/api/research/route.ts
export async function POST(request: Request) {
  const body = await request.json()

  const response = await fetch(`${process.env.BACKEND_URL}/api/research`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })

  return Response.json(await response.json())
}
```

### Method 2: Rewrites in next.config.mjs

```javascript
async rewrites() {
  return [
    {
      source: '/api/backend/:path*',
      destination: process.env.NEXT_PUBLIC_API_URL + '/:path*',
    },
  ]
}
```

Then use `/api/backend/research` instead of direct backend URL.

## Authentication

### API Key Authentication

```typescript
// lib/api.ts
async function fetchAPI<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const apiKey = process.env.NEXT_PUBLIC_API_KEY

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': apiKey,
      ...options.headers,
    },
  })

  // ...
}
```

### JWT Authentication

```typescript
// lib/auth.ts
export function getAuthToken(): string | null {
  return localStorage.getItem('auth_token')
}

// lib/api.ts
headers: {
  'Authorization': `Bearer ${getAuthToken()}`,
  ...
}
```

## Best Practices

1. **Environment Variables**: Always use `NEXT_PUBLIC_` prefix for client-side variables
2. **Error Handling**: Use try-catch with React Query's error boundaries
3. **Loading States**: Show loading indicators for all API calls
4. **Caching**: Configure React Query stale time appropriately
5. **Retries**: Use React Query's retry logic for transient failures

## Troubleshooting

**Issue: "Failed to fetch"**
- Check backend is running
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS configuration

**Issue: "Network request failed"**
- Ensure backend URL is accessible from browser
- Check for HTTPS/HTTP mismatch in production

**Issue: Stale data showing**
- Adjust React Query `staleTime` setting
- Manually invalidate queries after mutations
