---
name: LangGraph Multi-Agent System
description: Create a collaborative multi-agent system using LangGraph with researcher, writer, and reviewer agents working sequentially with conditional routing. Use this skill when the user wants to build multi-agent workflows, implement agent collaboration patterns (research-write-review), create systems where agents pass work to each other, or learn LangGraph basics with a practical example. Perfect for document generation, report writing, and quality-controlled content creation workflows.
allowed-tools: Write, Edit, Read, Bash
---

# LangGraph Multi-Agent System

Build production-ready multi-agent systems using LangGraph where specialized agents collaborate to complete complex tasks.

## When to Use This Skill

- Building systems with multiple AI agents working together
- Implementing research → write → review workflows
- Creating collaborative agent architectures
- Setting up agent orchestration with LangGraph

## 🎯 Target Use Case

Multi-agent systems for structured workflows where:
- Sequential analysis → writing → review is needed
- Quality control through iterative refinement is important
- Conditional routing based on quality metrics is required

> 💡 For **automated web research** of private companies, see the `company-deep-research` skill instead.

## Quick Start

### 1. Install Dependencies

```bash
pip install langgraph langchain-openai langchain-anthropic python-dotenv
```

### 2. Set API Key

```bash
export OPENAI_API_KEY=sk-...
# or
export ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Basic Example

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal

# Define state
class AgentState(TypedDict):
    topic: str
    research: str
    draft: str
    quality_score: int
    iteration_count: int

# Create agents
def research_node(state):
    llm = ChatOpenAI(model="gpt-4")
    result = llm.invoke(f"Research: {state['topic']}")
    return {"research": result.content}

def write_node(state):
    llm = ChatOpenAI(model="gpt-4")
    result = llm.invoke(f"Write based on: {state['research']}")
    return {"draft": result.content}

def review_node(state):
    llm = ChatOpenAI(model="gpt-4")
    # Review and score quality...
    return {
        "quality_score": 8,
        "iteration_count": state.get("iteration_count", 0) + 1
    }

# Routing logic
def should_continue(state) -> Literal["write", "end"]:
    if state.get("quality_score", 0) >= 8:
        return "end"
    if state.get("iteration_count", 0) >= 3:
        return "end"
    return "write"

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("research", research_node)
workflow.add_node("write", write_node)
workflow.add_node("review", review_node)

workflow.set_entry_point("research")
workflow.add_edge("research", "write")
workflow.add_edge("write", "review")
workflow.add_conditional_edges("review", should_continue, {"write": "write", "end": END})

graph = workflow.compile()

# Run
result = graph.invoke({"topic": "AI Agents", "iteration_count": 0})
print(result["draft"])
```

## Core Architecture

```
Researcher Agent → Writer Agent → Reviewer Agent
                        ↑              ↓
                        └──────────────┘
                     (loop back if revision needed)
```

**Key Components**:
- **State**: TypedDict defining shared data
- **Nodes**: Agent functions that process state
- **Edges**: Transitions between agents
- **Routing**: Conditional logic for branching/looping

## Common Patterns

1. **Sequential**: A → B → C → END
2. **Conditional**: A → [Decision] → B or C → END
3. **Iterative**: A → B → [Review] → A (loop) or END
4. **Parallel**: A → [B, C, D] → Merge → END

See [AGENT_PATTERNS.md](./references/AGENT_PATTERNS.md) for detailed examples.

## Advanced Features

- **Checkpointing**: Save/resume workflow state
- **Streaming**: Real-time progress updates
- **Human-in-the-Loop**: Manual approval checkpoints
- **Parallel Processing**: Concurrent agent execution

See [ARCHITECTURE.md](./references/ARCHITECTURE.md) for implementation details.

## Best Practices

1. ✅ **Single Responsibility**: Each agent has one clear purpose
2. ✅ **Type Safety**: Use TypedDict for all state definitions
3. ✅ **Termination Conditions**: Always check iteration limits in loops
4. ✅ **Error Handling**: Wrap LLM calls in try-except blocks
5. ✅ **Clear Routing**: Make conditional logic explicit and testable

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Infinite loops** | Add max_iterations counter in state |
| **Missing state keys** | Use `.get()` with defaults |
| **LLM rate limits** | Implement retry with exponential backoff |
| **Memory issues** | Clear old messages periodically |

## Reference Documentation

Comprehensive guides in `references/` directory:

- **[ARCHITECTURE.md](./references/ARCHITECTURE.md)** - System design, state management, graph structure
- **[AGENT_PATTERNS.md](./references/AGENT_PATTERNS.md)** - Sequential, conditional, iterative, parallel patterns
- **[IMPLEMENTATION.md](./references/IMPLEMENTATION.md)** - Step-by-step setup guide
- **[EXAMPLES.md](./references/EXAMPLES.md)** - 6 working code examples

## Official Resources

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Multi-agent Examples**: https://github.com/langchain-ai/langgraph/tree/main/examples/multi_agent
- **Tutorials**: https://langchain-ai.github.io/langgraph/tutorials/

---

**Next Steps**:
1. Read [IMPLEMENTATION.md](./references/IMPLEMENTATION.md) for detailed setup
2. Try examples in [EXAMPLES.md](./references/EXAMPLES.md)
3. Learn patterns in [AGENT_PATTERNS.md](./references/AGENT_PATTERNS.md)
