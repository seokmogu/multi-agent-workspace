# LangGraph Multi-Agent Architecture

Detailed architecture documentation for building collaborative multi-agent systems with LangGraph.

## Core Architecture Pattern

The multi-agent system follows this collaborative pattern:

```
Researcher Agent → Writer Agent → Reviewer Agent
                        ↑              ↓
                        └──────────────┘
                     (loop back if revision needed)
```

### Flow Description

1. **Researcher Agent**: Analyzes input data and extracts key insights
2. **Writer Agent**: Transforms research into structured output
3. **Reviewer Agent**: Evaluates quality and decides:
   - ✅ **Approve**: End workflow
   - 🔄 **Revise**: Loop back to Writer with feedback

## Components Overview

### 1. State Management

```python
from typing import TypedDict, Annotated, List
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """Shared state passed between agents"""
    messages: Annotated[List[BaseMessage], add_messages]
    next_agent: str
    iteration_count: int

    # Domain-specific fields
    research_results: str
    draft_output: str
    review_feedback: str
    final_output: str
```

**Key Principles**:
- Use `TypedDict` for type safety
- Include `messages` for conversation history
- Add domain-specific fields as needed
- Use `Annotated` for special reducers (e.g., `add_messages`)

### 2. Graph Structure

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)

# Add nodes (agents)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)

# Define edges (transitions)
workflow.set_entry_point("researcher")  # Start here
workflow.add_edge("researcher", "writer")  # researcher → writer
workflow.add_edge("writer", "reviewer")    # writer → reviewer

# Conditional routing (reviewer decides next step)
workflow.add_conditional_edges(
    "reviewer",
    should_continue,  # Decision function
    {
        "writer": "writer",  # Revision needed
        "end": END           # Approved
    }
)

# Compile graph
graph = workflow.compile()
```

### 3. Node Functions

Each node is a function that:
1. Receives current state
2. Performs its task
3. Returns state updates

```python
def researcher_node(state: AgentState) -> dict:
    """Research agent node"""
    # Extract input
    topic = state.get("topic", "")

    # Process (call LLM, tools, etc.)
    results = perform_research(topic)

    # Return state updates
    return {
        "research_results": results,
        "messages": [AIMessage(content=results)]
    }
```

### 4. Conditional Routing

Decision functions determine next steps:

```python
def should_continue(state: AgentState) -> str:
    """Decide whether to continue or end"""

    # Check quality score
    if state.get("quality_score", 0) >= 8:
        return "end"

    # Check iteration limit
    if state.get("iteration_count", 0) >= 3:
        return "end"

    # Continue refining
    return "writer"
```

## Advanced Architecture Patterns

### Checkpointing (State Persistence)

```python
from langgraph.checkpoint.memory import MemorySaver

# Add checkpointer for state persistence
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# Use with thread ID
config = {"configurable": {"thread_id": "session-123"}}
result = graph.invoke(initial_state, config=config)

# Resume from checkpoint
resumed = graph.invoke(None, config=config)  # Continues from last state
```

**Use Cases**:
- Long-running workflows
- Human-in-the-loop scenarios
- Debugging and replay

### Streaming Execution

```python
# Stream state updates in real-time
for state_update in graph.stream(initial_state):
    agent_name = list(state_update.keys())[0]
    agent_output = state_update[agent_name]
    print(f"[{agent_name}] {agent_output}")
```

**Use Cases**:
- Real-time progress updates
- Live monitoring dashboards
- Interactive applications

### Subgraphs (Nested Workflows)

```python
# Create subgraph for parallel processing
research_subgraph = StateGraph(ResearchState)
research_subgraph.add_node("web_search", web_search_node)
research_subgraph.add_node("db_query", db_query_node)
# ... compile subgraph ...

# Use subgraph as a node
main_workflow.add_node("research", research_subgraph.compile())
```

**Use Cases**:
- Parallel agent execution
- Modular workflow components
- Hierarchical agent systems

## State Reducers

Control how state updates are merged:

```python
from typing import Annotated
from operator import add

class AgentState(TypedDict):
    # Append new messages
    messages: Annotated[List[BaseMessage], add_messages]

    # Add numbers
    total_cost: Annotated[float, add]

    # Custom reducer
    research_notes: Annotated[List[str], custom_reducer]

def custom_reducer(existing: List[str], new: List[str]) -> List[str]:
    """Custom merge logic"""
    return existing + [note for note in new if note not in existing]
```

## Error Handling Architecture

### Node-Level Error Handling

```python
def safe_node(state: AgentState) -> dict:
    """Node with error handling"""
    try:
        result = risky_operation(state)
        return {"output": result, "error": None}
    except Exception as e:
        logger.error(f"Node failed: {e}")
        return {
            "output": None,
            "error": str(e),
            "next_agent": "fallback"
        }
```

### Graph-Level Error Handling

```python
from langgraph.errors import GraphRecursionError

try:
    result = graph.invoke(initial_state)
except GraphRecursionError:
    print("Max iterations reached")
except Exception as e:
    print(f"Graph execution failed: {e}")
```

## Performance Considerations

### State Size Management

```python
def cleanup_node(state: AgentState) -> dict:
    """Periodically clean up state"""
    messages = state.get("messages", [])

    # Keep only last 10 messages
    if len(messages) > 10:
        return {"messages": messages[-10:]}

    return {}
```

### Async Execution

```python
# Use async for I/O-bound operations
async def async_node(state: AgentState) -> dict:
    result = await async_llm_call(state["input"])
    return {"output": result}

# Compile with async support
graph = workflow.compile()
result = await graph.ainvoke(initial_state)
```

## Monitoring and Observability

### Built-in Callbacks

```python
from langchain.callbacks import StdOutCallbackHandler

# Add callbacks for monitoring
config = {
    "callbacks": [StdOutCallbackHandler()],
    "tags": ["production", "company-analysis"]
}

result = graph.invoke(initial_state, config=config)
```

### Custom Callbacks

```python
from langchain.callbacks.base import BaseCallbackHandler

class CustomCallback(BaseCallbackHandler):
    def on_chain_start(self, *args, **kwargs):
        print("Agent started")

    def on_chain_end(self, *args, **kwargs):
        print("Agent finished")
```

## Architecture Best Practices

1. **Single Responsibility**: Each agent has one clear purpose
2. **Immutable State**: Agents return updates, don't modify state directly
3. **Type Safety**: Use TypedDict for all state definitions
4. **Error Boundaries**: Handle errors at node level
5. **Idempotent Nodes**: Same input → same output
6. **Clear Routing**: Explicit conditional logic
7. **State Cleanup**: Prevent unbounded state growth
8. **Logging**: Track all agent transitions

## Common Anti-Patterns

❌ **Avoid**:
- Mutable state modifications
- Circular dependencies without limits
- Storing large data in state
- Complex routing logic
- Missing error handling

✅ **Instead**:
- Return state updates
- Add iteration counters
- Reference external storage
- Simple, explicit routing
- Comprehensive try-catch blocks

---

**See Also**:
- [AGENT_PATTERNS.md](./AGENT_PATTERNS.md) - Common workflow patterns
- [IMPLEMENTATION.md](./IMPLEMENTATION.md) - Step-by-step implementation guide
- [EXAMPLES.md](./EXAMPLES.md) - Working code examples

**Official Documentation**: https://langchain-ai.github.io/langgraph/
