"""
Demonstration script showing multiple investigation scenarios.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import run_investigation
from src.utils.formatters import format_terminal_report


def run_demo():
    """Run demonstration with multiple test cases."""
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║          HIGH-RISK INVESTIGATION AGENT - DEMO                        ║
║          Automated Case Analyst                                      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

This demonstration will run investigations on 3 different entities:
1. Low-risk entity (expected: Approve)
2. Medium-risk entity (expected: Monitor)
3. High-risk entity (expected: Soft-ban or Suspension)

The demo uses mock data to simulate various risk scenarios.

Press Enter to start the demonstrations...
""")
    
    input()
    
    # Test cases
    test_cases = [
        ("USER_001", "Low-Risk Entity"),
        ("USER_002", "Medium-Risk Entity"),
        ("USER_003", "High-Risk Entity"),
    ]
    
    results = []
    
    for entity_id, description in test_cases:
        print(f"\n\n{'#'*70}")
        print(f"DEMO CASE: {description}")
        print(f"{'#'*70}\n")
        
        try:
            final_state = run_investigation(entity_id, "user")
            results.append((description, final_state))
            
            # Brief pause between cases
            print("\n" + "="*70)
            print(f"Case complete. Risk Score: {final_state.get('risk_score', 0):.1f}/100")
            print(f"Decision: {final_state.get('recommendation', {}).get('decision', 'N/A')}")
            print("="*70 + "\n")
            
        except Exception as e:
            print(f"❌ Investigation failed for {entity_id}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print(f"\n\n{'#'*70}")
    print("DEMONSTRATION SUMMARY")
    print(f"{'#'*70}\n")
    
    for description, state in results:
        recommendation = state.get('recommendation', {})
        print(f"• {description}")
        print(f"  Risk Score: {state.get('risk_score', 0):.1f}/100")
        print(f"  Decision: {recommendation.get('decision', 'N/A')}")
        print(f"  Patterns Detected: {len(state.get('detected_patterns', []))}")
        print()
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║          DEMONSTRATION COMPLETE                                      ║
║                                                                      ║
║  The High-Risk Investigation Agent successfully processed all test  ║
║  cases and provided actionable recommendations for each entity.     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

To run a custom investigation, use:
  python src/main.py --entity-id YOUR_ENTITY_ID --entity-type user

For more options:
  python src/main.py --help
""")


if __name__ == "__main__":
    run_demo()
