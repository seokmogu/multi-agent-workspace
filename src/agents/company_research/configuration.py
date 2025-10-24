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

    llm_model: str = "claude-sonnet-4-5-20250929"  # Latest: Claude Sonnet 4.5 (Sep 2025)

    temperature: float = 0.7

    search_provider: Annotated[
        Literal["tavily", "google_adk", "hybrid", "serpapi", "bing", "duckduckgo", "brave"],
        Field(
            description="""Web search provider to use:
            - tavily: Tavily API (paid, $0.005/query, high quality, best for deep research)
            - google_adk: Google ADK google_search (free, Gemini 2+ only)
            - hybrid: Use both tavily and google_adk (tavily for main, google for follow-up)
            - serpapi: SerpAPI (paid, $50/mo for 5k searches, Google results scraping)
            - bing: Bing Search API (free tier 1k/mo, then $7 per 1k queries)
            - duckduckgo: DuckDuckGo (completely free, privacy-focused, rate limited)
            - brave: Brave Search API (free tier 2k/mo, privacy-focused)
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
