"""
Node 4: Recommendation and Review Agent

This agent makes the final decision based on risk score, patterns, and policy requirements.
Includes RAG integration for policy compliance.
"""

from typing import Dict, Any
from src.state import InvestigationState
from langchain.prompts import ChatPromptTemplate
from src.config import Config


def get_policy_guidance(risk_score: float, patterns: list) -> str:
    """
    Get relevant policy guidance based on the case.
    
    In a production system, this would use RAG to retrieve relevant policy sections.
    For this demo, we return mock policy guidance.
    
    Args:
        risk_score: Calculated risk score
        patterns: Detected patterns
        
    Returns:
        Relevant policy text
    """
    risk_level = Config.get_risk_level(risk_score)
    
    policies = {
        "low": """
Risk Management Policy Section 2.1 - Low Risk Entities

For entities with risk scores 0-25:
- Action: Approve and monitor
- No immediate restrictions required
- Schedule routine review in 30 days
- Maintain standard monitoring protocols
""",
        "medium": """
Risk Management Policy Section 2.2 - Medium Risk Entities

For entities with risk scores 26-50:
- Action: Enhanced monitoring required
- Implement transaction velocity limits
- Require additional verification for high-value transactions
- Schedule review in 14 days
- Document all suspicious activities
""",
        "high": """
Risk Management Policy Section 2.3 - High Risk Entities

For entities with risk scores 51-75:
- Action: Immediate restrictions (Soft-ban)
- Limit transaction capabilities
- Require manual approval for all transactions over $100
- Escalate to senior compliance officer
- Schedule review within 48 hours
- Consider account suspension if patterns persist
""",
        "critical": """
Risk Management Policy Section 2.4 - Critical Risk Entities

For entities with risk scores 76-100:
- Action: Full account suspension
- Immediate asset freeze
- Escalate to legal and compliance teams
- File Suspicious Activity Report (SAR) if required
- Notify law enforcement if criminal activity suspected
- Begin formal investigation process
"""
    }
    
    base_policy = policies.get(risk_level, policies["low"])
    
    # Add pattern-specific guidance
    if any(p.get('pattern_type') == 'repeat_offender' for p in patterns):
        base_policy += "\n\n⚠️ REPEAT OFFENDER PROTOCOL: Previous violations on record. Apply strictest interpretation of policy."
    
    if any(p.get('pattern_type') == 'wash_trading' for p in patterns):
        base_policy += "\n\n⚠️ WASH TRADING PROTOCOL: Evidence of market manipulation. Consider permanent ban."
    
    return base_policy.strip()


def generate_recommendation_with_llm(
    entity_id: str,
    risk_score: float,
    narrative: str,
    policy_guidance: str
) -> Dict[str, Any]:
    """
    Generate final recommendation using LLM.
    
    Args:
        entity_id: Entity being investigated
        risk_score: Risk score
        narrative: Investigation narrative
        policy_guidance: Relevant policy sections
        
    Returns:
        Recommendation dictionary
    """
    llm = Config.get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior compliance officer making final decisions on risk cases.
Your decisions must:
- Be based strictly on evidence and policy
- Include clear justification
- Specify concrete next steps
- Consider regulatory compliance
- Balance risk mitigation with customer experience
"""),
        ("user", """Review the following investigation and provide your final recommendation.

INVESTIGATION NARRATIVE:
{narrative}

RISK SCORE: {risk_score}/100

APPLICABLE POLICY:
{policy_guidance}

Provide your decision in the following format:
1. DECISION: [Approve/Monitor/Soft-ban/Full Suspension]
2. CONFIDENCE: [0-100%]
3. JUSTIFICATION: [2-3 sentences citing specific evidence and policy]
4. NEXT STEPS: [Specific actions to be taken]
5. ESCALATION: [Yes/No - whether this requires senior review]
""")
    ])
    
    inputs = {
        "narrative": narrative,
        "risk_score": f"{risk_score:.1f}",
        "policy_guidance": policy_guidance
    }
    
    chain = prompt | llm
    response = chain.invoke(inputs)
    
    # Parse response into structured format
    return {
        "entity_id": entity_id,
        "decision": Config.get_recommended_action(risk_score),
        "risk_score": risk_score,
        "risk_level": Config.get_risk_level(risk_score),
        "llm_analysis": response.content,
        "confidence": 85,  # Could be extracted from LLM response
        "policy_citations": policy_guidance,
        "requires_escalation": risk_score > Config.RISK_THRESHOLD_HIGH
    }


def generate_recommendation_fallback(
    entity_id: str,
    risk_score: float,
    patterns: list,
    policy_guidance: str
) -> Dict[str, Any]:
    """
    Generate recommendation without LLM (fallback).
    
    Args:
        entity_id: Entity being investigated
        risk_score: Risk score
        patterns: Detected patterns
        policy_guidance: Policy guidance
        
    Returns:
        Recommendation dictionary
    """
    decision = Config.get_recommended_action(risk_score)
    risk_level = Config.get_risk_level(risk_score)
    
    # Generate justification
    justification_parts = []
    justification_parts.append(f"Risk score of {risk_score:.1f}/100 falls in the {risk_level} risk category.")
    
    if patterns:
        high_severity = [p for p in patterns if p.get('severity') in ['high', 'critical']]
        if high_severity:
            pattern_types = ', '.join(p['pattern_type'] for p in high_severity)
            justification_parts.append(f"Critical patterns detected: {pattern_types}.")
    
    justification_parts.append(f"Action taken in accordance with risk management policy section 2.")
    
    # Determine next steps
    next_steps = []
    if risk_level == "low":
        next_steps = [
            "Continue standard monitoring",
            "Schedule routine review in 30 days",
"No immediate action required"
        ]
    elif risk_level == "medium":
        next_steps = [
            "Implement enhanced monitoring",
            "Apply transaction velocity limits",
            "Schedule review in 14 days"
        ]
    elif risk_level == "high":
        next_steps = [
            "Apply soft-ban restrictions",
            "Require manual approval for transactions over $100",
            "Escalate to senior compliance officer",
            "Schedule review within 48 hours"
        ]
    else:  # critical
        next_steps = [
            "Suspend account immediately",
            "Freeze all assets",
            "File Suspicious Activity Report (SAR)",
            "Escalate to legal and compliance teams",
            "Consider law enforcement notification"
        ]
    
    return {
        "entity_id": entity_id,
        "decision": decision,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "justification": " ".join(justification_parts),
        "next_steps": next_steps,
        "policy_citations": policy_guidance,
        "confidence": 80,
        "requires_escalation": risk_score > Config.RISK_THRESHOLD_HIGH,
        "timestamp": None
    }


def decision_agent(state: InvestigationState) -> InvestigationState:
    """
    Recommendation and Review Agent.
    
    Makes final decision based on investigation findings and policy.
    
    Args:
        state: Current investigation state with all analysis complete
        
    Returns:
        Updated state with final recommendation
    """
    print(f"\n{'='*60}")
    print(f"NODE 4: RECOMMENDATION AND REVIEW")
    print(f"{'='*60}")
    
    entity_id = state['entity_id']
    risk_score = state.get('risk_score', 0)
    narrative = state.get('narrative', '')
    patterns = state.get('detected_patterns', [])
    
    print("\n⚖️  Reviewing policy requirements...")
    policy_guidance = get_policy_guidance(risk_score, patterns)
    
    print("⚖️  Generating final recommendation...")
    
    # Try to use LLM, fall back to rule-based if needed
    try:
        if Config.has_api_key():
            recommendation = generate_recommendation_with_llm(
                entity_id, risk_score, narrative, policy_guidance
            )
            print(f"   Using {Config.LLM_PROVIDER.upper()} LLM-enhanced decision making")
        else:
            recommendation = generate_recommendation_fallback(
                entity_id, risk_score, patterns, policy_guidance
            )
            print("   Using rule-based decision making (no API key configured)")
    except Exception as e:
        print(f"   ⚠️  LLM decision failed: {str(e)}")
        print("   Falling back to rule-based decision making")
        recommendation = generate_recommendation_fallback(
            entity_id, risk_score, patterns, policy_guidance
        )
    
    # Update state
    state['recommendation'] = recommendation
    
    # Update metadata
    if state.get('metadata'):
        state['metadata']['decision_timestamp'] = 'now'
        state['metadata']['final_risk_level'] = recommendation.get('risk_level')
    
    print(f"\n✅ Decision complete")
    print(f"   FINAL DECISION: {recommendation.get('decision')}")
    print(f"   Risk Level: {recommendation.get('risk_level', '').upper()}")
    print(f"   Confidence: {recommendation.get('confidence', 0)}%")
    print(f"   Requires Escalation: {'Yes' if recommendation.get('requires_escalation') else 'No'}")
    
    return state
