# Database API Reference

Quick reference index for database operations across different platforms.

## 📚 Database-Specific Guides

Each database has its own dedicated guide with CRUD operations, connections, and examples.

| Database | Type | Use Case | Guide |
|----------|------|----------|-------|
| **Supabase** | PostgreSQL (SaaS) | MVP, Full-stack apps | [api/supabase.md](./api/supabase.md) |
| **PlanetScale** | MySQL (SaaS) | Serverless, Branching | [api/planetscale.md](./api/planetscale.md) |
| **Neon** | PostgreSQL (Serverless) | Edge, Auto-scaling | [api/neon.md](./api/neon.md) |
| **Firebase** | NoSQL (SaaS) | Mobile, Realtime | [api/firebase.md](./api/firebase.md) |
| **MongoDB** | NoSQL (SaaS) | Flexible schema | [api/mongodb.md](./api/mongodb.md) |
| **Redis** | Key-Value (Cache) | Caching, Queues | [api/redis.md](./api/redis.md) |
| **Prisma ORM** | Multi-DB (ORM) | Type-safe queries | [api/prisma.md](./api/prisma.md) |
| **PostgreSQL** | SQL (Native) | Full control | [api/postgresql.md](./api/postgresql.md) |

## 🛠️ Common Guides

- **[Best Practices](./api/best-practices.md)** - Connection pooling, caching, transactions, migrations, error handling

## 📖 Quick Navigation

### By Use Case

**Need real-time features?**
- [Firebase](./api/firebase.md) - Built-in realtime
- [Supabase](./api/supabase.md) - PostgreSQL + Realtime

**Need serverless?**
- [Neon](./api/neon.md) - Auto-scale to zero
- [PlanetScale](./api/planetscale.md) - Serverless MySQL

**Need caching/queue?**
- [Redis](./api/redis.md) - In-memory cache

**Need type-safety?**
- [Prisma](./api/prisma.md) - TypeScript ORM

**Need full control?**
- [PostgreSQL](./api/postgresql.md) - Native driver

### By Feature

| Feature | Databases |
|---------|-----------|
| **Auto-generated APIs** | [Supabase](./api/supabase.md) |
| **Database branching** | [PlanetScale](./api/planetscale.md), [Neon](./api/neon.md) |
| **Realtime subscriptions** | [Supabase](./api/supabase.md), [Firebase](./api/firebase.md) |
| **Offline support** | [Firebase](./api/firebase.md) |
| **Aggregation pipelines** | [MongoDB](./api/mongodb.md) |
| **Pub/Sub messaging** | [Redis](./api/redis.md), [Supabase](./api/supabase.md) |
| **Schema migrations** | [Prisma](./api/prisma.md), [PostgreSQL](./api/postgresql.md) |

## 📝 What's in Each Guide?

Each database guide includes:

- **Installation** - npm packages and setup
- **Connection** - Client initialization and connection strings
- **CRUD Operations** - Create, Read, Update, Delete examples
- **Advanced Features** - Transactions, filtering, aggregation, etc.
- **Official Documentation** - Links to official docs and GitHub

## 🚀 Getting Started

1. **Choose a database** from the table above based on your use case
2. **Read the specific guide** for detailed API examples
3. **Check best practices** for production-ready code

## 📚 Additional Resources

### Official Documentation Links

All guides include links to official documentation:

- **Supabase**: https://supabase.com/docs/reference/javascript
- **PlanetScale**: https://planetscale.com/docs
- **Neon**: https://neon.com/docs/serverless/serverless-driver
- **Firebase**: https://firebase.google.com/docs/reference/js
- **MongoDB**: https://www.mongodb.com/docs/drivers/node
- **Redis**: https://github.com/redis/ioredis
- **Prisma**: https://www.prisma.io/docs/orm/reference
- **PostgreSQL**: https://node-postgres.com

### Related References

- **[DATABASE_OPTIONS.md](./DATABASE_OPTIONS.md)** - Compare 15+ database options (pricing, pros/cons)
- **[SCHEMA_DESIGN_PATTERNS.md](./SCHEMA_DESIGN_PATTERNS.md)** - Common schema patterns (user mgmt, e-commerce, etc.)

---

**Total Guides**: 9 (8 databases + best practices)
**Last Updated**: 2025-10-23
**Maintainer**: Database Designer Skill
