---
name: Company Deep Research Agent
description: Build a production-ready AI agent that performs deep web research on companies using LangGraph with a research-extraction-reflection iterative loop. Supports 7+ web search providers (including free tiers), with rate limiting, deduplication, and token management. Use this when the user wants to automatically search the web for company information, extract structured JSON data, implement quality evaluation loops, or build production-ready research automation.
allowed-tools: Write, Edit, Read, Bash
---

# Company Deep Research Agent

Build a production-ready web research agent that automatically searches the web, extracts structured information, and iteratively improves research quality.

## When to Use This Skill

Use this skill when building agents that need to:
- Automatically search the web for company information
- Extract structured data from web searches (JSON schema-driven)
- Implement quality evaluation loops (reflection phase)
- Handle private SME research (non-public companies)
- Deploy production-ready systems with rate limiting and error handling

## Target Use Case: Private SME Research

This system is optimized for **private/unlisted companies** (10-1,000 employees) where structured data is limited. Research uses both direct sources (company websites, news) and indirect sources (public company filings, VC portfolios, government records).

## Architecture Overview

The agent uses a three-phase research loop:

```
1. RESEARCH → Generate queries → Execute web searches → Deduplicate → Collect notes
              ↓
2. EXTRACTION → Parse notes → Extract to JSON schema → Format output
              ↓
3. REFLECTION → Evaluate completeness → Identify gaps → Generate follow-ups
              ↓
         [Complete or Loop Back to Step 1]
```

**Production optimizations:**
- Rate limiting: 0.8 req/sec (Anthropic Tier 1 compliance)
- URL deduplication: Prevents duplicate API calls
- Token limits: Max 1,000 tokens per source
- Error handling: Automatic fallback to free providers

## Implementation Guide

### 1. Project Structure

Create the following directory structure:

```
src/agents/company_research/
├── __init__.py
├── configuration.py    # Config with 7+ search providers
├── state.py           # ResearchState, DEFAULT_SCHEMA
├── llm.py             # LLM with rate limiting
├── utils.py           # Reusable functions (deduplication, formatting)
├── prompts.py         # Centralized prompts
├── research.py        # Research phase (7 providers)
├── extraction.py      # JSON extraction
├── reflection.py      # Quality evaluation
└── graph.py           # LangGraph workflow
```

### 2. Implementation Steps

**Start with the existing implementation:**
The codebase already contains a complete implementation at `src/agents/company_research/`. Use this as the foundation:

1. **Configuration** (`configuration.py`): Supports 7 search providers (Tavily, Google ADK, Hybrid, SerpAPI, Bing, DuckDuckGo, Brave)

2. **Production utilities** (`llm.py`, `utils.py`, `prompts.py`):
   - Rate limiting via `InMemoryRateLimiter` (0.8 req/sec)
   - URL deduplication via `deduplicate_sources()`
   - Token management via `format_sources(max_tokens_per_source=1000)`
   - Centralized prompts for query generation, extraction, reflection

3. **Three-phase workflow** (`research.py`, `extraction.py`, `reflection.py`):
   - Research: Query generation + multi-provider web search
   - Extraction: JSON schema-driven data extraction
   - Reflection: Quality evaluation + follow-up query generation

4. **Graph orchestration** (`graph.py`):
   - LangGraph state machine with conditional routing
   - Automatic iteration until completeness threshold (85%) or max iterations

### 3. Search Provider Selection

Choose based on budget and quality needs:

| Provider | Free Tier | Cost | Quality | Use Case |
|----------|-----------|------|---------|----------|
| **Tavily** | 1,000/month | $0.005/query | ⭐⭐⭐⭐⭐ | Production (best) |
| **Google ADK** | Unlimited* | Free | ⭐⭐⭐⭐ | Free production |
| **Hybrid** | Mixed | Low | ⭐⭐⭐⭐ | Cost optimization |
| **DuckDuckGo** | Unlimited | Free | ⭐⭐ | Testing |

*Requires Gemini 2.0+ models

All providers are fully implemented in `research.py` with error handling and fallbacks.

### 4. Usage Example

```python
import asyncio
from src.agents.company_research import (
    Configuration, DEFAULT_SCHEMA, build_research_graph
)

async def main():
    # Configure with free provider
    config = Configuration(
        max_search_queries=3,
        max_search_results=3,
        search_provider="duckduckgo"  # Free
    )

    graph = build_research_graph(config)

    # Run research
    result = await graph.ainvoke({
        "company_name": "Anthropic",
        "extraction_schema": DEFAULT_SCHEMA,
        "user_context": "Focus on AI safety research",
        "research_queries": [],
        "search_results": [],
        "research_notes": "",
        "extracted_data": {},
        "reflection_count": 0,
        "missing_fields": [],
        "follow_up_queries": [],
        "is_complete": False,
        "messages": []
    })

    print(result["extracted_data"])

asyncio.run(main())
```

### 5. Customization

**Custom schemas:**
Replace `DEFAULT_SCHEMA` with domain-specific schemas (e.g., tech startups, financial analysis).

**Cost optimization:**
Use `search_provider="hybrid"` for 50% cost reduction (Tavily for main queries, Google ADK for follow-ups).

**Rate limiting:**
For Anthropic Tier 2, adjust in `llm.py`:
```python
_rate_limiter = InMemoryRateLimiter(
    requests_per_second=16.6,  # ~1,000 req/min
)
```

## Production Best Practices

1. **Start simple**: Use DuckDuckGo (free) for development
2. **Test quality**: Try Tavily with sample companies
3. **Optimize cost**: Switch to Hybrid for production
4. **Monitor performance**: Target 85%+ schema completeness
5. **Set API keys**: Export `TAVILY_API_KEY`, `GOOGLE_API_KEY`, etc.

## Performance Metrics

- **Processing time**: 45-90 seconds per company
- **API calls**: 3-9 per company (with deduplication)
- **Cost (Tavily)**: ~$0.015-0.045 per company
- **Cost (Hybrid)**: ~$0.0075-0.0225 per company (50% savings)
- **Success rate**: 85-95% (schema completeness)

## Reference Materials

For detailed implementation guidance, see:
- `references/IMPLEMENTATION_GUIDE.md` - Complete code examples for all 10 files
- `references/SEARCH_PROVIDERS.md` - Detailed guide for all 7 search providers
- `references/TROUBLESHOOTING.md` - Common issues and solutions
- `references/PRODUCTION_CHECKLIST.md` - Pre-deployment validation

## Dependencies

```bash
# Core
pip install langgraph>=0.2.0 langchain>=0.3.0 langchain-anthropic>=0.2.0
pip install langchain-community>=0.3.0 pydantic>=2.0.0

# Search providers (install as needed)
pip install tavily-python>=0.3.0          # Tavily
pip install langchain-google-genai        # Google ADK (free)
pip install duckduckgo-search            # DuckDuckGo (free)
```

## Quick Start Workflow

1. **Use existing code**: Check `src/agents/company_research/` - complete implementation exists
2. **Test locally**: Run `examples/basic_research.py` with DuckDuckGo
3. **Customize**: Adjust schema, provider, or rate limits
4. **Deploy**: Use production checklist in references

This skill leverages existing production-ready code. Focus on configuration and customization rather than building from scratch.
