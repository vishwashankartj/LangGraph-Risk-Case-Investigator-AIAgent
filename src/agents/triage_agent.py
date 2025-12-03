"""
Node 1: Triage and Data Gathering Agent

This agent receives a flagged entity ID and gathers all relevant data
from various sources to create a comprehensive data package.
"""

from typing import Dict, Any
from datetime import datetime
from src.state import InvestigationState
from src.tools.data_gathering import gather_all_data


def triage_agent(state: InvestigationState) -> InvestigationState:
    """
    Triage and Data Gathering Agent.
    
    Takes the flagged entity and gathers comprehensive data from all sources.
    
    Args:
        state: Current investigation state with entity_id and entity_type
        
    Returns:
        Updated state with raw_data populated
    """
    print(f"\n{'='*60}")
    print(f"NODE 1: TRIAGE AND DATA GATHERING")
    print(f"{'='*60}")
    print(f"Entity ID: {state.get('entity_id', 'UNKNOWN')}")
    print(f"Entity Type: {state.get('entity_type', 'user')}")
    
    # Validate entity
    if not state.get('entity_id'):
        raise ValueError("Entity ID is required")
    
    entity_id = state['entity_id']
    entity_type = state.get('entity_type', 'user')
    
    # Gather data from all sources
    print("\n📊 Gathering data from multiple sources...")
    print("  - User Database")
    print("  - Activity Logs")
    print("  - Social Graph")
    print("  - Flag History")
    print("  - Transaction Database")
    
    raw_data = gather_all_data(entity_id, entity_type)
    
    # Add gathering metadata
    metadata = {
        "triage_timestamp": datetime.now().isoformat(),
        "data_sources_queried": raw_data.get("data_sources", []),
        "data_completeness": "complete"
    }
    
    # Update state
    state['raw_data'] = raw_data
    state['metadata'] = metadata
    
    print(f"\n✅ Data gathering complete")
    print(f"   Sources queried: {len(raw_data.get('data_sources', []))}")
    print(f"   Account age: {raw_data.get('profile', {}).get('account_age_days', 'N/A')} days")
    print(f"   Total transactions: {raw_data.get('transactions', {}).get('total_transactions', 0)}")
    print(f"   Past flags: {raw_data.get('flags', {}).get('total_flags', 0)}")
    
    return state
