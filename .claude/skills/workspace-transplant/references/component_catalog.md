# Component Catalog

Complete reference for all reusable components in the workspace.

## Table of Contents

1. [Utils Module](#utils-module)
2. [LLM Module](#llm-module)
3. [Prompts Module](#prompts-module)
4. [State Module](#state-module)
5. [Configuration Module](#configuration-module)
6. [Graph Module](#graph-module)

---

## Utils Module

**File**: `src/common/utils.py`

**Dependencies**: None (pure Python)

### Functions

#### 1. `deduplicate_sources(search_response)`

Remove duplicate URLs from search results.

**Parameters**:
- `search_response` (Union[dict, List[dict]]): Search results from API

**Returns**: `List[dict]` - Deduplicated results

**Example**:
```python
from common.utils import deduplicate_sources

results = [
    {'url': 'https://example.com', 'title': 'A'},
    {'url': 'https://example.com', 'title': 'B'},  # duplicate
    {'url': 'https://other.com', 'title': 'C'}
]

unique = deduplicate_sources(results)
# → [{'url': 'https://example.com', ...}, {'url': 'https://other.com', ...}]
```

---

#### 2. `format_sources(sources_list, include_raw_content=True, max_tokens_per_source=1000)`

Format search results for LLM with token limits.

**Parameters**:
- `sources_list` (List[Dict]): Deduplicated search results
- `include_raw_content` (bool): Include full content (default: True)
- `max_tokens_per_source` (int): Token limit per source (default: 1000)

**Returns**: `str` - Formatted text

**Example**:
```python
formatted = format_sources(
    sources,
    max_tokens_per_source=500  # Limit to 500 tokens
)
```

**Token Estimation**: Uses 4 chars/token approximation.

---

#### 3. `format_all_notes(completed_notes)`

Consolidate multiple research notes into single string.

**Parameters**:
- `completed_notes` (List[str]): List of note strings

**Returns**: `str` - Formatted consolidated notes

**Example**:
```python
notes = [
    "Research iteration 1 findings...",
    "Research iteration 2 findings..."
]
formatted = format_all_notes(notes)
```

---

#### 4. `calculate_completeness(extracted, schema)`

Calculate extraction completeness score.

**Parameters**:
- `extracted` (Dict): Extracted data
- `schema` (Dict): JSON schema

**Returns**: `Tuple[List[str], float]`
- `missing_fields`: List of missing field names
- `completeness_score`: Float 0.0-1.0

**Example**:
```python
schema = {
    "properties": {"name": {}, "year": {}, "website": {}},
    "required": ["name"]
}
extracted = {"name": "Acme", "year": None, "website": "https://acme.com"}

missing, score = calculate_completeness(extracted, schema)
# missing = ["year"]
# score = 0.67 (2/3 fields filled)
```

**Empty Detection**: Checks for `None`, `""`, `"null"`, `"N/A"`, `[]`, `{}`

---

#### 5. `truncate_text(text, max_length=2000, suffix="... [truncated]")`

Safely truncate text to max length.

**Parameters**:
- `text` (str): Text to truncate
- `max_length` (int): Maximum length (default: 2000)
- `suffix` (str): Suffix when truncated (default: "... [truncated]")

**Returns**: `str` - Truncated text

**Example**:
```python
long_text = "A" * 3000
truncated = truncate_text(long_text, max_length=100)
# len(truncated) ≤ 100 + len(suffix)
```

---

#### 6. `extract_field_descriptions(schema)`

Extract field descriptions from JSON schema.

**Parameters**:
- `schema` (Dict): JSON schema

**Returns**: `Dict[str, str]` - Field name → description mapping

**Example**:
```python
schema = {
    "properties": {
        "name": {"type": "string", "description": "Company name"},
        "year": {"type": "integer", "description": "Founding year"}
    }
}
descriptions = extract_field_descriptions(schema)
# {'name': 'Company name', 'year': 'Founding year'}
```

---

### Compatibility Aliases

For backward compatibility:

```python
merge_research_results = format_all_notes
extract_unique_urls = deduplicate_sources
create_search_summary = format_sources
validate_extracted_data = calculate_completeness
calculate_confidence_score = calculate_completeness
```

---

## LLM Module

**File**: `src/common/llm.py`

**Dependencies**: `langchain-anthropic`, `langchain-core`

### Global Rate Limiter

```python
_rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.8,  # ~50 req/min (Tier 1)
    check_every_n_seconds=0.1,
    max_bucket_size=10
)
```

### Functions

#### 1. `get_llm(config, temperature=None)`

Get configured LLM with rate limiting.

**Parameters**:
- `config` (Configuration): Configuration object
- `temperature` (float, optional): Override temperature

**Returns**: `ChatAnthropic` - Configured LLM instance

**Example**:
```python
from common.llm import get_llm

llm = get_llm(config)
llm = get_llm(config, temperature=0.3)  # Override
```

---

#### 2. `get_llm_for_research(config)`

LLM optimized for research (temperature=0.7).

**Use**: Creative query generation, note-taking.

**Example**:
```python
llm = get_llm_for_research(config)
response = llm.invoke("Generate search queries...")
```

---

#### 3. `get_llm_for_extraction(config)`

LLM optimized for extraction (temperature=0.3).

**Use**: Precise JSON extraction, structured data.

**Example**:
```python
llm = get_llm_for_extraction(config)
response = llm.invoke("Extract to JSON schema...")
```

---

#### 4. `get_llm_for_reflection(config)`

LLM optimized for reflection (temperature=0.5).

**Use**: Quality evaluation, completeness analysis.

**Example**:
```python
llm = get_llm_for_reflection(config)
response = llm.invoke("Evaluate completeness...")
```

---

### Temperature Guidelines

| Task | Temperature | Reason |
|------|-------------|--------|
| Research | 0.7 | Creative query generation |
| Extraction | 0.3 | Precise JSON output |
| Reflection | 0.5 | Balanced evaluation |

---

## Prompts Module

**File**: `src/agents/company_research/prompts.py`

**Dependencies**: None

### Templates

#### 1. `QUERY_WRITER_PROMPT`

Generate search queries for company research.

**Variables**:
- `{company_name}`: Target company
- `{max_search_queries}`: Max number of queries
- `{schema}`: JSON schema for target data
- `{user_context}`: Additional user context

**Output**: JSON array of query strings

---

#### 2. `INFO_PROMPT`

Take structured notes from web content.

**Variables**:
- `{company_name}`: Target company
- `{schema}`: JSON schema
- `{content}`: Scraped web content
- `{user_context}`: Additional context

**Output**: Structured research notes (plain text)

---

#### 3. `EXTRACTION_PROMPT`

Extract structured data from research notes.

**Variables**:
- `{schema}`: JSON schema
- `{notes}`: Research notes

**Output**: Valid JSON matching schema

---

#### 4. `REFLECTION_PROMPT`

Evaluate extraction completeness.

**Variables**:
- `{schema}`: JSON schema
- `{extracted_info}`: Extracted data
- `{missing_fields}`: List of missing fields
- `{notes}`: Previous research notes

**Output**: JSON with analysis, follow_up_queries, is_complete

---

## State Module

**File**: `src/agents/company_research/state.py`

**Dependencies**: `langgraph`

### ResearchState (TypedDict)

Complete state definition for research workflow.

```python
class ResearchState(TypedDict):
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

### DEFAULT_SCHEMA

Default extraction schema for company information:

```python
DEFAULT_SCHEMA = {
    "type": "object",
    "properties": {
        "company_name": {...},
        "founded": {...},
        "headquarters": {...},
        "industry": {...},
        "description": {...},
        "products": {"type": "array", ...},
        "key_people": {"type": "array", ...},
        "revenue": {...},
        "employee_count": {...},
        "website": {...}
    },
    "required": ["company_name", "description"]
}
```

---

## Configuration Module

**File**: `src/agents/company_research/configuration.py`

**Dependencies**: `pydantic`

### Configuration (BaseModel)

Type-safe configuration with validation.

```python
class Configuration(BaseModel):
    max_search_queries: int = 3  # 1-10
    max_search_results: int = 3  # 1-10
    max_reflection_steps: int = 1  # 0-5
    llm_model: str = "claude-sonnet-4-5-20250929"
    temperature: float = 0.7
    search_provider: Literal["tavily", "google_adk", ...] = "tavily"

    class Config:
        frozen = True  # Immutable
```

**Validation**: Uses Pydantic `Field` with `ge`/`le` constraints.

**Usage**:
```python
config = Configuration(max_search_queries=5)
config = Configuration()  # Use defaults
```

---

## Graph Module

**File**: `src/agents/company_research/graph.py`

**Dependencies**: `langgraph`

### create_graph(config)

Create compiled LangGraph workflow.

**Parameters**:
- `config` (Configuration, optional): Configuration object

**Returns**: Compiled `StateGraph`

**Architecture**:
```
START → research → extract → reflect → [continue/complete]
                    ↑                      ↓
                    └──────────────────────┘
```

**Usage**:
```python
from agents.company_research.graph import create_graph

graph = create_graph(config)
result = graph.invoke({
    "company_name": "Acme Corp",
    "extraction_schema": DEFAULT_SCHEMA,
    "user_context": ""
})
```

---

## Integration Examples

### Example 1: Use Utils in Custom Agent

```python
from common.utils import deduplicate_sources, format_sources

def my_research_node(state):
    # Get search results
    results = search_api.query(state["query"])

    # Deduplicate
    unique = deduplicate_sources(results)

    # Format for LLM
    formatted = format_sources(unique, max_tokens_per_source=500)

    # Send to LLM
    response = llm.invoke(formatted)

    return state
```

### Example 2: Custom Prompts

```python
# my_prompts.py
CUSTOM_PROMPT = """You are analyzing: {target}

Schema:
{schema}

Generate queries."""

# Usage
prompt = CUSTOM_PROMPT.format(
    target="Acme Corp",
    schema=str(schema)
)
```

### Example 3: Custom Configuration

```python
from pydantic import BaseModel, Field

class MyConfig(BaseModel):
    max_retries: int = Field(ge=1, le=5, default=3)
    timeout: int = Field(ge=10, le=300, default=60)

    class Config:
        frozen = True
```

---

## Testing

### Unit Test Examples

```python
def test_deduplicate_sources():
    results = [
        {'url': 'http://a.com', 'title': 'A'},
        {'url': 'http://a.com', 'title': 'B'},  # duplicate
        {'url': 'http://b.com', 'title': 'C'}
    ]
    unique = deduplicate_sources(results)
    assert len(unique) == 2
    assert unique[0]['url'] == 'http://a.com'
    assert unique[1]['url'] == 'http://b.com'

def test_calculate_completeness():
    schema = {
        "properties": {"a": {}, "b": {}, "c": {}},
        "required": ["a"]
    }
    extracted = {"a": "value", "b": None, "c": "value"}

    missing, score = calculate_completeness(extracted, schema)

    assert "b" in missing
    assert score == 2/3  # 2 out of 3 filled

def test_rate_limiter():
    # Rate limiter prevents bursts
    start = time.time()
    for i in range(10):
        llm.invoke("test")  # Should throttle
    duration = time.time() - start

    assert duration >= 12  # 10 requests at 0.8 req/sec = 12.5 sec
```

---

## Performance Tips

1. **Deduplication**: Always deduplicate before formatting (saves API costs)
2. **Token Limits**: Use `max_tokens_per_source` to prevent overflow
3. **Rate Limiting**: Adjust `requests_per_second` based on your API tier
4. **Caching**: Cache search results in Redis (90% hit rate possible)
5. **Completeness**: Set threshold at 0.8 (80% complete) for good balance

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
