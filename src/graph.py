"""
LangGraph workflow for the High-Risk Investigation Agent.

This module defines the graph structure connecting all agent nodes.
"""

from langgraph.graph import StateGraph, END
from src.state import InvestigationState
from src.agents.triage_agent import triage_agent
from src.agents.analysis_agent import analysis_agent
from src.agents.narrative_agent import narrative_agent
from src.agents.decision_agent import decision_agent


def create_investigation_graph():
    """
    Create the investigation workflow graph.
    
    Returns:
        Compiled LangGraph StateGraph
    """
    # Initialize the graph
    workflow = StateGraph(InvestigationState)
    
    # Add nodes
    workflow.add_node("triage", triage_agent)
    workflow.add_node("analysis", analysis_agent)
    workflow.add_node("narrative", narrative_agent)
    workflow.add_node("decision", decision_agent)
    
    # Define edges (sequential flow)
    workflow.set_entry_point("triage")
    workflow.add_edge("triage", "analysis")
    workflow.add_edge("analysis", "narrative")
    workflow.add_edge("narrative", "decision")
    workflow.add_edge("decision", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def run_investigation(entity_id: str, entity_type: str = "user"):
    """
    Run a complete investigation for an entity.
    
    Args:
        entity_id: ID of the entity to investigate
        entity_type: Type of entity (user/transaction/account)
        
    Returns:
        Final investigation state with all results
    """
    # Create the graph
    app = create_investigation_graph()
    
    # Initialize state
    initial_state = InvestigationState(
        entity_id=entity_id,
        entity_type=entity_type,
        raw_data=None,
        risk_score=None,
        detected_patterns=None,
        narrative=None,
        recommendation=None,
        metadata=None
    )
    
    # Run the workflow
    final_state = app.invoke(initial_state)
    
    return final_state
