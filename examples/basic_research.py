"""
Basic example of the company deep research agent.
"""
import os
import json
import asyncio
from dotenv import load_dotenv

from src.agents.company_research import Configuration, DEFAULT_SCHEMA, build_research_graph

# Load environment variables
load_dotenv()


async def main():
    """Run basic company research example."""

    # Configuration
    config = Configuration(
        max_search_queries=3,
        max_search_results=3,
        max_reflection_steps=1,
        llm_model="claude-3-5-sonnet-20241022",
        temperature=0.7
    )

    print("=" * 80)
    print("COMPANY DEEP RESEARCH AGENT")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  Max search queries: {config.max_search_queries}")
    print(f"  Max search results: {config.max_search_results}")
    print(f"  Max reflection steps: {config.max_reflection_steps}")
    print(f"  LLM model: {config.llm_model}")

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
    print("\n🔍 Starting research workflow...\n")

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

    print("\n" + "=" * 80)


if __name__ == "__main__":
    # Check for required API keys
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found in environment")
        print("Please set it in your .env file")
        exit(1)

    if not os.getenv("TAVILY_API_KEY"):
        print("Error: TAVILY_API_KEY not found in environment")
        print("Please set it in your .env file")
        print("Get your key at: https://tavily.com/")
        exit(1)

    # Run async main
    asyncio.run(main())
