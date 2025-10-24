#!/usr/bin/env python3
"""
Scaffold a new agent from templates.

This script generates a complete agent structure from templates:
- LangGraph agent: 3-phase research workflow
- A2A agent: FastAPI-based independent agent
- Hybrid: Gradual migration wrapper

Usage:
    python scaffold_agent.py --type TYPE --name NAME --output PATH

Example:
    python scaffold_agent.py --type langgraph --name document_agent --output src/agents/
    python scaffold_agent.py --type a2a --name research_agent --output src/agents/a2a/
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict


TEMPLATES_DIR = Path(__file__).parent.parent / "assets" / "templates"


LANGGRAPH_STRUCTURE = {
    "__init__.py": """# {agent_name} agent

from .graph import create_graph
from .state import {state_class}
from .configuration import Configuration

__all__ = ["create_graph", "{state_class}", "Configuration"]
""",
    "state.py": """\"\"\"
State management for {agent_name} agent.
\"\"\"
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class {state_class}(TypedDict):
    \"\"\"
    State for the {agent_name} agent workflow.

    Tracks progress through agent phases.
    \"\"\"

    # Input
    input_data: Dict[str, Any]

    # Processing state
    intermediate_results: List[Dict[str, Any]]

    # Output
    final_output: Dict[str, Any]

    # Control flow
    iteration_count: int
    is_complete: bool
    messages: Annotated[List[BaseMessage], add_messages]
""",
    "configuration.py": """\"\"\"
Configuration for the {agent_name} agent.
\"\"\"
from typing import Annotated
from pydantic import BaseModel, Field


class Configuration(BaseModel):
    \"\"\"
    Configuration for the {agent_name} agent.

    Controls resource usage and iteration limits.
    \"\"\"

    max_iterations: Annotated[
        int,
        Field(
            description="Maximum number of processing iterations",
            ge=1,
            le=10,
        ),
    ] = 3

    llm_model: str = "claude-sonnet-4-5-20250929"

    temperature: float = 0.7

    class Config:
        \"\"\"Pydantic config.\"\"\"
        frozen = True
""",
    "prompts.py": """\"\"\"
Prompt templates for the {agent_name} agent.

All prompts are centralized here for easy maintenance and version control.
\"\"\"

# Main processing prompt
MAIN_PROMPT = \"\"\"You are an AI agent specialized in {{task}}.

Input:
{{input_data}}

Your task:
1. Analyze the input
2. Process according to requirements
3. Generate structured output

Please provide your response.\"\"\"


# Reflection prompt
REFLECTION_PROMPT = \"\"\"Review the following output:

{{output}}

Evaluate:
1. Completeness
2. Accuracy
3. Quality

Is this output satisfactory? If not, what improvements are needed?\"\"\"
""",
    "graph.py": """\"\"\"
LangGraph orchestration for {agent_name} agent.
\"\"\"
from typing import Literal
from langgraph.graph import StateGraph, END
from .state import {state_class}
from .configuration import Configuration


def process_node(state: {state_class}, config: Configuration) -> {state_class}:
    \"\"\"
    Main processing node.
    \"\"\"
    # TODO: Implement processing logic
    state["intermediate_results"].append({{"step": "processed"}})
    state["iteration_count"] += 1
    return state


def reflect_node(state: {state_class}, config: Configuration) -> {state_class}:
    \"\"\"
    Reflection node to evaluate quality.
    \"\"\"
    # TODO: Implement reflection logic
    is_complete = state["iteration_count"] >= config.max_iterations
    state["is_complete"] = is_complete
    return state


def should_continue(state: {state_class}) -> Literal["continue", "end"]:
    \"\"\"
    Route based on completion status.
    \"\"\"
    if state["is_complete"]:
        return "end"
    return "continue"


def create_graph(config: Configuration = None) -> StateGraph:
    \"\"\"
    Create the agent graph.

    Args:
        config: Configuration object (optional)

    Returns:
        Compiled StateGraph
    \"\"\"
    if config is None:
        config = Configuration()

    # Create graph
    graph = StateGraph({state_class})

    # Add nodes
    graph.add_node("process", lambda state: process_node(state, config))
    graph.add_node("reflect", lambda state: reflect_node(state, config))

    # Add edges
    graph.set_entry_point("process")
    graph.add_edge("process", "reflect")
    graph.add_conditional_edges(
        "reflect",
        should_continue,
        {{"continue": "process", "end": END}}
    )

    # Compile
    return graph.compile()
"""
}


A2A_STRUCTURE = {
    "app.py": """\"\"\"
A2A (Agent2Agent) HTTP API for {agent_name} agent.

Implements the A2A protocol for agent communication.
\"\"\"
import os
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="{agent_name} Agent",
    description="A2A protocol agent",
    version="1.0.0"
)


class A2ATask(BaseModel):
    id: str
    message: Dict[str, Any]


class A2AResponse(BaseModel):
    id: str
    status: Dict[str, str]
    messages: list


@app.get("/.well-known/agent.json")
async def agent_card():
    \"\"\"
    Agent Card - A2A protocol discovery endpoint.
    \"\"\"
    return {{
        "name": "{agent_name}",
        "description": "AI agent for processing tasks",
        "version": "1.0.0",
        "capabilities": [
            "process_data",
            "analyze_input"
        ],
        "input_schema": {{
            "type": "object",
            "properties": {{
                "data": {{"type": "string"}}
            }}
        }},
        "output_schema": {{
            "type": "object",
            "properties": {{
                "result": {{"type": "string"}}
            }}
        }}
    }}


@app.post("/tasks/send")
async def handle_task(task: A2ATask) -> A2AResponse:
    \"\"\"
    Handle incoming A2A task.
    \"\"\"
    try:
        # TODO: Implement task processing
        result = {{"result": "processed"}}

        return A2AResponse(
            id=task.id,
            status={{"state": "completed"}},
            messages=[
                {{
                    "role": "assistant",
                    "parts": [{{"text": str(result)}}]
                }}
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    \"\"\"Health check endpoint.\"\"\"
    return {{"status": "healthy"}}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
""",
    "Dockerfile": """FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app.py"]
""",
    "requirements.txt": """fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
""",
    ".well-known/agent.json": """{{
  "name": "{agent_name}",
  "description": "A2A protocol agent",
  "version": "1.0.0",
  "capabilities": [
    "process_data"
  ]
}}
"""
}


def create_langgraph_agent(agent_name: str, output_dir: Path):
    """Create LangGraph agent structure."""
    agent_dir = output_dir / agent_name
    agent_dir.mkdir(parents=True, exist_ok=True)

    # Convert agent_name to class name (e.g., document_agent -> DocumentAgentState)
    class_name = "".join(word.capitalize() for word in agent_name.split("_"))
    state_class = f"{class_name}State"

    print(f"Creating LangGraph agent: {agent_name}")
    print(f"Output directory: {agent_dir}")

    # Create files
    for filename, template in LANGGRAPH_STRUCTURE.items():
        file_path = agent_dir / filename
        content = template.format(
            agent_name=agent_name,
            state_class=state_class
        )
        file_path.write_text(content)
        print(f"  Created: {filename}")

    print(f"\n✅ LangGraph agent created successfully!")
    print(f"\nNext steps:")
    print(f"1. Customize prompts in {agent_name}/prompts.py")
    print(f"2. Implement logic in {agent_name}/graph.py")
    print(f"3. Update state fields in {agent_name}/state.py")
    print(f"4. Adjust configuration in {agent_name}/configuration.py")


def create_a2a_agent(agent_name: str, output_dir: Path):
    """Create A2A agent structure."""
    agent_dir = output_dir / agent_name
    agent_dir.mkdir(parents=True, exist_ok=True)

    print(f"Creating A2A agent: {agent_name}")
    print(f"Output directory: {agent_dir}")

    # Create files
    for filename, template in A2A_STRUCTURE.items():
        # Handle nested files
        file_path = agent_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)

        content = template.format(agent_name=agent_name)
        file_path.write_text(content)
        print(f"  Created: {filename}")

    print(f"\n✅ A2A agent created successfully!")
    print(f"\nNext steps:")
    print(f"1. Update agent card in .well-known/agent.json")
    print(f"2. Implement task processing in app.py")
    print(f"3. Add dependencies to requirements.txt")
    print(f"4. Build Docker image: docker build -t {agent_name} .")
    print(f"5. Run locally: docker run -p 8000:8000 {agent_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new agent from templates"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["langgraph", "a2a"],
        required=True,
        help="Agent type: langgraph or a2a"
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Agent name (e.g., document_agent, research_agent)"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output directory for agent"
    )

    args = parser.parse_args()

    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.type == "langgraph":
        create_langgraph_agent(args.name, output_dir)
    elif args.type == "a2a":
        create_a2a_agent(args.name, output_dir)
    else:
        print(f"Error: Unknown agent type: {args.type}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
