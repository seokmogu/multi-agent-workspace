## PlanetScale (MySQL)

**Official Documentation**: https://planetscale.com/docs
**GitHub**: https://github.com/planetscale/database-js
**npm**: `@planetscale/database`

### Installation

```bash
npm install @planetscale/database
```

### Connection Setup

```typescript
import { connect } from '@planetscale/database'

const conn = connect({
  host: process.env.DATABASE_HOST,
  username: process.env.DATABASE_USERNAME,
  password: process.env.DATABASE_PASSWORD
})

// Or using connection URL
const conn = connect({
  url: process.env.DATABASE_URL
})
```

### CRUD Operations

```typescript
// CREATE
const results = await conn.execute(
  'INSERT INTO companies (name, industry) VALUES (?, ?)',
  ['Acme Corp', 'Technology']
)

// READ
const results = await conn.execute(
  'SELECT * FROM companies WHERE industry = ?',
  ['Technology']
)

// UPDATE
const results = await conn.execute(
  'UPDATE companies SET industry = ? WHERE id = ?',
  ['FinTech', 123]
)

// DELETE
const results = await conn.execute(
  'DELETE FROM companies WHERE id = ?',
  [123]
)
```

### Transactions

```typescript
const tx = await conn.transaction()

try {
  await tx.execute('INSERT INTO companies ...')
  await tx.execute('UPDATE users ...')
  await tx.commit()
} catch (error) {
  await tx.rollback()
  throw error
}
```

### Branching (Development Workflow)

```bash
# Create development branch (like Git!)
pscale branch create my-database dev

# Make schema changes on dev branch
pscale connect my-database dev

# Deploy to production (zero-downtime)
pscale deploy-request create my-database dev

# Merge deploy request
pscale deploy-request deploy my-database <number>
```

**Full CLI Reference**: https://planetscale.com/docs/reference/cli

---

