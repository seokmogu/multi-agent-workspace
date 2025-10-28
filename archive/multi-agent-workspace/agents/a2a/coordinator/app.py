"""
Coordinator Service - FastAPI Application.

Orchestrates the multi-agent workflow:
1. Research Agent → generates queries and searches web
2. Extraction Agent → extracts structured data
3. Reflection (local) → evaluates quality and decides to continue/end

This is a simplified Phase 1 implementation. Future enhancements:
- Load balancing across multiple agent instances
- Circuit breaker pattern for fault tolerance
- Reflection as Lambda function
- Redis task queue for async processing
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import httpx
import logging
import json
import uuid

# Import reflection logic (local for Phase 1)
from src.agents.company_research.reflection import reflection_node
from src.agents.company_research.configuration import Configuration
from src.agents.company_research.state import ResearchState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Coordinator Service",
    description="Orchestrates multi-agent company research workflow",
    version="1.0.0"
)

# Configuration
RESEARCH_AGENT_URL = "http://research-agent:5001"
EXTRACTION_AGENT_URL = "http://extraction-agent:5002"

# For local development
# RESEARCH_AGENT_URL = "http://localhost:5001"
# EXTRACTION_AGENT_URL = "http://localhost:5002"


class CompanyResearchRequest(BaseModel):
    """Request for company research."""
    company_name: str = Field(description="Name of the company to research")
    extraction_schema: Dict[str, Any] = Field(description="JSON schema for data extraction")
    user_context: Optional[str] = Field(default="", description="Additional context")
    max_iterations: int = Field(default=3, description="Maximum reflection iterations")


class CompanyResearchResponse(BaseModel):
    """Response from company research."""
    company_name: str
    extracted_data: Dict[str, Any]
    research_notes: str
    reflection_summary: str
    iterations: int
    status: str


async def call_agent(agent_url: str, task_id: str, task_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call an A2A agent service.

    Args:
        agent_url: Agent service URL
        task_id: Unique task identifier
        task_input: Task input data

    Returns:
        Agent response data

    Raises:
        HTTPException: If agent call fails
    """
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            # Format A2A request
            request_data = {
                "id": task_id,
                "message": {
                    "role": "user",
                    "parts": [{"text": json.dumps(task_input)}]
                }
            }

            logger.info(f"Calling agent at {agent_url}/tasks/send")
            response = await client.post(
                f"{agent_url}/tasks/send",
                json=request_data
            )
            response.raise_for_status()

            result = response.json()

            # Check task status
            if result["status"]["state"] != "completed":
                raise HTTPException(
                    status_code=500,
                    detail=f"Agent task failed: {result['status'].get('message', 'Unknown error')}"
                )

            # Parse response
            output_text = result["messages"][0]["parts"][0]["text"]
            return json.loads(output_text)

    except httpx.RequestError as e:
        logger.error(f"Agent request error: {e}")
        raise HTTPException(status_code=503, detail=f"Agent service unavailable: {str(e)}")
    except httpx.HTTPStatusError as e:
        logger.error(f"Agent HTTP error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Agent error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error calling agent: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Agent call failed: {str(e)}")


@app.post("/research", response_model=CompanyResearchResponse)
async def research_company(request: CompanyResearchRequest):
    """
    Execute complete company research workflow.

    Orchestrates:
    1. Research Agent (web search + query generation)
    2. Extraction Agent (structured data extraction)
    3. Reflection (quality evaluation) - local for Phase 1
    4. Iterate if needed (up to max_iterations)

    Args:
        request: Company research request

    Returns:
        Complete research results with extracted data
    """
    try:
        logger.info(f"Starting research workflow for {request.company_name}")

        # Initialize state
        state: ResearchState = {
            "company_name": request.company_name,
            "extraction_schema": request.extraction_schema,
            "user_context": request.user_context,
            "research_queries": [],
            "search_results": [],
            "research_notes": "",
            "extracted_data": {},
            "reflection_summary": "",
            "follow_up_needed": False,
            "follow_up_queries": [],
            "reflection_count": 0,
            "messages": []
        }

        config = Configuration()

        # Main workflow loop
        for iteration in range(request.max_iterations):
            logger.info(f"Iteration {iteration + 1}/{request.max_iterations}")

            # Step 1: Research Agent
            research_input = {
                "company_name": request.company_name,
                "extraction_schema": request.extraction_schema,
                "user_context": request.user_context,
                "follow_up_queries": state["follow_up_queries"]
            }

            research_result = await call_agent(
                RESEARCH_AGENT_URL,
                f"research-{uuid.uuid4()}",
                research_input
            )

            state["research_queries"] = research_result["research_queries"]
            state["search_results"] = research_result["search_results"]
            state["research_notes"] = research_result["research_notes"]

            logger.info(f"Research completed: {len(research_result['research_queries'])} queries, "
                       f"{len(research_result['search_results'])} results")

            # Step 2: Extraction Agent
            extraction_input = {
                "company_name": request.company_name,
                "extraction_schema": request.extraction_schema,
                "research_notes": state["research_notes"],
                "user_context": request.user_context
            }

            extraction_result = await call_agent(
                EXTRACTION_AGENT_URL,
                f"extraction-{uuid.uuid4()}",
                extraction_input
            )

            state["extracted_data"] = extraction_result["extracted_data"]

            logger.info(f"Extraction completed: {len(state['extracted_data'])} fields")

            # Step 3: Reflection (local for Phase 1)
            state["reflection_count"] = iteration + 1
            reflection_result = await reflection_node(state, config)

            state.update(reflection_result)

            logger.info(f"Reflection completed: follow_up_needed={state['follow_up_needed']}")

            # Check if we should continue
            if not state["follow_up_needed"]:
                logger.info(f"Research completed successfully in {iteration + 1} iterations")
                break

        return CompanyResearchResponse(
            company_name=request.company_name,
            extracted_data=state["extracted_data"],
            research_notes=state["research_notes"],
            reflection_summary=state["reflection_summary"],
            iterations=state["reflection_count"],
            status="completed"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Research workflow failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Research workflow failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "coordinator",
        "agents": {
            "research": RESEARCH_AGENT_URL,
            "extraction": EXTRACTION_AGENT_URL
        }
    }


@app.get("/agents/discovery")
async def discover_agents():
    """
    Discover connected agents via their Agent Cards.

    Returns agent capabilities and endpoints.
    """
    agents_info = {}

    async with httpx.AsyncClient(timeout=10.0) as client:
        for agent_name, agent_url in [
            ("research", RESEARCH_AGENT_URL),
            ("extraction", EXTRACTION_AGENT_URL)
        ]:
            try:
                response = await client.get(f"{agent_url}/.well-known/agent.json")
                response.raise_for_status()
                agents_info[agent_name] = response.json()
            except Exception as e:
                logger.warning(f"Could not discover {agent_name} agent: {e}")
                agents_info[agent_name] = {"error": str(e)}

    return agents_info


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
