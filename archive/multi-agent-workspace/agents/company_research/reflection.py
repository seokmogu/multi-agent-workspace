"""
Reflection phase: Evaluate extraction quality and generate follow-up queries.
"""
from typing import Dict, Any, List
import json
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from .configuration import Configuration
from .state import ResearchState
from .prompts import REFLECTION_PROMPT
from src.common.utils import calculate_completeness, truncate_text
from src.common.llm import get_llm_for_reflection


# evaluate_completeness moved to utils.py


async def reflection_node(state: ResearchState, config: Configuration) -> Dict[str, Any]:
    """
    Reflection phase node.

    Evaluates extraction quality and determines whether to continue researching.

    Args:
        state: Current research state
        config: Agent configuration

    Returns:
        Updated state with reflection results
    """
    schema = state["extraction_schema"]
    extracted = state["extracted_data"]
    company_name = state["company_name"]
    reflection_count = state.get("reflection_count", 0)

    # Simple completeness check using utils
    missing_fields, completeness_score = calculate_completeness(extracted, schema)

    # Early exit conditions
    if (
        reflection_count >= config.max_reflection_steps or
        len(missing_fields) == 0 or
        completeness_score > 0.85
    ):
        return {
            "reflection_count": reflection_count + 1,
            "missing_fields": missing_fields,
            "follow_up_queries": [],
            "is_complete": True,
            "messages": [{
                "role": "assistant",
                "content": f"Research complete. Completeness: {completeness_score:.0%}"
            }]
        }

    # Use LLM with rate limiting to generate follow-up queries
    llm = get_llm_for_reflection(config)

    # Use centralized prompt template
    reflection_prompt = ChatPromptTemplate.from_messages([
        ("system", REFLECTION_PROMPT),
        ("human", "Analyze extraction quality for {company_name}.")
    ])

    parser = JsonOutputParser()
    chain = reflection_prompt | llm | parser

    try:
        evaluation = await chain.ainvoke({
            "schema": json.dumps(schema, indent=2),
            "extracted_info": json.dumps(extracted, indent=2),
            "missing_fields": ", ".join(missing_fields),
            "notes": truncate_text(state["research_notes"], max_length=2000),  # Use utils function
            "company_name": company_name
        })
    except Exception as e:
        print(f"Reflection error: {e}")
        evaluation = {
            "analysis": "Error during reflection",
            "follow_up_queries": [],
            "is_complete": True
        }

    # Limit follow-up queries
    follow_up_queries = evaluation.get("follow_up_queries", [])[:3]

    # Determine if complete
    is_complete = (
        evaluation.get("is_complete", False) or
        len(follow_up_queries) == 0 or
        reflection_count + 1 >= config.max_reflection_steps
    )

    return {
        "reflection_count": reflection_count + 1,
        "missing_fields": missing_fields,
        "follow_up_queries": follow_up_queries,
        "is_complete": is_complete,
        "messages": [{
            "role": "assistant",
            "content": evaluation.get("analysis", "Reflection complete")
        }]
    }
