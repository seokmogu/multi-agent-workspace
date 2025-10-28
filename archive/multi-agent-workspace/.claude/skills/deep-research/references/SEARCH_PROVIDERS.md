# Search Providers Guide

Complete guide for all 7 supported web search providers.

## Provider Comparison

| Provider | Free Tier | Pricing | Quality | Setup |
|----------|-----------|---------|---------|-------|
| Tavily | 1,000/month | $0.005/query | ⭐⭐⭐⭐⭐ | API key |
| Google ADK | Unlimited* | Free | ⭐⭐⭐⭐ | API key + Gemini |
| Hybrid | Mixed | Low | ⭐⭐⭐⭐ | Both keys |
| DuckDuckGo | Unlimited | Free | ⭐⭐ | None |
| Bing | 1,000/month | $7/1k | ⭐⭐⭐ | Subscription key |
| Brave | 2,000/month | Paid | ⭐⭐⭐ | API key |
| SerpAPI | Trial | $50/5k | ⭐⭐⭐⭐ | API key |

*Requires Gemini 2.0+ models

## 1. Tavily (Best Quality)

**Use for:** Production deployments requiring highest quality

**Setup:**
```bash
pip install tavily-python>=0.3.0
export TAVILY_API_KEY="your_key"
```

**Configuration:**
```python
config = Configuration(search_provider="tavily")
```

**Features:**
- Advanced search depth
- Raw content included
- Best accuracy
- Reliable extraction

**Cost:** $5 per 1,000 searches

## 2. Google ADK (Free Production)

**Use for:** Free production deployments with Gemini

**Setup:**
```bash
pip install langchain-google-genai
export GOOGLE_API_KEY="your_key"
```

**Configuration:**
```python
config = Configuration(
    search_provider="google_adk",
    use_gemini_for_google_search=True
)
```

**Requirements:**
- Must use Gemini 2.0+ models
- Free with Google API

**Limitations:**
- Requires Google account
- Results less structured than Tavily

## 3. Hybrid (Cost Optimization)

**Use for:** Production with 50% cost reduction

**Setup:**
```bash
pip install tavily-python langchain-google-genai
export TAVILY_API_KEY="your_key"
export GOOGLE_API_KEY="your_key"
```

**Configuration:**
```python
config = Configuration(search_provider="hybrid")
```

**Strategy:**
- First half of queries: Tavily (high quality)
- Second half: Google ADK (free)
- Cost: ~$0.0075-0.0225 per company

## 4. DuckDuckGo (Free Testing)

**Use for:** Development and testing

**Setup:**
```bash
pip install duckduckgo-search
# No API key needed
```

**Configuration:**
```python
config = Configuration(search_provider="duckduckgo")
```

**Features:**
- Completely free
- No API key needed
- Privacy-focused
- Rate limited

**Limitations:**
- Lower quality results
- Less structured data
- Rate limits

## 5. Bing

**Use for:** Microsoft ecosystem integration

**Setup:**
```bash
export BING_SUBSCRIPTION_KEY="your_key"
```

**Configuration:**
```python
config = Configuration(search_provider="bing")
```

**Pricing:**
- Free: 1,000 queries/month
- Paid: $7 per 1,000 queries

## 6. Brave

**Use for:** Privacy-focused production

**Setup:**
```bash
export BRAVE_API_KEY="your_key"
```

**Configuration:**
```python
config = Configuration(search_provider="brave")
```

**Features:**
- Privacy-focused
- 2,000 free queries/month
- Good quality

## 7. SerpAPI

**Use for:** Google results scraping

**Setup:**
```bash
pip install google-search-results
export SERPAPI_KEY="your_key"
```

**Configuration:**
```python
config = Configuration(search_provider="serpapi")
```

**Pricing:**
- Trial available
- $50 per 5,000 searches

## Provider Selection Decision Tree

```
Need production quality?
├─ Yes
│  ├─ Budget available?
│  │  ├─ Yes → Tavily
│  │  └─ No → Hybrid (50% savings)
│  └─ Budget constrained?
│     └─ Google ADK (free with Gemini)
└─ No (testing/development)
   └─ DuckDuckGo (completely free)
```

## Error Handling

All providers implement automatic fallback:

```python
try:
    results = await search_tool.ainvoke(query)
    all_results.extend(results)
except Exception as e:
    print(f"Search error for query '{query}': {e}")
    continue  # Skip to next query
```

Fallback chain:
1. Configured provider fails
2. Warning logged
3. Continue with next query
4. If all fail: Return empty results with error message

## API Rate Limits

| Provider | Rate Limit | Handling |
|----------|------------|----------|
| Tavily | 100 req/min | Built-in |
| Google ADK | Depends on tier | Built-in |
| DuckDuckGo | ~30 req/min | Client-side |
| Others | Varies | Provider-specific |

The agent's rate limiter (0.8 req/sec) ensures compliance with all provider limits.

## Best Practices

1. **Start with free**: Use DuckDuckGo for initial testing
2. **Validate quality**: Test Tavily with 10-20 companies
3. **Optimize cost**: Switch to Hybrid for production
4. **Monitor usage**: Track API costs and adjust
5. **Set fallbacks**: Always have a backup provider configured

## Troubleshooting

**Provider not working:**
1. Check API key is set correctly
2. Verify package is installed
3. Check API quota/limits
4. Try fallback provider

**Poor results:**
1. Try higher quality provider (Tavily)
2. Increase `max_search_queries`
3. Improve schema descriptions
4. Use indirect sources for private SMEs
