# Schema Design Patterns

Common database schema patterns for various use cases.

## Table of Contents

1. [User Management & Authentication](#1-user-management--authentication)
2. [E-commerce](#2-e-commerce)
3. [Blog / CMS](#3-blog--cms)
4. [Multi-tenancy](#4-multi-tenancy)
5. [Audit Logging](#5-audit-logging)
6. [File/Media Metadata](#6-filemedia-metadata)
7. [Social Features](#7-social-features)
8. [Analytics/Events](#8-analyticsevents)
9. [Notifications](#9-notifications)
10. [Tags/Categories](#10-tagscategories)

---

## 1. User Management & Authentication

**Use case:** User registration, login, profiles, roles

**Schema:**

```sql
-- Core users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT,  -- Only if using password auth
    full_name TEXT,
    avatar_url TEXT,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_login_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE
);

-- Sessions (for JWT alternatives or server-side sessions)
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- Roles and permissions (RBAC)
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE role_permissions (
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

**Common queries:**

```sql
-- Get user with roles and permissions
SELECT u.*, array_agg(DISTINCT r.name) as roles,
       array_agg(DISTINCT p.name) as permissions
FROM users u
LEFT JOIN user_roles ur ON u.id = ur.user_id
LEFT JOIN roles r ON ur.role_id = r.id
LEFT JOIN role_permissions rp ON r.id = rp.role_id
LEFT JOIN permissions p ON rp.permission_id = p.id
WHERE u.email = 'user@example.com'
GROUP BY u.id;

-- Clean expired sessions
DELETE FROM sessions WHERE expires_at < NOW();
```

---

## 2. E-commerce

**Use case:** Products, orders, shopping cart, inventory

**Schema:**

```sql
-- Products
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id UUID REFERENCES categories(id),
    sku TEXT UNIQUE,
    stock_quantity INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Shopping cart
CREATE TABLE cart_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    added_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, product_id)
);

-- Orders
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    status TEXT CHECK (status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(10, 2) NOT NULL,
    shipping_address JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,  -- Store price at time of purchase
    PRIMARY KEY (order_id, product_id)
);

-- Inventory transactions (for tracking stock changes)
CREATE TABLE inventory_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES products(id),
    quantity_change INTEGER NOT NULL,
    transaction_type TEXT CHECK (transaction_type IN ('purchase', 'sale', 'return', 'adjustment')),
    reference_id UUID,  -- Order ID or other reference
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

**Best practices:**
- Store `price_at_purchase` in `order_items` (prices change over time)
- Use `DECIMAL` for money (not FLOAT)
- Consider soft deletes for products (set `is_active = FALSE`)
- Track inventory changes for auditing

---

## 3. Blog / CMS

**Use case:** Blog posts, comments, authors

**Schema:**

```sql
-- Posts
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id UUID REFERENCES users(id),
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    content TEXT,
    excerpt TEXT,
    featured_image_url TEXT,
    status TEXT CHECK (status IN ('draft', 'published', 'archived')),
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    view_count INTEGER DEFAULT 0
);

-- Comments
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    parent_comment_id UUID REFERENCES comments(id),  -- For nested comments
    content TEXT NOT NULL,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Post tags (many-to-many)
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    slug TEXT UNIQUE NOT NULL
);

CREATE TABLE post_tags (
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

-- Indexes
CREATE INDEX idx_posts_author_id ON posts(author_id);
CREATE INDEX idx_posts_status ON posts(status);
CREATE INDEX idx_posts_published_at ON posts(published_at);
CREATE INDEX idx_posts_slug ON posts(slug);
CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_parent_id ON comments(parent_comment_id);
```

**Common queries:**

```sql
-- Get published posts with author and tags
SELECT p.*, u.full_name as author_name,
       array_agg(t.name) as tags
FROM posts p
JOIN users u ON p.author_id = u.id
LEFT JOIN post_tags pt ON p.id = pt.post_id
LEFT JOIN tags t ON pt.tag_id = t.id
WHERE p.status = 'published'
  AND p.published_at <= NOW()
GROUP BY p.id, u.full_name
ORDER BY p.published_at DESC
LIMIT 10;

-- Get comment thread (nested comments)
WITH RECURSIVE comment_tree AS (
  SELECT *, 0 as depth
  FROM comments
  WHERE post_id = $1 AND parent_comment_id IS NULL

  UNION ALL

  SELECT c.*, ct.depth + 1
  FROM comments c
  JOIN comment_tree ct ON c.parent_comment_id = ct.id
)
SELECT * FROM comment_tree ORDER BY created_at;
```

---

## 4. Multi-tenancy

**Use case:** SaaS apps with multiple organizations/workspaces

**Pattern A: Shared schema with tenant_id (simpler)**

```sql
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    plan TEXT,  -- free, pro, enterprise
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- All tables include tenant_id
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    status TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- CRITICAL: Add indexes on tenant_id for all tables
CREATE INDEX idx_projects_tenant_id ON projects(tenant_id);
CREATE INDEX idx_tasks_tenant_id ON tasks(tenant_id);

-- Row-level security (Supabase/PostgreSQL)
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON projects
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
```

**Pattern B: Separate schemas per tenant (isolation)**

```sql
-- Create schema per tenant
CREATE SCHEMA tenant_acme;
CREATE SCHEMA tenant_bigco;

-- Each schema has same structure
CREATE TABLE tenant_acme.projects (...);
CREATE TABLE tenant_bigco.projects (...);

-- Switch between tenants
SET search_path TO tenant_acme;
SELECT * FROM projects;  -- Queries tenant_acme.projects
```

**Best practices:**
- Pattern A (shared) is simpler, easier to manage migrations
- Pattern B (separate schemas) provides better isolation, but complex to manage
- Always filter by `tenant_id` in WHERE clauses
- Use Row-Level Security (RLS) for automatic enforcement

---

## 5. Audit Logging

**Use case:** Track all changes to data for compliance/debugging

**Schema:**

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name TEXT NOT NULL,
    record_id UUID NOT NULL,
    action TEXT CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_data JSONB,
    new_data JSONB,
    changed_by UUID REFERENCES users(id),
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- Indexes
CREATE INDEX idx_audit_logs_table_record ON audit_logs(table_name, record_id);
CREATE INDEX idx_audit_logs_changed_at ON audit_logs(changed_at);
CREATE INDEX idx_audit_logs_changed_by ON audit_logs(changed_by);

-- Trigger example (PostgreSQL)
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_logs (table_name, record_id, action, old_data, changed_by)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', to_jsonb(OLD), current_setting('app.current_user_id', TRUE)::UUID);
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_logs (table_name, record_id, action, old_data, new_data, changed_by)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW), current_setting('app.current_user_id', TRUE)::UUID);
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_logs (table_name, record_id, action, new_data, changed_by)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', to_jsonb(NEW), current_setting('app.current_user_id', TRUE)::UUID);
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables you want to audit
CREATE TRIGGER audit_companies
AFTER INSERT OR UPDATE OR DELETE ON companies
FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
```

**Best practices:**
- Store full `old_data` and `new_data` as JSONB
- Consider partitioning audit_logs by date for large volumes
- Separate audit DB for security-critical applications

---

## 6. File/Media Metadata

**Use case:** Store metadata about uploaded files (images, PDFs, etc.)

**Schema:**

```sql
CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    filename TEXT NOT NULL,
    original_filename TEXT,
    mime_type TEXT,
    file_size BIGINT,  -- bytes
    storage_path TEXT NOT NULL,  -- S3 key, Supabase storage path, etc.
    storage_bucket TEXT,
    public_url TEXT,
    thumbnail_url TEXT,
    metadata JSONB,  -- image dimensions, duration (video), etc.
    uploaded_at TIMESTAMPTZ DEFAULT NOW(),
    is_public BOOLEAN DEFAULT FALSE
);

-- Indexes
CREATE INDEX idx_files_user_id ON files(user_id);
CREATE INDEX idx_files_uploaded_at ON files(uploaded_at);
CREATE INDEX idx_files_mime_type ON files(mime_type);
```

**Example metadata (JSONB):**

```json
{
  "width": 1920,
  "height": 1080,
  "format": "jpeg",
  "exif": {...}
}
```

**Common queries:**

```sql
-- Get user's images
SELECT * FROM files
WHERE user_id = $1 AND mime_type LIKE 'image/%'
ORDER BY uploaded_at DESC;

-- Get files larger than 10MB
SELECT * FROM files
WHERE file_size > 10485760
ORDER BY file_size DESC;
```

---

## 7. Social Features

**Use case:** Likes, follows, shares

**Schema:**

```sql
-- Likes (polymorphic - can like posts, comments, etc.)
CREATE TABLE likes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    likeable_type TEXT NOT NULL,  -- 'post', 'comment', etc.
    likeable_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, likeable_type, likeable_id)
);

-- Follows
CREATE TABLE follows (
    follower_id UUID REFERENCES users(id) ON DELETE CASCADE,
    following_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (follower_id, following_id),
    CHECK (follower_id != following_id)
);

-- Shares
CREATE TABLE shares (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    shareable_type TEXT NOT NULL,
    shareable_id UUID NOT NULL,
    platform TEXT,  -- 'twitter', 'facebook', 'email', etc.
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_likes_likeable ON likes(likeable_type, likeable_id);
CREATE INDEX idx_likes_user_id ON likes(user_id);
CREATE INDEX idx_follows_follower_id ON follows(follower_id);
CREATE INDEX idx_follows_following_id ON follows(following_id);
```

**Common queries:**

```sql
-- Get post with like count and whether current user liked it
SELECT p.*,
       COUNT(l.id) as like_count,
       EXISTS(SELECT 1 FROM likes WHERE likeable_type = 'post'
              AND likeable_id = p.id AND user_id = $1) as user_liked
FROM posts p
LEFT JOIN likes l ON l.likeable_type = 'post' AND l.likeable_id = p.id
WHERE p.id = $2
GROUP BY p.id;

-- Get followers count
SELECT COUNT(*) FROM follows WHERE following_id = $1;

-- Get following count
SELECT COUNT(*) FROM follows WHERE follower_id = $1;

-- Check if user A follows user B
SELECT EXISTS(SELECT 1 FROM follows
              WHERE follower_id = $1 AND following_id = $2);
```

---

## 8. Analytics/Events

**Use case:** Track user events, page views, custom events

**Schema:**

```sql
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_name TEXT NOT NULL,
    user_id UUID REFERENCES users(id),
    session_id UUID,
    properties JSONB,  -- Flexible event properties
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- Indexes for time-series queries
CREATE INDEX idx_events_timestamp ON events(timestamp DESC);
CREATE INDEX idx_events_user_id_timestamp ON events(user_id, timestamp DESC);
CREATE INDEX idx_events_event_name_timestamp ON events(event_name, timestamp DESC);
CREATE INDEX idx_events_properties ON events USING GIN(properties);

-- For high volume, consider partitioning by time
CREATE TABLE events_2025_01 PARTITION OF events
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

**Example events:**

```sql
-- Page view
INSERT INTO events (event_name, user_id, properties)
VALUES ('page_view', $1, '{"url": "/products", "referrer": "google.com"}');

-- Purchase
INSERT INTO events (event_name, user_id, properties)
VALUES ('purchase', $1, '{"product_id": "123", "amount": 99.99, "currency": "USD"}');
```

**Common queries:**

```sql
-- Events in last 7 days
SELECT event_name, COUNT(*)
FROM events
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY event_name
ORDER BY COUNT(*) DESC;

-- User journey
SELECT event_name, properties->>'url', timestamp
FROM events
WHERE user_id = $1
ORDER BY timestamp DESC
LIMIT 50;
```

---

## 9. Notifications

**Use case:** In-app notifications, push notifications

**Schema:**

```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    notification_type TEXT NOT NULL,  -- 'comment', 'like', 'mention', etc.
    title TEXT NOT NULL,
    body TEXT,
    action_url TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    read_at TIMESTAMPTZ
);

-- Indexes
CREATE INDEX idx_notifications_user_id_created_at ON notifications(user_id, created_at DESC);
CREATE INDEX idx_notifications_is_read ON notifications(is_read) WHERE NOT is_read;
```

**Common queries:**

```sql
-- Get unread notifications
SELECT * FROM notifications
WHERE user_id = $1 AND is_read = FALSE
ORDER BY created_at DESC;

-- Mark as read
UPDATE notifications
SET is_read = TRUE, read_at = NOW()
WHERE id = $1;

-- Get unread count
SELECT COUNT(*) FROM notifications
WHERE user_id = $1 AND is_read = FALSE;
```

---

## 10. Tags/Categories

**Use case:** Flexible tagging system (many-to-many)

**Schema:**

```sql
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Polymorphic tagging (can tag multiple entity types)
CREATE TABLE taggings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    taggable_type TEXT NOT NULL,  -- 'post', 'product', etc.
    taggable_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tag_id, taggable_type, taggable_id)
);

-- Indexes
CREATE INDEX idx_taggings_taggable ON taggings(taggable_type, taggable_id);
CREATE INDEX idx_taggings_tag_id ON taggings(tag_id);
```

**Common queries:**

```sql
-- Get posts with tag "technology"
SELECT p.*
FROM posts p
JOIN taggings tg ON tg.taggable_type = 'post' AND tg.taggable_id = p.id
JOIN tags t ON tg.tag_id = t.id
WHERE t.slug = 'technology';

-- Get all tags for a post
SELECT t.*
FROM tags t
JOIN taggings tg ON tg.tag_id = t.id
WHERE tg.taggable_type = 'post' AND tg.taggable_id = $1;

-- Get popular tags
SELECT t.name, COUNT(tg.id) as usage_count
FROM tags t
JOIN taggings tg ON tg.tag_id = t.id
GROUP BY t.id
ORDER BY usage_count DESC
LIMIT 20;
```

---

## General Best Practices

### Naming Conventions
- **Tables**: Plural nouns (`users`, `posts`, not `user`, `post`)
- **Columns**: Snake_case (`created_at`, not `createdAt`)
- **Foreign keys**: `{table}_id` (e.g., `user_id`)
- **Timestamps**: Always use `TIMESTAMPTZ` (timezone-aware)
- **IDs**: Use `UUID` for distributed systems, `SERIAL`/`BIGSERIAL` for single server

### Indexes
- Index foreign keys
- Index columns used in WHERE, ORDER BY, GROUP BY
- Use composite indexes for multi-column queries
- Don't over-index (each index slows writes)

### Data Types
- Money: `DECIMAL(10, 2)` (never FLOAT)
- Timestamps: `TIMESTAMPTZ` (not TIMESTAMP)
- JSON: `JSONB` (not JSON) for PostgreSQL
- Text: `TEXT` (not VARCHAR unless you need length limit)
- IDs: `UUID` or `BIGSERIAL`

### Soft Deletes
```sql
ALTER TABLE posts ADD COLUMN deleted_at TIMESTAMPTZ;

-- Query only non-deleted
SELECT * FROM posts WHERE deleted_at IS NULL;

-- Soft delete
UPDATE posts SET deleted_at = NOW() WHERE id = $1;
```

### Timestamps
Always include:
```sql
created_at TIMESTAMPTZ DEFAULT NOW(),
updated_at TIMESTAMPTZ DEFAULT NOW()
```

Add trigger for `updated_at`:
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_posts_updated_at
BEFORE UPDATE ON posts
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## Conclusion

These patterns cover 90% of common application needs. Mix and match based on your requirements. When in doubt:

1. Start simple (fewer tables)
2. Add complexity as needed
3. Use JSONB for flexible data
4. Index strategically
5. Test with realistic data volumes

For specific database features (PostGIS, full-text search, etc.), consult `DATABASE_OPTIONS.md`.
