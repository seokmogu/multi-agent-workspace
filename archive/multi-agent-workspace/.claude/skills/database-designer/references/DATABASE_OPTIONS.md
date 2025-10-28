# Database Options - Complete Reference

Comprehensive comparison of database options for different project needs.

## Quick Comparison Table

| Database | Type | Free Tier | Best For | Pros | Cons |
|----------|------|-----------|----------|------|------|
| **Supabase** | PostgreSQL (SaaS) | 500MB, Unlimited API | MVP, Full-stack | Auth, Realtime, Storage, Instant APIs | PostgreSQL only |
| **PlanetScale** | MySQL (SaaS) | 5GB, 1B row reads | Serverless, Branching | Git-like branching, Zero-downtime schema | MySQL only, No foreign keys |
| **Neon** | PostgreSQL (SaaS) | 3GB, Autoscaling | Serverless Postgres | Branching, Auto-scale to zero | Newer, less proven |
| **Firebase** | NoSQL (SaaS) | 1GB, 10GB bandwidth | Mobile, Realtime | Realtime sync, Offline support | NoSQL learning curve |
| **MongoDB Atlas** | NoSQL (SaaS) | 512MB | Flexible schema | Document model, Great free tier | NoSQL, Complex queries harder |
| **PostgreSQL** | SQL (Self-hosted) | Free (self-host) | Full control, Complex queries | Most feature-rich, Extensions | Requires ops |
| **AWS RDS** | SQL (Cloud) | 750 hours/month (1 year) | AWS ecosystem | Managed, Reliable | More expensive |
| **SQLite** | SQL (Embedded) | Free | Local, Edge, Prototyping | Zero config, Single file | Not for concurrent writes |

---

## SaaS Databases (Managed, Easy Setup)

### 1. Supabase

**Overview:** Open-source Firebase alternative built on PostgreSQL

**Type:** PostgreSQL (Relational)

**Pricing:**
- **Free tier:**
  - 500MB database
  - Unlimited API requests
  - 2GB file storage
  - 50GB bandwidth/month
  - 50,000 monthly active users
- **Pro:** $25/month (8GB database, 100GB storage)
- **Team/Enterprise:** Custom pricing

**Pros:**
- ✅ All-in-one: Database + Auth + Storage + Realtime + Edge Functions
- ✅ Row-level security (RLS) for fine-grained access control
- ✅ Auto-generated REST and GraphQL APIs
- ✅ Built-in realtime subscriptions
- ✅ Generous free tier
- ✅ PostgreSQL = full SQL power + JSONB

**Cons:**
- ❌ PostgreSQL only (can't use MySQL/MongoDB)
- ❌ Newer platform (less mature than AWS/GCP)

**Best for:**
- MVP/Prototyping with tight deadlines
- Full-stack apps needing auth + database + storage
- Projects requiring realtime features
- Teams wanting minimal DevOps

**Quick Setup:**

```bash
# 1. Create project at https://supabase.com
# 2. Install client
npm install @supabase/supabase-js

# 3. Initialize
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key'
)

# 4. Use
const { data, error } = await supabase
  .from('companies')
  .select('*')
  .eq('industry', 'Technology')

# 5. Realtime subscriptions
supabase
  .channel('companies')
  .on('postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'companies' },
    (payload) => console.log('New company!', payload)
  )
  .subscribe()
```

---

### 2. PlanetScale

**Overview:** Serverless MySQL platform with Git-like branching

**Type:** MySQL (Relational)

**Pricing:**
- **Free (Hobby):**
  - 5GB storage
  - 1 billion row reads/month
  - 10 million row writes/month
  - 1 production branch + 2 dev branches
- **Scaler:** $29/month (starts)
- **Enterprise:** Custom

**Pros:**
- ✅ **Database branching** (like Git - branch, merge, deploy)
- ✅ Zero-downtime schema changes
- ✅ Automatic backups and point-in-time recovery
- ✅ Serverless (auto-scales, pay-per-use)
- ✅ Generous free tier

**Cons:**
- ❌ No foreign key constraints (uses Vitess - designed for scale)
- ❌ MySQL only
- ❌ Some MySQL features missing (triggers, stored procedures limited)

**Best for:**
- Serverless applications
- Teams wanting database branching workflow
- Projects needing zero-downtime deployments
- MySQL users

**Quick Setup:**

```bash
# 1. Create database at https://planetscale.com
# 2. Install CLI
brew install planetscale/tap/pscale

# 3. Create branch (like Git!)
pscale branch create my-database dev

# 4. Connect
pscale connect my-database main --port 3306

# 5. Use with Prisma
npm install @planetscale/database

import { connect } from '@planetscale/database'

const conn = connect({
  url: process.env.DATABASE_URL
})

const results = await conn.execute('SELECT * FROM companies')
```

---

### 3. Neon

**Overview:** Serverless Postgres with auto-scaling and branching

**Type:** PostgreSQL (Relational)

**Pricing:**
- **Free:**
  - 3GB storage per branch
  - Autoscaling (compute scales to zero)
  - Unlimited branches
- **Pro:** $19/month (starts)

**Pros:**
- ✅ **Serverless Postgres** - scales to zero when idle
- ✅ **Instant branching** - create database copy in <1s
- ✅ PostgreSQL (all features, extensions)
- ✅ Very fast provisioning

**Cons:**
- ❌ Newer platform (less battle-tested)
- ❌ Less features than Supabase (just database, no auth/storage/realtime)

**Best for:**
- Serverless apps needing Postgres
- Projects with variable load (auto-scale to zero)
- Development workflows needing database branching

**Quick Setup:**

```bash
# 1. Create project at https://neon.tech
# 2. Get connection string
DATABASE_URL="postgres://user:pass@ep-xxx.region.neon.tech/dbname"

# 3. Use with any Postgres client
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
})

const result = await pool.query('SELECT * FROM companies')

# 4. Create branches via CLI
neonctl branches create --name dev
```

---

### 4. Firebase Realtime Database / Firestore

**Overview:** Google's NoSQL database for mobile/web apps

**Type:** NoSQL (Document)

**Pricing:**
- **Spark (Free):**
  - 1GB storage
  - 10GB/month bandwidth
  - 50K document reads/day, 20K writes/day
- **Blaze (Pay as you go):** $0.18/GB storage, $0.12/GB bandwidth

**Pros:**
- ✅ **Realtime sync** across all clients
- ✅ **Offline support** - works offline, syncs when back online
- ✅ Excellent mobile SDKs (iOS, Android, Web)
- ✅ Integrated with Firebase ecosystem (Auth, Storage, Functions)
- ✅ Great for collaborative apps

**Cons:**
- ❌ NoSQL (different mental model from SQL)
- ❌ Complex queries limited
- ❌ Can get expensive at scale
- ❌ Vendor lock-in (hard to migrate away)

**Best for:**
- Mobile applications
- Real-time collaborative apps (chat, live dashboards)
- Apps needing offline-first functionality

**Quick Setup:**

```bash
# 1. Create project at https://firebase.google.com
# 2. Install SDK
npm install firebase

# 3. Initialize
import { initializeApp } from 'firebase/app'
import { getFirestore, collection, query, where, getDocs } from 'firebase/firestore'

const app = initializeApp(firebaseConfig)
const db = getFirestore(app)

# 4. Query
const q = query(
  collection(db, 'companies'),
  where('industry', '==', 'Technology')
)
const snapshot = await getDocs(q)

# 5. Realtime listener
onSnapshot(q, (snapshot) => {
  snapshot.docChanges().forEach((change) => {
    console.log('Change:', change.type, change.doc.data())
  })
})
```

---

### 5. MongoDB Atlas

**Overview:** Fully managed MongoDB (NoSQL) with generous free tier

**Type:** NoSQL (Document)

**Pricing:**
- **Free (M0):**
  - 512MB storage
  - Shared RAM
  - Limited to 3 clusters
- **Shared (M2):** $9/month (2GB)
- **Dedicated:** $57+/month

**Pros:**
- ✅ Flexible schema (documents, not tables)
- ✅ Great for hierarchical/nested data
- ✅ Excellent free tier
- ✅ Full-text search built-in
- ✅ Change streams (realtime)

**Cons:**
- ❌ NoSQL learning curve if coming from SQL
- ❌ Joins are complex (not designed for them)
- ❌ Eventual consistency can be tricky

**Best for:**
- Projects with evolving/flexible schemas
- Content management systems
- Catalogs with nested/hierarchical data
- Rapid prototyping

**Quick Setup:**

```bash
# 1. Create cluster at https://mongodb.com/atlas
# 2. Install driver
npm install mongodb mongoose

# 3. Connect with Mongoose
import mongoose from 'mongoose'

await mongoose.connect(process.env.MONGODB_URI)

# 4. Define schema
const companySchema = new mongoose.Schema({
  companyName: { type: String, required: true, unique: true },
  industry: String,
  metadata: mongoose.Schema.Types.Mixed,  // Flexible
  createdAt: { type: Date, default: Date.now }
})

const Company = mongoose.model('Company', companySchema)

# 5. Query
const companies = await Company.find({ industry: 'Technology' })
```

---

## Cloud Managed Databases

### 6. AWS RDS (Relational Database Service)

**Overview:** Managed PostgreSQL, MySQL, MariaDB, Oracle, SQL Server on AWS

**Type:** SQL (Relational) - Multiple engines

**Pricing:**
- **Free tier (12 months):**
  - 750 hours/month of db.t2.micro or db.t3.micro
  - 20GB storage
  - 20GB backups
- **After free tier:** ~$15-30/month for small instances

**Pros:**
- ✅ Fully managed (backups, patching, monitoring)
- ✅ Multiple database engines
- ✅ Deep AWS integration (VPC, IAM, CloudWatch)
- ✅ Read replicas, Multi-AZ deployments
- ✅ Battle-tested, highly reliable

**Cons:**
- ❌ More expensive than SaaS alternatives
- ❌ Requires AWS knowledge
- ❌ Less beginner-friendly

**Best for:**
- Production apps already on AWS
- Enterprise applications
- Apps needing high availability (Multi-AZ)

**Quick Setup:**

```bash
# 1. Create RDS instance via AWS Console or CLI
aws rds create-db-instance \
  --db-instance-identifier mydb \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password SecurePass123 \
  --allocated-storage 20

# 2. Get connection string from AWS Console
# 3. Connect like normal PostgreSQL
import { Pool } from 'pg'

const pool = new Pool({
  host: 'mydb.xxxxx.us-east-1.rds.amazonaws.com',
  port: 5432,
  database: 'mydb',
  user: 'admin',
  password: 'SecurePass123'
})
```

---

### 7. AWS Aurora

**Overview:** MySQL and PostgreSQL compatible database built for the cloud

**Type:** SQL (Relational) - MySQL or PostgreSQL compatible

**Pricing:**
- **Aurora Serverless v2:** Pay per ACU (Aurora Capacity Unit), scales to zero
- **Aurora Provisioned:** ~$29/month minimum

**Pros:**
- ✅ 5x faster than MySQL, 3x faster than PostgreSQL (AWS claims)
- ✅ Auto-scaling (Serverless v2)
- ✅ Automatic failover
- ✅ Compatible with MySQL/PostgreSQL drivers

**Cons:**
- ❌ AWS only (vendor lock-in)
- ❌ More expensive than RDS
- ❌ Minimum cost even with Serverless

**Best for:**
- High-performance applications on AWS
- Apps needing auto-scaling database
- Enterprise requiring 99.99% availability

---

### 8. Google Cloud SQL

**Overview:** Managed MySQL, PostgreSQL, SQL Server on Google Cloud

**Type:** SQL (Relational) - Multiple engines

**Pricing:**
- **Free trial:** $300 credit (90 days)
- **After trial:** ~$10-25/month for small instances

**Pros:**
- ✅ Fully managed
- ✅ Deep GCP integration
- ✅ Automatic backups, replication
- ✅ Good for apps on Google Cloud

**Cons:**
- ❌ Less generous free tier than AWS
- ❌ GCP ecosystem lock-in

**Best for:**
- Apps on Google Cloud Platform
- Integration with other GCP services

---

### 9. Azure Database

**Overview:** Managed MySQL, PostgreSQL, MariaDB on Microsoft Azure

**Type:** SQL (Relational) - Multiple engines

**Pricing:**
- **Free tier:** $200 credit for 30 days
- **After:** Similar to AWS RDS pricing

**Pros:**
- ✅ Fully managed
- ✅ Deep Azure integration
- ✅ Good for .NET applications

**Cons:**
- ❌ Azure ecosystem lock-in
- ❌ Less popular than AWS/GCP for startups

**Best for:**
- Apps on Microsoft Azure
- .NET/C# applications

---

## Self-Hosted Databases

### 10. PostgreSQL

**Overview:** World's most advanced open-source relational database

**Type:** SQL (Relational)

**Pricing:** Free (self-host) or use managed (Supabase, Neon, RDS)

**Pros:**
- ✅ Most feature-rich SQL database
- ✅ **JSONB** for flexible document storage
- ✅ **Extensions:** PostGIS (geo), TimescaleDB (time-series), pg_vector (embeddings)
- ✅ Full-text search built-in
- ✅ Excellent for complex queries
- ✅ Strong consistency, ACID compliant

**Cons:**
- ❌ Requires ops knowledge if self-hosting
- ❌ Can be overkill for simple projects

**Best for:**
- Complex applications needing advanced queries
- Projects requiring JSONB flexibility + SQL power
- Geospatial applications (with PostGIS)
- Time-series data (with TimescaleDB)

**Quick Setup (Self-hosted):**

```bash
# 1. Install (macOS)
brew install postgresql@16

# 2. Start
brew services start postgresql@16

# 3. Create database
createdb mydb

# 4. Connect
psql mydb

# 5. Or use Docker
docker run --name postgres -e POSTGRES_PASSWORD=mypass -p 5432:5432 -d postgres:16
```

---

### 11. MySQL

**Overview:** World's most popular open-source database

**Type:** SQL (Relational)

**Pricing:** Free (self-host) or use managed (PlanetScale, RDS)

**Pros:**
- ✅ Widely supported
- ✅ Great performance for read-heavy workloads
- ✅ Simpler than PostgreSQL for basic use

**Cons:**
- ❌ Less features than PostgreSQL
- ❌ JSON support weaker than PostgreSQL's JSONB

**Best for:**
- Web applications (WordPress, Drupal use MySQL)
- Read-heavy workloads
- Teams familiar with MySQL

---

### 12. SQLite

**Overview:** Embedded SQL database in a single file

**Type:** SQL (Embedded)

**Pricing:** Free

**Pros:**
- ✅ **Zero configuration** - just a file
- ✅ Perfect for local development
- ✅ Great for edge/serverless (Cloudflare D1, Turso)
- ✅ Small footprint

**Cons:**
- ❌ Not for high concurrent writes
- ❌ Limited for production web apps
- ❌ No built-in replication

**Best for:**
- Prototyping
- Mobile apps
- Edge/serverless with low writes (Turso, Cloudflare D1)
- Embedded applications

**Quick Setup:**

```python
import sqlite3

# Creates file if doesn't exist
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
  CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    industry TEXT
  )
''')
```

---

### 13. MongoDB (Self-hosted)

**Overview:** Popular NoSQL document database

**Type:** NoSQL (Document)

**Pricing:** Free (self-host) or use managed (MongoDB Atlas)

**Pros:**
- ✅ Flexible schema
- ✅ Horizontal scaling (sharding)
- ✅ Good for rapid iteration

**Cons:**
- ❌ Requires ops knowledge if self-hosting
- ❌ Different query language (not SQL)

**Best for:**
- Same as MongoDB Atlas, but when you want full control

---

## Special Purpose Databases

### 14. Redis

**Overview:** In-memory key-value store

**Type:** Key-Value (Cache/Database)

**Pricing:**
- **Redis Cloud:** Free 30MB
- **Self-hosted:** Free
- **AWS ElastiCache:** ~$15/month minimum

**Pros:**
- ✅ Extremely fast (in-memory)
- ✅ Great for caching
- ✅ Pub/sub, queues

**Cons:**
- ❌ Not for primary database (use as cache)
- ❌ Data loss risk if not configured properly

**Best for:**
- Caching layer
- Session storage
- Real-time leaderboards
- Rate limiting

---

### 15. ClickHouse

**Overview:** Column-oriented database for analytics

**Type:** SQL (Columnar/OLAP)

**Pricing:**
- **ClickHouse Cloud:** Free tier
- **Self-hosted:** Free

**Pros:**
- ✅ Extremely fast for analytics
- ✅ Handles billions of rows
- ✅ Great for logs, metrics, events

**Cons:**
- ❌ Not for transactional workloads
- ❌ No updates/deletes (append-only)

**Best for:**
- Analytics dashboards
- Log aggregation
- Time-series data at scale

---

## Decision Framework

### Start with these questions:

**1. What's your data model?**
- **Relational (tables with relationships)** → PostgreSQL, MySQL
- **Documents/Nested data** → MongoDB, Firebase
- **Key-value/Cache** → Redis
- **Analytics/Logs** → ClickHouse

**2. What's your budget?**
- **Free tier needed** → Supabase, MongoDB Atlas, PlanetScale
- **Budget < $50/month** → Supabase Pro, Neon, PlanetScale
- **Enterprise** → AWS Aurora, dedicated managed services

**3. What's your ops capacity?**
- **No ops team** → Supabase, PlanetScale, Firebase
- **Some ops** → Neon, MongoDB Atlas, AWS RDS
- **Full ops team** → Self-hosted PostgreSQL, MySQL

**4. What features do you need?**
- **Realtime** → Supabase, Firebase
- **Branching** → PlanetScale, Neon
- **Auth + Storage + DB** → Supabase, Firebase
- **Just database** → Neon, RDS, self-hosted

---

## Migration Paths

### Common migrations:

**SQLite → PostgreSQL:**
```bash
# Export from SQLite
sqlite3 database.db .dump > dump.sql

# Clean up SQLite-specific syntax
sed 's/INTEGER PRIMARY KEY AUTOINCREMENT/SERIAL PRIMARY KEY/g' dump.sql > pg_dump.sql

# Import to PostgreSQL
psql -d mydb -f pg_dump.sql
```

**Firebase → Supabase:**
1. Export Firebase data via Firebase Console
2. Transform JSON to relational schema
3. Import via Supabase SQL editor or client SDK

**MongoDB → PostgreSQL:**
1. Use JSONB columns for flexible data
2. Export MongoDB collections as JSON
3. Import to PostgreSQL JSONB columns
4. Gradually normalize as schema stabilizes

---

## Summary Recommendations

| Project Type | Recommendation | Why |
|--------------|----------------|-----|
| **MVP / Startup** | Supabase | All-in-one, free tier, fast setup |
| **Mobile app** | Firebase or Supabase | Realtime, offline support, auth |
| **Serverless** | PlanetScale or Neon | Auto-scaling, pay-per-use |
| **AWS ecosystem** | AWS RDS or Aurora | Deep integration |
| **Self-hosted / Full control** | PostgreSQL | Most powerful, flexible |
| **Analytics** | ClickHouse | Built for scale |
| **Prototyping** | SQLite or Supabase | Zero/low setup |
| **E-commerce** | PostgreSQL (Supabase/RDS) | Transactions, complex queries |
| **Content/CMS** | MongoDB Atlas | Flexible schema |

**When in doubt, start with Supabase.** It's free, fast to setup, and scales well. You can always migrate later.
