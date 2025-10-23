"""
Research phase: Query generation and web search.
"""
from typing import Dict, Any, List
import json
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults

from .configuration import Configuration
from .state import ResearchState
from .prompts import QUERY_WRITER_PROMPT, INFO_PROMPT
from src.common.utils import deduplicate_sources, format_sources, extract_field_descriptions
from src.common.llm import get_llm_for_research


def parse_queries_from_response(response_text: str) -> List[str]:
    """
    Parse search queries from LLM response.

    Expects numbered list or JSON array format.
    """
    queries = []

    # Try JSON first
    try:
        parsed = json.loads(response_text)
        if isinstance(parsed, list):
            return [str(q) for q in parsed]
    except (json.JSONDecodeError, ValueError):
        pass

    # Parse numbered list
    for line in response_text.split('\n'):
        line = line.strip()
        # Match patterns like "1. query" or "- query"
        if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
            # Remove numbering and bullets
            query = line.lstrip('0123456789.-* ').strip()
            if query:
                queries.append(query)

    return queries[:10]  # Limit to 10 max


async def research_node(state: ResearchState, config: Configuration) -> Dict[str, Any]:
    """
    Research phase node.

    Generates targeted search queries based on schema requirements
    and executes web searches to gather information.

    Args:
        state: Current research state
        config: Agent configuration

    Returns:
        Updated state with research results
    """
    company_name = state["company_name"]
    schema = state["extraction_schema"]
    user_context = state.get("user_context", "")
    follow_up_queries = state.get("follow_up_queries", [])

    # Initialize LLM with rate limiting
    llm = get_llm_for_research(config)

    # Extract schema fields for context
    field_descriptions = extract_field_descriptions(schema)

    # Generate search queries
    if follow_up_queries:
        # Use follow-up queries from reflection
        queries = follow_up_queries[:config.max_search_queries]
    else:
        # Generate initial queries using centralized prompt
        query_prompt = ChatPromptTemplate.from_messages([
            ("system", QUERY_WRITER_PROMPT),
            ("human", "Generate search queries for: {company_name}")
        ])

        chain = query_prompt | llm

        response = await chain.ainvoke({
            "company_name": company_name,
            "max_search_queries": config.max_search_queries,
            "schema": json.dumps(schema, indent=2),
            "user_context": f"\nAdditional context: {user_context}" if user_context else ""
        })

        queries = parse_queries_from_response(response.content)

    # Execute web searches based on search_provider
    all_results = []

    if config.search_provider == "tavily":
        # Use Tavily (paid, high quality)
        search_tool = TavilySearchResults(
            max_results=config.max_search_results,
            search_depth="advanced",
            include_raw_content=True
        )

        for query in queries[:config.max_search_queries]:
            try:
                results = await search_tool.ainvoke(query)
                if isinstance(results, list):
                    all_results.extend(results)
                elif isinstance(results, dict):
                    all_results.append(results)
            except Exception as e:
                print(f"Tavily search error for query '{query}': {e}")
                continue

    elif config.search_provider == "google_adk":
        # Use Google ADK google_search (free with Gemini 2+)
        try:
            from langchain_google_genai import GoogleSearchAPIWrapper

            google_search = GoogleSearchAPIWrapper()

            for query in queries[:config.max_search_queries]:
                try:
                    # Google search returns string, need to structure it
                    result_text = await google_search.arun(query)
                    all_results.append({
                        "title": f"Google Search: {query}",
                        "content": result_text[:1000],  # Limit content
                        "url": f"https://www.google.com/search?q={query.replace(' ', '+')}",
                        "raw_content": result_text
                    })
                except Exception as e:
                    print(f"Google ADK search error for query '{query}': {e}")
                    continue

        except ImportError:
            print("Warning: langchain-google-genai not installed. Install with: pip install langchain-google-genai")
            print("Falling back to Tavily...")
            # Fallback to Tavily
            search_tool = TavilySearchResults(
                max_results=config.max_search_results,
                search_depth="advanced"
            )
            for query in queries[:config.max_search_queries]:
                try:
                    results = await search_tool.ainvoke(query)
                    if isinstance(results, list):
                        all_results.extend(results)
                except Exception as e:
                    print(f"Fallback search error: {e}")
                    continue

    elif config.search_provider == "hybrid":
        # Use Tavily for main queries, Google ADK for follow-up (cost optimization)
        # First half with Tavily (high quality)
        tavily_tool = TavilySearchResults(
            max_results=config.max_search_results,
            search_depth="advanced",
            include_raw_content=True
        )

        mid_point = len(queries) // 2

        # Tavily for first half
        for query in queries[:mid_point]:
            try:
                results = await tavily_tool.ainvoke(query)
                if isinstance(results, list):
                    all_results.extend(results)
            except Exception as e:
                print(f"Tavily (hybrid) error for '{query}': {e}")
                continue

        # Google ADK for second half (free)
        try:
            from langchain_google_genai import GoogleSearchAPIWrapper
            google_search = GoogleSearchAPIWrapper()

            for query in queries[mid_point:config.max_search_queries]:
                try:
                    result_text = await google_search.arun(query)
                    all_results.append({
                        "title": f"Google Search: {query}",
                        "content": result_text[:1000],
                        "url": f"https://www.google.com/search?q={query.replace(' ', '+')}",
                        "raw_content": result_text
                    })
                except Exception as e:
                    print(f"Google ADK (hybrid) error for '{query}': {e}")
                    continue
        except ImportError:
            print("Warning: langchain-google-genai not installed for hybrid mode")
            # Continue with Tavily only
            for query in queries[mid_point:config.max_search_queries]:
                try:
                    results = await tavily_tool.ainvoke(query)
                    if isinstance(results, list):
                        all_results.extend(results)
                except Exception as e:
                    continue

    elif config.search_provider == "serpapi":
        # Use SerpAPI (Google results scraping, paid)
        try:
            from langchain_community.utilities import SerpAPIWrapper

            serpapi = SerpAPIWrapper()

            for query in queries[:config.max_search_queries]:
                try:
                    results = serpapi.results(query)
                    # SerpAPI returns dict with 'organic_results'
                    organic = results.get("organic_results", [])

                    for item in organic[:config.max_search_results]:
                        all_results.append({
                            "title": item.get("title", ""),
                            "content": item.get("snippet", ""),
                            "url": item.get("link", ""),
                            "raw_content": item.get("snippet", "")
                        })
                except Exception as e:
                    print(f"SerpAPI search error for query '{query}': {e}")
                    continue

        except ImportError:
            print("Warning: google-search-results not installed. Install with: pip install google-search-results")
            print("Falling back to DuckDuckGo (free alternative)...")
            # Fallback to free alternative
            config = config.model_copy(update={"search_provider": "duckduckgo"})

    elif config.search_provider == "bing":
        # Use Bing Search API (Microsoft, free tier available)
        try:
            from langchain_community.utilities import BingSearchAPIWrapper

            bing_search = BingSearchAPIWrapper(k=config.max_search_results)

            for query in queries[:config.max_search_queries]:
                try:
                    # Bing returns list of dicts
                    results = bing_search.results(query, num_results=config.max_search_results)

                    for item in results:
                        all_results.append({
                            "title": item.get("title", ""),
                            "content": item.get("snippet", ""),
                            "url": item.get("link", ""),
                            "raw_content": item.get("snippet", "")
                        })
                except Exception as e:
                    print(f"Bing search error for query '{query}': {e}")
                    continue

        except ImportError:
            print("Warning: Bing API not configured. Set BING_SUBSCRIPTION_KEY in environment")
            print("Falling back to DuckDuckGo (free alternative)...")
            config = config.model_copy(update={"search_provider": "duckduckgo"})

    elif config.search_provider == "duckduckgo":
        # Use DuckDuckGo (completely free, no API key needed)
        try:
            from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

            ddg_search = DuckDuckGoSearchAPIWrapper()

            for query in queries[:config.max_search_queries]:
                try:
                    # DuckDuckGo returns string, need to parse
                    result_text = ddg_search.run(query)

                    # Split by newlines and create structured results
                    snippets = result_text.split('\n')[:config.max_search_results]

                    for i, snippet in enumerate(snippets):
                        if snippet.strip():
                            all_results.append({
                                "title": f"DuckDuckGo Result {i+1}: {query}",
                                "content": snippet.strip(),
                                "url": f"https://duckduckgo.com/?q={query.replace(' ', '+')}",
                                "raw_content": snippet.strip()
                            })
                except Exception as e:
                    print(f"DuckDuckGo search error for query '{query}': {e}")
                    continue

        except ImportError:
            print("Warning: duckduckgo-search not installed. Install with: pip install duckduckgo-search")
            print("Cannot proceed without a search provider.")
            return {
                "research_queries": queries,
                "search_results": [],
                "research_notes": "Error: No search provider available. Please install duckduckgo-search or configure another provider.",
                "messages": [{"role": "assistant", "content": "Search provider not available"}]
            }

    elif config.search_provider == "brave":
        # Use Brave Search API (privacy-focused, free tier available)
        try:
            from langchain_community.utilities import BraveSearchWrapper

            brave_search = BraveSearchWrapper(search_kwargs={"count": config.max_search_results})

            for query in queries[:config.max_search_queries]:
                try:
                    result_text = brave_search.run(query)

                    # Parse Brave results (similar to DuckDuckGo)
                    snippets = result_text.split('\n')[:config.max_search_results]

                    for i, snippet in enumerate(snippets):
                        if snippet.strip():
                            all_results.append({
                                "title": f"Brave Result {i+1}: {query}",
                                "content": snippet.strip(),
                                "url": f"https://search.brave.com/search?q={query.replace(' ', '+')}",
                                "raw_content": snippet.strip()
                            })
                except Exception as e:
                    print(f"Brave search error for query '{query}': {e}")
                    continue

        except ImportError:
            print("Warning: Brave Search not configured. Set BRAVE_API_KEY in environment")
            print("Falling back to DuckDuckGo (free alternative)...")
            config = config.model_copy(update={"search_provider": "duckduckgo"})

    # Deduplicate search results by URL
    deduplicated_results = deduplicate_sources(all_results)

    # Format sources with token limits (prevents context overflow)
    formatted_sources = format_sources(
        deduplicated_results,
        include_raw_content=True,
        max_tokens_per_source=1000  # Limit per source to prevent LLM context overflow
    )

    # Generate structured research notes using centralized prompt
    notes_prompt = ChatPromptTemplate.from_messages([
        ("system", INFO_PROMPT),
        ("human", "Create research notes for {company_name}.")
    ])

    notes_chain = notes_prompt | llm

    notes_response = await notes_chain.ainvoke({
        "company_name": company_name,
        "schema": json.dumps(schema, indent=2),
        "content": formatted_sources,
        "user_context": user_context if user_context else "No additional context provided."
    })

    return {
        "research_queries": queries,
        "search_results": deduplicated_results,
        "research_notes": notes_response.content,
        "messages": [{"role": "assistant", "content": f"Researched {company_name} with {len(queries)} queries, found {len(deduplicated_results)} unique results"}]
    }
