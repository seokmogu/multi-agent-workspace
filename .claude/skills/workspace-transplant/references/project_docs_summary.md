# Project Documentation Summary

Key insights extracted from CLAUDE.md, A2A_ARCHITECTURE.md, and COST_OPTIMIZATION.md.

## Quick Reference

| Topic | Current (v2.0) | Target (v3.0) | Improvement |
|-------|----------------|---------------|-------------|
| **Architecture** | LangGraph monolith | A2A distributed | Horizontal scaling |
| **Performance** | 45-90 sec/item | 90 sec/1000 items | 480-1000x faster |
| **Cost** | $5,222/month | $464/month | 91% reduction |
| **Concurrency** | 1 (sequential) | 100+ (parallel) | 100x |
| **Scalability** | Vertical only | Unlimited horizontal | ♾️ |

---

## System Evolution

### v1.0 → v2.0 → v3.0

```
v1.0 (PoC)                v2.0 (Production)         v3.0 (Scale)
─────────                 ─────────────────         ────────────
Basic 3-phase             + Rate limiting           + Parallel processing
Sequential                + Token management        + Auto-scaling
                          + Prompt centralization   + Cost optimization (91%)
                          + Deduplication           + Fault tolerance
```

---

## Architecture Decisions

### Why LangGraph? (v2.0)

✅ **Rapid Development**: Graph abstraction simplifies workflow
✅ **State Management**: TypedDict integration
✅ **Debugging**: Easy to trace execution
✅ **Iteration**: Quick to modify phases

❌ **Limitation**: Sequential processing only

### Why A2A Migration? (v3.0)

✅ **Performance**: 480x faster for batch processing
✅ **Scalability**: Independent agent scaling
✅ **Cost**: 91% reduction through Spot instances + Lambda
✅ **Reliability**: Auto-recovery, fault isolation

**Decision Point**: v2.0 → v3.0 when batch size exceeds 100 items regularly.

---

## Cost Breakdown

### v2.0 Monthly Costs: $5,222

| Component | Cost | Details |
|-----------|------|---------|
| ECS Fargate (on-demand) | $3,456 | 4 vCPU, 8 GB, 24/7 |
| RDS Aurora (provisioned) | $1,152 | db.r5.large |
| Tavily API | $432 | 86,400 queries/mo |
| CloudWatch | $50 | Logs + metrics |
| NAT Gateway | $32 | 2 AZs |

### v3.0 Monthly Costs: $464 (Optimized)

| Component | Cost | Optimization Strategy |
|-----------|------|----------------------|
| ECS Fargate **Spot** | $346 | 70% discount vs on-demand |
| Lambda (Reflection) | $24 | Pay-per-execution |
| Aurora **Serverless v2** | $36 | 0.5-2 ACUs, auto-scale |
| Tavily API (cached) | $43 | 90% cache hit (10x reduction) |
| ElastiCache Redis | $15 | Caching layer |
| VPC Endpoints | $7 | Eliminates NAT Gateway |
| CloudWatch | $50 | Same |

**Key Optimizations**:
1. Fargate Spot: $3,456 → $346 (90% savings)
2. Aurora Serverless: $1,152 → $36 (97% savings)
3. Tavily Caching: $432 → $43 (90% savings)
4. VPC Endpoints: $32 → $0 (NAT Gateway eliminated)

**ROI**: $4,758/month savings, payback in 10.5 months.

---

## Performance Analysis

### v2.0 Bottlenecks

1. **Sequential Processing**: Only 1 item at a time
2. **Single Process**: CPU-bound
3. **In-Memory State**: Lost on crash
4. **Vertical Scaling**: Limited to instance size

**Result**: 1,000 items = 12-25 hours

### v3.0 Optimizations

1. **Parallel Execution**: 100+ concurrent tasks
2. **Distributed Agents**: Independent scaling
3. **Database State**: Persistent, fault-tolerant
4. **Horizontal Scaling**: Unlimited pods

**Result**: 1,000 items = 90 seconds

### Performance Metrics

| Metric | v2.0 | v3.0 | How Achieved |
|--------|------|------|--------------|
| Throughput | 80/hour | 400/hour | 5 research agents instead of 1 |
| Latency (single) | 45-90 sec | 30-60 sec | Caching + optimized prompts |
| Batch (1,000) | 12-25 hours | 90 sec | Parallel processing |
| Max concurrent | 1 | 100+ | Independent HTTP services |

---

## Key Technical Patterns

### 1. Prompt Centralization

**Problem**: Prompts scattered across code.

**Solution**: Single `prompts.py` module.

**Benefit**: Easy A/B testing, version control, documentation.

### 2. Rate Limiting

**Problem**: API throttling (429 errors).

**Solution**: InMemoryRateLimiter at 0.8 req/sec.

**Benefit**: Tier 1 compliance, no burst issues.

### 3. URL Deduplication

**Problem**: Repeated searches waste API calls.

**Solution**: `deduplicate_sources()` before scraping.

**Benefit**: 20-30% cost reduction.

### 4. Token Management

**Problem**: Context overflow with large documents.

**Solution**: `max_tokens_per_source=1000` limit.

**Benefit**: Prevents LLM errors, consistent performance.

### 5. Multi-Phase Workflow

**Problem**: Low data quality from single-pass extraction.

**Solution**: Research → Extract → Reflect loop.

**Benefit**: 80%+ completeness, iterative improvement.

### 6. A2A Protocol

**Problem**: Monolithic scaling limits.

**Solution**: Independent HTTP agents with Agent Cards.

**Benefit**: 100x concurrency, fault isolation.

---

## Migration Strategy

### 7-Week Plan

**Phase 1** (Week 1-2): Hybrid Wrapper
- Wrap existing code with A2A interfaces
- Test locally with Docker Compose
- Zero risk (v2.0 untouched)

**Phase 2** (Week 3-4): Infrastructure
- Deploy to AWS (VPC, ECS, Aurora, Redis)
- Use Terraform for IaC
- Run both v2.0 and v3.0

**Phase 3** (Week 5-6): Optimization
- Load test 1,000 items
- Tune auto-scaling
- Implement caching (90% hit rate)

**Phase 4** (Week 7): Production
- Blue-green deployment
- Gradual traffic shift (10% → 100%)
- Monitor and decommission v2.0

**Downtime**: Zero (blue-green)

**Rollback**: Immediate (route back to v2.0)

---

## Technology Stack

### v2.0 Stack

| Category | Technology |
|----------|-----------|
| Framework | LangGraph, LangChain |
| LLM | Claude Sonnet 4.5 |
| Search | Tavily API |
| Language | Python 3.10+ |
| State | In-memory TypedDict |
| Config | Pydantic |

### v3.0 Additional Stack

| Category | Technology |
|----------|-----------|
| Protocol | A2A (Agent2Agent) |
| Orchestration | FastAPI (Coordinator) |
| Compute | ECS Fargate Spot, Lambda |
| Database | Aurora Serverless v2 |
| Cache | ElastiCache Redis |
| Storage | S3 |
| Network | VPC, VPC Endpoints |
| IaC | Terraform |
| Monitoring | CloudWatch, Prometheus |

---

## Best Practices

### Development

1. **Start Simple**: Begin with v2.0 LangGraph for prototyping
2. **Centralize Early**: Use prompts.py, utils.py from day 1
3. **Rate Limit**: Always use InMemoryRateLimiter in production
4. **Test Locally**: Docker Compose for v3.0 testing

### Production

1. **Monitor Costs**: Track Tavily API usage, Fargate hours
2. **Cache Aggressively**: 90% cache hit rate = 10x cost savings
3. **Auto-Scale**: Target 70% CPU, scale out fast (60s), in slow (300s)
4. **Use Spot**: 70% savings, minimal interruptions for batch jobs

### Migration

1. **Hybrid First**: Wrap existing code, don't rewrite
2. **Blue-Green**: Zero downtime deployment
3. **Gradual**: 10% → 50% → 100% traffic over 1 week
4. **Rollback Ready**: Keep v2.0 running until v3.0 proven stable

---

## Common Pitfalls

### ❌ Don't Do This

1. **Skip Rate Limiting**: Will hit API limits in production
2. **No Deduplication**: Wastes 20-30% of API budget
3. **Unbounded Tokens**: Context overflow causes LLM errors
4. **No Caching**: Miss 10x cost savings opportunity
5. **Big Bang Migration**: High risk, rewrite everything at once

### ✅ Do This Instead

1. **Rate Limit Early**: Add from day 1, not after errors
2. **Deduplicate Always**: Before every API call
3. **Limit Tokens**: `max_tokens_per_source=1000`
4. **Cache Everything**: Search results, LLM responses (where appropriate)
5. **Gradual Migration**: Hybrid wrapper → Infrastructure → Optimization → Production

---

## Metrics to Track

### Development Metrics

- Unit test coverage (target: > 80%)
- Prompt success rate (target: > 95%)
- Extraction completeness (target: > 80%)

### Production Metrics

- **Performance**: Throughput (items/hour), latency (sec/item)
- **Cost**: API calls/day, AWS bill/month
- **Quality**: Completeness score, error rate
- **Reliability**: Uptime %, failed tasks

### A2A Metrics

- **Concurrency**: Active pods, queue depth
- **Cache**: Hit rate (target: > 90%)
- **Scaling**: Scale-out events, scale-in events
- **Errors**: 5xx rate (target: < 1%)

---

## Real-World Numbers

### Example: 1,000 Private SME Companies

**v2.0 (Sequential)**:
- Time: 45 sec/item × 1,000 = 12.5 hours
- Cost: $0.005/API call × 3 queries × 1,000 = $15 (Tavily only)
- Throughput: 80 items/hour
- Requires: 1 Fargate task running 12.5 hours

**v3.0 (Parallel)**:
- Time: 90 seconds for all 1,000
- Cost: $0.005 × 3 × 0.1 (90% cache) × 1,000 = $1.50 (cached)
- Throughput: 40,000 items/hour (theoretical)
- Requires: 10 research + 5 extraction + 2 reflection pods for 90 sec

**Savings**: 12.5 hours → 90 sec, $15 → $1.50 (with caching)

---

## Further Resources

### Internal Documentation

- **CLAUDE.md**: Complete project overview
- **A2A_ARCHITECTURE.md**: A2A protocol specification
- **COST_OPTIMIZATION.md**: Detailed cost breakdown
- **INFRASTRUCTURE_DESIGN.md**: Terraform infrastructure

### External References

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Agent2Agent Protocol](https://github.com/google/agent-protocol)
- [AWS ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)

---

## Decision Framework

### Should I use v2.0 or v3.0?

**Use v2.0 (LangGraph) if**:
- Batch size < 100 items
- Prototyping / MVP
- Team < 5 engineers
- No distributed systems experience
- 45-90 sec/item is acceptable

**Use v3.0 (A2A) if**:
- Batch size > 100 items regularly
- Production system with SLA
- Need < 1 min per 1,000 items
- Team comfortable with distributed systems
- Cost optimization important (91% savings)

### When to migrate?

**Trigger**: When v2.0 processing time becomes bottleneck (> 2 hours for daily batch).

**Timeline**: Allow 7 weeks for full migration.

**Resources**: 2-3 engineers + 1 DevOps.

**Budget**: ~$50k migration cost, payback in 10.5 months.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
**Maintained by**: Development Team
