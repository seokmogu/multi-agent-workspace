# Migration Strategies: LangGraph → A2A

Step-by-step guide for migrating from monolithic LangGraph agents to distributed A2A (Agent2Agent) architecture.

## Table of Contents

1. [Overview](#overview)
2. [When to Migrate](#when-to-migrate)
3. [Migration Phases](#migration-phases)
4. [Technical Details](#technical-details)
5. [Cost Optimization](#cost-optimization)
6. [Troubleshooting](#troubleshooting)

---

## Overview

### Current State: v2.0 (LangGraph Monolith)

```
Single Python Process
├── Research Phase  (query generation + search)
├── Extract Phase   (JSON extraction)
└── Reflect Phase   (quality evaluation)

Performance:
- 45-90 sec/item
- Sequential processing
- In-memory state
- Vertical scaling only
- ~1,920 items/day capacity
```

### Target State: v3.0 (A2A Distributed)

```
Distributed HTTP Services
├── Coordinator (FastAPI orchestrator)
├── Research Agents (10 pods, ECS Fargate)
├── Extract Agents (5 pods, ECS Fargate)
└── Reflect Agents (Lambda functions)

Performance:
- 90 sec/1,000 items
- Parallel processing (100+ concurrent)
- Database-backed state (Aurora Serverless)
- Horizontal scaling
- Unlimited capacity
```

### Expected Improvements

| Metric | v2.0 | v3.0 | Improvement |
|--------|------|------|-------------|
| **1,000 items** | 12-25 hours | 90 seconds | **480-1000x faster** |
| **Throughput** | 80/hour | 400/hour | **5x** |
| **Concurrent** | 1 | 100+ | **100x** |
| **Cost/month** | $5,222 | $464 | **91% reduction** |
| **Scalability** | Vertical | Horizontal | **Unlimited** |

---

## When to Migrate

### Migrate to A2A When:

✅ **Volume**: Processing 100+ items per batch regularly
✅ **Speed**: Current processing time is bottleneck (hours → minutes needed)
✅ **Scale**: Need to scale beyond single machine capacity
✅ **Reliability**: Need fault tolerance and auto-recovery
✅ **Cost**: Want to optimize cloud costs (91% reduction possible)
✅ **Independence**: Different agents scale at different rates

### Stay with LangGraph When:

❌ **Low Volume**: < 50 items per batch
❌ **Prototype**: Still iterating on core logic
❌ **Team Size**: Small team unfamiliar with distributed systems
❌ **Simplicity**: Development speed > runtime performance
❌ **Budget**: No cloud infrastructure budget

---

## Migration Phases

### Timeline: 7 Weeks Total

```
Week 1-2: Hybrid Wrapper
Week 3-4: Infrastructure Setup
Week 5-6: Performance Optimization
Week 7:   Production Deployment
```

### Phase 1: Hybrid Wrapper (Weeks 1-2)

**Goal**: Add A2A interfaces without changing existing code.

**Strategy**: Keep existing LangGraph logic, wrap with A2A HTTP endpoints.

#### Step 1.1: Create Research Agent Wrapper

```python
# src/agents/a2a/research_agent/app.py
from fastapi import FastAPI
from src.agents.company_research.research import research_node  # ← Reuse!
from src.agents.company_research.state import ResearchState

app = FastAPI()

@app.get("/.well-known/agent.json")
async def agent_card():
    """A2A Discovery endpoint."""
    return {
        "name": "research-agent",
        "capabilities": ["web_search", "note_taking"],
        "version": "1.0.0"
    }

@app.post("/tasks/send")
async def handle_task(task: dict):
    """A2A Task execution."""
    # Convert A2A format → LangGraph state
    state = {
        "company_name": task["message"]["parts"][0]["text"],
        # ... other fields
    }

    # Call existing LangGraph node!
    result = await research_node(state, config)

    # Convert LangGraph state → A2A format
    return {
        "id": task["id"],
        "status": {"state": "completed"},
        "messages": [{
            "role": "assistant",
            "parts": [{"text": str(result["research_notes"])}]
        }]
    }
```

**Benefits**:
- ✅ Reuses 100% of existing logic
- ✅ No changes to core algorithms
- ✅ Can run both v2.0 and v3.0 simultaneously
- ✅ Low risk, gradual migration

#### Step 1.2: Create Extraction Agent Wrapper

Same pattern for extraction:

```python
# src/agents/a2a/extraction_agent/app.py
from src.agents.company_research.extraction import extract_node

@app.post("/tasks/send")
async def handle_task(task: dict):
    # Reuse existing extract_node()
    result = await extract_node(state, config)
    return a2a_format(result)
```

#### Step 1.3: Create Coordinator

```python
# src/agents/a2a/coordinator/app.py
import httpx

async def process_company(company_name: str):
    """Orchestrate A2A workflow."""
    # 1. Call research agent
    research_result = await httpx.post(
        "http://research-agent:5001/tasks/send",
        json={"id": "task-1", "message": {...}}
    )

    # 2. Call extraction agent
    extract_result = await httpx.post(
        "http://extraction-agent:5002/tasks/send",
        json={"id": "task-2", "message": {...}}
    )

    return extract_result
```

#### Step 1.4: Local Testing with Docker Compose

```yaml
# docker-compose.a2a.yml
version: '3.8'
services:
  coordinator:
    build: ./src/agents/a2a/coordinator
    ports:
      - "5000:5000"

  research-agent:
    build: ./src/agents/a2a/research_agent
    ports:
      - "5001:5001"
    environment:
      - TAVILY_API_KEY=${TAVILY_API_KEY}

  extraction-agent:
    build: ./src/agents/a2a/extraction_agent
    ports:
      - "5002:5002"
```

**Test locally**:
```bash
docker-compose -f docker-compose.a2a.yml up
curl http://localhost:5000/process?company=Acme
```

**Milestone**: A2A system works locally with 1 pod per agent.

---

### Phase 2: Infrastructure Setup (Weeks 3-4)

**Goal**: Deploy to AWS with auto-scaling infrastructure.

#### Step 2.1: Create VPC and Networking

```hcl
# terraform/vpc.tf
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
}

# VPC Endpoints (eliminates NAT Gateway costs)
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.${var.region}.s3"
}
```

#### Step 2.2: Create ECS Cluster

```hcl
# terraform/ecs.tf
resource "aws_ecs_cluster" "agents" {
  name = "multi-agent-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# Research Agent Service (10 pods)
resource "aws_ecs_service" "research" {
  name            = "research-agent"
  cluster         = aws_ecs_cluster.agents.id
  task_definition = aws_ecs_task_definition.research.arn
  desired_count   = 10  # Scale up!

  capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"  # 70% cheaper!
    weight            = 100
  }

  network_configuration {
    subnets         = aws_subnet.private[*].id
    security_groups = [aws_security_group.agents.id]
  }
}
```

#### Step 2.3: Create Aurora Serverless Database

```hcl
# terraform/rds.tf
resource "aws_rds_cluster" "state_db" {
  cluster_identifier      = "agent-state-db"
  engine                  = "aurora-postgresql"
  engine_mode             = "provisioned"
  serverlessv2_scaling_configuration {
    min_capacity = 0.5  # Scales down when idle
    max_capacity = 2.0  # Scales up under load
  }
  database_name           = "agent_state"
  master_username         = "admin"
  master_password         = random_password.db_password.result
}
```

#### Step 2.4: Deploy with Terraform

```bash
cd terraform
terraform init
terraform plan
terraform apply

# Output:
# Apply complete! Resources: 47 added, 0 changed, 0 destroyed.
#
# Outputs:
# coordinator_url = "https://coordinator.example.com"
# research_agent_url = "http://research-agent.local:5001"
```

**Milestone**: A2A system deployed to AWS with 10 research pods, 5 extraction pods.

---

### Phase 3: Performance Optimization (Weeks 5-6)

**Goal**: Achieve 90 seconds for 1,000 items.

#### Step 3.1: Load Testing

```python
# tests/load_test.py
import asyncio
import httpx
import time

async def test_1000_companies():
    companies = ["Company " + str(i) for i in range(1000)]

    start = time.time()

    async with httpx.AsyncClient() as client:
        tasks = [
            client.post(
                "https://coordinator.example.com/process",
                json={"company": company}
            )
            for company in companies
        ]
        results = await asyncio.gather(*tasks)

    duration = time.time() - start
    success_count = sum(1 for r in results if r.status_code == 200)

    print(f"Duration: {duration:.1f} seconds")
    print(f"Success: {success_count}/1000")
    print(f"Throughput: {1000/duration:.1f} items/sec")

# Target: < 120 seconds
```

#### Step 3.2: Caching Strategy

**Goal**: 90% cache hit rate for repeated queries.

```python
# src/common/cache.py
import redis

redis_client = redis.Redis(
    host="elasticache.example.com",
    port=6379,
    decode_responses=True
)

def get_cached_search(query: str):
    """Get cached search results."""
    cache_key = f"search:{hash(query)}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    return None

def cache_search(query: str, results: dict, ttl: int = 86400):
    """Cache search results for 24 hours."""
    cache_key = f"search:{hash(query)}"
    redis_client.setex(
        cache_key,
        ttl,
        json.dumps(results)
    )
```

**Impact**: 90% fewer Tavily API calls = $0.0005/item → $0.00005/item.

#### Step 3.3: Auto-Scaling Tuning

```hcl
# terraform/autoscaling.tf
resource "aws_appautoscaling_target" "research" {
  max_capacity       = 20  # Scale up to 20 pods
  min_capacity       = 2   # Scale down to 2 pods
  resource_id        = "service/multi-agent-cluster/research-agent"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "research_cpu" {
  name               = "research-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.research.resource_id
  scalable_dimension = aws_appautoscaling_target.research.scalable_dimension
  service_namespace  = aws_appautoscaling_target.research.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 70.0  # Target 70% CPU
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    scale_in_cooldown  = 300   # Wait 5 min before scaling down
    scale_out_cooldown = 60    # Wait 1 min before scaling up
  }
}
```

#### Step 3.4: Connection Pooling

```python
# src/common/db.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://admin:password@aurora.example.com/agent_state",
    poolclass=QueuePool,
    pool_size=20,        # 20 connections per pod
    max_overflow=10,     # +10 overflow
    pool_pre_ping=True,  # Check connections before use
    pool_recycle=3600    # Recycle every hour
)
```

**Milestone**: 1,000 items in < 120 seconds, 95%+ success rate.

---

### Phase 4: Production Deployment (Week 7)

**Goal**: Blue-green deployment with zero downtime.

#### Step 4.1: Blue-Green Strategy

```
┌─────────────────┐
│ Load Balancer   │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌──────┐  ┌──────┐
│ Blue │  │Green │
│(v2.0)│  │(v3.0)│
└──────┘  └──────┘

Traffic:
Day 0:  100% Blue,    0% Green
Day 1:   90% Blue,   10% Green  (canary)
Day 3:   50% Blue,   50% Green
Day 5:   10% Blue,   90% Green
Day 7:    0% Blue,  100% Green  (complete)
```

#### Step 4.2: Monitoring Dashboard

```python
# CloudWatch Metrics
metrics = [
    "AgentRequestCount",
    "AgentErrorRate",
    "AgentLatencyP99",
    "DatabaseConnectionPool",
    "CacheHitRate",
    "TavilyAPICost"
]

# Alarms
if error_rate > 5%:
    rollback_to_blue()

if latency_p99 > 10_seconds:
    scale_up_agents()

if cache_hit_rate < 80%:
    alert_team("Cache degradation detected")
```

#### Step 4.3: Rollback Plan

If issues detected:
1. **Immediate**: Route 100% traffic back to Blue (v2.0)
2. **Investigate**: Check logs, metrics, database
3. **Fix**: Deploy hotfix to Green
4. **Retry**: Gradual traffic shift again

**Milestone**: v3.0 serving 100% production traffic, v2.0 decommissioned.

---

## Technical Details

### A2A Protocol Specification

#### Agent Card (Discovery)

```json
GET /.well-known/agent.json

{
  "name": "research-agent",
  "description": "Web search and note-taking agent",
  "version": "1.0.0",
  "capabilities": [
    "web_search",
    "note_taking"
  ],
  "input_schema": {
    "type": "object",
    "properties": {
      "company_name": {"type": "string"},
      "max_queries": {"type": "integer", "default": 3}
    },
    "required": ["company_name"]
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "research_notes": {"type": "string"}
    }
  }
}
```

#### Task Execution

```json
POST /tasks/send

Request:
{
  "id": "task-abc-123",
  "message": {
    "role": "user",
    "parts": [
      {
        "text": "{\"company_name\": \"Acme Corp\", \"max_queries\": 5}"
      }
    ]
  }
}

Response:
{
  "id": "task-abc-123",
  "status": {
    "state": "completed",
    "started_at": "2025-10-24T10:00:00Z",
    "completed_at": "2025-10-24T10:00:45Z"
  },
  "messages": [
    {
      "role": "assistant",
      "parts": [
        {
          "text": "{\"research_notes\": \"...\"}"
        }
      ]
    }
  ]
}
```

### State Management

#### v2.0: In-Memory State

```python
# TypedDict in memory
state = {
    "company_name": "Acme",
    "research_notes": "...",
    "extracted_data": {...}
}
# Lost if process crashes!
```

#### v3.0: Database-Backed State

```python
# PostgreSQL with JSONB
CREATE TABLE agent_state (
    task_id VARCHAR(255) PRIMARY KEY,
    company_name VARCHAR(255),
    state JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

# Persistent, survives crashes
await db.execute(
    "INSERT INTO agent_state VALUES ($1, $2, $3)",
    task_id, company_name, json.dumps(state)
)
```

---

## Cost Optimization

### v2.0 Cost Breakdown (Monthly)

| Service | Cost | Usage |
|---------|------|-------|
| ECS Fargate (on-demand) | $3,456 | 4 vCPU, 8 GB RAM, 24/7 |
| RDS Aurora (provisioned) | $1,152 | db.r5.large |
| NAT Gateway | $32 | 2 AZs |
| CloudWatch | $50 | Logs + metrics |
| Tavily API | $432 | 86,400 queries/mo |
| **Total** | **$5,222** | - |

### v3.0 Cost Breakdown (Monthly, Optimized)

| Service | Cost | Usage | Optimization |
|---------|------|-------|--------------|
| ECS Fargate **Spot** | $346 | 4 vCPU, 8 GB, 24/7 | 70% discount |
| Lambda (Reflection) | $24 | 10,000 invocations | Pay-per-use |
| Aurora **Serverless v2** | $36 | 0.5-2 ACUs | Auto-scale |
| ElastiCache Redis | $15 | cache.t3.micro | Caching |
| VPC Endpoints | $7 | S3 + DynamoDB | No NAT Gateway |
| CloudWatch | $50 | Logs + metrics | Same |
| Tavily API (cached) | **$43** | 90% cache hit | 10x reduction |
| **Total** | **$464** | - | **91% savings** |

**Savings**: $5,222 → $464 = **$4,758/month**

**ROI**: Migration cost ~$50k (7 weeks @ $7k/week), payback in **10.5 months**.

---

## Troubleshooting

### Issue: Slow Migration Performance

**Symptom**: 1,000 items still takes 5+ minutes.

**Debugging**:
```bash
# Check agent CPU
aws ecs describe-services --cluster multi-agent-cluster --services research-agent

# Check database connections
psql -c "SELECT count(*) FROM pg_stat_activity;"

# Check cache hit rate
redis-cli INFO stats | grep hits
```

**Solutions**:
- Scale up pods: 10 → 20
- Increase database ACUs: 2 → 4
- Add more cache memory
- Optimize prompts (reduce tokens)

### Issue: High Error Rate (>5%)

**Symptom**: Many tasks fail with 500 errors.

**Debugging**:
```bash
# Check agent logs
aws logs tail /aws/ecs/research-agent --follow

# Check database errors
SELECT * FROM agent_state WHERE state->>'error' IS NOT NULL;
```

**Solutions**:
- Add retry logic (3 attempts)
- Increase timeouts (30 → 60 sec)
- Fix database connection pool
- Add circuit breaker

### Issue: High Costs

**Symptom**: AWS bill > $1,000/month.

**Debugging**:
```bash
# Check Fargate usage
aws ce get-cost-and-usage --time-period Start=2025-10-01,End=2025-10-31 \
  --granularity MONTHLY --metrics BlendedCost --group-by Type=SERVICE

# Check Tavily costs
grep "tavily" logs/*.log | wc -l
```

**Solutions**:
- Use Fargate Spot (not on-demand)
- Increase cache TTL (24h → 7 days)
- Reduce max_search_queries (5 → 3)
- Use free search providers (DuckDuckGo) for follow-ups

---

## Summary

### Migration Checklist

- [ ] **Phase 1: Hybrid Wrapper** (Week 1-2)
  - [ ] Create research agent wrapper
  - [ ] Create extraction agent wrapper
  - [ ] Create coordinator
  - [ ] Test locally with Docker Compose

- [ ] **Phase 2: Infrastructure** (Week 3-4)
  - [ ] Deploy VPC and networking
  - [ ] Deploy ECS cluster with Fargate Spot
  - [ ] Deploy Aurora Serverless v2
  - [ ] Deploy ElastiCache Redis
  - [ ] Configure VPC Endpoints

- [ ] **Phase 3: Optimization** (Week 5-6)
  - [ ] Run load test (1,000 items)
  - [ ] Implement caching (90% hit rate)
  - [ ] Tune auto-scaling
  - [ ] Optimize connection pooling

- [ ] **Phase 4: Production** (Week 7)
  - [ ] Blue-green deployment
  - [ ] Gradual traffic shift (10% → 100%)
  - [ ] Monitor metrics and alarms
  - [ ] Decommission v2.0

### Expected Results

✅ **480-1000x faster**: 12 hours → 90 seconds
✅ **91% cost reduction**: $5,222 → $464/month
✅ **100+ concurrent**: Unlimited horizontal scaling
✅ **Auto-recovery**: Fault tolerant distributed system

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
