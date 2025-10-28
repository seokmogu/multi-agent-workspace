# Production Deployment Checklist

Pre-deployment validation for the company research agent.

## Phase 1: Configuration

### Search Provider
- [ ] Selected appropriate provider (Tavily/Hybrid for production)
- [ ] API keys set in environment
- [ ] Verified API quota/limits
- [ ] Tested provider with sample queries

### Rate Limiting
- [ ] Configured for correct API tier (Tier 1: 0.8 req/sec, Tier 2: 16.6 req/sec)
- [ ] Tested rate limiter with burst requests
- [ ] No `429` errors in test runs

### Resource Limits
- [ ] Set `max_search_queries` (recommended: 3-5)
- [ ] Set `max_search_results` (recommended: 3-5)
- [ ] Set `max_reflection_steps` (recommended: 1-2)
- [ ] Set `max_tokens_per_source` (recommended: 1000)

## Phase 2: Schema Design

### Schema Structure
- [ ] Schema is flat (avoid deep nesting)
- [ ] Field descriptions are clear and specific
- [ ] Only essential fields marked as `required`
- [ ] Tested with sample companies (public → private → very private)

### Validation
- [ ] Schema completeness target: >85%
- [ ] Required fields are achievable for target companies
- [ ] Tested with edge cases (very private companies, startups)

## Phase 3: Testing

### Unit Testing
- [ ] Test query generation with different schemas
- [ ] Test each search provider independently
- [ ] Test extraction with various data qualities
- [ ] Test reflection with different completeness scores

### Integration Testing
- [ ] Full workflow test with public company (high data availability)
- [ ] Full workflow test with private SME (medium data availability)
- [ ] Full workflow test with very private company (low data availability)
- [ ] Test error handling (invalid API keys, network failures)

### Performance Testing
- [ ] Processing time: <90 seconds per company
- [ ] API calls: <10 per company (verify deduplication works)
- [ ] Memory usage: <500MB per company
- [ ] Completeness rate: >85% on test set

## Phase 4: Production Features

### Error Handling
- [ ] All search providers have try-catch
- [ ] Fallback to free providers on failure
- [ ] Graceful degradation on partial failures
- [ ] Error logging implemented

### Monitoring
- [ ] API cost tracking implemented
- [ ] Processing time logging
- [ ] Completeness score tracking
- [ ] Error rate monitoring

### Optimization
- [ ] URL deduplication verified working
- [ ] Token limits prevent context overflow
- [ ] Rate limiting prevents throttling
- [ ] Caching strategy (if applicable)

## Phase 5: Cost Management

### Cost Estimation
- [ ] Calculated cost per company
- [ ] Projected monthly cost based on volume
- [ ] Set budget alerts (if available)
- [ ] Tested cost optimization (Hybrid mode)

### Provider Costs (per company)
- Tavily: ~$0.015-0.045
- Hybrid: ~$0.0075-0.0225 (50% savings)
- Google ADK: Free (with Gemini)
- DuckDuckGo: Free

### Monitoring
- [ ] Track actual costs vs. estimates
- [ ] Monitor API usage dashboards
- [ ] Set up cost alerts
- [ ] Review provider selection periodically

## Phase 6: Security

### API Keys
- [ ] Keys stored in environment variables (not code)
- [ ] Keys not committed to version control
- [ ] Key rotation policy defined
- [ ] Access restricted to authorized users

### Data Privacy
- [ ] No PII stored unnecessarily
- [ ] Search results not cached beyond necessity
- [ ] Compliance with data retention policies
- [ ] GDPR/privacy considerations addressed

## Phase 7: Documentation

### Code Documentation
- [ ] All functions have docstrings
- [ ] Complex logic has inline comments
- [ ] Configuration options documented
- [ ] Examples provided

### User Documentation
- [ ] Installation guide
- [ ] Configuration guide
- [ ] Usage examples
- [ ] Troubleshooting guide
- [ ] Performance expectations documented

## Phase 8: Deployment

### Environment Setup
- [ ] Production environment configured
- [ ] Dependencies installed
- [ ] API keys set
- [ ] Environment variables validated

### Deployment
- [ ] Code deployed to production
- [ ] Health checks passing
- [ ] Monitoring dashboards active
- [ ] Alerts configured

### Rollout
- [ ] Deployed to staging first
- [ ] Tested in staging environment
- [ ] Gradual rollout to production
- [ ] Rollback plan documented

## Phase 9: Monitoring & Maintenance

### Active Monitoring
- [ ] Processing time < 90 seconds
- [ ] Completeness rate > 85%
- [ ] Error rate < 5%
- [ ] API costs within budget

### Alerts
- [ ] High error rate (>10%)
- [ ] Slow processing (>120 seconds)
- [ ] High API costs
- [ ] Rate limit violations

### Maintenance
- [ ] Regular schema updates based on user feedback
- [ ] Provider performance review (monthly)
- [ ] Cost optimization review (monthly)
- [ ] Security updates applied

## Success Criteria

### Performance
- ✅ Processing time: 45-90 seconds per company
- ✅ Completeness: 85-95%
- ✅ Success rate: >95% (no errors)
- ✅ API calls: 3-9 per company

### Cost
- ✅ Within budget
- ✅ Cost per company predictable
- ✅ No unexpected charges

### Quality
- ✅ Accurate extractions
- ✅ Minimal hallucinations
- ✅ Reliable for production use

## Rollback Plan

If issues occur in production:

1. **Immediate**: Revert to previous version
2. **Short-term**: Fix issues in staging
3. **Long-term**: Re-deploy with fixes

Rollback triggers:
- Error rate > 20%
- Processing time > 180 seconds
- Completeness < 50%
- Critical bug discovered

## Post-Deployment Review

After 1 week:
- [ ] Review performance metrics
- [ ] Analyze cost actuals vs. estimates
- [ ] Collect user feedback
- [ ] Identify optimization opportunities

After 1 month:
- [ ] Comprehensive performance review
- [ ] Cost optimization analysis
- [ ] Schema update needs
- [ ] Provider comparison (switch if needed)

## Final Sign-Off

Before going live:

- [ ] All checklist items completed
- [ ] Testing successful
- [ ] Monitoring in place
- [ ] Documentation complete
- [ ] Team trained
- [ ] Rollback plan tested

**Deployment approved by:** _______________
**Date:** _______________
