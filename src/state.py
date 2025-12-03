"""
State management for the High-Risk Investigation Agent.

This module defines the state schema that flows through all agent nodes
in the investigation workflow.
"""

from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime


class InvestigationState(TypedDict):
    """
    State object that flows through the investigation graph.
    
    Each agent node reads from and writes to this state as the investigation
    progresses through the workflow.
    """
    
    # Input
    entity_id: str
    entity_type: str  # "user", "transaction", or "account"
    
    # Node 1: Triage and Data Gathering
    raw_data: Optional[Dict[str, Any]]
    
    # Node 2: Risk Scoring and Pattern Detection
    risk_score: Optional[float]
    detected_patterns: Optional[List[Dict[str, Any]]]
    
    # Node 3: Narrative Generation
    narrative: Optional[str]
    
    # Node 4: Recommendation and Review
    recommendation: Optional[Dict[str, Any]]
    
    # Metadata
    metadata: Optional[Dict[str, Any]]
