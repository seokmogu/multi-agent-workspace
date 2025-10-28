## Neon (PostgreSQL Serverless)

**Official Documentation**: https://neon.com/docs/serverless/serverless-driver
**GitHub**: https://github.com/neondatabase/serverless
**npm**: `@neondatabase/serverless`

### Installation

```bash
npm install @neondatabase/serverless
```

### Connection Setup

```typescript
import { neon } from '@neondatabase/serverless'

const sql = neon(process.env.DATABASE_URL)

// With connection pooling
import { Pool } from '@neondatabase/serverless'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
})
```

### CRUD Operations

```typescript
// CREATE
const result = await sql`
  INSERT INTO companies (name, industry)
  VALUES (${'Acme Corp'}, ${'Technology'})
  RETURNING *
`

// READ
const companies = await sql`
  SELECT * FROM companies
  WHERE industry = ${'Technology'}
  ORDER BY created_at DESC
  LIMIT 10
`

// UPDATE
const updated = await sql`
  UPDATE companies
  SET industry = ${'FinTech'}
  WHERE id = ${123}
  RETURNING *
`

// DELETE
const deleted = await sql`
  DELETE FROM companies
  WHERE id = ${123}
  RETURNING *
`
```

### Transactions

```typescript
import { neonConfig, Pool } from '@neondatabase/serverless'

const pool = new Pool({ connectionString: process.env.DATABASE_URL })
const client = await pool.connect()

try {
  await client.query('BEGIN')
  await client.query('INSERT INTO companies ...')
  await client.query('UPDATE users ...')
  await client.query('COMMIT')
} catch (e) {
  await client.query('ROLLBACK')
  throw e
} finally {
  client.release()
}
```

### Branching

```bash
# Create database branch
neonctl branches create --project-id <project-id> --name dev

# Connect to specific branch
neonctl connection-string <branch-name>
```

**Full API Reference**: https://neon.com/docs/serverless/serverless-driver

---

