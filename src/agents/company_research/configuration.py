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

    llm_model: Annotated[
        str,
        Field(
            description="""LLM model to use for research, extraction, and reflection.

            For latest pricing and new models, see:
            - .claude/skills/deep-research/references/LLM_SELECTION.md
            - docs/LLM_CLOUD_PRICING_2025.md

            Common options:
            - "deepseek-chat": $0.028/$0.42 (cached), lowest cost, ~$20/month for 1k companies
            - "qwen-flash": $0.05/$0.40, OpenAI-compatible, ~$19/month
            - "gemini-2.0-flash": $0.10/$0.40, Google ecosystem, ~$22/month
            - "claude-sonnet-4-5-20250929": $3/$15 (cached), best quality, ~$40/month (default)

            See LLM_SELECTION.md for implementation examples and cost comparisons.
            """
        ),
    ] = "claude-sonnet-4-5-20250929"  # Default: Claude Sonnet 4.5 (best quality)

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
