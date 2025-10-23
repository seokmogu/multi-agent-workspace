---
name: Database Designer
description: Design and implement database systems for any project based on PRD and requirements. Analyze requirements, select appropriate database (SaaS/Cloud/Self-hosted), design schema, and provide implementation guidance. Use this when you need to choose a database technology, design data models, implement schema migrations, or architect data storage for new projects. Supports Supabase, PostgreSQL, MongoDB, Firebase, AWS/GCP/Azure databases, and more.
allowed-tools: Write, Edit, Read, Bash
---

# Database Designer

Analyze project requirements and design appropriate database solutions - from database selection to schema implementation.

## When to Use This Skill

Use this skill when you need to:
- Choose the right database for a new project
- Design data models based on PRD/requirements
- Migrate from one database to another
- Optimize existing database schemas
- Implement database schema with migrations
- Evaluate SaaS vs self-hosted database options

## Workflow

```
1. ANALYZE → Read PRD/requirements → Identify data needs → List constraints
              ↓
2. SELECT → Compare DB options → Consider budget/scale → Choose database
              ↓
3. DESIGN → Create schema → Define relationships → Plan indexes
              ↓
4. IMPLEMENT → Generate migrations → Write models → Setup connection
```

## Quick Database Selection Guide

See `references/DATABASE_OPTIONS.md` for complete comparison.

| Need | Best Choice | Why |
|------|-------------|-----|
| **MVP / Prototyping** | Supabase (Free) | Instant setup, generous free tier, built-in auth |
| **Serverless / Edge** | PlanetScale or Neon | Auto-scaling, branching, pay-per-use |
| **Real-time features** | Supabase or Firebase | Built-in realtime subscriptions |
| **Full control** | PostgreSQL (self-hosted) | Maximum flexibility, no vendor lock-in |
| **Document store** | MongoDB Atlas | Flexible schema, great free tier |
| **AWS ecosystem** | AWS RDS or Aurora | Deep AWS integration |
| **Google ecosystem** | Firebase or Cloud SQL | Deep GCP integration |
| **Complex analytics** | PostgreSQL or ClickHouse | Advanced query capabilities |
| **Caching / Sessions** | Redis (ElastiCache) | Sub-millisecond performance, 800%+ throughput boost |
| **Task Queues** | Redis + RQ/Celery | Background jobs, batch processing |
| **Rate Limiting** | Redis | Token bucket, sliding window algorithms |
| **No budget** | Supabase/MongoDB Atlas/PlanetScale | All have generous free tiers |

## Implementation Steps

### Step 1: Analyze Requirements

Extract database requirements from PRD/specifications:

**Questions to answer:**
- What entities need to be stored? (users, products, orders, etc.)
- What relationships exist? (one-to-many, many-to-many)
- What queries will be most common?
- Expected data volume? (100s, 1000s, millions of records)
- Real-time needs? (live updates, subscriptions)
- Budget constraints? (free tier, $10/mo, enterprise)
- Deployment preference? (SaaS, cloud-managed, self-hosted)

**Example analysis:**

```
PRD: "Build a company research agent that stores research results"

Data needs:
- Entities: companies, research_sessions, search_results, extracted_data
- Relationships: 1 company → many sessions, 1 session → many results
- Common queries: "Get latest research for company X", "Find all companies in industry Y"
- Volume: ~1000 companies, ~10k research sessions (small scale)
- Real-time: Not needed
- Budget: Free tier preferred
- Deployment: SaaS (less ops overhead)

→ Recommendation: Supabase (PostgreSQL) - Free tier sufficient, JSONB for flexible data
```

### Step 2: Select Database

Use the decision tree in `references/DATABASE_OPTIONS.md` to choose:

**Primary factors:**
1. **Data structure**: Relational (SQL) vs Document (NoSQL) vs Key-Value
2. **Scale**: Small (<10k records) vs Medium (<1M) vs Large (>1M)
3. **Budget**: Free tier vs Paid
4. **Ops**: Managed (SaaS) vs Cloud (AWS/GCP) vs Self-hosted

**Common patterns:**

| Project Type | Recommended DB |
|--------------|----------------|
| **SaaS MVP** | Supabase (PostgreSQL + Auth + Storage) |
| **Mobile app** | Firebase (Realtime + Auth + Free tier) |
| **E-commerce** | PostgreSQL (Complex queries + Transactions) |
| **Analytics** | ClickHouse or PostgreSQL + TimescaleDB |
| **CMS / Blog** | MongoDB or PostgreSQL |
| **Microservices** | PostgreSQL per service or shared with schemas |
| **Serverless app** | PlanetScale or Neon (Auto-scaling) |

### Step 3: Design Schema

Apply appropriate design patterns from `references/SCHEMA_DESIGN_PATTERNS.md`:

**Basic process:**
1. Identify entities (tables/collections)
2. Define attributes (columns/fields)
3. Establish relationships (foreign keys, references)
4. Plan indexes (for common queries)
5. Consider constraints (unique, not null, check)

**Example schema design:**

```sql
-- Companies table
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL UNIQUE,
    industry TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Research sessions table
CREATE TABLE research_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    status TEXT CHECK (status IN ('running', 'completed', 'failed')),
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- Extracted data (JSONB for flexibility)
CREATE TABLE extracted_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES research_sessions(id) ON DELETE CASCADE,
    data JSONB NOT NULL,
    schema_version TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_companies_industry ON companies(industry);
CREATE INDEX idx_sessions_company ON research_sessions(company_id);
CREATE INDEX idx_extracted_data_session ON extracted_data(session_id);
CREATE INDEX idx_extracted_data_jsonb ON extracted_data USING GIN(data);
```

### Step 4: Implementation

Generate implementation code based on selected database:

**For Supabase:**
```typescript
// 1. Install
npm install @supabase/supabase-js

// 2. Initialize client
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
)

// 3. Use
const { data, error } = await supabase
  .from('companies')
  .select('*')
  .eq('industry', 'Technology')
```

**For PostgreSQL (self-hosted):**
```python
# 1. Install
pip install sqlalchemy psycopg2-binary alembic

# 2. Define models (SQLAlchemy)
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(UUID, primary_key=True, server_default=text('gen_random_uuid()'))
    company_name = Column(String, nullable=False, unique=True)
    industry = Column(String)
    created_at = Column(DateTime, server_default=text('NOW()'))

# 3. Create migrations with Alembic
alembic init alembic
alembic revision --autogenerate -m "Create companies table"
alembic upgrade head
```

**For MongoDB:**
```javascript
// 1. Install
npm install mongodb mongoose

// 2. Define schema (Mongoose)
const companySchema = new mongoose.Schema({
  companyName: { type: String, required: true, unique: true },
  industry: String,
  extractedData: mongoose.Schema.Types.Mixed,  // Flexible
  createdAt: { type: Date, default: Date.now }
});

const Company = mongoose.model('Company', companySchema);

// 3. Use
const company = await Company.findOne({ industry: 'Technology' });
```

See `references/DATABASE_OPTIONS.md` for complete implementation guides for each database.

## Database-Specific Features

### Supabase Advantages
- **Built-in Auth**: Row-level security, user management
- **Realtime**: Subscribe to database changes
- **Storage**: File uploads integrated
- **Instant APIs**: Auto-generated REST and GraphQL
- **Free tier**: 500MB database, 2GB file storage, 50GB bandwidth/month

### PlanetScale Advantages
- **Branching**: Database branches like Git (dev/staging/prod)
- **Zero-downtime schema changes**: Non-blocking DDL
- **Automatic backups**: Point-in-time recovery
- **Serverless**: Pay only for what you use

### PostgreSQL Advantages
- **JSONB**: Flexible JSON storage with indexing
- **Full-text search**: Built-in search capabilities
- **Extensions**: PostGIS (geo), TimescaleDB (time-series), pg_vector (embeddings)
- **Mature ecosystem**: Decades of production use

### Firebase Advantages
- **Realtime**: Instant sync across clients
- **Offline support**: Works offline, syncs when online
- **Mobile SDKs**: Native iOS/Android support
- **Free tier**: 1GB storage, 10GB/month bandwidth

### Redis Advantages
- **Ultra-fast**: Sub-millisecond latency (in-memory storage)
- **800%+ performance boost**: Reduce database load dramatically
- **Multiple data types**: Strings, lists, sets, sorted sets, hashes, streams
- **Task queues**: RQ, Celery for background job processing
- **Rate limiting**: Built-in support for token bucket algorithms
- **Pub/Sub**: Real-time messaging and notifications
- **Persistence options**: RDB snapshots + AOF append-only file
- **AWS ElastiCache Serverless (2025)**: Valkey engine 33% cheaper, 90% lower minimum storage (100MB vs 1GB)
- **Cost-effective**: ~$92/month for 1GB + 50k req/hr (ElastiCache Serverless)

**Common Redis Use Cases:**
- **Caching layer**: Cache database queries, API responses, session data
- **Session store**: Distributed session management for web apps
- **Task queue**: Background jobs with RQ or Celery
- **Rate limiting**: API throttling, user quotas
- **Leaderboards**: Sorted sets for real-time rankings
- **Real-time analytics**: Counting, metrics, time-series data

**Redis Implementation (Python):**
```python
# Install
pip install redis hiredis rq

# Basic usage
import redis

# Connect
r = redis.from_url("redis://localhost:6379")

# Cache example
def get_user(user_id):
    # Check cache
    cached = r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # Cache miss - fetch from database
    user = db.query(User).get(user_id)

    # Cache result (1 hour TTL)
    r.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user

# Task queue with RQ
from rq import Queue
queue = Queue(connection=r)
job = queue.enqueue(process_data, data_id)
```

**AWS ElastiCache Serverless:**
```hcl
resource "aws_elasticache_serverless_cache" "cache" {
  name   = "my-cache"
  engine = "valkey"  # 33% cheaper in 2025

  cache_usage_limits {
    data_storage {
      maximum = 10  # GB
    }
    ecpu_per_second {
      maximum = 5000
    }
  }
}
```

## Migration Strategies

### Migrating Between Databases

**Common scenarios:**

1. **SQLite → PostgreSQL** (Local dev → Production)
   ```bash
   # Export from SQLite
   sqlite3 database.db .dump > dump.sql

   # Import to PostgreSQL (after editing SQL)
   psql -d mydb -f dump.sql
   ```

2. **Firebase → Supabase** (NoSQL → SQL)
   - Export Firebase data as JSON
   - Transform to relational schema
   - Import via Supabase client or SQL

3. **MongoDB → PostgreSQL** (Document → Relational)
   - Export MongoDB collections
   - Flatten nested documents
   - Map to normalized tables

See `references/DATABASE_OPTIONS.md` for detailed migration guides.

## Best Practices

### Schema Design
1. **Normalize appropriately**: Balance between normalization and query performance
2. **Use appropriate data types**: UUID for IDs, TIMESTAMPTZ for dates, JSONB for flexible data
3. **Add indexes early**: Index foreign keys and frequently queried columns
4. **Plan for scale**: Consider partitioning for large tables

### Database Selection
1. **Start with managed**: Use SaaS (Supabase, PlanetScale) unless you have specific needs
2. **Choose SQL by default**: Unless you have a clear reason for NoSQL
3. **Consider free tiers**: Supabase, MongoDB Atlas, PlanetScale all have generous free tiers
4. **Match ecosystem**: If on AWS, consider RDS; if on GCP, consider Cloud SQL

### Implementation
1. **Use migrations**: Always version your schema changes (Alembic, Prisma, Supabase migrations)
2. **Validate constraints in DB**: Don't rely only on application-level validation
3. **Plan backups**: Automated backups from day one
4. **Monitor performance**: Set up query performance monitoring early

## Troubleshooting

**Schema changes breaking production:**
- Use migration tools (Alembic, Prisma, Supabase migrations)
- Test migrations on staging first
- Consider using PlanetScale for zero-downtime schema changes

**Slow queries:**
- Add indexes on frequently queried columns
- Use EXPLAIN ANALYZE to understand query plans
- Consider read replicas for heavy read workloads

**Vendor lock-in concerns:**
- Use ORMs (SQLAlchemy, Prisma) to abstract database logic
- Stick to standard SQL where possible
- Export data regularly
- Consider multi-cloud strategies

## References

- **`references/DATABASE_OPTIONS.md`** - Complete comparison of 15+ database options including pricing, features, pros/cons, and implementation guides
- **`references/SCHEMA_DESIGN_PATTERNS.md`** - Common schema design patterns for various use cases (user management, e-commerce, analytics, etc.)

## Example Usage

### Scenario: Building a Company Research Agent

**Requirements:**
- Store company profiles, research sessions, search results
- Query by company name, industry
- Store flexible JSON data (different schemas over time)
- Budget: Free tier
- Scale: ~1000 companies, ~10k research sessions

**Decision process:**
1. **Analyze**: Relational data with some flexibility (JSONB), small scale, free tier needed
2. **Select**: Supabase (PostgreSQL with JSONB, generous free tier, easy setup)
3. **Design**:
   - `companies` table (id, name, industry)
   - `research_sessions` table (id, company_id FK, status, timestamps)
   - `extracted_data` table (id, session_id FK, data JSONB)
4. **Implement**:
   - Create Supabase project
   - Run migrations via Supabase Studio or CLI
   - Connect via `@supabase/supabase-js`

**Result:** Production-ready database in ~30 minutes, no ops overhead, scales to 100k+ records on free tier.

---

**Database Designer** - From requirements to production-ready schema
