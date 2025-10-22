---
name: Langfuse Monitoring for Research Agents
description: Integrate Langfuse observability platform to monitor LangGraph research agent quality, track LLM costs, analyze research completeness, and optimize prompts. Use this when you need to monitor multi-agent workflows, track research quality metrics, debug agent behavior, optimize LLM costs, or implement production-grade observability for private company research systems.
allowed-tools: Write, Edit, Read, Bash
---

# Langfuse Monitoring for Research Agents

This skill integrates Langfuse - an open-source LLM observability platform - into the LangGraph-based company research agent to provide comprehensive monitoring, cost tracking, and quality analytics.

## 🎯 Why Langfuse for Private SME Research?

**Perfect fit for research-heavy workflows:**

| Challenge | Langfuse Solution |
|-----------|-------------------|
| **Complex multi-step workflow** | Trace Research → Extraction → Reflection loop |
| **Iterative quality improvement** | Track completeness scores across reflections |
| **High LLM costs** | Monitor token usage, identify expensive prompts |
| **Unpredictable research quality** | Analyze correlation between query types and data completeness |
| **Debugging failures** | Inspect exact prompts/responses when extraction fails |
| **A/B testing prompts** | Compare different search query strategies |

**Key Metrics for Private Company Research:**
- Research completeness score (% of schema fields filled)
- Reflection iterations needed per company
- Search query effectiveness (which queries find useful data)
- Indirect source discovery rate (public filings mentioning target)
- Cost per company profile
- Average time per research phase

## When to Use This Skill

- Adding observability to LangGraph research workflows
- Monitoring production research agent deployments
- Optimizing research quality and costs
- Debugging complex multi-agent behaviors
- Implementing prompt versioning and management
- Analyzing research performance over time

## Architecture: Langfuse + LangGraph

```
┌─────────────────────────────────────────────────────┐
│  LangGraph Research Workflow                        │
│                                                     │
│  Research → Extraction → Reflection                │
│      ↓           ↓            ↓                     │
│  [Langfuse Callback Handler]                       │
│      ↓           ↓            ↓                     │
│  - Trace each LLM call                             │
│  - Log custom metrics (completeness_score)         │
│  - Track generation costs                          │
│  - Capture prompts & responses                     │
└────────────────┬────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────┐
│  Langfuse Cloud/Self-Hosted                        │
│                                                     │
│  📊 Dashboard                                       │
│  - Trace timeline visualization                    │
│  - Cost analytics                                  │
│  - Quality metrics over time                       │
│                                                     │
│  🔍 Debugging                                       │
│  - Inspect failed extractions                      │
│  - Compare successful vs. failed research          │
│                                                     │
│  📈 Analytics                                       │
│  - Avg completeness by industry                    │
│  - Most effective search query patterns            │
│  - Reflection ROI (cost vs. quality gain)          │
└─────────────────────────────────────────────────────┘
```

## Implementation Guide

### 1. Installation

```bash
pip install langfuse langgraph langchain-anthropic
```

Add to `requirements.txt`:
```
langfuse>=2.0.0
```

### 2. Environment Setup

Add to `.env`:

```bash
# Existing keys
ANTHROPIC_API_KEY=your_key
TAVILY_API_KEY=your_key

# Langfuse configuration
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com  # or self-hosted URL

# Optional: Enable detailed logging
LANGFUSE_DEBUG=false
```

**Getting Langfuse Keys:**
1. Sign up at https://cloud.langfuse.com (free tier available)
2. Or self-host: https://langfuse.com/docs/deployment/self-host
3. Create a new project
4. Copy API keys from project settings

### 3. Basic Integration

Create `src/observability/langfuse_config.py`:

```python
import os
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

# Initialize Langfuse client
langfuse_client = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

def create_langfuse_handler(
    session_id: str = None,
    user_id: str = None,
    metadata: dict = None
) -> CallbackHandler:
    """
    Create Langfuse callback handler for LangChain/LangGraph.

    Args:
        session_id: Unique identifier for research session
        user_id: User/researcher ID (optional)
        metadata: Additional context (company_name, schema_name, etc.)
    """
    return CallbackHandler(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        session_id=session_id,
        user_id=user_id,
        metadata=metadata or {}
    )
```

### 4. Integrate with Research Node

Modify `src/agent/research.py`:

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from ..observability.langfuse_config import create_langfuse_handler, langfuse_client
import uuid

async def research_node(state: ResearchState, config: Configuration) -> Dict[str, Any]:
    """
    Research node with Langfuse monitoring.
    """
    company_name = state["company_name"]
    schema = state["extraction_schema"]

    # Create session ID for this research
    session_id = state.get("_session_id") or str(uuid.uuid4())

    # Create Langfuse handler with metadata
    langfuse_handler = create_langfuse_handler(
        session_id=session_id,
        metadata={
            "company_name": company_name,
            "phase": "research",
            "schema_name": state.get("_schema_name", "default"),
            "reflection_count": state.get("reflection_count", 0)
        }
    )

    # Initialize LLM with Langfuse callback
    llm = ChatAnthropic(
        model=config.llm_model,
        callbacks=[langfuse_handler]
    )

    # Generate search queries
    query_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research query generator for PRIVATE small-to-mid-sized companies.

        Generate {max_queries} specific search queries to find information about {company_name}.

        Target data points:
        {schema_fields}

        IMPORTANT - Search strategy:
        - Direct: company websites, news, job postings
        - Indirect: public company filings mentioning target, VC portfolios, gov contracts
        - Example: "{company_name} site:dart.fss.or.kr" (Korean public filings)
        """),
        ("human", "Company: {company_name}")
    ])

    # Track query generation with Langfuse
    with langfuse_client.trace(
        name="generate_search_queries",
        session_id=session_id,
        metadata={"company": company_name}
    ) as trace:

        fields = list(schema.get("properties", {}).keys())

        chain = query_prompt | llm
        response = await chain.ainvoke(
            {
                "company_name": company_name,
                "max_queries": config.max_search_queries,
                "schema_fields": ", ".join(fields)
            },
            config={"callbacks": [langfuse_handler]}
        )

        queries = parse_queries(response.content)

        # Log generated queries as observation
        trace.observation(
            name="queries_generated",
            input={"fields": fields},
            output={"queries": queries},
            metadata={
                "query_count": len(queries),
                "target_count": config.max_search_queries
            }
        )

    # Execute web searches (Tavily)
    # Note: Tavily calls aren't LLM calls, but we can still track them
    all_results = []
    search_tool = TavilySearchResults(
        max_results=config.max_search_results,
        search_depth="advanced"
    )

    for query in queries:
        with langfuse_client.span(
            name="tavily_search",
            input={"query": query},
            metadata={"company": company_name}
        ) as span:
            results = await search_tool.ainvoke(query)
            all_results.extend(results)

            span.end(
                output={"result_count": len(results)},
                metadata={
                    "has_indirect_sources": any(
                        "dart.fss.or.kr" in r.get("url", "") or
                        "sec.gov" in r.get("url", "")
                        for r in results
                    )
                }
            )

    # Generate research notes
    notes_prompt = ChatPromptTemplate.from_messages([
        ("system", """Analyze search results and create structured research notes about {company_name}.

        Organize by: {schema_fields}

        Search Results:
        {search_results}
        """),
        ("human", "Create research notes.")
    ])

    with langfuse_client.generation(
        name="create_research_notes",
        input={
            "company": company_name,
            "result_count": len(all_results)
        },
        metadata={"phase": "research"}
    ) as gen:

        notes_chain = notes_prompt | llm
        notes_response = await notes_chain.ainvoke(
            {
                "company_name": company_name,
                "schema_fields": ", ".join(fields),
                "search_results": format_search_results(all_results)
            },
            config={"callbacks": [langfuse_handler]}
        )

        gen.end(
            output={"notes_length": len(notes_response.content)},
            metadata={
                "search_result_count": len(all_results),
                "queries_executed": len(queries)
            }
        )

    return {
        "research_queries": queries,
        "search_results": all_results,
        "research_notes": notes_response.content,
        "_session_id": session_id
    }
```

### 5. Integrate with Extraction Node

Modify `src/agent/extraction.py`:

```python
from ..observability.langfuse_config import create_langfuse_handler, langfuse_client

async def extraction_node(state: ResearchState, config: Configuration) -> Dict[str, Any]:
    """
    Extraction node with quality tracking.
    """
    session_id = state.get("_session_id")
    company_name = state["company_name"]
    schema = state["extraction_schema"]
    notes = state["research_notes"]

    langfuse_handler = create_langfuse_handler(
        session_id=session_id,
        metadata={
            "company_name": company_name,
            "phase": "extraction"
        }
    )

    llm = ChatAnthropic(
        model=config.llm_model,
        callbacks=[langfuse_handler]
    )

    extraction_prompt = ChatPromptTemplate.from_messages([
        ("system", """Extract company information from research notes according to this JSON schema:

        {schema}

        Research Notes:
        {notes}

        Return only valid JSON matching the schema. Use null for missing information."""),
        ("human", "Extract data for {company_name}.")
    ])

    with langfuse_client.generation(
        name="extract_company_data",
        input={
            "company": company_name,
            "notes_length": len(notes),
            "schema_fields": len(schema.get("properties", {}))
        },
        metadata={"phase": "extraction"}
    ) as gen:

        chain = extraction_prompt | llm | JsonOutputParser()

        extracted = await chain.ainvoke(
            {
                "schema": json.dumps(schema, indent=2),
                "notes": notes,
                "company_name": company_name
            },
            config={"callbacks": [langfuse_handler]}
        )

        # Calculate completeness
        total_fields = len(schema.get("properties", {}))
        filled_fields = sum(
            1 for v in extracted.values()
            if v is not None and v != "" and v != []
        )
        completeness = filled_fields / total_fields if total_fields > 0 else 0

        # Log extraction quality
        gen.end(
            output=extracted,
            metadata={
                "completeness_score": completeness,
                "filled_fields": filled_fields,
                "total_fields": total_fields,
                "extraction_success": True
            }
        )

        # Score the generation quality
        gen.score(
            name="extraction_completeness",
            value=completeness,
            comment=f"Filled {filled_fields}/{total_fields} fields"
        )

    return {
        "extracted_data": extracted,
        "_completeness_score": completeness
    }
```

### 6. Integrate with Reflection Node

Modify `src/agent/reflection.py`:

```python
from ..observability.langfuse_config import create_langfuse_handler, langfuse_client

async def reflection_node(state: ResearchState, config: Configuration) -> Dict[str, Any]:
    """
    Reflection node with quality evaluation tracking.
    """
    session_id = state.get("_session_id")
    company_name = state["company_name"]
    schema = state["extraction_schema"]
    extracted = state["extracted_data"]
    reflection_count = state.get("reflection_count", 0)

    langfuse_handler = create_langfuse_handler(
        session_id=session_id,
        metadata={
            "company_name": company_name,
            "phase": "reflection",
            "iteration": reflection_count + 1
        }
    )

    llm = ChatAnthropic(
        model=config.llm_model,
        callbacks=[langfuse_handler]
    )

    reflection_prompt = ChatPromptTemplate.from_messages([
        ("system", """Evaluate extracted company data against the schema.

        Schema:
        {schema}

        Extracted Data:
        {extracted}

        Evaluate:
        1. Missing or incomplete required fields?
        2. Fields needing more detail?
        3. Specific search queries to fill gaps (focus on indirect sources like public filings)?

        Respond with:
        - missing_fields: list
        - follow_up_queries: list
        - is_complete: boolean
        """),
        ("human", "Evaluate extraction quality.")
    ])

    with langfuse_client.generation(
        name="evaluate_extraction_quality",
        input={
            "company": company_name,
            "reflection_iteration": reflection_count + 1,
            "current_completeness": state.get("_completeness_score", 0)
        },
        metadata={"phase": "reflection"}
    ) as gen:

        chain = reflection_prompt | llm | JsonOutputParser()

        evaluation = await chain.ainvoke(
            {
                "schema": json.dumps(schema, indent=2),
                "extracted": json.dumps(extracted, indent=2)
            },
            config={"callbacks": [langfuse_handler]}
        )

        missing_count = len(evaluation.get("missing_fields", []))
        is_complete = (
            evaluation.get("is_complete", False) or
            reflection_count >= config.max_reflection_steps or
            missing_count == 0
        )

        # Log reflection decision
        gen.end(
            output=evaluation,
            metadata={
                "is_complete": is_complete,
                "missing_field_count": missing_count,
                "will_iterate": not is_complete,
                "reflection_iteration": reflection_count + 1,
                "max_iterations": config.max_reflection_steps
            }
        )

        # Score reflection quality
        if is_complete:
            gen.score(
                name="reflection_decision",
                value=1.0,
                comment="Research complete"
            )
        else:
            gen.score(
                name="reflection_decision",
                value=0.5,
                comment=f"Need iteration {reflection_count + 2}, missing {missing_count} fields"
            )

    # Log session-level metric
    if is_complete:
        langfuse_client.score(
            name="final_research_quality",
            value=state.get("_completeness_score", 0),
            trace_id=session_id,
            comment=f"Completed after {reflection_count + 1} iterations"
        )

    return {
        "reflection_count": reflection_count + 1,
        "missing_fields": evaluation.get("missing_fields", []),
        "follow_up_queries": evaluation.get("follow_up_queries", []),
        "is_complete": is_complete
    }
```

### 7. Usage Example

```python
from src.agent.graph import build_research_graph
from src.agent.configuration import Configuration
from src.agent.state import DEFAULT_SCHEMA
from src.observability.langfuse_config import langfuse_client

async def research_with_monitoring(company_name: str):
    """
    Run research with full Langfuse monitoring.
    """
    config = Configuration(
        max_search_queries=5,
        max_search_results=3,
        max_reflection_steps=2
    )

    # Build graph
    graph = build_research_graph(config)

    # Create trace for entire research session
    trace = langfuse_client.trace(
        name="company_research_session",
        metadata={
            "company_name": company_name,
            "schema": "default",
            "config": config.model_dump()
        }
    )

    # Run research
    initial_state = {
        "company_name": company_name,
        "extraction_schema": DEFAULT_SCHEMA,
        "research_queries": [],
        "search_results": [],
        "research_notes": "",
        "extracted_data": {},
        "reflection_count": 0,
        "missing_fields": [],
        "follow_up_queries": [],
        "is_complete": False,
        "_session_id": trace.id,
        "_schema_name": "default"
    }

    result = await graph.ainvoke(initial_state)

    # Finalize trace with summary
    trace.update(
        output=result["extracted_data"],
        metadata={
            "final_completeness": result.get("_completeness_score", 0),
            "total_reflections": result["reflection_count"],
            "total_queries": len(result.get("research_queries", [])),
            "is_complete": result["is_complete"]
        }
    )

    print(f"✅ Research complete for {company_name}")
    print(f"📊 View trace: https://cloud.langfuse.com/trace/{trace.id}")
    print(f"🎯 Completeness: {result.get('_completeness_score', 0):.1%}")

    return result


# Run
if __name__ == "__main__":
    import asyncio
    result = asyncio.run(research_with_monitoring("PrivateTech Solutions"))
```

### 8. Custom Metrics Dashboard

Create `src/observability/analytics.py` for custom analytics:

```python
from langfuse import Langfuse
import pandas as pd
from datetime import datetime, timedelta

class ResearchAnalytics:
    """
    Custom analytics for private company research.
    """

    def __init__(self):
        self.langfuse = Langfuse()

    def get_completeness_over_time(self, days: int = 30) -> pd.DataFrame:
        """
        Get average completeness score over time.
        """
        # Fetch traces from last N days
        traces = self.langfuse.fetch_traces(
            from_timestamp=datetime.now() - timedelta(days=days)
        )

        data = []
        for trace in traces:
            if "final_completeness" in trace.metadata:
                data.append({
                    "date": trace.timestamp,
                    "company": trace.metadata.get("company_name"),
                    "completeness": trace.metadata["final_completeness"],
                    "reflections": trace.metadata.get("total_reflections", 0)
                })

        df = pd.DataFrame(data)
        return df.groupby(df['date'].dt.date)['completeness'].mean()

    def get_reflection_roi(self) -> dict:
        """
        Calculate ROI of reflection iterations.

        Returns:
            {
                "avg_improvement_per_reflection": 0.15,
                "cost_per_reflection": 0.02,  # USD
                "roi": 7.5  # improvement / cost
            }
        """
        traces = self.langfuse.fetch_traces(limit=100)

        improvements = []
        costs = []

        for trace in traces:
            reflections = trace.metadata.get("total_reflections", 0)
            if reflections > 0:
                # Get completeness improvement
                # (This would require storing intermediate scores)
                final_score = trace.metadata.get("final_completeness", 0)

                # Estimate cost (example: $0.01 per reflection)
                cost = reflections * 0.01
                costs.append(cost)

                # Calculate improvement (simplified)
                # In reality, you'd track score after each reflection
                improvement = final_score * 0.2 * reflections  # Estimate
                improvements.append(improvement)

        if not improvements:
            return {"avg_improvement_per_reflection": 0, "cost_per_reflection": 0, "roi": 0}

        return {
            "avg_improvement_per_reflection": sum(improvements) / len(improvements),
            "cost_per_reflection": sum(costs) / len(costs),
            "roi": (sum(improvements) / sum(costs)) if sum(costs) > 0 else 0
        }

    def get_query_effectiveness(self) -> pd.DataFrame:
        """
        Analyze which search query patterns find the most useful data.
        """
        # This would analyze observations logged during research phase
        # Example: queries containing "site:dart.fss.or.kr" → high indirect source discovery

        observations = self.langfuse.fetch_observations(
            name="queries_generated",
            limit=500
        )

        query_patterns = []
        for obs in observations:
            queries = obs.output.get("queries", [])
            for q in queries:
                query_patterns.append({
                    "query": q,
                    "has_site_operator": "site:" in q,
                    "targets_indirect": any(kw in q.lower() for kw in ["filing", "supplier", "customer", "partner"])
                })

        df = pd.DataFrame(query_patterns)
        return df.groupby("targets_indirect")["has_site_operator"].value_counts()

    def get_industry_completeness(self) -> dict:
        """
        Get average completeness by industry.

        Useful for understanding which industries have better data availability.
        """
        traces = self.langfuse.fetch_traces(limit=1000)

        by_industry = {}
        for trace in traces:
            company = trace.metadata.get("company_name")
            completeness = trace.metadata.get("final_completeness")

            # You'd need to extract industry from extracted_data or metadata
            industry = trace.output.get("industry", "Unknown")

            if industry not in by_industry:
                by_industry[industry] = []

            by_industry[industry].append(completeness)

        return {
            industry: sum(scores) / len(scores)
            for industry, scores in by_industry.items()
            if len(scores) > 0
        }


# Usage
analytics = ResearchAnalytics()

print("📊 Completeness over last 30 days:")
print(analytics.get_completeness_over_time(days=30))

print("\n💰 Reflection ROI:")
print(analytics.get_reflection_roi())

print("\n🎯 Query Effectiveness:")
print(analytics.get_query_effectiveness())

print("\n🏭 Industry Completeness:")
print(analytics.get_industry_completeness())
```

### 9. Prompt Management

Use Langfuse prompt management for version control:

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Create prompt template in Langfuse UI or via API
langfuse.create_prompt(
    name="research_query_generator_v1",
    prompt="""You are a research query generator for PRIVATE small-to-mid-sized companies.

Generate {max_queries} specific search queries to find information about {company_name}.

Target data points:
{schema_fields}

IMPORTANT - Search strategy:
- Direct: company websites, news, job postings
- Indirect: public company filings mentioning target, VC portfolios, gov contracts
- Example: "{company_name} site:dart.fss.or.kr" (Korean public filings)

Generate diverse queries targeting different aspects.""",
    config={
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.7
    },
    labels=["research", "query-generation", "private-sme"]
)

# Use in code
def get_query_prompt():
    """Fetch latest prompt version from Langfuse."""
    prompt = langfuse.get_prompt("research_query_generator_v1")
    return prompt.compile(
        max_queries=5,
        company_name="{{company_name}}",
        schema_fields="{{schema_fields}}"
    )

# Benefits:
# - Version control (rollback if new prompt performs worse)
# - A/B testing (compare v1 vs v2)
# - Centralized management (update without code deployment)
```

### 10. Cost Tracking

Monitor costs per company research:

```python
# Langfuse automatically tracks token usage and costs for supported models
# View in dashboard: https://cloud.langfuse.com/project/[your-project]/analytics

# Custom cost calculation
from src.observability.langfuse_config import langfuse_client

def get_research_cost_summary(trace_id: str) -> dict:
    """
    Get detailed cost breakdown for a research session.
    """
    trace = langfuse_client.get_trace(trace_id)

    total_cost = 0
    phase_costs = {
        "research": 0,
        "extraction": 0,
        "reflection": 0
    }

    for generation in trace.observations:
        if generation.type == "generation":
            # Langfuse calculates cost automatically for Anthropic
            cost = generation.calculated_cost or 0
            total_cost += cost

            phase = generation.metadata.get("phase", "unknown")
            if phase in phase_costs:
                phase_costs[phase] += cost

    return {
        "total_cost_usd": total_cost,
        "phase_breakdown": phase_costs,
        "cost_per_phase": {
            phase: cost for phase, cost in phase_costs.items()
        },
        "company": trace.metadata.get("company_name"),
        "completeness_score": trace.metadata.get("final_completeness", 0),
        "cost_efficiency": total_cost / trace.metadata.get("final_completeness", 1) if trace.metadata.get("final_completeness") else 0
    }

# Example usage
cost_summary = get_research_cost_summary("trace-abc-123")
print(f"Total cost: ${cost_summary['total_cost_usd']:.4f}")
print(f"Research phase: ${cost_summary['phase_breakdown']['research']:.4f}")
print(f"Cost efficiency: ${cost_summary['cost_efficiency']:.4f} per completeness point")
```

## Advanced Features

### 1. Dataset Creation for Fine-Tuning

```python
# Export high-quality research sessions as training data
from langfuse import Langfuse

langfuse = Langfuse()

# Fetch successful research sessions (completeness > 0.8)
traces = langfuse.fetch_traces()

training_data = []
for trace in traces:
    if trace.metadata.get("final_completeness", 0) > 0.8:
        # Extract query generation examples
        for obs in trace.observations:
            if obs.name == "generate_search_queries":
                training_data.append({
                    "input": obs.input,
                    "output": obs.output,
                    "quality": trace.metadata["final_completeness"]
                })

# Export for fine-tuning
import json
with open("high_quality_queries.jsonl", "w") as f:
    for item in training_data:
        f.write(json.dumps(item) + "\n")
```

### 2. Error Detection

```python
# Monitor extraction failures
def detect_extraction_anomalies():
    """
    Identify research sessions with poor extraction quality.
    """
    traces = langfuse.fetch_traces(limit=100)

    anomalies = []
    for trace in traces:
        completeness = trace.metadata.get("final_completeness", 0)
        reflections = trace.metadata.get("total_reflections", 0)

        # Anomaly: many reflections but low completeness
        if reflections >= 2 and completeness < 0.5:
            anomalies.append({
                "trace_id": trace.id,
                "company": trace.metadata.get("company_name"),
                "completeness": completeness,
                "reflections": reflections,
                "issue": "High reflection count but low quality"
            })

        # Anomaly: no search results found
        total_results = trace.metadata.get("total_queries", 0)
        if total_results == 0:
            anomalies.append({
                "trace_id": trace.id,
                "company": trace.metadata.get("company_name"),
                "issue": "No search results found"
            })

    return anomalies

# Send alerts
anomalies = detect_extraction_anomalies()
if anomalies:
    print(f"⚠️ Found {len(anomalies)} anomalies:")
    for a in anomalies:
        print(f"  - {a['company']}: {a['issue']}")
```

### 3. Experimentation Framework

```python
# A/B test different query generation strategies
from langfuse import Langfuse
import random

langfuse = Langfuse()

EXPERIMENT_VARIANTS = {
    "control": "research_query_generator_v1",
    "variant_a": "research_query_generator_v2_with_indirect_focus"
}

def run_ab_test(company_name: str):
    """
    Randomly assign research to A/B test variant.
    """
    variant = random.choice(list(EXPERIMENT_VARIANTS.keys()))
    prompt_name = EXPERIMENT_VARIANTS[variant]

    # Tag trace with experiment variant
    trace = langfuse.trace(
        name="company_research_session",
        metadata={
            "company_name": company_name,
            "experiment_variant": variant,
            "prompt_version": prompt_name
        }
    )

    # Use variant-specific prompt
    prompt = langfuse.get_prompt(prompt_name)

    # ... run research with this prompt ...

    return trace.id

# Analyze results
def analyze_ab_test():
    """
    Compare completeness scores between variants.
    """
    traces = langfuse.fetch_traces(limit=500)

    results = {"control": [], "variant_a": []}

    for trace in traces:
        variant = trace.metadata.get("experiment_variant")
        completeness = trace.metadata.get("final_completeness", 0)

        if variant in results:
            results[variant].append(completeness)

    for variant, scores in results.items():
        if scores:
            avg = sum(scores) / len(scores)
            print(f"{variant}: {avg:.1%} avg completeness (n={len(scores)})")
```

## Best Practices

### 1. Metadata Tagging

Always include rich metadata for filtering and analysis:

```python
metadata = {
    "company_name": company_name,
    "company_size": "mid-sized",  # small, mid-sized
    "industry": "manufacturing",
    "is_private": True,
    "schema_version": "v1.2",
    "deployment_env": "production"  # staging, production
}
```

### 2. Sampling for Cost Control

Don't log every single request in high-volume production:

```python
import random

# Sample 10% of requests
if random.random() < 0.1:
    langfuse_handler = create_langfuse_handler(...)
else:
    langfuse_handler = None  # Skip logging
```

### 3. Session Management

Group related traces into sessions:

```python
# Use session_id to group all research for a company
session_id = f"company-{company_name}-{date.today()}"

langfuse_handler = create_langfuse_handler(
    session_id=session_id,
    metadata={"company": company_name}
)
```

### 4. Privacy Considerations

**For private company research, be mindful of data privacy:**

```python
# Option 1: Redact sensitive data before logging
def redact_sensitive_data(data: dict) -> dict:
    """Remove PII before logging to Langfuse."""
    redacted = data.copy()
    # Redact key people names, specific revenue figures, etc.
    if "key_people" in redacted:
        redacted["key_people"] = ["<REDACTED>"] * len(redacted["key_people"])
    return redacted

# Option 2: Self-host Langfuse
# Deploy Langfuse on your own infrastructure
# See: https://langfuse.com/docs/deployment/self-host

# Option 3: Use masking
langfuse_client = Langfuse(
    mask_pii=True  # Auto-redact common PII patterns
)
```

## Troubleshooting

### Issue: Traces not appearing in Langfuse

```python
# Solution 1: Flush manually
from langfuse.callback import CallbackHandler

handler = CallbackHandler(...)
# ... use handler ...
handler.flush()  # Ensure all events are sent

# Solution 2: Check environment variables
import os
print("LANGFUSE_PUBLIC_KEY:", os.getenv("LANGFUSE_PUBLIC_KEY")[:10] + "...")
print("LANGFUSE_HOST:", os.getenv("LANGFUSE_HOST"))

# Solution 3: Enable debug logging
langfuse_client = Langfuse(debug=True)
```

### Issue: High latency due to logging

```python
# Use async logging (non-blocking)
langfuse_client = Langfuse(
    flush_at=10,  # Send batch every 10 events
    flush_interval=1.0  # Or every 1 second
)
```

### Issue: Cost tracking not working

```python
# Ensure model name matches Langfuse's pricing database
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",  # Exact model name
    callbacks=[langfuse_handler]
)

# For custom models, set cost manually
langfuse_client.generation(
    name="custom_model_call",
    usage={
        "input_tokens": 1000,
        "output_tokens": 500
    },
    usage_details={
        "input_cost": 0.003,  # $0.003 per 1K input tokens
        "output_cost": 0.015   # $0.015 per 1K output tokens
    }
)
```

## Production Deployment Checklist

- [ ] Set up Langfuse project (cloud or self-hosted)
- [ ] Configure environment variables (`.env`)
- [ ] Integrate CallbackHandler in all LLM calls
- [ ] Add custom metrics (completeness_score, reflection_count)
- [ ] Create dashboards for key metrics
- [ ] Set up cost alerts (e.g., >$10/day)
- [ ] Implement error monitoring
- [ ] Configure data retention policies
- [ ] Set up team access controls
- [ ] Document trace ID format for support tickets

## Resources

- **Langfuse Docs**: https://langfuse.com/docs
- **LangChain Integration**: https://langfuse.com/docs/integrations/langchain
- **Self-Hosting Guide**: https://langfuse.com/docs/deployment/self-host
- **Pricing**: https://langfuse.com/pricing (free tier: 50K observations/month)
- **GitHub**: https://github.com/langfuse/langfuse

## Summary

Langfuse provides comprehensive observability for the private SME research agent:

| Feature | Benefit |
|---------|---------|
| **Trace visualization** | Debug complex Research→Extraction→Reflection loops |
| **Cost tracking** | Optimize LLM spending per company profile |
| **Quality metrics** | Track completeness scores and reflection ROI |
| **Prompt management** | Version control and A/B test query strategies |
| **Analytics** | Identify best practices (which queries find indirect sources) |
| **Error detection** | Alert on extraction failures or anomalies |

**Next Steps:**
1. Install Langfuse: `pip install langfuse`
2. Sign up at https://cloud.langfuse.com
3. Add callbacks to your research workflow
4. Start analyzing data quality and costs!
