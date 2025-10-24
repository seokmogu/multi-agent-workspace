# Architecture Patterns

Detailed documentation of the 6 core patterns identified in multi-agent workspaces.

## Table of Contents

1. [Prompt Centralization](#1-prompt-centralization)
2. [Rate Limiting](#2-rate-limiting)
3. [State Management](#3-state-management)
4. [Pydantic Configuration](#4-pydantic-configuration)
5. [Utils Module](#5-utils-module)
6. [Multi-Agent Architecture](#6-multi-agent-architecture)

---

## 1. Prompt Centralization

### Overview

Centralize all LLM prompts in a single module (`prompts.py`) for maintainability, version control, and testing.

### Problem

Scattered prompts across codebase:
- Hard to maintain consistency
- Difficult to A/B test prompt variations
- No single source of truth
- Version control is messy (prompts buried in code)

### Solution

```python
# prompts.py
QUERY_WRITER_PROMPT = """You are a search query expert...

Target Company: {company_name}

Generate {max_search_queries} queries for:
{schema}

Return JSON array: ["query 1", "query 2"]
"""

INFO_PROMPT = """You are researching: {company_name}

Schema:
{schema}

Website contents:
{content}

Take detailed notes.
"""

EXTRACTION_PROMPT = """Extract from notes:
{notes}

To schema:
{schema}

Return valid JSON.
"""
```

### Benefits

✅ **Single Source**: All prompts in one place
✅ **Version Control**: Easy to track prompt changes in git
✅ **Testing**: Can test prompts independently
✅ **Variables**: Use `.format()` for dynamic content
✅ **Documentation**: Add comments explaining prompt strategy

### Implementation

```python
# agents/my_agent/prompts.py

# Query Generation
MAIN_PROMPT = """Your prompt here with {variables}."""

# Follow-up prompt
REFLECTION_PROMPT = """Another prompt with {other_vars}."""

# Usage in code
from .prompts import MAIN_PROMPT

prompt = MAIN_PROMPT.format(
    variables="value",
    other_vars="data"
)
response = llm.invoke(prompt)
```

### When to Use

✅ Use when:
- Multiple LLM calls in agent
- Prompts need iteration/testing
- Team collaboration on prompts
- A/B testing prompt variations

❌ Don't use when:
- Single simple prompt
- Prototype/one-off script
- No collaboration needed

---

## 2. Rate Limiting

### Overview

Implement API rate limiting to prevent throttling and ensure compliance with LLM provider tiers.

### Problem

API throttling errors:
```
anthropic.RateLimitError: Rate limit exceeded
```

Causes:
- Burst requests exceed tier limits
- No backoff/retry strategy
- Multiple agents share quota

### Solution

```python
# llm.py
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_anthropic import ChatAnthropic

# Global rate limiter
_rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.8,  # ~50 req/min (Tier 1)
    check_every_n_seconds=0.1,
    max_bucket_size=10,  # Allow small bursts
)

def get_llm(config, temperature=None):
    """Get rate-limited LLM instance."""
    return ChatAnthropic(
        model=config.llm_model,
        temperature=temperature or config.temperature,
        rate_limiter=_rate_limiter,
        max_tokens=4096,
    )
```

### Anthropic API Tier Limits

| Tier | Requests/min | Tokens/min | Recommended Setting |
|------|--------------|------------|---------------------|
| Tier 1 | 50 | 40,000 | 0.8 req/sec |
| Tier 2 | 1,000 | 80,000 | 16 req/sec |
| Tier 3 | 2,000 | 160,000 | 32 req/sec |
| Tier 4 | 4,000 | 400,000 | 64 req/sec |

**Formula**: `requests_per_second = (requests_per_min / 60) * 0.95` (5% safety margin)

### Task-Specific Temperature

Different tasks need different temperatures:

```python
def get_llm_for_research(config):
    """Higher temperature for creative research."""
    return get_llm(config, temperature=0.7)

def get_llm_for_extraction(config):
    """Lower temperature for precise extraction."""
    return get_llm(config, temperature=0.3)

def get_llm_for_reflection(config):
    """Balanced temperature for quality analysis."""
    return get_llm(config, temperature=0.5)
```

### Benefits

✅ **No Throttling**: Automatic rate limiting prevents 429 errors
✅ **Tier Compliance**: Configurable per API tier
✅ **Burst Support**: Small bursts allowed (max_bucket_size)
✅ **Task Optimization**: Different temperatures per task

### Implementation Checklist

- [ ] Create `llm.py` module
- [ ] Configure rate limiter for your API tier
- [ ] Replace all direct `ChatAnthropic()` calls with `get_llm()`
- [ ] Use task-specific functions (`get_llm_for_research()`, etc.)
- [ ] Monitor rate limit errors in logs

### When to Use

✅ Use when:
- Production LLM application
- Batch processing multiple items
- Subject to API tier limits
- Multiple concurrent requests

❌ Don't use when:
- Single request prototype
- Testing/development only
- No rate limits on API

---

## 3. State Management

### Overview

Type-safe state tracking with TypedDict for LangGraph multi-phase workflows.

### Problem

Unstructured state:
```python
# ❌ Bad: No type safety
state = {}
state["results"] = []  # Typo-prone
state["comptele"] = True  # Typo undetected!
```

### Solution

```python
# state.py
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class ResearchState(TypedDict):
    """
    State for research agent workflow.

    Tracks: Research → Extraction → Reflection
    """

    # Input
    company_name: str
    extraction_schema: Dict[str, Any]
    user_context: str

    # Research phase
    research_queries: List[str]
    search_results: List[Dict[str, Any]]
    research_notes: str

    # Extraction phase
    extracted_data: Dict[str, Any]

    # Reflection phase
    reflection_count: int
    missing_fields: List[str]
    follow_up_queries: List[str]

    # Control flow
    is_complete: bool
    messages: Annotated[List[BaseMessage], add_messages]
```

### Benefits

✅ **Type Safety**: IDE autocomplete, type checking
✅ **Documentation**: Self-documenting workflow phases
✅ **LangGraph Compatible**: Works seamlessly with StateGraph
✅ **Reducers**: Use `Annotated` for custom merge logic

### LangGraph Integration

```python
from langgraph.graph import StateGraph
from .state import ResearchState

# Create graph with typed state
graph = StateGraph(ResearchState)

# Add nodes
graph.add_node("research", research_node)
graph.add_node("extract", extract_node)
graph.add_node("reflect", reflect_node)

# Nodes receive/return typed state
def research_node(state: ResearchState, config) -> ResearchState:
    # IDE knows all fields!
    company = state["company_name"]
    state["research_queries"] = ["query 1", "query 2"]
    return state
```

### Reducers with Annotated

For fields that need special merge logic:

```python
from langgraph.graph.message import add_messages

# Messages use add_messages reducer
messages: Annotated[List[BaseMessage], add_messages]

# Custom reducer
def append_unique(existing: List[str], new: List[str]) -> List[str]:
    return list(set(existing + new))

queries: Annotated[List[str], append_unique]
```

### When to Use

✅ Use when:
- Multi-phase LangGraph workflow
- State passed between nodes
- Need type safety and documentation
- Complex state with many fields

❌ Don't use when:
- Single-phase simple agent
- No LangGraph (use Pydantic BaseModel instead)
- State fits in function arguments

---

## 4. Pydantic Configuration

### Overview

Type-safe, validated, documented configuration with Pydantic BaseModel.

### Problem

Unvalidated config:
```python
# ❌ Bad: No validation
config = {
    "max_queries": "5",  # Should be int!
    "temprature": 0.7,   # Typo undetected!
}
```

### Solution

```python
# configuration.py
from typing import Annotated, Literal
from pydantic import BaseModel, Field

class Configuration(BaseModel):
    """Configuration for research agent."""

    max_search_queries: Annotated[
        int,
        Field(
            description="Max search queries per company",
            ge=1,  # >= 1
            le=10,  # <= 10
        ),
    ] = 3

    max_search_results: Annotated[
        int,
        Field(
            description="Max results per query",
            ge=1,
            le=10,
        ),
    ] = 3

    llm_model: str = "claude-sonnet-4-5-20250929"

    temperature: float = 0.7

    search_provider: Annotated[
        Literal["tavily", "google_adk", "duckduckgo"],
        Field(description="Web search provider"),
    ] = "tavily"

    class Config:
        frozen = True  # Immutable
```

### Benefits

✅ **Type Safety**: Runtime validation
✅ **Constraints**: `ge`, `le`, `gt`, `lt` validation
✅ **Documentation**: Self-documenting fields
✅ **Immutability**: `frozen=True` prevents accidental changes
✅ **IDE Support**: Autocomplete and type hints

### Usage

```python
from .configuration import Configuration

# Valid
config = Configuration(max_search_queries=5)

# Validation error
config = Configuration(max_search_queries=20)
# ❌ ValidationError: max_search_queries must be <= 10

# Immutable
config.temperature = 0.5
# ❌ ValidationError: "Configuration" is frozen
```

### Advanced Features

**Literal types** for enums:
```python
Literal["option1", "option2", "option3"]
```

**Custom validators**:
```python
from pydantic import validator

@validator("temperature")
def validate_temperature(cls, v):
    if not 0.0 <= v <= 1.0:
        raise ValueError("Temperature must be 0.0-1.0")
    return v
```

**Nested configs**:
```python
class DatabaseConfig(BaseModel):
    host: str
    port: int = 5432

class Configuration(BaseModel):
    database: DatabaseConfig
```

### When to Use

✅ Use when:
- Multiple configuration parameters
- Need validation and constraints
- Configuration shared across modules
- Production application

❌ Don't use when:
- 1-2 simple parameters
- Prototype/one-off script
- No validation needed

---

## 5. Utils Module

### Overview

Reusable helper functions shared across agents to avoid code duplication.

### Problem

Duplicated logic:
```python
# research.py
def deduplicate(sources):
    seen = set()
    unique = []
    for s in sources:
        if s["url"] not in seen:
            seen.add(s["url"])
            unique.append(s)
    return unique

# extraction.py
def deduplicate(sources):  # ❌ Same code repeated!
    # ... same logic ...
```

### Solution

```python
# utils.py - Centralized utilities

def deduplicate_sources(search_response):
    """Deduplicate by URL."""
    # Handle multiple input formats
    if isinstance(search_response, dict):
        sources_list = search_response.get('results', [])
    elif isinstance(search_response, list):
        sources_list = []
        for resp in search_response:
            if isinstance(resp, dict) and 'results' in resp:
                sources_list.extend(resp['results'])

    # Deduplicate
    unique_urls = set()
    unique_sources = []
    for source in sources_list:
        url = source.get('url', '')
        if url and url not in unique_urls:
            unique_urls.add(url)
            unique_sources.append(source)

    return unique_sources


def format_sources(sources_list, max_tokens_per_source=1000):
    """Format with token limits to prevent overflow."""
    if not sources_list:
        return "No sources found."

    formatted = "Sources:\\n\\n"
    for idx, source in enumerate(sources_list, 1):
        title = source.get('title', 'No title')
        url = source.get('url', 'No URL')
        content = source.get('content', 'No content')

        formatted += f"Source {idx}: {title}\\n"
        formatted += f"URL: {url}\\n"
        formatted += f"Snippet: {content}\\n"

        # Limit raw_content to prevent token overflow
        raw_content = source.get('raw_content', '')
        char_limit = max_tokens_per_source * 4  # ~4 chars/token
        if len(raw_content) > char_limit:
            raw_content = raw_content[:char_limit] + "... [truncated]"

        formatted += f"Full Content: {raw_content}\\n\\n"

    return formatted


def calculate_completeness(extracted, schema):
    """Calculate extraction completeness score."""
    properties = schema.get('properties', {})
    required_fields = schema.get('required', [])

    if not properties:
        return [], 1.0

    missing = []
    filled = 0

    for field in properties:
        value = extracted.get(field)
        is_empty = (
            value is None or
            value == "" or
            value == "null" or
            value == "unknown" or
            (isinstance(value, list) and len(value) == 0)
        )

        if is_empty:
            if field in required_fields:
                missing.append(f"{field} (required)")
            else:
                missing.append(field)
        else:
            filled += 1

    completeness = filled / len(properties)
    return missing, completeness
```

### Complete Function List

1. **`deduplicate_sources()`**: Remove duplicate URLs
2. **`format_sources()`**: Format with token limits
3. **`format_all_notes()`**: Consolidate research notes
4. **`calculate_completeness()`**: Score extraction completeness
5. **`truncate_text()`**: Safe text truncation
6. **`extract_field_descriptions()`**: Get schema descriptions
7. **`merge_research_results()`**: Alias for `format_all_notes()`
8. **`calculate_confidence_score()`**: Alias for `calculate_completeness()`

### Benefits

✅ **DRY Principle**: Don't Repeat Yourself
✅ **Tested Once**: Bugs fixed in one place
✅ **Consistent Behavior**: Same logic everywhere
✅ **Easy Updates**: Change once, applies everywhere

### When to Use

✅ Use when:
- Function used in 2+ places
- Logic is domain-agnostic
- Want consistent behavior
- Testing strategy matters

❌ Don't use when:
- Function used only once
- Highly domain-specific logic
- Performance-critical (inline instead)

---

## 6. Multi-Agent Architecture

### Overview

3-phase iterative loop: Research → Extraction → Reflection → Loop or Complete.

### Architecture Diagram

```
┌─────────────┐
│   START     │
│ (Input)     │
└──────┬──────┘
       ↓
┌─────────────────────────────────┐
│  RESEARCH PHASE                  │
│  - Generate search queries       │
│  - Execute web searches          │
│  - Deduplicate results           │
│  - Take structured notes         │
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│  EXTRACTION PHASE                │
│  - Parse research notes          │
│  - Extract to JSON schema        │
│  - Validate structure            │
│  - Calculate completeness        │
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│  REFLECTION PHASE                │
│  - Evaluate completeness         │
│  - Identify missing fields       │
│  - Generate follow-up queries    │
│  - Decide: Complete or Continue  │
└──────────────┬──────────────────┘
               │
         ┌─────┴─────┐
         ↓           ↓
    [COMPLETE]   [CONTINUE]
         ↓           │
      ┌─────┐       │
      │ END │       │
      └─────┘       │
                    │
     ───────────────┘
     (Loop back to RESEARCH)
```

### Implementation

```python
# graph.py
from langgraph.graph import StateGraph, END
from .state import ResearchState
from .research import research_node
from .extraction import extract_node
from .reflection import reflect_node

def should_continue(state: ResearchState) -> str:
    """Route based on reflection result."""
    if state["is_complete"]:
        return "complete"
    if state["reflection_count"] >= config.max_reflection_steps:
        return "complete"
    return "continue"

def create_graph(config):
    """Create research agent graph."""
    graph = StateGraph(ResearchState)

    # Add nodes
    graph.add_node("research", lambda s: research_node(s, config))
    graph.add_node("extract", lambda s: extract_node(s, config))
    graph.add_node("reflect", lambda s: reflect_node(s, config))

    # Set entry
    graph.set_entry_point("research")

    # Add edges
    graph.add_edge("research", "extract")
    graph.add_edge("extract", "reflect")

    # Conditional routing
    graph.add_conditional_edges(
        "reflect",
        should_continue,
        {"continue": "research", "complete": END}
    )

    return graph.compile()
```

### Phase Details

#### Research Phase

**Input**: `company_name`, `extraction_schema`, `user_context`

**Process**:
1. Generate 3-5 search queries (LLM)
2. Execute searches (Tavily/Google/etc.)
3. Deduplicate URLs (save costs)
4. Scrape content
5. Take structured notes (LLM)

**Output**: `research_notes` (plain text)

#### Extraction Phase

**Input**: `research_notes`, `extraction_schema`

**Process**:
1. Parse notes
2. Extract to JSON matching schema
3. Validate structure
4. Calculate completeness score

**Output**: `extracted_data` (JSON), `missing_fields`

#### Reflection Phase

**Input**: `extracted_data`, `missing_fields`, `schema`

**Process**:
1. Evaluate completeness (threshold: 0.8)
2. Identify critical missing fields
3. Generate 2-3 follow-up queries
4. Decide: complete or continue

**Output**: `is_complete`, `follow_up_queries`

### Quality Assurance

**Completeness threshold**: 80% of fields filled

**Max iterations**: 1-3 (configurable)

**Early exit**: If no new info after retry

### Benefits

✅ **Quality Improvement**: Iterative refinement
✅ **Completeness**: Fills missing fields
✅ **Flexibility**: Configurable max iterations
✅ **Cost Control**: Deduplication + iteration limits

### When to Use

✅ Use when:
- Data extraction from unstructured sources
- Quality matters more than speed
- Information may be scattered
- Schema has required fields

❌ Don't use when:
- Simple single-step tasks
- Speed is critical
- Data is already structured
- No quality iteration needed

---

## Pattern Combinations

### Recommended Combinations

**Minimal Setup** (small project):
- Prompts Centralization
- Utils Module

**Production Setup** (recommended):
- All 6 patterns

**High-Volume Setup** (1,000+ items):
- All 6 patterns + A2A migration

### Anti-Patterns

❌ **Don't**: Use multi-agent for simple tasks
❌ **Don't**: Skip rate limiting in production
❌ **Don't**: Scatter prompts across files
❌ **Don't**: Use untyped state in complex workflows

---

## Further Reading

- **Migration Strategies**: See `migration_strategies.md` for A2A transition
- **Component Catalog**: See `component_catalog.md` for detailed API docs
- **Project Insights**: See `project_docs_summary.md` for real-world case study

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
