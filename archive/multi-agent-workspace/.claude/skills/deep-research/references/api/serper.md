## 3. Serper.dev

**Best for:** Free production usage, Google SERP results

### Overview
- **Free Tier:** 2,500 queries (lifetime, no credit card)
- **Pricing:** $0.30-$1.00 per 1k queries (pay-as-you-go)
- **Quality:** ⭐⭐⭐⭐
- **Speed:** Very Fast (1-2 seconds)
- **Special Features:**
  - Real Google SERP data
  - Multiple search types (web, images, news, maps, shopping, scholar)
  - Knowledge graph results
  - No subscriptions, pay-as-you-go

### Setup

```bash
pip install google-search-results langchain-community
```

**Environment Variable:**
```bash
export SERPER_API_KEY="your_api_key_here"
```

Get your free API key: https://serper.dev/ (2,500 free queries, no CC required)

### LangChain Integration

```python
from langchain_community.utilities import GoogleSerperAPIWrapper

# Initialize
search = GoogleSerperAPIWrapper()

# Basic search
results = search.results("Anthropic AI research")

# Result format:
# {
#   "searchParameters": {...},
#   "organic": [
#     {
#       "title": "Page title",
#       "link": "https://...",
#       "snippet": "Description...",
#       "position": 1
#     }
#   ],
#   "knowledgeGraph": {...},  # If available
#   "answerBox": {...}  # If available
# }
```

```python
# For LangChain agents
from langchain.agents import Tool

serper_tool = Tool(
    name="google_search",
    description="Search Google for recent results",
    func=search.run
)
```

### Advanced Options

```python
# News search
search = GoogleSerperAPIWrapper(type="news")

# Images
search = GoogleSerperAPIWrapper(type="images")

# With parameters
results = search.results(
    "query",
    num=10,  # Note: >10 results costs 2 credits
    gl="us",  # Country
    hl="en"   # Language
)
```

### Rate Limits
- Free tier: 2,500 lifetime queries
- Paid: No per-minute limits

### Best Practices
- **Best free production option** with 2,500 lifetime queries
- Use `num<=10` to avoid double credit usage
- Returns raw Google SERP data - great for knowledge graphs
- Upgrade to paid when free tier exhausted (very affordable)

---

