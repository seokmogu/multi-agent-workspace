## Provider Selection Guide

### For Different Use Cases

**Just Starting / Testing:**
- **Best choice:** DuckDuckGo (free, no key)
- **Why:** Zero setup, unlimited testing

**Development / MVP:**
- **Best choice:** Jina AI Reader (200 RPM free) or Serper (2,500 lifetime free)
- **Why:** High free tiers, good quality

**Production (Budget-Conscious):**
- **Best choice:** Serper.dev
- **Why:** 2,500 free queries, then very affordable ($0.30-1.00/1k)

**Production (Best Quality):**
- **Best choice:** Tavily
- **Why:** Optimized for AI/LLMs, best quality results

**Semantic / AI-Native Search:**
- **Best choice:** Exa
- **Why:** Neural search, semantic understanding

**Privacy-Focused:**
- **Best choice:** Brave or DuckDuckGo
- **Why:** No tracking, independent indexes

### Cost Comparison (per 1,000 queries)

| Provider | Free Tier | Cost After Free |
|----------|-----------|-----------------|
| DuckDuckGo | ∞ | Free |
| Jina AI | 10M tokens | Token-based |
| Serper | 2,500 lifetime | $0.30-$1.00 |
| Tavily | 1,000/month | $8.00 |
| Exa | $10 credit or 1k/mo | Varies |
| Brave | Yes | Unknown |
| SerpAPI | 100/month | $10.00 |
| Bing | 1,000/month | $7.00 (retiring) |

### Recommended Stack

**Hybrid Approach:**
```python
def get_search_provider(query_type: str, budget_remaining: int):
    if budget_remaining == 0:
        return "duckduckgo"  # Free fallback
    elif query_type == "semantic":
        return "exa"  # AI-native search
    elif budget_remaining < 100:
        return "serper"  # Best free production option
    else:
        return "tavily"  # Best quality
```

---

## Error Handling Patterns

### Universal Error Handler

```python
import asyncio
from typing import Optional, List, Dict

async def search_with_fallback(
    query: str,
    providers: List[str] = ["tavily", "serper", "duckduckgo"]
) -> Optional[List[Dict]]:
    """Try providers in order until one succeeds."""

    for provider in providers:
        try:
            if provider == "tavily":
                search = TavilySearchResults(max_results=3)
                return await search.ainvoke(query)

            elif provider == "serper":
                search = GoogleSerperAPIWrapper()
                results = search.results(query)
                return results.get("organic", [])

            elif provider == "duckduckgo":
                search = DuckDuckGoSearchAPIWrapper()
                result_text = search.run(query)
                # Parse and return
                return [{"content": result_text}]

        except Exception as e:
            print(f"{provider} failed: {e}, trying next...")
            continue

    print("All providers failed")
    return None
```

### Rate Limit Handling

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def search_with_retry(query: str, provider: str):
    """Retry with exponential backoff."""
    # Your search logic here
    pass
```

---

## Conclusion

**TL;DR Recommendations:**

1. **Starting out?** Use **DuckDuckGo** (free, no setup)
2. **Building MVP?** Use **Serper** (2,500 free queries)
3. **Production app?** Use **Tavily** (best quality) or **Serper** (best value)
4. **Need semantic search?** Use **Exa**
5. **Privacy matters?** Use **Brave**
6. **No budget ever?** Use **DuckDuckGo**

All providers integrate seamlessly with LangChain. Start with free tiers, monitor quality, and upgrade as needed.
