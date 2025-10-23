# LangGraph Multi-Agent Patterns

Common workflow patterns for building collaborative multi-agent systems with LangGraph.

## Pattern Overview

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| **Sequential** | Linear workflows | ⭐ Simple |
| **Conditional** | Decision-based routing | ⭐⭐ Medium |
| **Iterative** | Quality refinement loops | ⭐⭐⭐ Advanced |
| **Parallel** | Concurrent processing | ⭐⭐⭐⭐ Expert |

---

## 1. Sequential Processing

**Pattern**: Linear chain of agents, each building on previous output.

```
Agent A → Agent B → Agent C → END
```

### When to Use

- Fixed workflow steps
- Each step depends on previous output
- No branching logic needed

### Example: Research → Write → Publish

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class SequentialState(TypedDict):
    topic: str
    research_notes: str
    draft_content: str
    final_output: str

# Agent nodes
def research_node(state):
    """Research the topic"""
    topic = state["topic"]
    # Perform research
    notes = f"Research findings about {topic}..."
    return {"research_notes": notes}

def write_node(state):
    """Write based on research"""
    notes = state["research_notes"]
    # Generate content
    draft = f"Article based on: {notes}..."
    return {"draft_content": draft}

def publish_node(state):
    """Finalize for publication"""
    draft = state["draft_content"]
    # Format and publish
    final = f"Published: {draft}"
    return {"final_output": final}

# Build graph
workflow = StateGraph(SequentialState)

workflow.add_node("research", research_node)
workflow.add_node("write", write_node)
workflow.add_node("publish", publish_node)

# Sequential edges
workflow.set_entry_point("research")
workflow.add_edge("research", "write")
workflow.add_edge("write", "publish")
workflow.add_edge("publish", END)

graph = workflow.compile()

# Run
result = graph.invoke({"topic": "AI Agents"})
print(result["final_output"])
```

### Key Characteristics

- ✅ Simple to understand and debug
- ✅ Predictable execution order
- ❌ No flexibility for branching
- ❌ Cannot skip or repeat steps

---

## 2. Conditional Branching

**Pattern**: Route to different agents based on conditions.

```
Agent A → [Decision] → Agent B or Agent C → END
```

### When to Use

- Different paths based on input type
- Content-based routing
- Error handling with fallback agents

### Example: Sentiment-Based Routing

```python
from typing import Literal

class ConditionalState(TypedDict):
    text: str
    sentiment: str  # positive, negative, neutral
    response: str

# Agent nodes
def analyze_sentiment_node(state):
    """Classify sentiment"""
    text = state["text"]
    # Simple sentiment analysis
    sentiment = "positive" if "good" in text.lower() else "negative"
    return {"sentiment": sentiment}

def positive_response_node(state):
    """Handle positive sentiment"""
    return {"response": "Thank you for the positive feedback!"}

def negative_response_node(state):
    """Handle negative sentiment"""
    return {"response": "We apologize for your experience. How can we help?"}

# Routing function
def route_by_sentiment(state) -> Literal["positive", "negative"]:
    """Decide which response agent to use"""
    sentiment = state.get("sentiment", "negative")
    return "positive" if sentiment == "positive" else "negative"

# Build graph
workflow = StateGraph(ConditionalState)

workflow.add_node("analyze", analyze_sentiment_node)
workflow.add_node("positive", positive_response_node)
workflow.add_node("negative", negative_response_node)

workflow.set_entry_point("analyze")

# Conditional routing from analyze
workflow.add_conditional_edges(
    "analyze",
    route_by_sentiment,
    {
        "positive": "positive",
        "negative": "negative"
    }
)

# End after response
workflow.add_edge("positive", END)
workflow.add_edge("negative", END)

graph = workflow.compile()

# Test
result1 = graph.invoke({"text": "This is good!"})
print(result1["response"])  # Positive response

result2 = graph.invoke({"text": "This is bad."})
print(result2["response"])  # Negative response
```

### Advanced: Multi-Way Routing

```python
def route_by_complexity(state) -> Literal["simple", "medium", "complex"]:
    """Route based on task complexity"""
    word_count = len(state["text"].split())

    if word_count < 50:
        return "simple"
    elif word_count < 200:
        return "medium"
    else:
        return "complex"

workflow.add_conditional_edges(
    "analyzer",
    route_by_complexity,
    {
        "simple": "basic_agent",
        "medium": "standard_agent",
        "complex": "expert_agent"
    }
)
```

### Key Characteristics

- ✅ Flexible routing based on conditions
- ✅ Can optimize resource usage (route to cheaper/faster agents)
- ❌ More complex than sequential
- ❌ Need to handle all routing cases

---

## 3. Iterative Refinement

**Pattern**: Loop back to previous agent for quality improvement.

```
Agent A → Agent B → [Review] → Agent A (loop) or END
```

### When to Use

- Quality assurance workflows
- Peer review systems
- Iterative improvement (e.g., code review, editing)

### Example: Write → Review Loop

```python
class IterativeState(TypedDict):
    topic: str
    draft: str
    review_feedback: str
    quality_score: int
    iteration_count: int
    final_output: str

def writer_node(state):
    """Write or revise draft"""
    topic = state["topic"]
    feedback = state.get("review_feedback", "")

    if feedback:
        # Revise based on feedback
        draft = f"Revised draft addressing: {feedback}..."
    else:
        # Initial draft
        draft = f"Initial draft about {topic}..."

    return {"draft": draft}

def reviewer_node(state):
    """Review draft and provide feedback"""
    draft = state["draft"]

    # Evaluate quality (simplified)
    quality_score = len(draft.split())  # Just word count as proxy
    feedback = ""

    if quality_score < 50:
        feedback = "Too short, add more details"
        quality_score = 5
    else:
        feedback = "Looks good!"
        quality_score = 10

    # Increment iteration counter
    iteration_count = state.get("iteration_count", 0) + 1

    return {
        "review_feedback": feedback,
        "quality_score": quality_score,
        "iteration_count": iteration_count
    }

# Routing function
def should_continue(state) -> Literal["writer", "end"]:
    """Decide whether to revise or finish"""

    # Check quality
    if state.get("quality_score", 0) >= 8:
        return "end"

    # Check max iterations
    if state.get("iteration_count", 0) >= 3:
        return "end"

    # Continue refining
    return "writer"

# Build graph
workflow = StateGraph(IterativeState)

workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)

workflow.set_entry_point("writer")
workflow.add_edge("writer", "reviewer")

# Conditional loop
workflow.add_conditional_edges(
    "reviewer",
    should_continue,
    {
        "writer": "writer",  # Loop back
        "end": END
    }
)

graph = workflow.compile()

# Run
result = graph.invoke({"topic": "AI Agents"})
print(f"Iterations: {result['iteration_count']}")
print(f"Final quality: {result['quality_score']}")
```

### Preventing Infinite Loops

**Always include termination conditions**:

```python
def should_continue(state) -> str:
    """Safe loop termination"""

    # 1. Quality threshold
    if state.get("quality_score", 0) >= 8:
        return "end"

    # 2. Max iterations (CRITICAL)
    if state.get("iteration_count", 0) >= 5:
        print("Max iterations reached, forcing completion")
        return "end"

    # 3. No improvement check
    if state.get("quality_score", 0) <= state.get("previous_score", 0):
        print("No improvement, stopping")
        return "end"

    return "continue"
```

### Key Characteristics

- ✅ Improves output quality through iteration
- ✅ Self-correcting workflows
- ❌ Can be slow (multiple LLM calls)
- ❌ Risk of infinite loops without safeguards

---

## 4. Parallel Processing

**Pattern**: Multiple agents run concurrently, results merged.

```
                  ┌─→ Agent B ─┐
Agent A (Splitter) ├─→ Agent C ─┤→ Agent E (Merger) → END
                  └─→ Agent D ─┘
```

### When to Use

- Independent subtasks that can run concurrently
- Speed optimization (reduce total time)
- Multiple data sources or perspectives

### Example: Multi-Source Research

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class ParallelState(TypedDict):
    topic: str
    web_results: str
    db_results: str
    api_results: str
    combined_results: str

# Parallel research nodes
def web_search_node(state):
    """Search the web"""
    topic = state["topic"]
    results = f"Web findings about {topic}..."
    return {"web_results": results}

def database_query_node(state):
    """Query internal database"""
    topic = state["topic"]
    results = f"Database records for {topic}..."
    return {"db_results": results}

def api_call_node(state):
    """Call external API"""
    topic = state["topic"]
    results = f"API data about {topic}..."
    return {"api_results": results}

def combine_results_node(state):
    """Merge all results"""
    combined = f"""
    Web: {state.get('web_results', 'N/A')}
    DB: {state.get('db_results', 'N/A')}
    API: {state.get('api_results', 'N/A')}
    """
    return {"combined_results": combined}

# Build parallel graph
workflow = StateGraph(ParallelState)

# Add all nodes
workflow.add_node("web_search", web_search_node)
workflow.add_node("db_query", database_query_node)
workflow.add_node("api_call", api_call_node)
workflow.add_node("combine", combine_results_node)

# Set multiple entry points (parallel execution)
workflow.set_entry_point("web_search")
workflow.set_entry_point("db_query")
workflow.set_entry_point("api_call")

# All paths converge to combine
workflow.add_edge("web_search", "combine")
workflow.add_edge("db_query", "combine")
workflow.add_edge("api_call", "combine")
workflow.add_edge("combine", END)

graph = workflow.compile()

# Run (all parallel nodes execute concurrently)
result = graph.invoke({"topic": "AI Research"})
print(result["combined_results"])
```

### Advanced: Subgraph Pattern

For more complex parallel orchestration:

```python
from langgraph.graph import StateGraph

# Create subgraph for parallel research
research_subgraph = StateGraph(ResearchState)
research_subgraph.add_node("web", web_node)
research_subgraph.add_node("db", db_node)
# ... configure subgraph ...
research_compiled = research_subgraph.compile()

# Use subgraph as a node in main graph
main_workflow = StateGraph(MainState)
main_workflow.add_node("research", research_compiled)  # Parallel research
main_workflow.add_node("analyze", analyze_node)
main_workflow.add_edge("research", "analyze")
```

### Key Characteristics

- ✅ Faster execution (parallel processing)
- ✅ Independent failure isolation
- ❌ More complex setup
- ❌ Need result merging logic
- ❌ Resource-intensive (multiple concurrent LLM calls)

---

## Combining Patterns

### Example: Hybrid Workflow

Combine multiple patterns for real-world complexity:

```
                  ┌─→ Quick Research ─┐
Entry → Classifier ├─→ Deep Research ──┤→ Writer → Reviewer → [Loop] → END
                  └─→ Expert Research ─┘
                   (conditional)        (parallel)  (iterative)
```

```python
# 1. Conditional routing
workflow.add_conditional_edges(
    "classifier",
    route_by_complexity,
    {
        "quick": "quick_research",
        "deep": "deep_research",
        "expert": "expert_research"
    }
)

# 2. Parallel research (all paths converge)
workflow.add_edge("quick_research", "writer")
workflow.add_edge("deep_research", "writer")
workflow.add_edge("expert_research", "writer")

# 3. Iterative refinement
workflow.add_edge("writer", "reviewer")
workflow.add_conditional_edges(
    "reviewer",
    should_continue,
    {"writer": "writer", "end": END}
)
```

---

## Pattern Selection Guide

| Requirement | Recommended Pattern |
|-------------|---------------------|
| **Fixed steps** | Sequential |
| **Different paths by input** | Conditional |
| **Quality matters** | Iterative |
| **Speed matters** | Parallel |
| **Complex workflow** | Hybrid (combine patterns) |

---

## Best Practices

1. **Start simple**: Begin with Sequential, add complexity as needed
2. **Safety first**: Always add termination conditions for loops
3. **Monitor costs**: Parallel and Iterative patterns use more LLM calls
4. **Test independently**: Validate each pattern in isolation
5. **Clear routing**: Make decision logic explicit and debuggable

---

**See Also**:
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Core LangGraph concepts
- [IMPLEMENTATION.md](./IMPLEMENTATION.md) - Step-by-step setup
- [EXAMPLES.md](./EXAMPLES.md) - Full working examples

**LangGraph Docs**: https://langchain-ai.github.io/langgraph/concepts/multi_agent/
