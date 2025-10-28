## 5. Brave Search

**Best for:** Privacy-focused search, independent index

### Overview
- **Free Tier:** Available (sign up required)
- **Pricing:** Free tier, paid plans for higher volume
- **Quality:** ⭐⭐⭐
- **Speed:** Medium
- **Special Features:**
  - Independent web index (not Bing-based)
  - Privacy-first (no user tracking)
  - Multiple endpoints (web, news, images)

### Setup

```bash
pip install langchain-community
```

**Environment Variable:**
```bash
export BRAVE_SEARCH_API_KEY="your_api_key_here"
```

Get your free API key: https://brave.com/search/api/

### LangChain Integration

```python
from langchain_community.utilities import BraveSearchWrapper

# Initialize
search = BraveSearchWrapper(search_kwargs={"count": 3})

# Basic search
result = search.run("Anthropic Claude AI")

# Returns: String with top results formatted

# For structured results
results = search.results("query", count=5)
```

```python
# As a tool
from langchain_community.tools import BraveSearch

brave_tool = BraveSearch.from_api_key(
    api_key="your_key",
    search_kwargs={"count": 3}
)

# Use in agent
results = await brave_tool.ainvoke("AI research news")
```

### Rate Limits
- Free tier limits vary (check current documentation)
- Generally suitable for development/testing

### Best Practices
- Best choice if privacy is a priority
- Independent index means different results than Google/Bing
- Good complement to other providers

---

