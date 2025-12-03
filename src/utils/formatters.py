"""
Output formatting utilities for investigation reports.
"""

from typing import Dict, Any
import json
from datetime import datetime


def format_terminal_report(final_state: Dict[str, Any]) -> str:
    """
    Format investigation results for terminal display.
    
    Args:
        final_state: Final investigation state
        
    Returns:
        Formatted string for terminal output
    """
    entity_id = final_state.get('entity_id', 'N/A')
    risk_score = final_state.get('risk_score', 0)
    patterns = final_state.get('detected_patterns', [])
    narrative = final_state.get('narrative', '')
    recommendation = final_state.get('recommendation', {})
    
    output = f"""
{'='*70}
INVESTIGATION REPORT
{'='*70}

Entity ID: {entity_id}
Investigation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*70}
RISK ASSESSMENT
{'='*70}

Risk Score: {risk_score:.1f}/100
Risk Level: {recommendation.get('risk_level', 'N/A').upper()}
Patterns Detected: {len(patterns)}

Detected Patterns:
"""
    
    if patterns:
        for i, pattern in enumerate(patterns, 1):
            output += f"\n  {i}. {pattern['pattern_type'].replace('_', ' ').title()}"
            output += f"\n     Severity: {pattern['severity'].upper()}"
            output += f"\n     {pattern['description']}\n"
    else:
        output += "\n  No suspicious patterns detected\n"
    
    output += f"""
{'='*70}
INVESTIGATION NARRATIVE
{'='*70}

{narrative}

{'='*70}
FINAL RECOMMENDATION
{'='*70}

Decision: {recommendation.get('decision', 'N/A').upper()}
Confidence: {recommendation.get('confidence', 0)}%
Requires Escalation: {'YES' if recommendation.get('requires_escalation') else 'NO'}

"""
    
    if 'justification' in recommendation:
        output += f"Justification:\n{recommendation['justification']}\n\n"
    
    if 'next_steps' in recommendation:
        output += "Next Steps:\n"
        for step in recommendation['next_steps']:
            output += f"  • {step}\n"
    
    output += f"\n{'='*70}\n"
    
    return output


def save_json_report(final_state: Dict[str, Any], filepath: str):
    """
    Save investigation report as JSON.
    
    Args:
        final_state: Final investigation state
        filepath: Path to save JSON file
    """
    report = {
        "investigation_metadata": {
            "entity_id": final_state.get('entity_id'),
            "entity_type": final_state.get('entity_type'),
            "timestamp": datetime.now().isoformat(),
        },
        "risk_assessment": {
            "risk_score": final_state.get('risk_score'),
            "risk_level": final_state.get('recommendation', {}).get('risk_level'),
            "detected_patterns": final_state.get('detected_patterns', [])
        },
        "narrative": final_state.get('narrative'),
        "recommendation": final_state.get('recommendation'),
        "raw_data_summary": {
            "profile": final_state.get('raw_data', {}).get('profile', {}),
            "transaction_count": final_state.get('raw_data', {}).get('transactions', {}).get('total_transactions'),
            "flag_count": final_state.get('raw_data', {}).get('flags', {}).get('total_flags')
        }
    }
    
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=2, default=str)


def save_markdown_report(final_state: Dict[str, Any], filepath: str):
    """
    Save investigation report as Markdown.
    
    Args:
        final_state: Final investigation state
        filepath: Path to save Markdown file
    """
    entity_id = final_state.get('entity_id', 'N/A')
    risk_score = final_state.get('risk_score', 0)
    patterns = final_state.get('detected_patterns', [])
    narrative = final_state.get('narrative', '')
    recommendation = final_state.get('recommendation', {})
    
    md_content = f"""# Investigation Report: {entity_id}

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

- **Entity ID:** {entity_id}
- **Risk Score:** {risk_score:.1f}/100
- **Risk Level:** {recommendation.get('risk_level', 'N/A').upper()}
- **Decision:** {recommendation.get('decision', 'N/A').upper()}
- **Patterns Detected:** {len(patterns)}

## Risk Assessment

### Detected Patterns

"""
    
    if patterns:
        for pattern in patterns:
            md_content += f"""
#### {pattern['pattern_type'].replace('_', ' ').title()}
- **Severity:** {pattern['severity'].upper()}
- **Description:** {pattern['description']}
- **Evidence:** {pattern.get('evidence', {})}

"""
    else:
        md_content += "No suspicious patterns detected.\n\n"
    
    md_content += f"""
## Investigation Narrative

{narrative}

## Final Recommendation

**Decision:** {recommendation.get('decision', 'N/A').upper()}  
**Confidence:** {recommendation.get('confidence', 0)}%  
**Requires Escalation:** {'Yes' if recommendation.get('requires_escalation') else 'No'}

### Justification

{recommendation.get('justification', 'N/A')}

### Next Steps

"""
    
    if 'next_steps' in recommendation:
        for step in recommendation['next_steps']:
            md_content += f"- {step}\n"
    
    md_content += "\n---\n\n*This report was generated automatically by the High-Risk Investigation Agent.*\n"
    
    with open(filepath, 'w') as f:
        f.write(md_content)
