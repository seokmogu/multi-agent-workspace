"""
Example using hybrid search strategy (Tavily + Google ADK).

This example demonstrates:
- Cost optimization: Tavily for quality, Google ADK for volume
- First half queries use Tavily (high quality)
- Second half queries use Google ADK (free)
- Best of both worlds: quality + cost savings

Cost Analysis:
- All Tavily: 6 queries x $0.005 = $0.030
- Hybrid: 3 Tavily + 3 Google = $0.015 (50% savings)
- All Google ADK: $0.00 (but may have quality trade-offs)
"""
import os
import json
import asyncio
from dotenv import load_dotenv

from src.agents.company_research import Configuration, DEFAULT_SCHEMA, build_research_graph

# Load environment variables
load_dotenv()


async def main():
    """Run company research with hybrid search strategy."""

    # Configuration with hybrid search
    config = Configuration(
        max_search_queries=6,  # More queries to show hybrid split
        max_search_results=3,
        max_reflection_steps=1,
        llm_model="claude-3-5-sonnet-20241022",
        temperature=0.7,
        search_provider="hybrid"  # ⭐ Use hybrid (Tavily + Google ADK)
    )

    print("=" * 80)
    print("COMPANY RESEARCH WITH HYBRID SEARCH STRATEGY")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  Search provider: {config.search_provider} (HYBRID)")
    print(f"  Max search queries: {config.max_search_queries}")
    print(f"  Strategy: First half Tavily, second half Google ADK")
    print(f"  Max search results: {config.max_search_results}")
    print(f"  Max reflection steps: {config.max_reflection_steps}")
    print(f"  LLM model: {config.llm_model}")

    print("\n💡 Cost Comparison:")
    queries = config.max_search_queries
    tavily_half = queries // 2
    google_half = queries - tavily_half

    print(f"  All Tavily: ${queries * 0.005:.3f} (6 queries)")
    print(f"  Hybrid: ${tavily_half * 0.005:.3f} ({tavily_half} Tavily) + $0.00 ({google_half} Google)")
    print(f"  All Google ADK: $0.00 (but may have quality trade-offs)")
    print(f"  Hybrid Savings: 50% cost reduction vs all-Tavily")

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
    print("\n🔍 Starting hybrid search workflow...\n")
    print("   Strategy: High-value queries → Tavily (quality)")
    print("            Follow-up queries → Google ADK (free)\n")

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

    print("\n💰 COST ANALYSIS (HYBRID STRATEGY):")
    print("-" * 80)
    total_queries = len(final_state['research_queries'])
    estimated_tavily = total_queries // 2
    estimated_google = total_queries - estimated_tavily

    print(f"Total queries: {total_queries}")
    print(f"  ├─ Tavily (high quality): ~{estimated_tavily} queries")
    print(f"  └─ Google ADK (free): ~{estimated_google} queries")
    print(f"\nEstimated costs:")
    print(f"  Tavily portion: ${estimated_tavily * 0.005:.3f}")
    print(f"  Google ADK portion: $0.00")
    print(f"  Total hybrid cost: ${estimated_tavily * 0.005:.3f}")
    print(f"  vs All-Tavily cost: ${total_queries * 0.005:.3f}")
    print(f"  Savings: ${(total_queries - estimated_tavily) * 0.005:.3f} (~50%)")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    # Check for required API keys
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found in environment")
        print("Please set it in your .env file")
        exit(1)

    if not os.getenv("TAVILY_API_KEY"):
        print("Warning: TAVILY_API_KEY not found in environment")
        print("Hybrid mode requires Tavily for first half of queries")
        print("Get your key at: https://tavily.com/")
        exit(1)

    print("\n📌 NOTE: Hybrid mode uses:")
    print("   - Tavily API for critical queries (requires TAVILY_API_KEY)")
    print("   - Google ADK for follow-up queries (FREE)")
    print("   - Optimal balance of quality and cost\n")

    # Run async main
    asyncio.run(main())
