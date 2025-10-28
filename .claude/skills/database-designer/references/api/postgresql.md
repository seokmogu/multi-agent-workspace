## PostgreSQL (Native)

**Official Documentation**: https://node-postgres.com/
**GitHub**: https://github.com/brianc/node-postgres
**npm**: `pg`

### Installation

```bash
npm install pg
```

### Connection Setup

```typescript
import { Pool } from 'pg'

const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  user: 'postgres',
  password: 'password'
})

// Or with connection string
const pool = new Pool({
  connectionString: process.env.DATABASE_URL
})
```

### CRUD Operations

```typescript
// CREATE
const result = await pool.query(
  'INSERT INTO companies (name, industry) VALUES ($1, $2) RETURNING *',
  ['Acme Corp', 'Technology']
)

// READ
const result = await pool.query(
  'SELECT * FROM companies WHERE industry = $1 ORDER BY created_at DESC LIMIT $2',
  ['Technology', 10]
)
const companies = result.rows

// UPDATE
const result = await pool.query(
  'UPDATE companies SET industry = $1 WHERE id = $2 RETURNING *',
  ['FinTech', 123]
)

// DELETE
const result = await pool.query(
  'DELETE FROM companies WHERE id = $1 RETURNING *',
  [123]
)
```

### Transactions

```typescript
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

**Full node-postgres Docs**: https://node-postgres.com/

---

