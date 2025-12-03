"""
Node 3: Narrative Generation Agent

This agent synthesizes the investigation findings into a clear,
plain-language narrative suitable for decision makers.
"""

from typing import Dict, Any
from src.state import InvestigationState
from langchain_core.prompts import ChatPromptTemplate
from src.config import Config


def generate_narrative_with_llm(
    entity_id: str,
    risk_score: float,
    patterns: list,
    raw_data: Dict[str, Any]
) -> str:
    """
    Generate investigation narrative using LLM.
    
    Args:
        entity_id: Entity being investigated
        risk_score: Calculated risk score
        patterns: Detected suspicious patterns
        raw_data: Complete data package
        
    Returns:
        Formatted narrative string
    """
    # Initialize LLM
    llm = Config.get_llm()
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert financial investigator tasked with creating clear, 
concise investigation narratives. Your narratives should be:
- Professional and objective
- Focused on facts and evidence
- Clear for both technical and non-technical audiences
- Structured with sections: Executive Summary, Timeline, Evidence, and Impact Assessment
"""),
        ("user", """Generate an investigation narrative for the following case:

ENTITY ID: {entity_id}
RISK SCORE: {risk_score}/100

ACCOUNT INFORMATION:
- Account Age: {account_age} days
- Verification Status: {verification_status}
- Country: {country}
- Total Transactions: {total_transactions}
- Transaction Volume: ${transaction_volume}
- Past Flags: {past_flags}

DETECTED PATTERNS:
{patterns_text}

ADDITIONAL CONTEXT:
- 24h Transaction Activity: {last_24h_transactions} transactions, ${last_24h_volume}
- VPN Usage: {vpn_detected}
- Geographic Spread: {geo_spread} different locations
- Linked Accounts: {linked_accounts}

Please provide a structured investigation narrative with:
1. Executive Summary (2-3 sentences)
2. Timeline of Suspicious Activities
3. Specific Evidence Citations
4. Quantified Impact Assessment
""")
    ])
    
    # Extract data
    profile = raw_data.get('profile', {})
    activity = raw_data.get('activity', {})
    transactions = raw_data.get('transactions', {})
    flags = raw_data.get('flags', {})
    connections = raw_data.get('connections', {})
    
    # Format patterns
    patterns_text = "\n".join([
        f"- {p['pattern_type'].upper()} ({p['severity']}): {p['description']}"
        for p in patterns
    ]) if patterns else "No suspicious patterns detected"
    
    # Prepare inputs
    inputs = {
        "entity_id": entity_id,
        "risk_score": f"{risk_score:.1f}",
        "account_age": profile.get('account_age_days', 'N/A'),
        "verification_status": profile.get('verification_status', 'N/A'),
        "country": profile.get('country', 'N/A'),
        "total_transactions": transactions.get('total_transactions', 0),
        "transaction_volume": f"{transactions.get('total_volume_usd', 0):.2f}",
        "past_flags": flags.get('total_flags', 0),
        "patterns_text": patterns_text,
        "last_24h_transactions": transactions.get('last_24h_transactions', 0),
        "last_24h_volume": f"{transactions.get('last_24h_volume_usd', 0):.2f}",
        "vpn_detected": "Yes" if activity.get('vpn_usage_detected') else "No",
        "geo_spread": activity.get('geographic_spread', 1),
        "linked_accounts": connections.get('total_connections', 0)
    }
    
    # Generate narrative
    chain = prompt | llm
    response = chain.invoke(inputs)
    
    return response.content


def generate_narrative_fallback(
    entity_id: str,
    risk_score: float,
    patterns: list,
    raw_data: Dict[str, Any]
) -> str:
    """
    Generate narrative without LLM (fallback for when API key is not configured).
    
    Args:
        entity_id: Entity being investigated
        risk_score: Calculated risk score
        patterns: Detected suspicious patterns
        raw_data: Complete data package
        
    Returns:
        Formatted narrative string
    """
    profile = raw_data.get('profile', {})
    transactions = raw_data.get('transactions', {})
    flags = raw_data.get('flags', {})
    activity = raw_data.get('activity', {})
    
    risk_level = Config.get_risk_level(risk_score)
    
    narrative = f"""
INVESTIGATION NARRATIVE
Entity ID: {entity_id}
Risk Score: {risk_score:.1f}/100 ({risk_level.upper()} RISK)

═══════════════════════════════════════════════════════════════

EXECUTIVE SUMMARY
─────────────────────────────────────────────────────────────
Entity {entity_id} has been flagged for investigation with a risk score of {risk_score:.1f}/100. 
The account was created {profile.get('account_age_days', 'N/A')} days ago and has completed {transactions.get('total_transactions', 0)} 
transactions with a total volume of ${transactions.get('total_volume_usd', 0):.2f}. 

{len(patterns)} suspicious pattern(s) were detected during the investigation.

TIMELINE OF ACTIVITIES
─────────────────────────────────────────────────────────────
Account Registration: {profile.get('account_age_days', 'N/A')} days ago
Total Transaction Activity: {transactions.get('total_transactions', 0)} transactions
Recent Activity (24h): {transactions.get('last_24h_transactions', 0)} transactions, ${transactions.get('last_24h_volume_usd', 0):.2f}
Past Security Flags: {flags.get('total_flags', 0)}

DETECTED PATTERNS & EVIDENCE
─────────────────────────────────────────────────────────────
"""
    
    if patterns:
        for i, pattern in enumerate(patterns, 1):
            narrative += f"\n{i}. {pattern['pattern_type'].replace('_', ' ').upper()} ({pattern['severity'].upper()} SEVERITY)"
            narrative += f"\n   Description: {pattern['description']}"
            narrative += f"\n   Evidence: {pattern.get('evidence', {})}\n"
    else:
        narrative += "\nNo suspicious patterns detected.\n"
    
    narrative += f"""
IMPACT ASSESSMENT
─────────────────────────────────────────────────────────────
Financial Exposure: ${transactions.get('total_volume_usd', 0):.2f} total volume
24-Hour Velocity: {transactions.get('last_24h_transactions', 0)} transactions
Geographic Risk: {activity.get('geographic_spread', 1)} different locations
Network Risk: {raw_data.get('connections', {}).get('total_connections', 0)} linked accounts
Historical Risk: {flags.get('total_flags', 0)} past flags

═══════════════════════════════════════════════════════════════
"""
    
    return narrative.strip()


def narrative_agent(state: InvestigationState) -> InvestigationState:
    """
    Narrative Generation Agent.
    
    Synthesizes findings into a clear investigation narrative.
    
    Args:
        state: Current investigation state with risk_score, patterns, and raw_data
        
    Returns:
        Updated state with narrative
    """
    print(f"\n{'='*60}")
    print(f"NODE 3: NARRATIVE GENERATION")
    print(f"{'='*60}")
    
    entity_id = state['entity_id']
    risk_score = state.get('risk_score', 0)
    patterns = state.get('detected_patterns', [])
    raw_data = state.get('raw_data', {})
    
    print("\n📝 Generating investigation narrative...")
    
    # Try to use LLM, fall back to template if API key not configured
    try:
        if Config.has_api_key():
            narrative = generate_narrative_with_llm(entity_id, risk_score, patterns, raw_data)
            print(f"   Using {Config.LLM_PROVIDER.upper()} LLM-generated narrative")
        else:
            narrative = generate_narrative_fallback(entity_id, risk_score, patterns, raw_data)
            print("   Using template-based narrative (no API key configured)")
    except Exception as e:
        print(f"   ⚠️  LLM generation failed: {str(e)}")
        print("   Falling back to template-based narrative")
        narrative = generate_narrative_fallback(entity_id, risk_score, patterns, raw_data)
    
    # Update state
    state['narrative'] = narrative
    
    print(f"\n✅ Narrative generation complete")
    print(f"   Length: {len(narrative)} characters")
    
    return state
