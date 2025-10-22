"""
Main graph construction for the research agent.
"""
from typing import Literal
from langgraph.graph import StateGraph, END

from .configuration import Configuration
from .state import ResearchState
from .research import research_node
from .extraction import extraction_node
from .reflection import reflection_node


def should_continue(state: ResearchState) -> Literal["research", "end"]:
    """
    Determine whether to continue researching or end the workflow.

    Args:
        state: Current research state

    Returns:
        Next node name
    """
    if state.get("is_complete", False):
        return "end"
    return "research"


def build_research_graph(config: Configuration):
    """
    Build the research workflow graph.

    The workflow follows this pattern:
    1. Research: Generate queries and search web
    2. Extract: Extract structured data from results
    3. Reflect: Evaluate quality and decide next steps
    4. Loop back to Research if needed, or End

    Args:
        config: Agent configuration

    Returns:
        Compiled StateGraph
    """
    workflow = StateGraph(ResearchState)

    # Add nodes with config binding
    workflow.add_node(
        "research",
        lambda state: research_node(state, config)
    )
    workflow.add_node(
        "extract",
        lambda state: extraction_node(state, config)
    )
    workflow.add_node(
        "reflect",
        lambda state: reflection_node(state, config)
    )

    # Define workflow
    workflow.set_entry_point("research")

    # Sequential flow: research → extract → reflect
    workflow.add_edge("research", "extract")
    workflow.add_edge("extract", "reflect")

    # Conditional routing from reflection
    workflow.add_conditional_edges(
        "reflect",
        should_continue,
        {
            "research": "research",  # Continue researching
            "end": END               # Finish
        }
    )

    return workflow.compile()
