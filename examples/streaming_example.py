"""
Example showing streaming execution with real-time updates.
"""
import os
import asyncio
from dotenv import load_dotenv

from src.agents.company_research import Configuration, DEFAULT_SCHEMA, build_research_graph

load_dotenv()


async def main():
    """Stream research workflow execution."""

    config = Configuration(
        max_search_queries=3,
        max_search_results=3,
        max_reflection_steps=1,
    )

    print("=" * 80)
    print("STREAMING COMPANY RESEARCH")
    print("=" * 80)

    graph = build_research_graph(config)

    company_name = "OpenAI"

    print(f"\nResearching: {company_name}")
    print("Streaming real-time updates...\n")
    print("-" * 80)

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

    # Stream execution
    async for event in graph.astream(initial_state):
        print(f"\n📍 EVENT UPDATE:")
        print("-" * 80)

        # Parse event
        if "research" in event:
            data = event["research"]
            queries = data.get("research_queries", [])
            results = data.get("search_results", [])

            print("🔍 RESEARCH PHASE")
            print(f"   Queries executed: {len(queries)}")
            if queries:
                print("   Queries:")
                for i, q in enumerate(queries, 1):
                    print(f"     {i}. {q}")
            print(f"   Results found: {len(results)}")

        elif "extract" in event:
            data = event["extract"]
            extracted = data.get("extracted_data", {})

            print("📊 EXTRACTION PHASE")
            print(f"   Fields extracted: {len(extracted)}")
            print("   Fields:")
            for field, value in extracted.items():
                if value and str(value) != "null":
                    display_value = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                    print(f"     • {field}: {display_value}")

        elif "reflect" in event:
            data = event["reflect"]
            missing = data.get("missing_fields", [])
            follow_ups = data.get("follow_up_queries", [])
            is_complete = data.get("is_complete", False)

            print("🤔 REFLECTION PHASE")
            print(f"   Status: {'COMPLETE ✓' if is_complete else 'NEEDS MORE DATA'}")
            print(f"   Missing fields: {len(missing)}")
            if missing:
                print(f"   Missing: {', '.join(missing[:5])}")
            if follow_ups:
                print("   Follow-up queries:")
                for q in follow_ups:
                    print(f"     → {q}")

        print("-" * 80)

    print("\n" + "=" * 80)
    print("STREAMING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        print("Error: Required API keys not found")
        exit(1)

    asyncio.run(main())
