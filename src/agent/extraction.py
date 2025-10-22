"""
Extraction phase: Extract structured data from research notes.
"""
from typing import Dict, Any
import json
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from .configuration import Configuration
from .state import ResearchState
from .prompts import EXTRACTION_PROMPT
from .llm import get_llm_for_extraction


async def extraction_node(state: ResearchState, config: Configuration) -> Dict[str, Any]:
    """
    Extraction phase node.

    Extracts structured data from research notes according to the schema.

    Args:
        state: Current research state
        config: Agent configuration

    Returns:
        Updated state with extracted data
    """
    schema = state["extraction_schema"]
    notes = state["research_notes"]
    company_name = state["company_name"]

    # Initialize LLM with rate limiting (optimized for extraction)
    llm = get_llm_for_extraction(config)

    # Create extraction prompt using centralized template
    extraction_prompt = ChatPromptTemplate.from_messages([
        ("system", EXTRACTION_PROMPT),
        ("human", "Extract structured data for {company_name}.")
    ])

    # Use JSON output parser for structured extraction
    parser = JsonOutputParser()

    chain = extraction_prompt | llm | parser

    try:
        extracted = await chain.ainvoke({
            "schema": json.dumps(schema, indent=2),
            "notes": notes,
            "company_name": company_name
        })
    except Exception as e:
        print(f"Extraction error: {e}")
        # Fallback: return empty structure matching schema
        extracted = {
            field: None
            for field in schema.get("properties", {}).keys()
        }
        extracted["company_name"] = company_name

    return {
        "extracted_data": extracted,
        "messages": [{"role": "assistant", "content": f"Extracted {len(extracted)} fields for {company_name}"}]
    }
