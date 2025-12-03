"""
Chat Router Agent for the High-Risk Investigation System.

This agent acts as the entry point for the graph, handling both:
1. Structured inputs (direct entity_id provided)
2. Chat inputs (natural language requests)
"""

from typing import Dict, Any, List
from src.state import InvestigationState
from src.config import Config
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import re

def chat_router(state: InvestigationState) -> InvestigationState:
    """
    Analyzes input to determine if it's a chat message or structured input.
    Extracts entity information from chat messages if needed.
    """
    print(f"\n{'='*60}")
    print(f"ROUTER: ANALYZING INPUT")
    print(f"{'='*60}")
    
    # Case 1: Structured Input (Entity ID already provided)
    if state.get('entity_id') and state['entity_id'] != "UNKNOWN":
        print(f"✅ Structured input detected: {state['entity_id']}")
        return state
        
    # Case 2: Chat Input
    messages = state.get('messages', [])
    if not messages:
        print("⚠️ No input provided")
        return state
        
    # Get last user message
    last_message = messages[-1]
    content = last_message.content if hasattr(last_message, 'content') else str(last_message)
    
    # Handle list content (common in LangChain for multimodal messages)
    if isinstance(content, list):
        text_parts = [block.get('text', '') for block in content if isinstance(block, dict) and block.get('type') == 'text']
        content = " ".join(text_parts)
        
    print(f"📨 Received message: {content}")
    
    # Simple regex extraction for entities
    # Looks for patterns like "USER_123", "ACC_456", "TXN_789"
    # Or common variations like "user 123"
    
    entity_id = None
    entity_type = "user"
    
    # Regex for standard ID formats
    id_pattern = r'\b(USER|ACC|TXN)[-_]?(\w+)\b'
    match = re.search(id_pattern, content, re.IGNORECASE)
    
    if match:
        prefix = match.group(1).upper()
        value = match.group(2)
        entity_id = f"{prefix}_{value}"
        
        if prefix == 'ACC':
            entity_type = 'account'
        elif prefix == 'TXN':
            entity_type = 'transaction'
            
    # Fallback: Look for "investigate X" pattern
    if not entity_id:
        investigate_pattern = r'investigate\s+(?:user|account|transaction)?\s*(\w+)'
        match = re.search(investigate_pattern, content, re.IGNORECASE)
        if match:
            entity_id = match.group(1)
            # Default to user if not specified, or try to infer
            if "account" in content.lower():
                entity_type = "account"
            elif "transaction" in content.lower():
                entity_type = "transaction"
    
    if entity_id:
        print(f"✅ Extracted Entity: {entity_id} ({entity_type})")
        state['entity_id'] = entity_id
        state['entity_type'] = entity_type
        
        # Add confirmation message
        if isinstance(messages, list):
            state['messages'].append(
                AIMessage(content=f"I've identified the entity **{entity_id}**. Starting investigation now...")
            )
    else:
        print("❓ No entity found in message")
        # Add clarification request
        if isinstance(messages, list):
            state['messages'].append(
                AIMessage(content="I can help you investigate high-risk entities. Please provide an Entity ID (e.g., 'Investigate USER_001').")
            )
            
    return state

def route_from_chat(state: InvestigationState) -> str:
    """
    Determines next step based on whether entity_id was found.
    """
    if state.get('entity_id') and state['entity_id'] != "UNKNOWN":
        return "triage"
    return "__end__"
