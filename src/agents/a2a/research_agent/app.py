"""
Research Agent A2A Service - FastAPI Application.

Wraps the company_research research phase as an independent HTTP service
following the Agent2Agent (A2A) protocol.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import asyncio
import logging

# Import existing research logic
from src.agents.company_research.research import research_node
from src.agents.company_research.configuration import Configuration
from src.agents.company_research.state import ResearchState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Research Agent A2A Service",
    description="Independent research agent for company information gathering",
    version="1.0.0"
)

# A2A Protocol Models
class MessagePart(BaseModel):
    """Part of an A2A message."""
    text: str

class Message(BaseModel):
    """A2A message format."""
    role: str
    parts: List[MessagePart]

class TaskRequest(BaseModel):
    """A2A task request format."""
    id: str = Field(description="Unique task identifier")
    message: Message = Field(description="Task message")

class TaskStatus(BaseModel):
    """Task execution status."""
    state: str = Field(description="Task state: pending, in_progress, completed, failed")
    message: Optional[str] = None

class TaskResponse(BaseModel):
    """A2A task response format."""
    id: str
    status: TaskStatus
    messages: List[Message]


@app.get("/.well-known/agent.json")
async def get_agent_card():
    """
    Agent Card endpoint for A2A discovery.

    Returns agent capabilities, skills, and I/O schema.
    """
    return {
        "agentId": "research-agent",
        "name": "Research Agent",
        "description": "Generates targeted search queries and gathers web information for company research",
        "version": "1.0.0",
        "capabilities": [
            "query_generation",
            "web_search",
            "result_deduplication",
            "research_note_creation"
        ],
        "skills": [
            {
                "name": "company_research",
                "description": "Research company information using multiple search providers",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "company_name": {
                            "type": "string",
                            "description": "Name of the company to research"
                        },
                        "extraction_schema": {
                            "type": "object",
                            "description": "JSON schema defining what information to extract"
                        },
                        "user_context": {
                            "type": "string",
                            "description": "Additional context about what to research"
                        },
                        "follow_up_queries": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific follow-up queries from reflection phase"
                        }
                    },
                    "required": ["company_name", "extraction_schema"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "research_queries": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Generated search queries"
                        },
                        "search_results": {
                            "type": "array",
                            "description": "Deduplicated search results"
                        },
                        "research_notes": {
                            "type": "string",
                            "description": "Structured research notes"
                        }
                    }
                }
            }
        ],
        "endpoints": {
            "task": "/tasks/send",
            "discovery": "/.well-known/agent.json"
        }
    }


@app.post("/tasks/send", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    """
    Execute a research task following A2A protocol.

    Args:
        request: A2A task request with company research parameters

    Returns:
        A2A task response with research results
    """
    try:
        logger.info(f"Received task {request.id}")

        # Parse input from A2A message
        input_text = request.message.parts[0].text
        import json
        task_input = json.loads(input_text)

        # Validate required fields
        if "company_name" not in task_input:
            raise HTTPException(status_code=400, detail="Missing required field: company_name")
        if "extraction_schema" not in task_input:
            raise HTTPException(status_code=400, detail="Missing required field: extraction_schema")

        # Create state for research node
        state: ResearchState = {
            "company_name": task_input["company_name"],
            "extraction_schema": task_input["extraction_schema"],
            "user_context": task_input.get("user_context", ""),
            "follow_up_queries": task_input.get("follow_up_queries", []),
            "research_queries": [],
            "search_results": [],
            "research_notes": "",
            "extracted_data": {},
            "reflection_summary": "",
            "follow_up_needed": False,
            "reflection_count": 0,
            "messages": []
        }

        # Create configuration
        config = Configuration()

        # Execute research using existing logic
        logger.info(f"Executing research for {task_input['company_name']}")
        result = await research_node(state, config)

        # Format response in A2A format
        output_json = json.dumps({
            "research_queries": result["research_queries"],
            "search_results": result["search_results"][:10],  # Limit for response size
            "research_notes": result["research_notes"]
        })

        return TaskResponse(
            id=request.id,
            status=TaskStatus(
                state="completed",
                message=f"Research completed for {task_input['company_name']}"
            ),
            messages=[
                Message(
                    role="assistant",
                    parts=[MessagePart(text=output_json)]
                )
            ]
        )

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON input: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON input: {str(e)}")
    except Exception as e:
        logger.error(f"Task execution failed: {e}", exc_info=True)
        return TaskResponse(
            id=request.id,
            status=TaskStatus(
                state="failed",
                message=str(e)
            ),
            messages=[
                Message(
                    role="assistant",
                    parts=[MessagePart(text=f"Error: {str(e)}")]
                )
            ]
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "research-agent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
