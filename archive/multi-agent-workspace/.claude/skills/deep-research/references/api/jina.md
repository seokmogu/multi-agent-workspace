## 2. Jina AI Reader

**Best for:** Development, content extraction, URL-to-LLM-friendly text conversion

### Overview
- **Free Tier:**
  - Without API key: 20 requests/minute
  - With free API key: 200 requests/minute
  - Free trial: 10M tokens
- **Pricing:** Pay-per-token model
- **Quality:** ⭐⭐⭐
- **Speed:** Fast
- **Special Features:**
  - URL to clean markdown conversion
  - No API key required for basic usage
  - LLM-optimized output format

### Setup

```bash
# No installation needed for basic HTTP usage
# For advanced features:
pip install jina-ai langchain-community
```

**Environment Variable (optional for higher rate limits):**
```bash
export JINA_API_KEY="your_api_key_here"
```

Get your free API key: https://jina.ai/reader/ (10M tokens free trial)

### LangChain Integration

```python
# Method 1: Direct HTTP (no API key needed)
import requests

def jina_search(url: str) -> str:
    """Convert any URL to LLM-friendly markdown."""
    response = requests.get(f"https://r.jina.ai/{url}")
    return response.text

# Usage
content = jina_search("https://www.anthropic.com")
```

```python
# Method 2: With API key for higher rate limits
import requests

headers = {"Authorization": f"Bearer {JINA_API_KEY}"}

def jina_search_with_key(url: str) -> str:
    response = requests.get(
        f"https://r.jina.ai/{url}",
        headers=headers
    )
    return response.text
```

```python
# Method 3: For search queries (not just URLs)
# Note: Jina is primarily for URL conversion, not web search
# For search, use other providers like Tavily or Serper
```

### Rate Limits
- Without API key: 20 RPM
- With free API key: 200 RPM
- Token limits tracked per minute

### Best Practices
- Best for converting known URLs to LLM-friendly format
- Not ideal for discovery/search - use Tavily/Serper for that
- Perfect for follow-up deep dives on specific URLs found via other search APIs

---

