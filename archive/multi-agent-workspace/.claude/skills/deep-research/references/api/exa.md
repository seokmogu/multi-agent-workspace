## 4. Exa

**Best for:** AI-native semantic search, finding similar content

### Overview
- **Free Tier:**
  - Python: $10 free credit on signup
  - JavaScript: 1,000 searches/month
- **Pricing:** Varies by search type
- **Quality:** ⭐⭐⭐⭐ (AI-native, semantic understanding)
- **Speed:** Fast
- **Special Features:**
  - 4 search modes: Auto, Fast, Keyword, Neural
  - Semantic similarity search
  - Find similar content
  - Highlights extraction

### Setup

```bash
pip install exa-py langchain-exa
```

**Environment Variable:**
```bash
export EXA_API_KEY="your_api_key_here"
```

Get your free API key: https://exa.ai/ ($10 credit or 1k searches/month)

### LangChain Integration

```python
from langchain_exa import ExaSearchRetriever

# Initialize
retriever = ExaSearchRetriever(
    k=3,  # Number of results
    highlights=True
)

# Search
documents = await retriever.ainvoke("AI safety research latest developments")

# Result format: List of LangChain Documents
# [
#   Document(
#     page_content="...",
#     metadata={"url": "...", "title": "...", "highlights": [...]}
#   )
# ]
```

```python
# Advanced: Using ExaSearchResults tool
from langchain_exa import ExaSearchResults

search_tool = ExaSearchResults(
    num_results=5,
    text_contents_options=True,  # Get full text
    highlights={"num_sentences": 3}
)

results = await search_tool.ainvoke("quantum computing breakthroughs")
```

### Search Modes

```python
from exa_py import Exa

exa = Exa(api_key="your_key")

# Auto mode (recommended)
results = exa.search("AI safety", type="auto", num_results=5)

# Neural mode (semantic search)
results = exa.search("companies like Anthropic", type="neural")

# Keyword mode (traditional)
results = exa.search("exact phrase matching", type="keyword")
```

### Rate Limits
- Free tier: $10 credit or 1,000/month depending on platform
- Varies by search type (neural vs keyword)

### Best Practices
- Use `type="neural"` for semantic/conceptual queries
- Use `type="keyword"` for exact phrase matching
- Enable `highlights` to get key sentences extracted
- Great for "find similar to X" queries

---

