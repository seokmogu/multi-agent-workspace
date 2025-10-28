# Troubleshooting Guide

Common issues and solutions for the company research agent.

## Empty or Incomplete Extractions

**Symptoms:**
- `extracted_data` contains mostly `null` values
- Completeness score below 50%
- Missing required fields

**Causes:**
1. Low-quality search results
2. Private company with limited data
3. Unclear schema descriptions
4. Wrong search provider

**Solutions:**

1. **Upgrade search provider**
   ```python
   # Try better provider
   config = Configuration(search_provider="tavily")  # Best quality
   ```

2. **Increase search queries**
   ```python
   config = Configuration(max_search_queries=5)  # More data
   ```

3. **Improve schema descriptions**
   ```python
   schema = {
       "properties": {
           "revenue": {
               "type": "string",
               "description": "Annual revenue in USD (e.g., $10M, $50M). For private companies, use estimates from news or public filings."
           }
       }
   }
   ```

4. **Use indirect sources**
   ```python
   user_context = """
   Focus on indirect sources:
   - Public company filings mentioning this company
   - VC portfolio pages
   - Government procurement records
   """
   ```

## Rate Limit Errors

**Symptoms:**
- `429 Too Many Requests`
- API throttling errors
- Slow processing

**Causes:**
1. Exceeding Anthropic API limits
2. Too many concurrent requests
3. Rate limiter misconfigured

**Solutions:**

1. **Verify rate limiter** (default: 0.8 req/sec for Tier 1)
   ```python
   # In llm.py
   _rate_limiter = InMemoryRateLimiter(
       requests_per_second=0.8,  # Tier 1: ~50 req/min
   )
   ```

2. **For Tier 2, increase limit**
   ```python
   _rate_limiter = InMemoryRateLimiter(
       requests_per_second=16.6,  # Tier 2: ~1,000 req/min
   )
   ```

3. **Reduce concurrent processing**
   - Process companies sequentially
   - Add delays between batches

4. **Check API tier**
   ```bash
   # Anthropic tiers:
   # Tier 1: 50 req/min, 40,000 tokens/min
   # Tier 2: 1,000 req/min, 80,000 tokens/min
   ```

## Infinite Reflection Loops

**Symptoms:**
- Agent never reaches `is_complete=True`
- Exceeds `max_reflection_steps`
- Keeps generating follow-up queries

**Causes:**
1. Unrealistic schema `required` fields
2. Completeness threshold too high
3. Follow-up queries not finding data

**Solutions:**

1. **Adjust max iterations**
   ```python
   config = Configuration(max_reflection_steps=1)  # Limit iterations
   ```

2. **Lower completeness threshold**
   ```python
   # In reflection.py, change from 0.85 to 0.75
   if completeness_score > 0.75:  # Less strict
       return {"is_complete": True}
   ```

3. **Review required fields**
   ```python
   # Only mark truly essential fields as required
   schema = {
       "required": ["company_name", "description"]  # Minimal
   }
   ```

4. **Check follow-up query quality**
   - Review generated queries in logs
   - Ensure they're specific and actionable

## API Key Errors

**Symptoms:**
- `AuthenticationError`
- `Invalid API key`
- Import errors

**Solutions:**

1. **Set all required API keys**
   ```bash
   export ANTHROPIC_API_KEY="your_key"
   export TAVILY_API_KEY="your_key"
   export GOOGLE_API_KEY="your_key"  # For Google ADK
   ```

2. **Verify key format**
   ```bash
   # Anthropic: sk-ant-...
   # Tavily: tvly-...
   # Google: AI...
   ```

3. **Check key permissions**
   - Ensure keys have correct scopes
   - Verify account status

4. **Install required packages**
   ```bash
   pip install langchain-anthropic tavily-python
   ```

## Context Overflow Errors

**Symptoms:**
- `Context length exceeded`
- Token limit errors
- Slow processing

**Causes:**
1. Too many search results
2. Large raw content
3. No token limiting

**Solutions:**

1. **Verify token limits** (default: 1,000 tokens/source)
   ```python
   # In research.py
   formatted_sources = format_sources(
       deduplicated_results,
       max_tokens_per_source=1000  # Adjust as needed
   )
   ```

2. **Reduce search results**
   ```python
   config = Configuration(
       max_search_queries=3,    # Fewer queries
       max_search_results=3     # Fewer results per query
   )
   ```

3. **Truncate research notes**
   ```python
   # In reflection.py
   notes = truncate_text(state["research_notes"], max_length=2000)
   ```

## Provider-Specific Issues

### Tavily

**Issue:** API quota exceeded
**Solution:**
- Check usage at https://tavily.com/dashboard
- Upgrade plan or switch to Hybrid

### Google ADK

**Issue:** Requires Gemini model
**Solution:**
```python
config = Configuration(
    search_provider="google_adk",
    use_gemini_for_google_search=True  # Required
)
```

### DuckDuckGo

**Issue:** Rate limiting
**Solution:**
- Reduce `max_search_queries`
- Add delays between queries
- Switch to paid provider

## Performance Issues

**Symptoms:**
- Slow processing (>120 seconds)
- High API costs
- Low success rate

**Solutions:**

1. **Optimize search provider**
   ```python
   # Hybrid for balance
   config = Configuration(search_provider="hybrid")
   ```

2. **Enable deduplication** (default: enabled)
   ```python
   # In research.py
   deduplicated_results = deduplicate_sources(all_results)
   ```

3. **Monitor performance**
   ```python
   import time
   start = time.time()
   result = await graph.ainvoke(state)
   print(f"Processing time: {time.time() - start:.1f}s")
   ```

4. **Profile bottlenecks**
   - Research phase: 20-40 seconds
   - Extraction phase: 10-20 seconds
   - Reflection phase: 10-20 seconds

## Debugging Tips

1. **Enable logging**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

2. **Inspect state**
   ```python
   print(f"Queries: {result['research_queries']}")
   print(f"Completeness: {calculate_completeness(result['extracted_data'], schema)}")
   ```

3. **Check search results**
   ```python
   print(f"Found {len(result['search_results'])} unique results")
   for r in result['search_results'][:3]:
       print(f"- {r['title']}: {r['url']}")
   ```

4. **Review missing fields**
   ```python
   print(f"Missing: {result['missing_fields']}")
   print(f"Follow-ups: {result['follow_up_queries']}")
   ```

## Getting Help

1. Check existing implementation at `src/agents/company_research/`
2. Review examples in `examples/`
3. Read inline documentation in code
4. Test with simple cases first (public companies)
5. Enable verbose logging for debugging

## Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `AuthenticationError` | Invalid API key | Set correct key |
| `429 Too Many Requests` | Rate limit exceeded | Reduce rate or upgrade tier |
| `Context length exceeded` | Too many tokens | Reduce `max_tokens_per_source` |
| `No search provider available` | Missing package | Install provider package |
| `Extraction error` | JSON parsing failed | Check schema validity |
| `Reflection error` | Quality check failed | Review completeness threshold |
