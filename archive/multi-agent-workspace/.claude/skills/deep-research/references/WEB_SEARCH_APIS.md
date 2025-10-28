# Web Search APIs - Complete Reference

Quick reference index for web search APIs with free tiers and production-ready options.

## 🔍 API-Specific Guides

Each API has its own dedicated guide with pricing, setup, code examples, and best practices.

| API | Free Tier | Quality | Speed | Guide |
|-----|-----------|---------|-------|-------|
| **Tavily** | 1,000/month | ⭐⭐⭐⭐⭐ | Fast | [api/tavily.md](./api/tavily.md) |
| **Jina AI Reader** | 200 RPM | ⭐⭐⭐ | Fast | [api/jina.md](./api/jina.md) |
| **Serper.dev** | 2,500 lifetime | ⭐⭐⭐⭐ | Very Fast | [api/serper.md](./api/serper.md) |
| **Exa** | $10 credit | ⭐⭐⭐⭐ | Fast | [api/exa.md](./api/exa.md) |
| **Brave Search** | Free tier | ⭐⭐⭐ | Medium | [api/brave.md](./api/brave.md) |
| **DuckDuckGo** | Unlimited | ⭐⭐ | Slow | [api/duckduckgo.md](./api/duckduckgo.md) |
| **SerpAPI** | 100/month | ⭐⭐⭐⭐ | Fast | [api/serpapi.md](./api/serpapi.md) |
| **Bing Search** | 1,000/month | ⭐⭐⭐ | Fast | [api/bing.md](./api/bing.md) |

## 🛠️ Common Guides

- **[Best Practices](./api/best-practices.md)** - Provider selection, error handling, rate limiting

## 📊 Quick Comparison

### By Use Case

**Production Deep Research?**
- [Tavily](./api/tavily.md) - Best quality, AI-optimized
- [Serper.dev](./api/serper.md) - Best free tier (2,500 lifetime)

**Development & Testing?**
- [Jina AI Reader](./api/jina.md) - Great free tier (200 RPM)
- [DuckDuckGo](./api/duckduckgo.md) - Unlimited, free

**Semantic/AI Search?**
- [Exa](./api/exa.md) - AI-native search

**Privacy-Focused?**
- [Brave Search](./api/brave.md) - No tracking

**Google Results?**
- [SerpAPI](./api/serpapi.md) - Google scraping
- [Serper.dev](./api/serper.md) - Google API

**Microsoft Ecosystem?**
- [Bing Search](./api/bing.md) - Bing API

### By Budget

| Budget | Recommended APIs |
|--------|------------------|
| **$0 (Free)** | [DuckDuckGo](./api/duckduckgo.md) (unlimited), [Serper.dev](./api/serper.md) (2,500 lifetime) |
| **$0-$10/month** | [Tavily](./api/tavily.md) (1,000 free), [Jina](./api/jina.md), [Brave](./api/brave.md) |
| **Production** | [Tavily](./api/tavily.md), [Serper.dev](./api/serper.md), [Exa](./api/exa.md) |

### By Speed

| Speed | APIs |
|-------|------|
| **Very Fast (1-2s)** | [Serper.dev](./api/serper.md), [Tavily](./api/tavily.md) |
| **Fast (2-4s)** | [Jina](./api/jina.md), [Exa](./api/exa.md), [SerpAPI](./api/serpapi.md), [Bing](./api/bing.md) |
| **Medium (5-10s)** | [Brave](./api/brave.md) |
| **Slow (10s+)** | [DuckDuckGo](./api/duckduckgo.md) |

## 📝 What's in Each Guide?

Each API guide includes:

- **Overview** - What the API is best for
- **Pricing** - Free tier and paid pricing
- **Setup** - Installation and API key setup
- **LangChain Integration** - Ready-to-use code examples
- **Direct HTTP Example** - For non-LangChain use
- **Rate Limits** - Request limits and handling
- **Pros & Cons** - Detailed comparison
- **Official Docs** - Links to documentation

## 🚀 Getting Started

1. **Choose an API** from the table above based on your use case and budget
2. **Read the specific guide** for setup and code examples
3. **Check best practices** for production-ready implementation

## 💡 Quick Recommendations

### For Your Project

```python
# Prototyping / Testing (Free)
from langchain_community.tools import DuckDuckGoSearchResults
# See: api/duckduckgo.md

# Production (Best Quality)
from langchain_community.tools.tavily_search import TavilySearchResults
# See: api/tavily.md

# Production (Best Free Tier)
from langchain_community.utilities import GoogleSerperAPIWrapper
# See: api/serper.md

# Semantic Search
from langchain_community.tools import ExaSearchResults
# See: api/exa.md
```

## 📚 Additional Resources

### Official Documentation

All guides include links to official documentation:

- **Tavily**: https://docs.tavily.com/
- **Jina AI**: https://jina.ai/reader/
- **Serper.dev**: https://serper.dev/
- **Exa**: https://exa.ai/
- **Brave Search**: https://brave.com/search/api/
- **DuckDuckGo**: https://github.com/deedy5/duckduckgo_search
- **SerpAPI**: https://serpapi.com/
- **Bing Search**: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api

### Related References

- **[PRIVATE_SME_RESEARCH.md](./PRIVATE_SME_RESEARCH.md)** - Research strategies for private companies

---

**Total Guides**: 9 (8 APIs + best practices)
**Last Updated**: 2025-10-23
**Maintainer**: Deep Research Skill
