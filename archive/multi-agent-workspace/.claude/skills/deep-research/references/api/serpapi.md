## 7. SerpAPI

**Best for:** Google result scraping, enterprise reliability

### Overview
- **Free Tier:** 100 searches/month
- **Pricing:** $50/month for 5,000 searches
- **Quality:** ⭐⭐⭐⭐
- **Speed:** Fast
- **Special Features:**
  - Real Google results (all features)
  - Multiple search engines (Google, Bing, Yahoo, etc.)
  - All SERP features (knowledge graph, featured snippets, etc.)
  - Official LangChain integration

### Setup

```bash
pip install google-search-results langchain-community
```

**Environment Variable:**
```bash
export SERPAPI_API_KEY="your_api_key_here"
```

Get your API key: https://serpapi.com/ (100 free searches/month)

### LangChain Integration

```python
from langchain_community.utilities import SerpAPIWrapper

# Initialize
search = SerpAPIWrapper()

# Basic search
results = search.run("Anthropic AI")

# For structured results
result_dict = search.results("query")

# Result format:
# {
#   "organic_results": [...],
#   "knowledge_graph": {...},
#   "answer_box": {...}
# }
```

```python
# Advanced options
from serpapi import GoogleSearch

params = {
    "q": "AI research",
    "location": "Austin, Texas",
    "hl": "en",
    "gl": "us",
    "api_key": "your_key"
}

search = GoogleSearch(params)
results = search.get_dict()
```

### Rate Limits
- Free tier: 100 searches/month
- Paid: Based on plan

### Best Practices
- Most reliable for scraping Google results
- Expensive compared to Serper - use Serper for better value
- Good for enterprise applications needing reliability
- Supports many search engines beyond Google

---

