## 1. Tavily

**Best for:** Production deep research, LLM-optimized results

### Overview
- **Free Tier:** 1,000 API credits/month (no credit card required)
- **Pricing:** $0.008 per request (pay-as-you-go) or monthly plans
- **Quality:** ⭐⭐⭐⭐⭐ (Best quality, specifically optimized for AI/LLM research)
- **Speed:** Fast
- **Special Features:**
  - Advanced search depth
  - Raw content inclusion
  - Domain filtering
  - Image search support

### Setup

```bash
pip install tavily-python langchain-community
```

**Environment Variable:**
```bash
export TAVILY_API_KEY="your_api_key_here"
```

Get your API key: https://tavily.com/ (sign up, no credit card needed for free tier)

### LangChain Integration

```python
from langchain_community.tools.tavily_search import TavilySearchResults

# Basic usage
search_tool = TavilySearchResults(
    max_results=3,
    search_depth="advanced",  # or "basic"
    include_raw_content=True,
    include_images=False
)

# Execute search
results = await search_tool.ainvoke("Anthropic AI safety research")

# Result format:
# [
#   {
#     "title": "Page title",
#     "url": "https://example.com",
#     "content": "Snippet...",
#     "raw_content": "Full content..."
#   }
# ]
```

### Advanced Options

```python
# Domain filtering
search_tool = TavilySearchResults(
    max_results=5,
    include_domains=["anthropic.com", "openai.com"],  # Only these domains
    exclude_domains=["example.com"]  # Exclude these
)

# With images
search_tool = TavilySearchResults(
    max_results=3,
    include_images=True
)
```

### Rate Limits
- Free tier: 1,000 requests/month
- No per-minute limits

### Best Practices
- Use `search_depth="advanced"` for comprehensive research
- Enable `include_raw_content=True` for LLM processing
- Set `max_results` based on budget (each result counts as 1 credit)

---

