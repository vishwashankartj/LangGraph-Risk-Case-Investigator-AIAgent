"""
Main entry point for the High-Risk Investigation Agent.
"""

import argparse
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import run_investigation
from src.utils.formatters import format_terminal_report, save_json_report, save_markdown_report


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="High-Risk Investigation Agent - Automated Case Analyst"
    )
    parser.add_argument(
        "--entity-id",
        type=str,
        required=True,
        help="ID of the entity to investigate"
    )
    parser.add_argument(
        "--entity-type",
        type=str,
        default="user",
        choices=["user", "transaction", "account"],
        help="Type of entity to investigate"
    )
    parser.add_argument(
        "--output-json",
        type=str,
        help="Path to save JSON report"
    )
    parser.add_argument(
        "--output-md",
        type=str,
        help="Path to save Markdown report"
    )
    
    args = parser.parse_args()
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║          HIGH-RISK INVESTIGATION AGENT                               ║
║          Automated Case Analyst                                      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

Starting investigation for entity: {args.entity_id}
Entity type: {args.entity_type}
""")
    
    try:
        # Run investigation
        final_state = run_investigation(args.entity_id, args.entity_type)
        
        # Display results
        print(format_terminal_report(final_state))
        
        # Save reports if requested
        if args.output_json:
            save_json_report(final_state, args.output_json)
            print(f"✅ JSON report saved to: {args.output_json}")
        
        if args.output_md:
            save_markdown_report(final_state, args.output_md)
            print(f"✅ Markdown report saved to: {args.output_md}")
        
        # Exit with appropriate code based on decision
        recommendation = final_state.get('recommendation', {})
        if recommendation.get('requires_escalation'):
            print("\n⚠️  This case requires escalation to senior compliance officer.")
            sys.exit(2)
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Investigation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
