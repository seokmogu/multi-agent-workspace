## Connection Patterns

### Environment Variables

```bash
# .env file
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/dbname
REDIS_URL=redis://user:pass@localhost:6379
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
```

### Connection Pooling

```typescript
// PostgreSQL
const pool = new Pool({
  max: 20,        // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})

// MongoDB
const client = new MongoClient(uri, {
  maxPoolSize: 20,
  minPoolSize: 5,
  maxIdleTimeMs: 30000
})

// Redis (ioredis)
const redis = new Redis({
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  lazyConnect: true
})
```

### Error Handling

```typescript
try {
  const result = await db.query(...)
} catch (error) {
  if (error.code === '23505') {
    // PostgreSQL unique violation
    console.error('Duplicate key error')
  } else if (error.code === '23503') {
    // Foreign key violation
    console.error('Referenced record does not exist')
  } else {
    throw error
  }
}
```

---

## Best Practices

### 1. Use Connection Pooling

```typescript
// ✅ Good - Reuse connections
const pool = new Pool({ ... })

// ❌ Bad - New connection every time
const client = new Client({ ... })
await client.connect()
```

### 2. Use Prepared Statements

```typescript
// ✅ Good - Prevents SQL injection
await pool.query('SELECT * FROM users WHERE id = $1', [userId])

// ❌ Bad - SQL injection vulnerability
await pool.query(`SELECT * FROM users WHERE id = ${userId}`)
```

### 3. Handle Errors Gracefully

```typescript
try {
  await db.operation()
} catch (error) {
  console.error('Database error:', error)
  // Retry logic, fallback, or alert
  throw error
}
```

### 4. Use Transactions for Related Operations

```typescript
// ✅ Good - Atomic operations
await prisma.$transaction([
  prisma.user.create({ ... }),
  prisma.account.create({ ... })
])

// ❌ Bad - Can leave partial data
await prisma.user.create({ ... })
await prisma.account.create({ ... })  // Might fail
```

### 5. Index Frequently Queried Fields

```sql
-- PostgreSQL
CREATE INDEX idx_companies_industry ON companies(industry);

-- Prisma
model Company {
  industry String
  @@index([industry])
}
```

### 6. Implement Caching

```typescript
async function getData(id: string) {
  // 1. Check cache
  const cached = await redis.get(`data:${id}`)
  if (cached) return JSON.parse(cached)

  // 2. Query database
  const data = await db.findOne({ id })

  // 3. Store in cache (1 hour TTL)
  await redis.setex(`data:${id}`, 3600, JSON.stringify(data))

  return data
}
```

### 7. Close Connections Properly

```typescript
// Graceful shutdown
process.on('SIGTERM', async () => {
  await pool.end()
  await redis.quit()
  await mongoClient.close()
  process.exit(0)
})
```

### 8. Use Environment-Specific Configs

```typescript
const config = {
  development: {
    database: 'myapp_dev',
    logging: true
  },
  production: {
    database: 'myapp_prod',
    logging: false,
    ssl: { rejectUnauthorized: true }
  }
}

const dbConfig = config[process.env.NODE_ENV]
```

---

## Migration Strategies

### Schema Migrations

```bash
# Prisma
npx prisma migrate dev --name add_companies_table

# Knex.js
npx knex migrate:make add_companies_table
npx knex migrate:latest

# Sequelize
npx sequelize-cli migration:generate --name add-companies-table
npx sequelize-cli db:migrate
```

### Data Migrations

```typescript
// Example: Backfill industry field
const companies = await db.companies.findMany({
  where: { industry: null }
})

for (const company of companies) {
  await db.companies.update({
    where: { id: company.id },
    data: { industry: inferIndustry(company.name) }
  })
}
```

### Zero-Downtime Migrations

1. **Add new column** (nullable)
2. **Dual write** (write to both old & new)
3. **Backfill data** (copy old → new)
4. **Switch reads** (read from new column)
5. **Remove old column**

---

## Additional Resources

### Official Documentation

| Database | Documentation | API Reference |
|----------|---------------|---------------|
| **Supabase** | https://supabase.com/docs | https://supabase.com/docs/reference/javascript |
| **PlanetScale** | https://planetscale.com/docs | https://github.com/planetscale/database-js |
| **Neon** | https://neon.com/docs | https://neon.com/docs/serverless/serverless-driver |
| **Firebase** | https://firebase.google.com/docs | https://firebase.google.com/docs/reference/js |
| **MongoDB** | https://www.mongodb.com/docs/drivers/node | https://mongodb.github.io/node-mongodb-native/ |
| **Redis** | https://redis.io/docs/latest/develop/clients/nodejs/ | https://github.com/redis/ioredis |
| **Prisma** | https://www.prisma.io/docs | https://www.prisma.io/docs/orm/reference |
| **PostgreSQL** | https://node-postgres.com | https://node-postgres.com/apis/client |

### Community Resources

- **Stack Overflow**: Database-specific tags
- **GitHub Discussions**: Official repos
- **Discord/Slack**: Community servers

---

**Last Updated**: 2025-10-23
**Maintainer**: Database Designer Skill
**License**: MIT

**Note**: Always refer to official documentation for the most up-to-date API information, as libraries and services evolve frequently.
