"""
Example using Google ADK google_search (free web search).

This example demonstrates:
- Using Google ADK google_search instead of Tavily (free vs paid)
- Cost optimization for large-scale research
- Fallback to Tavily if Google ADK not available

Requirements:
- pip install langchain-google-genai
- GOOGLE_API_KEY in .env (for Gemini models if using them)
- ANTHROPIC_API_KEY in .env (for Claude models)
"""
import os
import json
import asyncio
from dotenv import load_dotenv

from src.agents.company_research import Configuration, DEFAULT_SCHEMA, build_research_graph

# Load environment variables
load_dotenv()


async def main():
    """Run company research with Google ADK google_search."""

    # Configuration with Google ADK
    config = Configuration(
        max_search_queries=3,
        max_search_results=3,
        max_reflection_steps=1,
        llm_model="claude-3-5-sonnet-20241022",  # Can use Claude with Google search
        temperature=0.7,
        search_provider="google_adk"  # ⭐ Use free Google ADK google_search
    )

    print("=" * 80)
    print("COMPANY RESEARCH WITH GOOGLE ADK (FREE SEARCH)")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  Search provider: {config.search_provider} (FREE)")
    print(f"  Max search queries: {config.max_search_queries}")
    print(f"  Max search results: {config.max_search_results}")
    print(f"  Max reflection steps: {config.max_reflection_steps}")
    print(f"  LLM model: {config.llm_model}")

    print("\n💡 Cost Comparison:")
    print("  Tavily API: $0.005/query x 3 queries = $0.015")
    print("  Google ADK: $0.00 (FREE with Gemini 2+)")
    print("  Savings: 100% on search costs")

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
    print("\n🔍 Starting research with Google ADK...\n")

    final_state = await graph.ainvoke(initial_state)

    # Display results
    print("\n" + "=" * 80)
    print("RESEARCH COMPLETE")
    print("=" * 80)

    print("\n📊 EXTRACTED DATA:")
    print("-" * 80)
    print(json.dumps(final_state["extracted_data"], indent=2))

    print("\n\n📝 RESEARCH NOTES (PREVIEW):")
    print("-" * 80)
    notes = final_state["research_notes"]
    preview = notes[:500] + "..." if len(notes) > 500 else notes
    print(preview)

    print("\n\n📈 STATISTICS:")
    print("-" * 80)
    print(f"Search queries executed: {len(final_state['research_queries'])}")
    print(f"Search results found: {len(final_state['search_results'])}")
    print(f"Reflection iterations: {final_state['reflection_count']}")
    print(f"Fields extracted: {len(final_state['extracted_data'])}")
    print(f"Missing fields: {len(final_state['missing_fields'])}")

    if final_state['missing_fields']:
        print(f"\nMissing/incomplete fields: {', '.join(final_state['missing_fields'])}")

    print("\n💰 COST ANALYSIS:")
    print("-" * 80)
    queries = len(final_state['research_queries'])
    print(f"Search queries: {queries}")
    print(f"Tavily cost (alternative): ${queries * 0.005:.3f}")
    print(f"Google ADK cost: $0.00 (FREE)")
    print(f"Total savings: ${queries * 0.005:.3f}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    # Check for required API keys
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found in environment")
        print("Please set it in your .env file")
        exit(1)

    # Google ADK doesn't require API key for basic google_search
    # But if you want to use Gemini models, you need GOOGLE_API_KEY
    print("\n📌 NOTE: Google ADK google_search is FREE")
    print("   If using Gemini models, set GOOGLE_API_KEY in .env")
    print("   Otherwise, you can use Claude models with Google search\n")

    # Run async main
    asyncio.run(main())
