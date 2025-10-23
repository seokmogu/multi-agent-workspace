"""
Common utilities and shared modules for all agents.

This package contains reusable components that can be shared across
different agent implementations.
"""

from .llm import get_llm_for_research, get_llm_for_extraction, get_llm_for_reflection
from .utils import (
    deduplicate_sources,
    format_sources,
    calculate_completeness,
    merge_research_results,
    extract_unique_urls,
    create_search_summary,
    validate_extracted_data,
    calculate_confidence_score,
)

__all__ = [
    # LLM functions
    "get_llm_for_research",
    "get_llm_for_extraction",
    "get_llm_for_reflection",
    # Utility functions
    "deduplicate_sources",
    "format_sources",
    "calculate_completeness",
    "merge_research_results",
    "extract_unique_urls",
    "create_search_summary",
    "validate_extracted_data",
    "calculate_confidence_score",
]
