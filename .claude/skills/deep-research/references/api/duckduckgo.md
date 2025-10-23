## 6. DuckDuckGo

**Best for:** Testing, no-budget projects, completely free usage

### Overview
- **Free Tier:** Unlimited (no API key required!)
- **Pricing:** Free
- **Quality:** ⭐⭐
- **Speed:** Slow (rate limited)
- **Special Features:**
  - No API key required
  - No cost ever
  - Privacy-focused
  - Good for development/testing

### Setup

```bash
pip install duckduckgo-search langchain-community
```

**No API key needed!**

### LangChain Integration

```python
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# Initialize (no key needed!)
search = DuckDuckGoSearchAPIWrapper()

# Basic search
results = search.run("Anthropic AI")

# Returns: String with search results
```

```python
# For structured results
from langchain_community.tools import DuckDuckGoSearchResults

search_tool = DuckDuckGoSearchResults()

results = await search_tool.ainvoke("AI safety research")

# Result format: List of dicts with title, snippet, link
```

### Rate Limits
- Rate limited by IP address
- No hard limits, but aggressive rate limiting
- Expect slower responses than paid APIs

### Best Practices
- **Perfect for development and testing** - no setup required
- Not recommended for production due to rate limits and quality
- Use as fallback when other APIs fail
- Great for quick prototypes before committing to paid service

---

