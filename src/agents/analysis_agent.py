"""
Node 2: Risk Scoring and Pattern Detection Agent

This agent analyzes the gathered data to calculate a risk score and
detect known high-risk patterns.
"""

from typing import Dict, Any, List
from datetime import datetime
from src.state import InvestigationState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.config import Config


def calculate_base_risk_score(raw_data: Dict[str, Any]) -> float:
    """
    Calculate base risk score using heuristics.
    
    Args:
        raw_data: Comprehensive data package
        
    Returns:
        Risk score from 0-100
    """
    score = 0.0
    
    profile = raw_data.get('profile', {})
    activity = raw_data.get('activity', {})
    flags = raw_data.get('flags', {})
    transactions = raw_data.get('transactions', {})
    
    # Account age risk (newer accounts = higher risk)
    account_age_days = profile.get('account_age_days', 365)
    if account_age_days < 30:
        score += 20
    elif account_age_days < 90:
        score += 10
    
    # Verification status
    if not profile.get('kyc_completed', True):
        score += 15
    
    # VPN usage
    if activity.get('vpn_usage_detected', False):
        score += 10
    
    # Geographic spread (multiple countries = suspicious)
    if activity.get('geographic_spread', 1) > 3:
        score += 15
    
    # Past flags
    total_flags = flags.get('total_flags', 0)
    score += min(total_flags * 10, 30)  # Cap at 30
    
    # Transaction velocity
    last_24h_transactions = transactions.get('last_24h_transactions', 0)
    if last_24h_transactions > 20:
        score += 20
    elif last_24h_transactions > 10:
        score += 10
    
    # Cash-out ratio (high cash-out activity is suspicious)
    cash_out_ratio = transactions.get('cash_out_ratio', 0)
    if cash_out_ratio > 0.5:
        score += 15
    
    return min(score, 100)  # Cap at 100


def detect_patterns(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detect known high-risk patterns in the data.
    
    Args:
        raw_data: Comprehensive data package
        
    Returns:
        List of detected patterns with descriptions
    """
    patterns = []
    
    activity = raw_data.get('activity', {})
    transactions = raw_data.get('transactions', {})
    flags = raw_data.get('flags', {})
    connections = raw_data.get('connections', {})
    
    # Pattern 1: Wash Trading Detection
    recent_transactions = transactions.get('recent_transactions', [])
    gift_sent = [t for t in recent_transactions if t.get('type') == 'gift_sent']
    gift_received = [t for t in recent_transactions if t.get('type') == 'gift_received']
    
    if len(gift_sent) > 5 and len(gift_received) > 5:
        patterns.append({
            "pattern_type": "wash_trading",
            "severity": "high",
            "description": f"Circular gifting pattern detected: {len(gift_sent)} gifts sent, {len(gift_received)} received",
            "evidence": {
                "gifts_sent": len(gift_sent),
                "gifts_received": len(gift_received)
            }
        })
    
    # Pattern 2: Rapid Follow/Unfollow
    follows = connections.get('follows', 0)
    followers = connections.get('followers', 0)
    
    if follows > 500 and followers < 50:
        patterns.append({
            "pattern_type": "rapid_follow_unfollow",
            "severity": "medium",
            "description": f"Asymmetric follow pattern: {follows} following, {followers} followers",
            "evidence": {
                "follows": follows,
                "followers": followers,
                "ratio": round(follows / max(followers, 1), 2)
            }
        })
    
    # Pattern 3: Sudden Cash-Out
    cash_out_transactions = [t for t in recent_transactions if t.get('type') == 'cash_out']
    if cash_out_transactions:
        total_cash_out = sum(t.get('amount', 0) for t in cash_out_transactions)
        if total_cash_out > 1000:
            patterns.append({
                "pattern_type": "sudden_cash_out",
                "severity": "high",
                "description": f"High-value cash-out detected: ${total_cash_out:.2f}",
                "evidence": {
                    "total_amount": total_cash_out,
                    "num_transactions": len(cash_out_transactions)
                }
            })
    
    # Pattern 4: VPN/Proxy Usage with High-Value Activity
    if activity.get('vpn_usage_detected') and transactions.get('last_24h_volume_usd', 0) > 500:
        patterns.append({
            "pattern_type": "vpn_with_high_value",
            "severity": "medium",
            "description": "VPN usage combined with high-value transactions",
            "evidence": {
                "vpn_detected": True,
                "24h_volume": transactions.get('last_24h_volume_usd')
            }
        })
    
    # Pattern 5: Multi-Account Coordination
    linked_accounts = connections.get('linked_accounts', [])
    high_confidence_links = [acc for acc in linked_accounts if acc.get('confidence', 0) > 0.8]
    
    if len(high_confidence_links) > 2:
        patterns.append({
            "pattern_type": "multi_account_coordination",
            "severity": "high",
            "description": f"Multiple linked accounts detected: {len(high_confidence_links)} high-confidence connections",
            "evidence": {
                "total_connections": len(linked_accounts),
                "high_confidence": len(high_confidence_links),
                "relationships": [acc.get('relationship') for acc in high_confidence_links]
            }
        })
    
    # Pattern 6: Repeat Offender
    past_flags = flags.get('past_flags', [])
    high_severity_flags = [f for f in past_flags if f.get('severity') == 'high']
    
    if len(high_severity_flags) >= 2:
        patterns.append({
            "pattern_type": "repeat_offender",
            "severity": "critical",
            "description": f"Multiple high-severity flags in history: {len(high_severity_flags)} incidents",
            "evidence": {
                "total_flags": flags.get('total_flags'),
                "high_severity_count": len(high_severity_flags),
                "flag_types": [f.get('flag_type') for f in high_severity_flags]
            }
        })
    
    return patterns


def analysis_agent(state: InvestigationState) -> InvestigationState:
    """
    Risk Scoring and Pattern Detection Agent.
    
    Analyzes the data package to calculate risk score and detect patterns.
    
    Args:
        state: Current investigation state with raw_data
        
    Returns:
        Updated state with risk_score and detected_patterns
    """
    print(f"\n{'='*60}")
    print(f"NODE 2: RISK SCORING AND PATTERN DETECTION")
    print(f"{'='*60}")
    
    raw_data = state.get('raw_data', {})
    
    # Calculate base risk score
    print("\n🔍 Calculating risk score...")
    base_score = calculate_base_risk_score(raw_data)
    
    # Detect patterns
    print("🔍 Detecting suspicious patterns...")
    patterns = detect_patterns(raw_data)
    
    # Adjust score based on patterns
    pattern_adjustment = 0
    for pattern in patterns:
        severity = pattern.get('severity', 'low')
        if severity == 'critical':
            pattern_adjustment += 15
        elif severity == 'high':
            pattern_adjustment += 10
        elif severity == 'medium':
            pattern_adjustment += 5
        else:
            pattern_adjustment += 2
    
    final_score = min(base_score + pattern_adjustment, 100)
    
    # Update state
    state['risk_score'] = final_score
    state['detected_patterns'] = patterns
    
    print(f"\n✅ Risk analysis complete")
    print(f"   Base risk score: {base_score:.1f}")
    print(f"   Pattern adjustment: +{pattern_adjustment:.1f}")
    print(f"   FINAL RISK SCORE: {final_score:.1f}/100")
    print(f"   Patterns detected: {len(patterns)}")
    
    if patterns:
        print("\n   Detected patterns:")
        for pattern in patterns:
            print(f"   - {pattern['pattern_type']} ({pattern['severity']}): {pattern['description']}")
    
    return state
