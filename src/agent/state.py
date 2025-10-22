"""
State management for the research agent.
"""
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class ResearchState(TypedDict):
    """
    State for the company research agent workflow.

    Tracks research progress through three phases:
    1. Research: Query generation and web search
    2. Extraction: Data extraction into schema
    3. Reflection: Quality evaluation and iteration
    """

    # Input
    company_name: str
    extraction_schema: Dict[str, Any]
    user_context: str  # Optional additional context from user

    # Research phase
    research_queries: List[str]
    search_results: List[Dict[str, Any]]
    research_notes: str

    # Extraction phase
    extracted_data: Dict[str, Any]

    # Reflection phase
    reflection_count: int
    missing_fields: List[str]
    follow_up_queries: List[str]

    # Control flow
    is_complete: bool
    messages: Annotated[List[BaseMessage], add_messages]


# Default extraction schema
DEFAULT_SCHEMA = {
    "title": "Company Information",
    "description": "Comprehensive information about a company",
    "type": "object",
    "properties": {
        "company_name": {
            "type": "string",
            "description": "Official registered company name"
        },
        "founded": {
            "type": "string",
            "description": "Year the company was founded"
        },
        "headquarters": {
            "type": "string",
            "description": "City and country of headquarters location"
        },
        "industry": {
            "type": "string",
            "description": "Primary industry or sector"
        },
        "description": {
            "type": "string",
            "description": "Brief overview of what the company does (2-3 sentences)"
        },
        "products": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of main products or services offered"
        },
        "key_people": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Person's full name"},
                    "role": {"type": "string", "description": "Job title or position"}
                },
                "required": ["name", "role"]
            },
            "description": "Key executives and leadership"
        },
        "revenue": {
            "type": "string",
            "description": "Most recent annual revenue (if publicly available)"
        },
        "employee_count": {
            "type": "string",
            "description": "Approximate number of employees"
        },
        "website": {
            "type": "string",
            "description": "Official company website URL"
        }
    },
    "required": ["company_name", "description"]
}
