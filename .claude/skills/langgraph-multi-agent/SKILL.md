---
name: LangGraph Multi-Agent System
description: Create a collaborative multi-agent system using LangGraph with researcher, writer, and reviewer agents working sequentially with conditional routing. Use this skill when the user wants to build multi-agent workflows, implement agent collaboration patterns (research-write-review), create systems where agents pass work to each other, or learn LangGraph basics with a practical example. Perfect for document generation, report writing, and quality-controlled content creation workflows.
allowed-tools: Write, Edit, Read, Bash
---

# LangGraph Multi-Agent System

This skill helps you create a production-ready multi-agent system using LangGraph, where multiple specialized agents collaborate to complete complex tasks.

## When to Use This Skill

- Building systems with multiple AI agents working together
- Implementing research → write → review workflows
- Creating collaborative agent architectures
- Setting up agent orchestration with LangGraph

## 🎯 Target Use Case

This multi-agent system is designed for analyzing **small to mid-sized private companies** where:
- Company data comes from provided sources (not web search)
- Sequential analysis → writing → review workflow is needed
- Quality control through peer review is important

> 💡 For **automated web research** of private companies, see the `Company Deep Research Agent` skill instead.

## Architecture Overview

The multi-agent system follows this pattern:

```
Researcher Agent → Writer Agent → Reviewer Agent
                        ↑              ↓
                        └──────────────┘
                     (loop back if revision needed)
```

## Implementation Steps

### 1. Project Structure

Create the following directory structure (this matches the company-search-agent implementation):

```
company-search-agent/
├── agents/                 # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py      # BaseAgent abstract class
│   ├── researcher.py      # ResearcherAgent
│   ├── writer.py          # WriterAgent
│   └── reviewer.py        # ReviewerAgent
│
├── utils/                  # Utilities
│   ├── __init__.py
│   └── state.py           # AgentState, CompanySearchState
│
├── multi_agent_graph.py   # MultiAgentGraph class
│
├── examples/               # Usage examples
│   ├── basic_example.py
│   └── advanced_example.py  # With Human-in-the-loop
│
├── requirements.txt        # Dependencies
└── .env                   # API keys
```

**Reference Implementation**: See `company-search-agent/` folder for complete working code.

### 2. Core Components

#### Base Agent Class

Create an abstract base class that all agents inherit from:

```python
from abc import ABC, abstractmethod
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage

class BaseAgent(ABC):
    def __init__(self, llm: BaseChatModel, name: str):
        self.llm = llm
        self.name = name

    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass
```

#### State Management

Define typed state using TypedDict:

```python
from typing import TypedDict, Annotated, List
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    next_agent: str
    # Add domain-specific fields
```

#### Graph Building

Use StateGraph to orchestrate agents:

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)

# Define edges
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")

# Conditional routing
workflow.add_conditional_edges(
    "reviewer",
    should_continue,
    {"writer": "writer", "end": END}
)

graph = workflow.compile()
```

### 3. Agent Implementation Pattern

Each agent should:

1. **Receive state** with previous agent outputs
2. **Execute its task** using LLM and tools
3. **Update state** with results
4. **Specify next agent** in the workflow

Example:

```python
class ResearcherAgent(BaseAgent):
    def execute(self, state):
        # Get input from state
        topic = state.get("topic")

        # Perform research
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a researcher..."),
            ("human", "{topic}")
        ])

        chain = prompt | self.llm
        response = chain.invoke({"topic": topic})

        # Update state
        return {
            "research_results": response.content,
            "next_agent": "writer"
        }
```

### 4. Advanced Features

#### Checkpointing

Add state persistence:

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# Use with thread ID
config = {"configurable": {"thread_id": "session-1"}}
graph.invoke(initial_state, config=config)
```

#### Human-in-the-Loop

Add human review checkpoints:

```python
def human_review_node(state):
    print(state["current_output"])
    approval = input("Approve? (yes/no): ")

    if approval == "yes":
        return {"next_agent": "next_step"}
    else:
        return {"next_agent": "previous_step"}
```

#### Streaming

Stream execution for real-time updates:

```python
for state_update in graph.stream(initial_state):
    print(f"Agent update: {state_update}")
```

### 5. Dependencies

Add to requirements.txt:

```
langgraph>=0.2.0
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-anthropic>=0.2.0
python-dotenv>=1.0.0
```

### 6. Environment Setup

Create .env file:

```bash
OPENAI_API_KEY=your_key
# or
ANTHROPIC_API_KEY=your_key
```

## Best Practices

1. **Single Responsibility**: Each agent should have one clear purpose
2. **Typed State**: Use TypedDict for type safety
3. **Clear Routing**: Make conditional edges explicit and predictable
4. **Error Handling**: Add try-catch blocks in agent execute methods
5. **Logging**: Log agent transitions and decisions
6. **Testing**: Test each agent independently before integration

## Common Patterns

### Sequential Processing

```
Agent A → Agent B → Agent C → END
```

### Conditional Branching

```
Agent A → [Decision] → Agent B or Agent C → END
```

### Iterative Refinement

```
Agent A → Agent B → [Review] → Agent A (loop) or END
```

### Parallel Processing

Use subgraphs for parallel agent execution.

## Example Usage

```python
from multi_agent_graph import MultiAgentGraph

# Initialize
agent_graph = MultiAgentGraph(
    llm_provider="openai",
    model="gpt-4",
    temperature=0.7
)

# Run workflow
result = agent_graph.run(
    task="Analyze this company...",
    data=input_data
)

print(result["final_output"])
```

## Troubleshooting

- **Infinite loops**: Add max_iterations counter in state
- **Missing state keys**: Validate state schema at each node
- **LLM errors**: Implement retry logic with exponential backoff
- **Memory issues**: Clear old messages from state periodically

## References

- LangGraph Docs: https://langchain-ai.github.io/langgraph/
- Multi-agent Examples: https://github.com/langchain-ai/langgraph/tree/main/examples/multi_agent
