## Supabase (PostgreSQL)

**Official Documentation**: https://supabase.com/docs/reference/javascript/introduction
**GitHub**: https://github.com/supabase/supabase-js
**npm**: `@supabase/supabase-js`

### Installation

```bash
npm install @supabase/supabase-js
```

### Connection Setup

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key'
)
```

### CRUD Operations

```typescript
// CREATE (Insert)
const { data, error } = await supabase
  .from('companies')
  .insert([
    { name: 'Acme Corp', industry: 'Technology' }
  ])
  .select()

// READ (Select)
const { data, error } = await supabase
  .from('companies')
  .select('*')
  .eq('industry', 'Technology')
  .order('created_at', { ascending: false })
  .limit(10)

// UPDATE
const { data, error } = await supabase
  .from('companies')
  .update({ industry: 'FinTech' })
  .eq('id', 123)
  .select()

// DELETE
const { data, error } = await supabase
  .from('companies')
  .delete()
  .eq('id', 123)

// UPSERT (Insert or Update)
const { data, error } = await supabase
  .from('companies')
  .upsert({ id: 123, name: 'Updated Name' })
  .select()
```

### Realtime Subscriptions

```typescript
// Subscribe to INSERT events
const channel = supabase
  .channel('companies-changes')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'companies'
    },
    (payload) => {
      console.log('New company:', payload.new)
    }
  )
  .subscribe()

// Unsubscribe
channel.unsubscribe()
```

### Filtering

```typescript
// Equality
.eq('column', 'value')

// Greater than / Less than
.gt('column', value)
.lt('column', value)
.gte('column', value)
.lte('column', value)

// Pattern matching
.like('column', '%pattern%')
.ilike('column', '%pattern%')  // Case-insensitive

// IN operator
.in('column', ['value1', 'value2'])

// NULL checks
.is('column', null)

// Range
.range(0, 9)  // Pagination
```

**Full API Reference**: https://supabase.com/docs/reference/javascript/select

---

