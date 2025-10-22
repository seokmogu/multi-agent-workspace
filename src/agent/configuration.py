"""
Configuration for the company research agent.
"""
from typing import Annotated, Literal
from pydantic import BaseModel, Field


class Configuration(BaseModel):
    """
    Configuration for the research agent.

    Controls resource usage and iteration limits.
    """

    max_search_queries: Annotated[
        int,
        Field(
            description="Maximum number of search queries to generate per company",
            ge=1,
            le=10,
        ),
    ] = 3

    max_search_results: Annotated[
        int,
        Field(
            description="Maximum number of results to retrieve per search query",
            ge=1,
            le=10,
        ),
    ] = 3

    max_reflection_steps: Annotated[
        int,
        Field(
            description="Maximum number of reflection/improvement iterations",
            ge=0,
            le=5,
        ),
    ] = 1

    llm_model: str = "claude-3-5-sonnet-20241022"

    temperature: float = 0.7

    search_provider: Annotated[
        Literal["tavily", "google_adk", "hybrid"],
        Field(
            description="""Web search provider to use:
            - tavily: Tavily API (paid, $0.005/query, high quality)
            - google_adk: Google ADK google_search (free, Gemini 2+ only)
            - hybrid: Use both (tavily for main, google_adk for follow-up)
            """
        ),
    ] = "tavily"

    use_gemini_for_google_search: Annotated[
        bool,
        Field(
            description="Use Gemini 2.0 Flash when google_adk is selected (required for free google_search)"
        ),
    ] = True

    class Config:
        """Pydantic config."""
        frozen = True
