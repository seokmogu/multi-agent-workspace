## Prisma ORM

**Official Documentation**: https://www.prisma.io/docs/orm/reference/prisma-client-reference
**GitHub**: https://github.com/prisma/prisma
**npm**: `@prisma/client`, `prisma`

### Installation

```bash
npm install @prisma/client
npm install -D prisma

# Initialize Prisma
npx prisma init
```

### Schema Definition

```prisma
// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model Company {
  id        Int      @id @default(autoincrement())
  name      String
  industry  String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([industry])
}
```

### Generate Client

```bash
npx prisma generate
npx prisma db push  # Create tables in database
```

### Connection Setup

```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()
```

### CRUD Operations

```typescript
// CREATE
const company = await prisma.company.create({
  data: {
    name: 'Acme Corp',
    industry: 'Technology'
  }
})

// CREATE MANY
const companies = await prisma.company.createMany({
  data: [
    { name: 'Company 1', industry: 'Tech' },
    { name: 'Company 2', industry: 'Finance' }
  ]
})

// READ (Find Unique)
const company = await prisma.company.findUnique({
  where: { id: 123 }
})

// READ (Find First)
const company = await prisma.company.findFirst({
  where: { industry: 'Technology' }
})

// READ (Find Many)
const companies = await prisma.company.findMany({
  where: {
    industry: 'Technology'
  },
  orderBy: {
    createdAt: 'desc'
  },
  take: 10
})

// UPDATE
const updated = await prisma.company.update({
  where: { id: 123 },
  data: { industry: 'FinTech' }
})

// UPDATE MANY
const result = await prisma.company.updateMany({
  where: { industry: 'Technology' },
  data: { category: 'Tech' }
})

// UPSERT (Update or Insert)
const company = await prisma.company.upsert({
  where: { id: 123 },
  update: { industry: 'FinTech' },
  create: { name: 'New Company', industry: 'FinTech' }
})

// DELETE
const deleted = await prisma.company.delete({
  where: { id: 123 }
})

// DELETE MANY
const result = await prisma.company.deleteMany({
  where: { industry: 'Technology' }
})
```

### Relations

```prisma
model Company {
  id       Int       @id @default(autoincrement())
  name     String
  users    User[]
}

model User {
  id        Int     @id @default(autoincrement())
  email     String
  company   Company @relation(fields: [companyId], references: [id])
  companyId Int
}
```

```typescript
// Create with relations
const company = await prisma.company.create({
  data: {
    name: 'Acme Corp',
    users: {
      create: [
        { email: 'alice@acme.com' },
        { email: 'bob@acme.com' }
      ]
    }
  }
})

// Query with relations
const company = await prisma.company.findUnique({
  where: { id: 123 },
  include: {
    users: true
  }
})
```

### Transactions

```typescript
// Sequential operations (Interactive Transactions)
const result = await prisma.$transaction(async (tx) => {
  const company = await tx.company.create({
    data: { name: 'Acme Corp' }
  })

  await tx.user.create({
    data: {
      email: 'admin@acme.com',
      companyId: company.id
    }
  })

  return company
})

// Batch operations
const [deletedCompanies, createdCompany] = await prisma.$transaction([
  prisma.company.deleteMany({ where: { industry: 'Old' } }),
  prisma.company.create({ data: { name: 'New Corp' } })
])
```

### Migrations

```bash
# Create migration
npx prisma migrate dev --name add_company_table

# Apply migrations to production
npx prisma migrate deploy

# Reset database (development only)
npx prisma migrate reset
```

**Full Prisma Client API**: https://www.prisma.io/docs/orm/reference/prisma-client-reference

---

