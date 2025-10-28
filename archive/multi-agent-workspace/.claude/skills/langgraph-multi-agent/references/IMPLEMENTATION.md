# LangGraph Multi-Agent Implementation Guide

Step-by-step guide for building a production-ready multi-agent system with LangGraph.

## Prerequisites

- Python 3.10+
- Basic understanding of LangChain
- OpenAI or Anthropic API key

---

## Step 1: Project Setup

### Create Directory Structure

```bash
mkdir -p company-search-agent
cd company-search-agent

mkdir -p agents utils examples
touch agents/__init__.py utils/__init__.py
```

**Recommended structure**:

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
├── multi_agent_graph.py   # MultiAgentGraph orchestrator
│
├── examples/               # Usage examples
│   ├── basic_example.py
│   └── advanced_example.py
│
├── requirements.txt        # Dependencies
├── .env                   # API keys
└── README.md
```

### Install Dependencies

Create `requirements.txt`:

```txt
# Core LangGraph
langgraph>=0.2.0
langchain>=0.3.0
langchain-core>=0.3.0

# LLM Providers (choose one or both)
langchain-openai>=0.2.0      # For OpenAI (GPT-4, etc.)
langchain-anthropic>=0.2.0   # For Anthropic (Claude)

# Utilities
python-dotenv>=1.0.0
pydantic>=2.0.0
```

Install:

```bash
pip install -r requirements.txt
```

### Configure Environment

Create `.env`:

```bash
# Choose your LLM provider
OPENAI_API_KEY=sk-...           # For GPT-4
# OR
ANTHROPIC_API_KEY=sk-ant-...    # For Claude

# Optional: LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-...
LANGCHAIN_PROJECT=multi-agent-system
```

---

## Step 2: Define State

Create `utils/state.py`:

```python
"""State definitions for multi-agent system."""

from typing import TypedDict, Annotated, List, Optional
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """Base state shared between all agents."""

    # Message history
    messages: Annotated[List[BaseMessage], add_messages]

    # Workflow control
    next_agent: str

    # Domain-specific fields (customize as needed)
    topic: str
    research_results: Optional[str]
    draft_output: Optional[str]
    review_feedback: Optional[str]
    final_output: Optional[str]

    # Quality control
    iteration_count: int
    quality_score: Optional[int]
```

**Key Points**:
- `add_messages` automatically appends new messages to the list
- Use `Optional` for fields populated later in workflow
- Add domain-specific fields as needed

---

## Step 3: Create Base Agent

Create `agents/base_agent.py`:

```python
"""Base agent class for all multi-agent implementations."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self, llm: BaseChatModel, name: str):
        """
        Initialize agent.

        Args:
            llm: Language model to use
            name: Agent name for logging
        """
        self.llm = llm
        self.name = name

    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent logic.

        Args:
            state: Current workflow state

        Returns:
            State updates
        """
        pass

    def _create_message(self, content: str) -> AIMessage:
        """Helper to create AI message."""
        return AIMessage(
            content=content,
            name=self.name
        )
```

---

## Step 4: Implement Agents

### Researcher Agent

Create `agents/researcher.py`:

```python
"""Researcher agent for data gathering."""

from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from .base_agent import BaseAgent

class ResearcherAgent(BaseAgent):
    """Agent that performs research on given topics."""

    def __init__(self, llm, name="Researcher"):
        super().__init__(llm, name)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert researcher.
Your task is to analyze the given topic and create comprehensive research notes.

Focus on:
- Key facts and data
- Important context
- Relevant insights
- Sources (if available)

Provide structured, well-organized notes."""),
            ("human", "Research topic: {topic}")
        ])

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Perform research and create notes."""
        topic = state.get("topic", "")

        # Create chain
        chain = self.prompt | self.llm

        # Execute research
        response = chain.invoke({"topic": topic})

        # Return state updates
        return {
            "research_results": response.content,
            "messages": [self._create_message(response.content)]
        }
```

### Writer Agent

Create `agents/writer.py`:

```python
"""Writer agent for content creation."""

from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from .base_agent import BaseAgent

class WriterAgent(BaseAgent):
    """Agent that creates written content from research."""

    def __init__(self, llm, name="Writer"):
        super().__init__(llm, name)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert writer.
Your task is to create clear, engaging content based on research notes.

{revision_context}

Requirements:
- Well-structured and coherent
- Based on provided research
- Professional tone
- Clear and concise"""),
            ("human", "Research notes:\n{research_results}\n\nCreate a draft.")
        ])

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Create or revise draft content."""
        research = state.get("research_results", "")
        feedback = state.get("review_feedback", "")

        # Add revision context if feedback exists
        revision_context = ""
        if feedback:
            revision_context = f"REVISION NEEDED:\n{feedback}\n\nPlease revise the draft to address this feedback."

        # Create chain
        chain = self.prompt | self.llm

        # Generate draft
        response = chain.invoke({
            "research_results": research,
            "revision_context": revision_context
        })

        return {
            "draft_output": response.content,
            "messages": [self._create_message(response.content)]
        }
```

### Reviewer Agent

Create `agents/reviewer.py`:

```python
"""Reviewer agent for quality assurance."""

from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from .base_agent import BaseAgent
import json

class ReviewerAgent(BaseAgent):
    """Agent that reviews content and provides feedback."""

    def __init__(self, llm, name="Reviewer"):
        super().__init__(llm, name)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert content reviewer.
Your task is to evaluate the draft and provide feedback.

Evaluate:
1. Quality (1-10 score)
2. Completeness
3. Clarity
4. Accuracy

Provide response in JSON format:
{{
    "quality_score": <1-10>,
    "feedback": "<specific feedback or 'Approved'>",
    "approved": <true/false>
}}"""),
            ("human", "Draft to review:\n{draft}")
        ])

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Review draft and provide feedback."""
        draft = state.get("draft_output", "")
        iteration_count = state.get("iteration_count", 0) + 1

        # Create chain
        chain = self.prompt | self.llm

        # Review draft
        response = chain.invoke({"draft": draft})

        # Parse JSON response
        try:
            review = json.loads(response.content)
            quality_score = review.get("quality_score", 0)
            feedback = review.get("feedback", "")
        except json.JSONDecodeError:
            # Fallback if LLM doesn't return valid JSON
            quality_score = 7
            feedback = response.content

        return {
            "review_feedback": feedback,
            "quality_score": quality_score,
            "iteration_count": iteration_count,
            "messages": [self._create_message(response.content)]
        }
```

---

## Step 5: Build Graph

Create `multi_agent_graph.py`:

```python
"""Multi-agent graph orchestration."""

from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent
from agents.reviewer import ReviewerAgent
from utils.state import AgentState

class MultiAgentGraph:
    """Orchestrates multi-agent workflow."""

    def __init__(
        self,
        llm_provider: str = "openai",
        model: str = "gpt-4",
        temperature: float = 0.7
    ):
        """
        Initialize multi-agent system.

        Args:
            llm_provider: 'openai' or 'anthropic'
            model: Model name (e.g., 'gpt-4', 'claude-3-5-sonnet-20241022')
            temperature: LLM temperature (0.0-1.0)
        """
        # Initialize LLM
        if llm_provider == "openai":
            self.llm = ChatOpenAI(model=model, temperature=temperature)
        elif llm_provider == "anthropic":
            self.llm = ChatAnthropic(model=model, temperature=temperature)
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")

        # Initialize agents
        self.researcher = ResearcherAgent(self.llm)
        self.writer = WriterAgent(self.llm)
        self.reviewer = ReviewerAgent(self.llm)

        # Build graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow."""

        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("writer", self._writer_node)
        workflow.add_node("reviewer", self._reviewer_node)

        # Set entry point
        workflow.set_entry_point("researcher")

        # Add edges
        workflow.add_edge("researcher", "writer")
        workflow.add_edge("writer", "reviewer")

        # Conditional edge from reviewer
        workflow.add_conditional_edges(
            "reviewer",
            self._should_continue,
            {
                "writer": "writer",  # Revise
                "end": END           # Approve
            }
        )

        return workflow.compile()

    def _researcher_node(self, state: AgentState) -> Dict[str, Any]:
        """Researcher node."""
        return self.researcher.execute(state)

    def _writer_node(self, state: AgentState) -> Dict[str, Any]:
        """Writer node."""
        return self.writer.execute(state)

    def _reviewer_node(self, state: AgentState) -> Dict[str, Any]:
        """Reviewer node."""
        result = self.reviewer.execute(state)

        # Save final output if approved
        if state.get("quality_score", 0) >= 8:
            result["final_output"] = state.get("draft_output", "")

        return result

    def _should_continue(self, state: AgentState) -> Literal["writer", "end"]:
        """Decide whether to continue or end."""

        # Check quality score
        if state.get("quality_score", 0) >= 8:
            return "end"

        # Check max iterations
        if state.get("iteration_count", 0) >= 3:
            print("⚠️  Max iterations reached, forcing completion")
            return "end"

        # Continue refining
        return "writer"

    def run(self, topic: str) -> Dict[str, Any]:
        """
        Run multi-agent workflow.

        Args:
            topic: Research topic

        Returns:
            Final state with results
        """
        initial_state = {
            "topic": topic,
            "messages": [],
            "iteration_count": 0
        }

        result = self.graph.invoke(initial_state)
        return result
```

---

## Step 6: Create Examples

Create `examples/basic_example.py`:

```python
"""Basic multi-agent example."""

import os
from dotenv import load_dotenv
from multi_agent_graph import MultiAgentGraph

# Load environment variables
load_dotenv()

def main():
    """Run basic example."""

    # Initialize multi-agent system
    agent_graph = MultiAgentGraph(
        llm_provider="openai",  # or "anthropic"
        model="gpt-4",
        temperature=0.7
    )

    # Run workflow
    print("🚀 Starting multi-agent workflow...\n")

    result = agent_graph.run(
        topic="The impact of AI agents on software development"
    )

    # Print results
    print("\n" + "="*60)
    print("📊 RESULTS")
    print("="*60)
    print(f"\nIterations: {result['iteration_count']}")
    print(f"Quality Score: {result.get('quality_score', 'N/A')}")
    print(f"\n📝 Final Output:\n{result.get('final_output', 'N/A')}")

if __name__ == "__main__":
    main()
```

---

## Step 7: Test

Run the example:

```bash
python examples/basic_example.py
```

Expected output:

```
🚀 Starting multi-agent workflow...

[Researcher] Analyzing topic...
[Writer] Creating draft...
[Reviewer] Reviewing draft...
[Writer] Revising based on feedback...
[Reviewer] Final review...

============================================================
📊 RESULTS
============================================================

Iterations: 2
Quality Score: 9

📝 Final Output:
[Your generated content here]
```

---

## Advanced Features

### 1. Add Checkpointing

```python
from langgraph.checkpoint.memory import MemorySaver

# In MultiAgentGraph.__init__
self.memory = MemorySaver()
self.graph = self._build_graph().compile(checkpointer=self.memory)

# In run() method
config = {"configurable": {"thread_id": "session-123"}}
result = self.graph.invoke(initial_state, config=config)
```

### 2. Add Streaming

```python
def run_streaming(self, topic: str):
    """Run with streaming updates."""
    initial_state = {"topic": topic, "messages": [], "iteration_count": 0}

    for state_update in self.graph.stream(initial_state):
        agent_name = list(state_update.keys())[0]
        print(f"[{agent_name}] Processing...")
```

### 3. Add Human-in-the-Loop

```python
def _human_review_node(self, state: AgentState) -> Dict[str, Any]:
    """Allow human approval."""
    draft = state.get("draft_output", "")

    print(f"\n📄 Draft:\n{draft}\n")
    approval = input("Approve? (yes/no): ").lower()

    if approval == "yes":
        return {"quality_score": 10, "final_output": draft}
    else:
        feedback = input("Provide feedback: ")
        return {"quality_score": 5, "review_feedback": feedback}
```

---

## Troubleshooting

### Issue: Infinite Loops

**Solution**: Ensure termination conditions in `_should_continue`:

```python
def _should_continue(self, state):
    # Always check iteration count!
    if state.get("iteration_count", 0) >= 5:
        return "end"
    # ... other checks
```

### Issue: Missing State Keys

**Solution**: Use `.get()` with defaults:

```python
# ❌ BAD
topic = state["topic"]  # KeyError if missing

# ✅ GOOD
topic = state.get("topic", "")
```

### Issue: LLM Rate Limits

**Solution**: Add retry logic:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def execute_with_retry(self, state):
    return self.llm.invoke(...)
```

---

## Best Practices

1. **Start Simple**: Begin with 2-3 agents, add more as needed
2. **Type Safety**: Use TypedDict for all state definitions
3. **Logging**: Add print statements or logging at each node
4. **Testing**: Test each agent independently before integration
5. **Error Handling**: Wrap LLM calls in try-except blocks
6. **Documentation**: Comment your routing logic clearly

---

**See Also**:
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design principles
- [AGENT_PATTERNS.md](./AGENT_PATTERNS.md) - Workflow patterns
- [EXAMPLES.md](./EXAMPLES.md) - More code examples

**Next Steps**: Check [EXAMPLES.md](./EXAMPLES.md) for advanced use cases!
