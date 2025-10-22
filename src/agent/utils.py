"""
Utility functions for the research agent.

Includes search result processing, deduplication, and formatting.
"""
from typing import List, Dict, Any, Union


def deduplicate_sources(search_response: Union[dict, List[dict]]) -> List[dict]:
    """
    Deduplicate search results based on URL.

    Args:
        search_response: Either:
            - A dict with a 'results' key containing a list of search results
            - A list of dicts, each containing search results
            - A list of individual result dicts

    Returns:
        List of deduplicated search results

    Example:
        >>> results = deduplicate_sources([
        ...     {'url': 'https://example.com', 'title': 'A'},
        ...     {'url': 'https://example.com', 'title': 'B'},  # duplicate
        ...     {'url': 'https://other.com', 'title': 'C'}
        ... ])
        >>> len(results)
        2
    """
    # Convert input to list of results
    if isinstance(search_response, dict):
        if 'results' in search_response:
            sources_list = search_response['results']
        else:
            # Single result dict
            sources_list = [search_response]
    elif isinstance(search_response, list):
        sources_list = []
        for response in search_response:
            if isinstance(response, dict) and 'results' in response:
                sources_list.extend(response['results'])
            elif isinstance(response, dict):
                sources_list.append(response)
            else:
                # Assume it's already a flattened list
                sources_list.extend(response if isinstance(response, list) else [response])
    else:
        raise ValueError(
            "Input must be either a dict with 'results' or a list of search results"
        )

    # Deduplicate by URL
    unique_urls = set()
    unique_sources_list = []

    for source in sources_list:
        url = source.get('url', '')
        if url and url not in unique_urls:
            unique_urls.add(url)
            unique_sources_list.append(source)

    return unique_sources_list


def format_sources(
    sources_list: List[Dict[str, Any]],
    include_raw_content: bool = True,
    max_tokens_per_source: int = 1000,
) -> str:
    """
    Format search results for LLM consumption with token limits.

    Args:
        sources_list: List of deduplicated search results
        include_raw_content: Whether to include raw_content from search
        max_tokens_per_source: Maximum tokens per source (4 chars ≈ 1 token)

    Returns:
        Formatted string with source information

    Example:
        >>> sources = [{'title': 'A', 'url': 'http://a.com', 'content': 'snippet', 'raw_content': 'full text'}]
        >>> formatted = format_sources(sources, max_tokens_per_source=100)
    """
    if not sources_list:
        return "No sources found."

    formatted_text = "Sources:\n\n"

    for idx, source in enumerate(sources_list, 1):
        title = source.get('title', 'No title')
        url = source.get('url', 'No URL')
        content = source.get('content', source.get('snippet', 'No content'))

        formatted_text += f"Source {idx}: {title}\n"
        formatted_text += f"{'='*60}\n"
        formatted_text += f"URL: {url}\n"
        formatted_text += f"{'='*60}\n"
        formatted_text += f"Snippet: {content}\n"
        formatted_text += f"{'='*60}\n"

        if include_raw_content:
            # Using rough estimate of 4 characters per token
            char_limit = max_tokens_per_source * 4

            raw_content = source.get('raw_content', '')
            if raw_content is None:
                raw_content = ''
                print(f"Warning: No raw_content found for source {url}")

            if len(raw_content) > char_limit:
                raw_content = raw_content[:char_limit] + "... [truncated]"

            formatted_text += f"Full Content (limited to {max_tokens_per_source} tokens):\n{raw_content}\n\n"

    return formatted_text.strip()


def format_all_notes(completed_notes: List[str]) -> str:
    """
    Format a list of accumulated research notes into a single string.

    This is useful when multiple research iterations have occurred,
    and we want to consolidate all findings.

    Args:
        completed_notes: List of note strings from different research iterations

    Returns:
        Formatted consolidated notes

    Example:
        >>> notes = ["Research 1 findings...", "Research 2 findings..."]
        >>> formatted = format_all_notes(notes)
    """
    if not completed_notes:
        return "No research notes available."

    formatted_str = ""
    for idx, note in enumerate(completed_notes, 1):
        formatted_str += f"""
{'='*60}
Research Iteration {idx}:
{'='*60}
{note}
{'='*60}
"""
    return formatted_str.strip()


def calculate_completeness(
    extracted: Dict[str, Any],
    schema: Dict[str, Any]
) -> tuple[List[str], float]:
    """
    Calculate extraction completeness score.

    Args:
        extracted: Extracted data dictionary
        schema: JSON schema definition

    Returns:
        Tuple of (missing_fields_list, completeness_score)
        - missing_fields_list: List of field names that are empty/missing
        - completeness_score: Float between 0.0 and 1.0

    Example:
        >>> schema = {"properties": {"name": {}, "year": {}}, "required": ["name"]}
        >>> extracted = {"name": "Acme", "year": None}
        >>> missing, score = calculate_completeness(extracted, schema)
        >>> score
        0.5
    """
    properties = schema.get('properties', {})
    required_fields = schema.get('required', [])

    if not properties:
        return [], 1.0

    missing = []
    total_fields = len(properties)
    filled_fields = 0

    for field, field_schema in properties.items():
        value = extracted.get(field)

        # Check if field is empty
        is_empty = (
            value is None or
            value == "" or
            value == "null" or
            value == "unknown" or
            value == "N/A" or
            (isinstance(value, list) and len(value) == 0) or
            (isinstance(value, dict) and len(value) == 0)
        )

        if is_empty:
            if field in required_fields:
                missing.append(f"{field} (required)")
            else:
                missing.append(field)
        else:
            filled_fields += 1

    completeness = filled_fields / total_fields if total_fields > 0 else 0.0

    return missing, completeness


def truncate_text(text: str, max_length: int = 2000, suffix: str = "... [truncated]") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append when truncated

    Returns:
        Truncated text

    Example:
        >>> long_text = "A" * 3000
        >>> truncated = truncate_text(long_text, max_length=100)
        >>> len(truncated) <= 100 + len("... [truncated]")
        True
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + suffix


def extract_field_descriptions(schema: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract field descriptions from a JSON schema.

    Args:
        schema: JSON schema definition

    Returns:
        Dictionary mapping field names to descriptions

    Example:
        >>> schema = {
        ...     "properties": {
        ...         "name": {"type": "string", "description": "Company name"},
        ...         "year": {"type": "integer", "description": "Founding year"}
        ...     }
        ... }
        >>> descriptions = extract_field_descriptions(schema)
        >>> descriptions['name']
        'Company name'
    """
    properties = schema.get('properties', {})
    return {
        field: field_schema.get('description', 'No description')
        for field, field_schema in properties.items()
    }
