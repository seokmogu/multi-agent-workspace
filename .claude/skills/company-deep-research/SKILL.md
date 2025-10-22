---
name: Company Deep Research Agent
description: Build an AI agent that performs deep web research on companies using LangGraph with a research-extraction-reflection iterative loop and Tavily web search. Use this when the user wants to automatically search the web for company information, extract structured JSON data, implement quality evaluation loops, create schema-driven data extraction systems, or build production-ready research automation. Ideal for company profiling, market research, competitive analysis, and any task requiring automated web research with structured output.
allowed-tools: Write, Edit, Read, Bash
---

# Company Deep Research Agent

This skill implements a sophisticated web research agent based on LangChain's company-researcher architecture. It automatically searches the web, extracts structured information, and iteratively improves research quality.

## 🎯 Target Companies

**This system is optimized for small to mid-sized private companies:**

| Characteristic | Details |
|----------------|---------|
| **Company Size** | Small (10-300 employees) to Mid-sized (300-1,000 employees) |
| **Listing Status** | **Private/Unlisted companies only** (public companies have better structured data sources) |
| **Industries** | B2B manufacturing, IT services, SaaS, etc. |
| **Data Sources** | Company websites, news articles, job postings, press releases |

**Search Strategy:**

*Direct Sources:*
- ✅ Company websites, blogs, case studies
- ✅ Industry news and tech media
- ✅ Job postings (reveal tech stack and org size)
- ✅ Customer testimonials and partnerships

*Indirect Sources (Critical!):*
- ✅ **Public company filings mentioning the target as supplier/partner**
  - Major customer/supplier lists in 10-K/annual reports
  - Subsidiary/affiliate disclosures
  - Related party transaction details
  - Strategic partnership announcements
- ✅ **VC portfolio pages** (for funded private companies)
- ✅ **Government procurement records** (public contracts, awards)

*Example Search Queries:*
```
"[Company Name] supplier"
"[Company Name] partner"
"[Company Name] customer"
"[Company Name] site:sec.gov OR site:dart.fss.or.kr"  (public filings)
"[Company Name] funding OR investment"
"[Company Name] awarded contract"
```

> 💡 **Why indirect sources matter:** Private companies don't file public reports, BUT public companies they do business with must disclose major suppliers/customers. This reveals transaction volumes, relationship nature, and business scope.

**All default schemas, example queries, and prompts are designed for private SME research.**

## When to Use This Skill

- Building automated company research systems
- Extracting structured data from web searches
- Creating research agents with quality control
- Implementing iterative research workflows
- Generating company reports with web-sourced data

## Architecture: Three-Phase Research Loop

```
┌─────────────────────────────────────────────────────┐
│  1. RESEARCH PHASE                                  │
│  - Generate targeted search queries                 │
│  - Execute concurrent web searches (Tavily)         │
│  - Collect structured research notes                │
└────────────────┬────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────┐
│  2. EXTRACTION PHASE                                │
│  - Consolidate research notes                       │
│  - Extract data into JSON schema                    │
│  - Format structured output                         │
└────────────────┬────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────┐
│  3. REFLECTION PHASE                                │
│  - Evaluate extraction completeness                 │
│  - Identify missing fields                          │
│  - Generate follow-up queries                       │
└────────────────┬────────────────────────────────────┘
                 │
                 ↓
          [Complete or Loop Back]
```

## Implementation Guide

### 1. Project Structure

Create this structure (matches the company-search-agent implementation):

```
company-search-agent/
├── src/
│   ├── __init__.py
│   └── agent/
│       ├── __init__.py
│       ├── configuration.py    # Configuration (Pydantic)
│       ├── state.py           # ResearchState, DEFAULT_SCHEMA
│       ├── research.py        # Research phase (Tavily)
│       ├── extraction.py      # Extraction phase (JSON)
│       ├── reflection.py      # Reflection phase (Quality)
│       └── graph.py           # build_research_graph()
│
├── examples_deep_research/     # Example scripts
│   ├── basic_research.py      # Basic usage
│   ├── custom_schema.py       # Custom schema (startup analysis)
│   └── streaming_example.py   # Streaming execution
│
├── requirements.txt            # Include tavily-python
├── .env                       # ANTHROPIC_API_KEY, TAVILY_API_KEY
└── README_DEEP_RESEARCH.md    # Detailed guide
```

**Reference Implementation**: See `company-search-agent/src/agent/` for complete working code.

**Required Dependencies**:
```
langgraph>=0.2.0
langchain>=0.3.0
langchain-anthropic>=0.2.0
langchain-community>=0.3.0
tavily-python>=0.3.0
pydantic>=2.0.0
```

### 2. Configuration

Define research parameters in `configuration.py`:

```python
from typing import Annotated
from pydantic import BaseModel, Field

class Configuration(BaseModel):
    """Agent configuration."""

    max_search_queries: Annotated[int, Field(
        description="Maximum number of search queries per company",
        ge=1, le=10
    )] = 3

    max_search_results: Annotated[int, Field(
        description="Maximum results per search query",
        ge=1, le=10
    )] = 3

    max_reflection_steps: Annotated[int, Field(
        description="Maximum reflection iterations",
        ge=0, le=5
    )] = 1

    llm_model: str = "claude-3-5-sonnet-20241022"
```

### 3. State Management

Define state with schema tracking:

```python
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class ResearchState(TypedDict):
    """Research agent state."""

    # Input
    company_name: str
    extraction_schema: Dict[str, Any]  # User-defined JSON schema
    user_context: str  # Optional additional context

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

    # Control
    is_complete: bool
    messages: Annotated[List[BaseMessage], add_messages]

# Default extraction schema (optimized for private SMEs)
DEFAULT_SCHEMA = {
    "title": "Private Company Information",
    "type": "object",
    "properties": {
        "company_name": {
            "type": "string",
            "description": "Official company name"
        },
        "founded": {
            "type": "string",
            "description": "Year founded or established"
        },
        "headquarters": {
            "type": "string",
            "description": "Headquarters location (city, country)"
        },
        "industry": {
            "type": "string",
            "description": "Primary industry or sector (e.g., B2B SaaS, Manufacturing)"
        },
        "description": {
            "type": "string",
            "description": "Brief company description and business model"
        },
        "products_services": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Main products or services offered"
        },
        "target_customers": {
            "type": "string",
            "description": "Target customer segments (B2B/B2C, industries served)"
        },
        "key_people": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "role": {"type": "string"}
                }
            },
            "description": "CEO, founders, key executives"
        },
        "employee_count": {
            "type": "string",
            "description": "Approximate number of employees (range acceptable)"
        },
        "funding_status": {
            "type": "string",
            "description": "Bootstrapped, angel-funded, VC-backed, etc. (for private companies)"
        },
        "major_clients": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Notable clients or partners (from case studies, news, OR public company filings mentioning this company as supplier)"
        },
        "public_company_relationships": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "public_company": {"type": "string"},
                    "relationship_type": {"type": "string"},
                    "details": {"type": "string"}
                }
            },
            "description": "Relationships with public companies as mentioned in their SEC/DART filings (as supplier, customer, partner, etc.)"
        },
        "technology_stack": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Technologies used (from job postings, tech blogs)"
        },
        "recent_news": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Recent company news or announcements"
        }
    },
    "required": ["company_name", "description", "industry"]
}
```

### 4. Research Phase Implementation

```python
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate

async def research_node(state: ResearchState, config: Configuration) -> Dict[str, Any]:
    """
    Generate search queries and collect research notes.
    """
    company_name = state["company_name"]
    schema = state["extraction_schema"]

    # Initialize Tavily search
    search_tool = TavilySearchResults(
        max_results=config.max_search_results,
        search_depth="advanced",
        include_raw_content=True
    )

    # Generate targeted queries based on schema (optimized for private SMEs)
    query_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research query generator for PRIVATE small-to-mid-sized companies.

        Generate {max_queries} specific search queries to find information about {company_name}.

        Target data points:
        {schema_fields}

        IMPORTANT - Search strategy for private companies:

        DIRECT sources:
        - Company websites, news articles, job postings, press releases
        - Industry reports, tech blogs, case studies
        - Recent news (use time ranges like "past year")

        INDIRECT sources (very valuable!):
        - Public company filings WHERE the target is mentioned as supplier/customer/partner
        - VC portfolio pages (if the company raised funding)
        - Government procurement records (if they have public contracts)

        Example query patterns:
        - "{company_name} technology stack"
        - "{company_name} customers OR clients"
        - "{company_name} supplier OR vendor" (find who mentions them)
        - "{company_name} site:sec.gov OR site:dart.fss.or.kr" (public filings mentioning them)

        Generate diverse queries targeting different aspects."""),
        ("human", "Company: {company_name}")
    ])

    llm = ChatAnthropic(model=config.llm_model)
    chain = query_prompt | llm

    # Extract schema fields
    fields = list(schema.get("properties", {}).keys())

    response = await chain.ainvoke({
        "company_name": company_name,
        "max_queries": config.max_search_queries,
        "schema_fields": ", ".join(fields)
    })

    # Parse queries from response
    queries = parse_queries(response.content)

    # Execute searches concurrently
    all_results = []
    for query in queries:
        results = await search_tool.ainvoke(query)
        all_results.extend(results)

    # Generate structured research notes
    notes_prompt = ChatPromptTemplate.from_messages([
        ("system", """Analyze these search results and create structured research notes
        about {company_name}.

        Organize information by these categories:
        {schema_fields}

        Search Results:
        {search_results}

        Create detailed, well-organized notes."""),
        ("human", "Create research notes.")
    ])

    notes_chain = notes_prompt | llm
    notes_response = await notes_chain.ainvoke({
        "company_name": company_name,
        "schema_fields": ", ".join(fields),
        "search_results": format_search_results(all_results)
    })

    return {
        "research_queries": queries,
        "search_results": all_results,
        "research_notes": notes_response.content
    }
```

### 5. Extraction Phase Implementation

```python
from langchain_core.output_parsers import JsonOutputParser

async def extraction_node(state: ResearchState) -> Dict[str, Any]:
    """
    Extract structured data from research notes.
    """
    schema = state["extraction_schema"]
    notes = state["research_notes"]
    company_name = state["company_name"]

    extraction_prompt = ChatPromptTemplate.from_messages([
        ("system", """Extract company information from the research notes
        according to this JSON schema:

        {schema}

        Research Notes:
        {notes}

        Return only valid JSON matching the schema.
        Use null for missing information."""),
        ("human", "Extract data for {company_name}.")
    ])

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    parser = JsonOutputParser()

    chain = extraction_prompt | llm | parser

    extracted = await chain.ainvoke({
        "schema": json.dumps(schema, indent=2),
        "notes": notes,
        "company_name": company_name
    })

    return {
        "extracted_data": extracted
    }
```

### 6. Reflection Phase Implementation

```python
async def reflection_node(state: ResearchState, config: Configuration) -> Dict[str, Any]:
    """
    Evaluate extraction quality and determine next steps.
    """
    schema = state["extraction_schema"]
    extracted = state["extracted_data"]
    reflection_count = state.get("reflection_count", 0)

    reflection_prompt = ChatPromptTemplate.from_messages([
        ("system", """Evaluate this extracted company data against the required schema.

        Schema:
        {schema}

        Extracted Data:
        {extracted}

        Evaluate:
        1. Which required fields are missing or incomplete?
        2. Which fields need more detailed information?
        3. What specific search queries would fill these gaps?

        Respond with:
        - missing_fields: list of incomplete fields
        - follow_up_queries: specific searches to run
        - is_complete: true if data is sufficient, false otherwise"""),
        ("human", "Evaluate the extraction quality.")
    ])

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    parser = JsonOutputParser()

    chain = reflection_prompt | llm | parser

    evaluation = await chain.ainvoke({
        "schema": json.dumps(schema, indent=2),
        "extracted": json.dumps(extracted, indent=2)
    })

    # Check if we should continue researching
    is_complete = (
        evaluation.get("is_complete", False) or
        reflection_count >= config.max_reflection_steps or
        len(evaluation.get("missing_fields", [])) == 0
    )

    return {
        "reflection_count": reflection_count + 1,
        "missing_fields": evaluation.get("missing_fields", []),
        "follow_up_queries": evaluation.get("follow_up_queries", []),
        "is_complete": is_complete
    }
```

### 7. Graph Assembly

```python
from langgraph.graph import StateGraph, END

def build_research_graph(config: Configuration):
    """Build the research workflow graph."""

    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node("research", lambda s: research_node(s, config))
    workflow.add_node("extract", extraction_node)
    workflow.add_node("reflect", lambda s: reflection_node(s, config))

    # Define flow
    workflow.set_entry_point("research")
    workflow.add_edge("research", "extract")
    workflow.add_edge("extract", "reflect")

    # Conditional: continue or end
    workflow.add_conditional_edges(
        "reflect",
        lambda state: "research" if not state["is_complete"] else "end",
        {
            "research": "research",
            "end": END
        }
    )

    return workflow.compile()
```

### 8. Dependencies

```
langgraph>=0.2.0
langchain>=0.3.0
langchain-anthropic>=0.2.0
langchain-community>=0.3.0
tavily-python>=0.3.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

### 9. Environment Setup

```bash
# .env
ANTHROPIC_API_KEY=your_anthropic_key
TAVILY_API_KEY=your_tavily_key

# Optional
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
```

### 10. Usage Example

```python
from src.agent.graph import build_research_graph
from src.agent.configuration import Configuration
from src.agent.state import DEFAULT_SCHEMA

# Configure agent
config = Configuration(
    max_search_queries=5,
    max_search_results=3,
    max_reflection_steps=2
)

# Build graph
graph = build_research_graph(config)

# Run research
initial_state = {
    "company_name": "Anthropic",
    "extraction_schema": DEFAULT_SCHEMA,
    "user_context": "",
    "research_queries": [],
    "search_results": [],
    "research_notes": "",
    "extracted_data": {},
    "reflection_count": 0,
    "missing_fields": [],
    "follow_up_queries": [],
    "is_complete": False,
    "messages": []
}

result = await graph.ainvoke(initial_state)

print(json.dumps(result["extracted_data"], indent=2))
```

## Advanced Features

### Custom Schema

```python
custom_schema = {
    "title": "Tech Startup Analysis",
    "type": "object",
    "properties": {
        "funding_rounds": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "round": {"type": "string"},
                    "amount": {"type": "string"},
                    "date": {"type": "string"},
                    "investors": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        "technology_stack": {
            "type": "array",
            "items": {"type": "string"}
        },
        "competitors": {
            "type": "array",
            "items": {"type": "string"}
        }
    }
}
```

### Streaming Results

```python
async for event in graph.astream(initial_state):
    if "research" in event:
        print(f"🔍 Research: {len(event['research']['search_results'])} results")
    elif "extract" in event:
        print(f"📊 Extracted: {len(event['extract']['extracted_data'])} fields")
    elif "reflect" in event:
        print(f"🤔 Reflection: {event['reflect']['is_complete']}")
```

### Error Handling

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def research_with_retry(state, config):
    return await research_node(state, config)
```

## Best Practices

1. **Schema Design**
   - Keep schemas flat (avoid deep nesting)
   - Use arrays of simple objects instead of nested structures
   - Include clear descriptions for each field
   - Mark truly required fields in schema

2. **Query Generation**
   - Generate diverse queries targeting different aspects
   - Include temporal queries ("recent news about X")
   - Use specific terminology from the industry

3. **Resource Management**
   - Set reasonable max_search_queries (3-5)
   - Limit max_reflection_steps to prevent infinite loops
   - Cache search results when possible

4. **Quality Control**
   - Validate extracted JSON against schema
   - Log missing fields for analysis
   - Track research quality metrics

5. **Cost Optimization**
   - Use cheaper models for query generation
   - Use advanced models for extraction
   - Batch API calls when possible

## Troubleshooting

**Empty Extractions**
- Check if search results contain relevant information
- Verify schema field descriptions are clear
- Try more specific search queries

**Infinite Reflection Loops**
- Set appropriate max_reflection_steps
- Check schema required fields are achievable
- Review follow-up query quality

**API Rate Limits**
- Add exponential backoff
- Reduce max_search_queries
- Implement request throttling

## References

- Company Researcher: https://github.com/langchain-ai/company-researcher
- Tavily API: https://tavily.com/
- LangGraph: https://langchain-ai.github.io/langgraph/
