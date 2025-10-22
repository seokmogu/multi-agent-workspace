"""
Example using a custom extraction schema for tech startups.
"""
import os
import json
import asyncio
from dotenv import load_dotenv

from src.agent import Configuration, build_research_graph

load_dotenv()


# Custom schema for tech startup analysis
TECH_STARTUP_SCHEMA = {
    "title": "Tech Startup Analysis",
    "description": "Detailed analysis of a technology startup",
    "type": "object",
    "properties": {
        "company_name": {
            "type": "string",
            "description": "Official company name"
        },
        "tagline": {
            "type": "string",
            "description": "Company tagline or one-line description"
        },
        "founded": {
            "type": "string",
            "description": "Year founded"
        },
        "founders": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Names of company founders"
        },
        "headquarters": {
            "type": "string",
            "description": "HQ location"
        },
        "business_model": {
            "type": "string",
            "description": "Business model (B2B, B2C, SaaS, etc.)"
        },
        "target_market": {
            "type": "string",
            "description": "Target market or customer segment"
        },
        "funding_rounds": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "round": {"type": "string"},
                    "amount": {"type": "string"},
                    "date": {"type": "string"},
                    "lead_investor": {"type": "string"}
                }
            },
            "description": "Funding rounds and investors"
        },
        "total_funding": {
            "type": "string",
            "description": "Total funding raised"
        },
        "valuation": {
            "type": "string",
            "description": "Latest valuation (if available)"
        },
        "technology_stack": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Key technologies used"
        },
        "competitors": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Main competitors"
        },
        "unique_value_proposition": {
            "type": "string",
            "description": "What makes this company unique"
        },
        "recent_news": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Recent significant news or announcements"
        }
    },
    "required": ["company_name", "business_model", "target_market"]
}


async def main():
    """Research a tech startup with custom schema."""

    config = Configuration(
        max_search_queries=5,  # More queries for detailed research
        max_search_results=3,
        max_reflection_steps=2,  # More reflection iterations
    )

    print("=" * 80)
    print("TECH STARTUP DEEP RESEARCH")
    print("=" * 80)

    graph = build_research_graph(config)

    # Research a tech startup
    company_name = "Anthropic"
    user_context = "Focus on AI safety, research breakthroughs, and funding details"

    print(f"\nResearching: {company_name}")
    print(f"Context: {user_context}")
    print("-" * 80)

    initial_state = {
        "company_name": company_name,
        "extraction_schema": TECH_STARTUP_SCHEMA,
        "user_context": user_context,
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

    print("\n🔍 Starting deep research...\n")

    final_state = await graph.ainvoke(initial_state)

    # Display results
    print("\n" + "=" * 80)
    print("STARTUP ANALYSIS COMPLETE")
    print("=" * 80)

    extracted = final_state["extracted_data"]

    print("\n🏢 COMPANY OVERVIEW")
    print("-" * 80)
    print(f"Name: {extracted.get('company_name', 'N/A')}")
    print(f"Tagline: {extracted.get('tagline', 'N/A')}")
    print(f"Founded: {extracted.get('founded', 'N/A')}")
    print(f"HQ: {extracted.get('headquarters', 'N/A')}")

    print("\n💼 BUSINESS")
    print("-" * 80)
    print(f"Model: {extracted.get('business_model', 'N/A')}")
    print(f"Target Market: {extracted.get('target_market', 'N/A')}")
    print(f"Value Proposition: {extracted.get('unique_value_proposition', 'N/A')}")

    print("\n💰 FUNDING")
    print("-" * 80)
    print(f"Total Funding: {extracted.get('total_funding', 'N/A')}")
    print(f"Valuation: {extracted.get('valuation', 'N/A')}")

    funding_rounds = extracted.get('funding_rounds', [])
    if funding_rounds:
        print("\nFunding Rounds:")
        for round_info in funding_rounds:
            print(f"  - {round_info.get('round', 'N/A')}: {round_info.get('amount', 'N/A')} ({round_info.get('date', 'N/A')})")

    print("\n🔧 TECHNOLOGY")
    print("-" * 80)
    tech_stack = extracted.get('technology_stack', [])
    if tech_stack:
        print(f"Tech Stack: {', '.join(tech_stack)}")

    print("\n🏆 COMPETITION")
    print("-" * 80)
    competitors = extracted.get('competitors', [])
    if competitors:
        print(f"Competitors: {', '.join(competitors)}")

    print("\n📰 RECENT NEWS")
    print("-" * 80)
    news = extracted.get('recent_news', [])
    if news:
        for item in news[:5]:  # Show up to 5 news items
            print(f"  • {item}")

    print("\n\n📊 FULL JSON DATA:")
    print("-" * 80)
    print(json.dumps(extracted, indent=2))

    print("\n" + "=" * 80)


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        print("Error: Required API keys not found")
        print("Please set ANTHROPIC_API_KEY and TAVILY_API_KEY in .env")
        exit(1)

    asyncio.run(main())
