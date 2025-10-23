"""
Extraction Agent A2A Service - FastAPI Application.

Wraps the company_research extraction phase as an independent HTTP service
following the Agent2Agent (A2A) protocol.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import logging
import json

# Import existing extraction logic
from src.agents.company_research.extraction import extraction_node
from src.agents.company_research.configuration import Configuration
from src.agents.company_research.state import ResearchState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Extraction Agent A2A Service",
    description="Independent extraction agent for structured data extraction from research notes",
    version="1.0.0"
)

# A2A Protocol Models (reuse from research_agent)
class MessagePart(BaseModel):
    text: str

class Message(BaseModel):
    role: str
    parts: List[MessagePart]

class TaskRequest(BaseModel):
    id: str = Field(description="Unique task identifier")
    message: Message = Field(description="Task message")

class TaskStatus(BaseModel):
    state: str = Field(description="Task state: pending, in_progress, completed, failed")
    message: Optional[str] = None

class TaskResponse(BaseModel):
    id: str
    status: TaskStatus
    messages: List[Message]


@app.get("/.well-known/agent.json")
async def get_agent_card():
    """Agent Card endpoint for A2A discovery."""
    return {
        "agentId": "extraction-agent",
        "name": "Extraction Agent",
        "description": "Extracts structured data from research notes using LLM-based parsing",
        "version": "1.0.0",
        "capabilities": [
            "structured_extraction",
            "json_schema_validation",
            "confidence_scoring"
        ],
        "skills": [
            {
                "name": "data_extraction",
                "description": "Extract structured data from research notes according to JSON schema",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "extraction_schema": {
                            "type": "object",
                            "description": "JSON schema defining extraction structure"
                        },
                        "research_notes": {
                            "type": "string",
                            "description": "Research notes to extract from"
                        },
                        "company_name": {
                            "type": "string",
                            "description": "Company name for context"
                        }
                    },
                    "required": ["extraction_schema", "research_notes"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "extracted_data": {
                            "type": "object",
                            "description": "Extracted structured data"
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
    Execute an extraction task following A2A protocol.

    Args:
        request: A2A task request with extraction parameters

    Returns:
        A2A task response with extracted data
    """
    try:
        logger.info(f"Received task {request.id}")

        # Parse input from A2A message
        input_text = request.message.parts[0].text
        task_input = json.loads(input_text)

        # Validate required fields
        if "extraction_schema" not in task_input:
            raise HTTPException(status_code=400, detail="Missing required field: extraction_schema")
        if "research_notes" not in task_input:
            raise HTTPException(status_code=400, detail="Missing required field: research_notes")

        # Create state for extraction node
        state: ResearchState = {
            "company_name": task_input.get("company_name", "Unknown"),
            "extraction_schema": task_input["extraction_schema"],
            "research_notes": task_input["research_notes"],
            "user_context": task_input.get("user_context", ""),
            "research_queries": [],
            "search_results": [],
            "extracted_data": {},
            "reflection_summary": "",
            "follow_up_needed": False,
            "follow_up_queries": [],
            "reflection_count": 0,
            "messages": []
        }

        # Create configuration
        config = Configuration()

        # Execute extraction using existing logic
        logger.info(f"Executing extraction for {state['company_name']}")
        result = await extraction_node(state, config)

        # Format response in A2A format
        output_json = json.dumps({
            "extracted_data": result["extracted_data"]
        })

        return TaskResponse(
            id=request.id,
            status=TaskStatus(
                state="completed",
                message=f"Extraction completed for {state['company_name']}"
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
    return {"status": "healthy", "service": "extraction-agent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
