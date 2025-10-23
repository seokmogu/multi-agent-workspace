## 8. Bing Search API

**Best for:** Microsoft ecosystem integration

### Overview
- **Free Tier:** 1,000 transactions/month
- **Pricing:** $7 per 1,000 queries after free tier
- **Quality:** ⭐⭐⭐
- **Speed:** Fast
- **Special Features:**
  - Microsoft Azure integration
  - Web, image, video, news search
  - Spell check, autosuggest

### ⚠️ Important Note
**Bing Search API is being retired on August 11, 2025.** Microsoft is migrating users to "Grounding with Bing Search." Consider alternative providers for new projects.

### Setup (while still available)

```bash
pip install langchain-community
```

**Environment Variable:**
```bash
export BING_SUBSCRIPTION_KEY="your_subscription_key"
export BING_SEARCH_URL="https://api.bing.microsoft.com/v7.0/search"
```

Get your key: https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/

### LangChain Integration

```python
from langchain_community.utilities import BingSearchAPIWrapper

# Initialize
search = BingSearchAPIWrapper(k=3)

# Search
results = search.results("AI research", num_results=5)

# Result format:
# [
#   {
#     "title": "...",
#     "link": "...",
#     "snippet": "..."
#   }
# ]
```

### Rate Limits
- Free tier: 1,000/month
- Paid: $7 per 1,000 queries

### Best Practices
- **Migrate to alternatives before August 2025**
- Consider Serper or Brave as replacements
- Only use if already in Microsoft ecosystem

---

