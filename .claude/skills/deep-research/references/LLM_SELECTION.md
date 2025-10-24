# LLM Selection Guide for Deep Research Agent

> **Always refer to**: [docs/LLM_CLOUD_PRICING_2025.md](../../../../docs/LLM_CLOUD_PRICING_2025.md) for latest pricing and models

## Overview

This guide helps you select the most cost-effective LLM for the deep research agent. Instead of maintaining pricing info here, we reference the central pricing document that is regularly updated.

## Quick Recommendations

### 🥇 Production (Lowest Cost)

**DeepSeek-chat + Caching** - $20/month for 1,000 companies

```python
from configuration import Configuration

config = Configuration(
    llm_model="deepseek-chat",
    temperature=0.3,
    search_provider="google_adk"  # Free search
)
```

**Why DeepSeek?**
- **$0.028/$0.42 per 1M tokens** (with caching)
- 90% cache discount for repeated queries
- 50-75% off-peak discount (16:30-00:30 UTC)
- **Total: $10-20/month** for production workload

See: [LLM_CLOUD_PRICING_2025.md - DeepSeek Section](../../../../docs/LLM_CLOUD_PRICING_2025.md#5%EF%B8%8F⃣-deepseek-2025년-10월)

---

### 🥈 Balanced (Quality + Cost)

**Qwen-Flash** - $19/month for 1,000 companies

```python
config = Configuration(
    llm_model="qwen-flash",
    temperature=0.3,
    search_provider="google_adk"
)
```

**Why Qwen?**
- **$0.05/$0.40 per 1M tokens**
- OpenAI API compatible
- Good quality, second-lowest price

See: [LLM_CLOUD_PRICING_2025.md - Qwen Section](../../../../docs/LLM_CLOUD_PRICING_2025.md#4%EF%B8%8F⃣-alibaba-qwen-2025년-10월)

---

### 🥉 Google Ecosystem

**Gemini 2.0 Flash** - $22/month for 1,000 companies

```python
config = Configuration(
    llm_model="gemini-2.0-flash",
    temperature=0.3,
    search_provider="google_adk",  # Native integration
    use_gemini_for_google_search=True
)
```

**Why Gemini?**
- **$0.10/$0.40 per 1M tokens**
- Native google_search tool (free)
- Best integration with Google ADK

See: [LLM_CLOUD_PRICING_2025.md - Gemini Section](../../../../docs/LLM_CLOUD_PRICING_2025.md#3%EF%B8%8F⃣-google-gemini-2025년-10월)

---

### 🏆 Premium Quality

**Claude Sonnet 4.5** - $40/month for 1,000 companies

```python
config = Configuration(
    llm_model="claude-sonnet-4-5-20250929",
    temperature=0.3,
    search_provider="hybrid"  # Cost optimization
)
```

**Why Claude?**
- **$3/$15 per 1M tokens**
- Best for complex reasoning and extraction
- Prompt caching: 90% discount
- Current default model

See: [LLM_CLOUD_PRICING_2025.md - Claude Section](../../../../docs/LLM_CLOUD_PRICING_2025.md#2%EF%B8%8F⃣-anthropic-claude-2025년-10월)

---

## Hybrid Strategy (Recommended for Scale)

Use different models for different phases:

```python
# Research phase (simple query generation)
research_llm = "deepseek-chat"  # $0.028/$0.42

# Extraction phase (complex JSON parsing)
extraction_llm = "claude-sonnet-4-5-20250929"  # $3/$15

# Reflection phase (quality evaluation)
reflection_llm = "qwen-flash"  # $0.05/$0.40
```

**Benefits:**
- 60-70% cost reduction
- Maintain quality where it matters
- Best performance/cost ratio

---

## Cost Comparison (1,000 companies/month)

| Strategy | LLM Cost | Search Cost | Total | Quality |
|----------|----------|-------------|-------|---------|
| **DeepSeek Only** | $2.66 | $0 (Google ADK) | **$20** | ⭐⭐⭐ |
| **Qwen Only** | $3.00 | $0 (Google ADK) | **$19** | ⭐⭐⭐ |
| **Gemini Only** | $4.00 | $0 (Google ADK) | **$22** | ⭐⭐⭐⭐ |
| **Claude Only** | $135 | $0 (Google ADK) | **$40** (cached) | ⭐⭐⭐⭐⭐ |
| **Hybrid** | $25 | $0 | **$25** | ⭐⭐⭐⭐ |

Assumptions: 20k input, 5k output tokens per company

---

## Implementation Examples

### DeepSeek with Caching

```python
from langchain_openai import ChatOpenAI  # DeepSeek is OpenAI-compatible

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3
)
```

### Qwen with OpenAI API

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="qwen-flash",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("QWEN_API_KEY"),
    temperature=0.3
)
```

### Gemini (Native)

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)
```

---

## When to Update LLM Selection

**Check pricing document when:**
1. New models are released (quarterly)
2. Pricing changes announced
3. Scaling to production (10,000+ companies/month)
4. Budget constraints change

**Action:** Review [LLM_CLOUD_PRICING_2025.md](../../../../docs/LLM_CLOUD_PRICING_2025.md) for latest recommendations.

---

## Migration Path

### Phase 1: Development (Free)
- Use: **DuckDuckGo** (free search) + **Gemini 2.0 Flash** (cheap)
- Cost: ~$0-5/month

### Phase 2: Testing (50-100 companies)
- Use: **DeepSeek** + **Google ADK** (free search)
- Cost: ~$5-10/month

### Phase 3: Production (1,000+ companies)
- Use: **DeepSeek Off-Peak** + **Caching** + **Google ADK**
- Cost: ~$10-20/month

### Phase 4: Scale (10,000+ companies)
- Use: **Hybrid strategy** (DeepSeek + Claude for complex cases)
- Cost: ~$100-200/month

---

## Best Practices

1. **Always check pricing doc first**: Models and pricing change frequently
2. **Test quality**: Run 10-20 companies with each model before committing
3. **Monitor costs**: Track actual token usage vs. estimates
4. **Use caching**: 90% discount for repeated system prompts
5. **Off-peak processing**: Schedule batch jobs during off-peak hours (DeepSeek)

---

## Troubleshooting

**Problem**: DeepSeek API is slow
- **Solution**: Use off-peak hours for better performance

**Problem**: Qwen giving errors
- **Solution**: Check API key format and base URL

**Problem**: Costs higher than expected
- **Solution**: Check context window usage (Qwen has tiered pricing)

---

## Additional Resources

- **Central Pricing Document**: [docs/LLM_CLOUD_PRICING_2025.md](../../../../docs/LLM_CLOUD_PRICING_2025.md)
- **Search Provider Selection**: [SEARCH_PROVIDERS.md](./SEARCH_PROVIDERS.md)
- **Production Checklist**: [PRODUCTION_CHECKLIST.md](./PRODUCTION_CHECKLIST.md)

---

**Last Updated**: 2025-10-24
**Pricing Source**: See central pricing document for authoritative pricing
