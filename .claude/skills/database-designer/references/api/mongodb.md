## MongoDB Atlas

**Official Documentation**: https://www.mongodb.com/docs/drivers/node/current/
**GitHub**: https://github.com/mongodb/node-mongodb-native
**npm**: `mongodb`

### Installation

```bash
npm install mongodb
```

### Connection Setup

```typescript
import { MongoClient } from 'mongodb'

const uri = process.env.MONGODB_URI
const client = new MongoClient(uri)

await client.connect()
const db = client.db('my-database')
const collection = db.collection('companies')
```

### CRUD Operations

```typescript
// CREATE (Insert One)
const result = await collection.insertOne({
  name: 'Acme Corp',
  industry: 'Technology'
})
console.log('Inserted ID:', result.insertedId)

// CREATE (Insert Many)
const result = await collection.insertMany([
  { name: 'Company 1', industry: 'Tech' },
  { name: 'Company 2', industry: 'Finance' }
])

// READ (Find One)
const company = await collection.findOne({ name: 'Acme Corp' })

// READ (Find Many)
const companies = await collection
  .find({ industry: 'Technology' })
  .sort({ createdAt: -1 })
  .limit(10)
  .toArray()

// UPDATE (Update One)
const result = await collection.updateOne(
  { name: 'Acme Corp' },
  { $set: { industry: 'FinTech' } }
)

// UPDATE (Update Many)
const result = await collection.updateMany(
  { industry: 'Technology' },
  { $set: { category: 'Tech' } }
)

// DELETE (Delete One)
const result = await collection.deleteOne({ name: 'Acme Corp' })

// DELETE (Delete Many)
const result = await collection.deleteMany({ industry: 'Technology' })
```

### Aggregation

```typescript
const pipeline = [
  { $match: { industry: 'Technology' } },
  { $group: { _id: '$category', count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 10 }
]

const results = await collection.aggregate(pipeline).toArray()
```

### Transactions

```typescript
const session = client.startSession()

try {
  await session.withTransaction(async () => {
    await collection.insertOne({ name: 'Company A' }, { session })
    await anotherCollection.updateOne(
      { userId: 123 },
      { $inc: { count: 1 } },
      { session }
    )
  })
} finally {
  await session.endSession()
}
```

**Full Driver Reference**: https://www.mongodb.com/docs/drivers/node/current/quick-reference/

---

