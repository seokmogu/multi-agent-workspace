"""
FREE research example using DuckDuckGo (no API key needed).

This example demonstrates how to run deep research completely free
using DuckDuckGo as the search provider.

No API keys required - just ANTHROPIC_API_KEY for the LLM.
"""
import os
import json
import asyncio
from dotenv import load_dotenv

from src.agents.company_research import Configuration, DEFAULT_SCHEMA, build_research_graph

load_dotenv()


async def main():
    """Run free company research with DuckDuckGo."""

    # Configuration using free DuckDuckGo search
    config = Configuration(
        max_search_queries=3,
        max_search_results=3,
        max_reflection_steps=1,
        llm_model="claude-sonnet-4-5-20250929",  # Latest Claude Sonnet 4.5
        temperature=0.7,
        search_provider="duckduckgo"  # FREE! No API key needed
    )

    print("=" * 80)
    print("FREE COMPANY RESEARCH - DuckDuckGo")
    print("=" * 80)
    print("\nUsing DuckDuckGo (completely free, no API key needed)")
    print(f"Configuration:")
    print(f"  Max search queries: {config.max_search_queries}")
    print(f"  Max search results: {config.max_search_results}")
    print(f"  Search provider: {config.search_provider} (FREE)")

    # Build graph
    print("\nBuilding research graph...")
    graph = build_research_graph(config)

    # Company to research
    company_name = "Anthropic"

    print(f"\nResearching: {company_name}")
    print("-" * 80)

    # Initial state
    initial_state = {
        "company_name": company_name,
        "extraction_schema": DEFAULT_SCHEMA,
        "user_context": "",
        "research_queries": [],
        "search_results": [],
        "research_notes": "",
        "extracted_data": {},
        "reflection_count": 0,
        "missing_fields": [],
        "follow_up_queries": [],
        "is_complete": False,
        "messages": []
    }

    # Run research
    print("\n🔍 Starting FREE research workflow...\n")

    final_state = await graph.ainvoke(initial_state)

    # Display results
    print("\n" + "=" * 80)
    print("RESEARCH COMPLETE (USING FREE DUCKDUCKGO)")
    print("=" * 80)

    print("\n📊 EXTRACTED DATA:")
    print("-" * 80)
    print(json.dumps(final_state["extracted_data"], indent=2))

    print("\n\n📈 STATISTICS:")
    print("-" * 80)
    print(f"Search queries executed: {len(final_state['research_queries'])}")
    print(f"Search results found: {len(final_state['search_results'])}")
    print(f"Cost: $0 for search (DuckDuckGo is free!)")
    print(f"Only paid for LLM usage: ~$0.01-0.05 per research")

    print("\n" + "=" * 80)
    print("\n💡 TIP: DuckDuckGo is completely free and privacy-focused!")
    print("   Perfect for development, testing, or low-budget research.")
    print("   For production/higher quality, consider Tavily or SerpAPI.")
    print("=" * 80)


if __name__ == "__main__":
    # Only ANTHROPIC_API_KEY needed - no search API key!
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found in environment")
        print("Please set it in your .env file")
        exit(1)

    print("\n✓ No search API key needed - using free DuckDuckGo!\n")

    # Run async main
    asyncio.run(main())
