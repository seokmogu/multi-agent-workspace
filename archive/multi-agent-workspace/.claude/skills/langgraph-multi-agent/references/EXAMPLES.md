# LangGraph Multi-Agent Examples

Working code examples for common multi-agent use cases.

## Table of Contents

1. [Basic Example](#1-basic-example) - Simple research-write-review workflow
2. [Streaming Example](#2-streaming-example) - Real-time progress updates
3. [Human-in-the-Loop](#3-human-in-the-loop) - Manual approval checkpoints
4. [Conditional Routing](#4-conditional-routing) - Route by complexity
5. [Parallel Processing](#5-parallel-processing) - Multi-source research
6. [Custom State](#6-custom-state) - Domain-specific fields

---

## 1. Basic Example

Simple research → write → review workflow with automatic iteration.

```python
"""Basic multi-agent example."""

import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict, Literal

load_dotenv()

# State definition
class AgentState(TypedDict):
    topic: str
    research: str
    draft: str
    feedback: str
    quality_score: int
    iteration_count: int

# Agent nodes
def research_node(state):
    """Research the topic."""
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a researcher. Create detailed research notes."),
        ("human", "Topic: {topic}")
    ])
    chain = prompt | llm
    result = chain.invoke({"topic": state["topic"]})
    return {"research": result.content}

def write_node(state):
    """Write content based on research."""
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a writer. Create clear content from research notes."),
        ("human", "Research:\n{research}\n\nFeedback: {feedback}")
    ])
    chain = prompt | llm
    result = chain.invoke({
        "research": state.get("research", ""),
        "feedback": state.get("feedback", "Initial draft")
    })
    return {"draft": result.content}

def review_node(state):
    """Review the draft."""
    llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Rate quality 1-10 and provide feedback. Format: SCORE: X\nFEEDBACK: ..."),
        ("human", "Draft:\n{draft}")
    ])
    chain = prompt | llm
    result = chain.invoke({"draft": state["draft"]})

    # Parse response
    lines = result.content.split("\n")
    score_line = [l for l in lines if "SCORE:" in l][0]
    score = int(score_line.split(":")[1].strip())

    return {
        "quality_score": score,
        "feedback": result.content,
        "iteration_count": state.get("iteration_count", 0) + 1
    }

# Routing logic
def should_continue(state) -> Literal["write", "end"]:
    """Decide whether to continue or end."""
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
if __name__ == "__main__":
    result = graph.invoke({
        "topic": "Impact of AI on software development",
        "iteration_count": 0
    })

    print(f"✅ Completed in {result['iteration_count']} iterations")
    print(f"📊 Quality Score: {result['quality_score']}")
    print(f"\n📝 Final Draft:\n{result['draft']}")
```

---

## 2. Streaming Example

Real-time progress updates as agents work.

```python
"""Streaming multi-agent example."""

from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from typing import TypedDict
import time

class StreamState(TypedDict):
    input: str
    step1_output: str
    step2_output: str
    step3_output: str

def step1_node(state):
    """First processing step."""
    print("🔍 Step 1: Analyzing input...")
    time.sleep(1)  # Simulate work
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)
    result = llm.invoke(f"Analyze: {state['input']}")
    return {"step1_output": result.content}

def step2_node(state):
    """Second processing step."""
    print("⚙️  Step 2: Processing...")
    time.sleep(1)
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)
    result = llm.invoke(f"Process: {state['step1_output']}")
    return {"step2_output": result.content}

def step3_node(state):
    """Final step."""
    print("✨ Step 3: Finalizing...")
    time.sleep(1)
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)
    result = llm.invoke(f"Finalize: {state['step2_output']}")
    return {"step3_output": result.content}

# Build graph
workflow = StateGraph(StreamState)
workflow.add_node("step1", step1_node)
workflow.add_node("step2", step2_node)
workflow.add_node("step3", step3_node)

workflow.set_entry_point("step1")
workflow.add_edge("step1", "step2")
workflow.add_edge("step2", "step3")
workflow.add_edge("step3", END)

graph = workflow.compile()

# Run with streaming
if __name__ == "__main__":
    print("🚀 Starting streaming workflow...\n")

    for state_update in graph.stream({"input": "AI agents"}):
        agent_name = list(state_update.keys())[0]
        agent_output = state_update[agent_name]

        print(f"✅ [{agent_name}] completed")
        print(f"   Output preview: {str(agent_output)[:100]}...\n")

    print("🎉 Workflow complete!")
```

---

## 3. Human-in-the-Loop

Manual approval before proceeding to next step.

```python
"""Human-in-the-loop example."""

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal

class HILState(TypedDict):
    task: str
    draft: str
    approved: bool
    feedback: str

def create_draft_node(state):
    """Create initial draft."""
    llm = ChatOpenAI(model="gpt-4")
    result = llm.invoke(f"Create draft for: {state['task']}")
    return {"draft": result.content}

def human_review_node(state):
    """Human reviews and approves/rejects."""
    print("\n" + "="*60)
    print("📄 DRAFT FOR REVIEW")
    print("="*60)
    print(state["draft"])
    print("="*60)

    approval = input("\n✅ Approve? (yes/no): ").lower()

    if approval == "yes":
        return {"approved": True, "feedback": "Approved"}
    else:
        feedback = input("💬 Provide feedback: ")
        return {"approved": False, "feedback": feedback}

def revise_draft_node(state):
    """Revise based on feedback."""
    llm = ChatOpenAI(model="gpt-4")
    result = llm.invoke(f"Revise draft:\n{state['draft']}\n\nFeedback: {state['feedback']}")
    return {"draft": result.content}

# Routing
def should_revise(state) -> Literal["revise", "end"]:
    """Check if revision needed."""
    return "end" if state.get("approved", False) else "revise"

# Build graph
workflow = StateGraph(HILState)
workflow.add_node("create", create_draft_node)
workflow.add_node("review", human_review_node)
workflow.add_node("revise", revise_draft_node)

workflow.set_entry_point("create")
workflow.add_edge("create", "review")
workflow.add_conditional_edges("review", should_revise, {"revise": "revise", "end": END})
workflow.add_edge("revise", "review")  # Loop back to review

graph = workflow.compile()

# Run
if __name__ == "__main__":
    result = graph.invoke({"task": "Write a product announcement"})
    print(f"\n✅ Final approved draft:\n{result['draft']}")
```

---

## 4. Conditional Routing

Route to different agents based on input complexity.

```python
"""Conditional routing example."""

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal

class RoutingState(TypedDict):
    query: str
    complexity: str
    answer: str

def analyze_complexity_node(state):
    """Classify query complexity."""
    query = state["query"]
    word_count = len(query.split())

    if word_count < 10:
        complexity = "simple"
    elif word_count < 30:
        complexity = "medium"
    else:
        complexity = "complex"

    return {"complexity": complexity}

def simple_agent_node(state):
    """Handle simple queries."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
    result = llm.invoke(f"Answer briefly: {state['query']}")
    return {"answer": f"[Simple Agent] {result.content}"}

def medium_agent_node(state):
    """Handle medium queries."""
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    result = llm.invoke(f"Answer with detail: {state['query']}")
    return {"answer": f"[Medium Agent] {result.content}"}

def complex_agent_node(state):
    """Handle complex queries."""
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    # Could use tools, multiple steps, etc.
    result = llm.invoke(f"Provide comprehensive answer: {state['query']}")
    return {"answer": f"[Expert Agent] {result.content}"}

# Routing function
def route_by_complexity(state) -> Literal["simple", "medium", "complex"]:
    """Route to appropriate agent."""
    return state["complexity"]

# Build graph
workflow = StateGraph(RoutingState)
workflow.add_node("analyze", analyze_complexity_node)
workflow.add_node("simple", simple_agent_node)
workflow.add_node("medium", medium_agent_node)
workflow.add_node("complex", complex_agent_node)

workflow.set_entry_point("analyze")
workflow.add_conditional_edges(
    "analyze",
    route_by_complexity,
    {
        "simple": "simple",
        "medium": "medium",
        "complex": "complex"
    }
)
workflow.add_edge("simple", END)
workflow.add_edge("medium", END)
workflow.add_edge("complex", END)

graph = workflow.compile()

# Test with different queries
if __name__ == "__main__":
    queries = [
        "What is AI?",  # Simple
        "Explain how neural networks work.",  # Medium
        "Compare and contrast different approaches to multi-agent systems, including their trade-offs."  # Complex
    ]

    for query in queries:
        print(f"\n{'='*60}\nQuery: {query}\n{'='*60}")
        result = graph.invoke({"query": query})
        print(f"Complexity: {result['complexity']}")
        print(f"Answer: {result['answer']}\n")
```

---

## 5. Parallel Processing

Multiple agents run concurrently, results merged.

```python
"""Parallel processing example."""

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict
import asyncio

class ParallelState(TypedDict):
    topic: str
    web_research: str
    academic_research: str
    news_research: str
    combined_report: str

def web_research_node(state):
    """Simulate web research."""
    llm = ChatOpenAI(model="gpt-4")
    result = llm.invoke(f"Find web information about: {state['topic']}")
    return {"web_research": result.content}

def academic_research_node(state):
    """Simulate academic research."""
    llm = ChatOpenAI(model="gpt-4")
    result = llm.invoke(f"Find academic papers about: {state['topic']}")
    return {"academic_research": result.content}

def news_research_node(state):
    """Simulate news research."""
    llm = ChatOpenAI(model="gpt-4")
    result = llm.invoke(f"Find recent news about: {state['topic']}")
    return {"news_research": result.content}

def combine_results_node(state):
    """Merge all research results."""
    llm = ChatOpenAI(model="gpt-4")

    combined_input = f"""
    Web Research: {state.get('web_research', 'N/A')}

    Academic Research: {state.get('academic_research', 'N/A')}

    News: {state.get('news_research', 'N/A')}

    Create a comprehensive report combining all sources.
    """

    result = llm.invoke(combined_input)
    return {"combined_report": result.content}

# Build parallel graph
workflow = StateGraph(ParallelState)

# Add all nodes
workflow.add_node("web", web_research_node)
workflow.add_node("academic", academic_research_node)
workflow.add_node("news", news_research_node)
workflow.add_node("combine", combine_results_node)

# Parallel execution (all start simultaneously)
workflow.set_entry_point("web")
workflow.set_entry_point("academic")
workflow.set_entry_point("news")

# All converge to combine
workflow.add_edge("web", "combine")
workflow.add_edge("academic", "combine")
workflow.add_edge("news", "combine")
workflow.add_edge("combine", END)

graph = workflow.compile()

# Run
if __name__ == "__main__":
    print("🚀 Starting parallel research...\n")

    result = graph.invoke({"topic": "LangGraph multi-agent systems"})

    print("✅ Research complete!")
    print(f"\n📊 Combined Report:\n{result['combined_report']}")
```

---

## 6. Custom State

Domain-specific state for company analysis.

```python
"""Custom state example for company analysis."""

from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from typing import TypedDict, Optional
from pydantic import BaseModel, Field

# Pydantic model for structured output
class CompanyData(BaseModel):
    """Structured company information."""
    name: str = Field(description="Company name")
    industry: str = Field(description="Industry sector")
    funding: Optional[str] = Field(description="Funding amount", default=None)
    employees: Optional[int] = Field(description="Employee count", default=None)
    description: str = Field(description="Company description")

class CompanyState(TypedDict):
    company_name: str
    raw_research: str
    structured_data: Optional[CompanyData]
    quality_score: int

def research_company_node(state):
    """Research company information."""
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    result = llm.invoke(f"Research information about: {state['company_name']}")
    return {"raw_research": result.content}

def extract_structured_data_node(state):
    """Extract structured data from research."""
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

    # Use structured output
    llm_with_structure = llm.with_structured_output(CompanyData)

    result = llm_with_structure.invoke(
        f"Extract company data from:\n{state['raw_research']}"
    )

    return {"structured_data": result}

def validate_data_node(state):
    """Validate extracted data."""
    data = state["structured_data"]

    # Calculate completeness score
    score = 0
    if data.name:
        score += 20
    if data.industry:
        score += 20
    if data.funding:
        score += 20
    if data.employees:
        score += 20
    if data.description and len(data.description) > 50:
        score += 20

    return {"quality_score": score}

# Build graph
workflow = StateGraph(CompanyState)
workflow.add_node("research", research_company_node)
workflow.add_node("extract", extract_structured_data_node)
workflow.add_node("validate", validate_data_node)

workflow.set_entry_point("research")
workflow.add_edge("research", "extract")
workflow.add_edge("extract", "validate")
workflow.add_edge("validate", END)

graph = workflow.compile()

# Run
if __name__ == "__main__":
    result = graph.invoke({"company_name": "Anthropic"})

    print(f"✅ Company: {result['structured_data'].name}")
    print(f"📊 Quality Score: {result['quality_score']}/100")
    print(f"\n📄 Structured Data:")
    print(f"   Industry: {result['structured_data'].industry}")
    print(f"   Funding: {result['structured_data'].funding}")
    print(f"   Employees: {result['structured_data'].employees}")
    print(f"   Description: {result['structured_data'].description}")
```

---

## Running Examples

### Setup

```bash
# Install dependencies
pip install langgraph langchain-openai langchain-anthropic python-dotenv

# Set API key
export OPENAI_API_KEY=sk-...
# or
export ANTHROPIC_API_KEY=sk-ant-...
```

### Execute

```bash
# Run any example
python examples/basic_example.py
python examples/streaming_example.py
python examples/human_in_loop_example.py
# etc.
```

---

## Best Practices

1. **Error Handling**: Wrap LLM calls in try-except blocks
2. **Logging**: Add print statements for debugging
3. **Type Safety**: Use TypedDict and Pydantic models
4. **Testing**: Test each node independently first
5. **Cost Management**: Monitor LLM API usage

---

**See Also**:
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
- [AGENT_PATTERNS.md](./AGENT_PATTERNS.md) - Workflow patterns
- [IMPLEMENTATION.md](./IMPLEMENTATION.md) - Setup guide

**LangGraph Examples**: https://github.com/langchain-ai/langgraph/tree/main/examples
