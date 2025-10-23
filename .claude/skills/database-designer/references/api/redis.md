## Redis

**Official Documentation**: https://redis.io/docs/latest/develop/clients/nodejs/
**ioredis GitHub**: https://github.com/redis/ioredis
**npm**: `ioredis` (recommended) or `redis`

### Installation

```bash
npm install ioredis
```

### Connection Setup

```typescript
import Redis from 'ioredis'

const redis = new Redis({
  host: 'localhost',
  port: 6379,
  password: 'your-password'
})

// Or with URL
const redis = new Redis(process.env.REDIS_URL)

// With TLS (Redis Cloud)
const redis = new Redis({
  host: 'your-redis.cloud.redislabs.com',
  port: 12345,
  password: 'your-password',
  tls: {}
})
```

### Basic Operations

```typescript
// SET (Create/Update)
await redis.set('company:123', JSON.stringify({ name: 'Acme Corp' }))

// SET with expiration (TTL)
await redis.setex('session:abc', 3600, 'user-data')  // 1 hour

// GET (Read)
const data = await redis.get('company:123')
const company = JSON.parse(data)

// DELETE
await redis.del('company:123')

// EXISTS
const exists = await redis.exists('company:123')  // Returns 1 or 0

// EXPIRE (Set TTL)
await redis.expire('company:123', 3600)  // 1 hour
```

### Hash Operations

```typescript
// Set hash fields
await redis.hset('company:123', 'name', 'Acme Corp')
await redis.hset('company:123', 'industry', 'Technology')

// Get single field
const name = await redis.hget('company:123', 'name')

// Get all fields
const company = await redis.hgetall('company:123')
// { name: 'Acme Corp', industry: 'Technology' }

// Delete field
await redis.hdel('company:123', 'industry')
```

### List Operations

```typescript
// Push to list
await redis.lpush('companies', 'Company A')  // Left push
await redis.rpush('companies', 'Company B')  // Right push

// Get list
const companies = await redis.lrange('companies', 0, -1)  // All items

// Pop from list
const company = await redis.lpop('companies')  // Left pop
const company = await redis.rpop('companies')  // Right pop
```

### Set Operations

```typescript
// Add to set
await redis.sadd('industries', 'Technology', 'Finance', 'Healthcare')

// Get all members
const industries = await redis.smembers('industries')

// Check membership
const isMember = await redis.sismember('industries', 'Technology')

// Remove from set
await redis.srem('industries', 'Technology')
```

### Pub/Sub

```typescript
// Publisher
await redis.publish('company-updates', JSON.stringify({
  action: 'created',
  companyId: 123
}))

// Subscriber
const subscriber = new Redis()
await subscriber.subscribe('company-updates')

subscriber.on('message', (channel, message) => {
  console.log('Received:', JSON.parse(message))
})
```

### Caching Pattern

```typescript
async function getCompany(id: string) {
  const cacheKey = `company:${id}`

  // Try cache first
  const cached = await redis.get(cacheKey)
  if (cached) {
    return JSON.parse(cached)
  }

  // Cache miss - fetch from database
  const company = await db.companies.findOne({ id })

  // Store in cache with 1 hour expiration
  await redis.setex(cacheKey, 3600, JSON.stringify(company))

  return company
}
```

**Full ioredis API**: https://github.com/redis/ioredis#api-reference

---

