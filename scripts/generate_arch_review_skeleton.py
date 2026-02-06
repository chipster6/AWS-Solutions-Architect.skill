#!/usr/bin/env python3
"""
Generate architecture review skeleton documents.

Creates the initial structure for Well-Architected review outputs
based on templates in assets/.
"""

from pathlib import Path
from datetime import datetime
import argparse

def generate_waf_review_skeleton(workload_name: str, output_dir: Path = Path(".")):
    """Generate a Well-Architected Review Report skeleton."""
    template_path = Path("assets/WAF_REVIEW_REPORT_TEMPLATE.md")
    if not template_path.exists():
        print("ERROR: WAF_REVIEW_REPORT_TEMPLATE.md not found in assets/")
        return None
    
    template_content = template_path.read_text()
    
    # Replace placeholders
    skeleton = template_content.replace("{WORKLOAD_NAME}", workload_name)
    skeleton = skeleton.replace("{YYYY-MM-DD}", datetime.now().strftime("%Y-%m-%d"))
    
    output_path = output_dir / f"waf-review-{workload_name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}.md"
    output_path.write_text(skeleton)
    
    print(f"Generated: {output_path}")
    return output_path

def generate_decision_matrix_skeleton(decision_title: str, output_dir: Path = Path(".")):
    """Generate an Architecture Decision Matrix skeleton."""
    template_path = Path("assets/ARCH_DECISION_MATRIX_TEMPLATE.md")
    if not template_path.exists():
        print("ERROR: ARCH_DECISION_MATRIX_TEMPLATE.md not found in assets/")
        return None
    
    template_content = template_path.read_text()
    
    skeleton = template_content.replace("{DECISION_TITLE}", decision_title)
    skeleton = skeleton.replace("{YYYY-MM-DD}", datetime.now().strftime("%Y-%m-%d"))
    
    output_path = output_dir / f"decision-matrix-{decision_title.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}.md"
    output_path.write_text(skeleton)
    
    print(f"Generated: {output_path}")
    return output_path

def generate_adr_skeleton(decision_title: str, adr_number: int = 1, output_dir: Path = Path(".")):
    """Generate an Architecture Decision Record skeleton."""
    template_path = Path("assets/ADR_TEMPLATE.md")
    if not template_path.exists():
        print("ERROR: ADR_TEMPLATE.md not found in assets/")
        return None
    
    template_content = template_path.read_text()
    
    skeleton = template_content.replace("{TITLE}", decision_title)
    skeleton = skeleton.replace("{YYYY-MM-DD}", datetime.now().strftime("%Y-%m-%d"))
    skeleton = skeleton.replace("{NUMBER}", str(adr_number).zfill(2))
    
    output_path = output_dir / f"ADR-{str(adr_number).zfill(2)}-{decision_title.lower().replace(' ', '-')}.md"
    output_path.write_text(skeleton)
    
    print(f"Generated: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Generate architecture review skeletons")
    parser.add_argument("--workload", "-w", help="Workload name for WAF review")
    parser.add_argument("--decision", "-d", help="Decision title for decision matrix")
    parser.add_argument("--adr", "-a", type=int, help="ADR number for ADR skeleton")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated = False
    
    if args.workload:
        generate_waf_review_skeleton(args.workload, output_dir)
        generated = True
    
    if args.decision:
        generate_decision_matrix_skeleton(args.decision, output_dir)
        generated = True
    
    if args.adr:
        decision_title = f"Decision-{args.adr}"
        generate_adr_skeleton(decision_title, args.adr, output_dir)
        generated = True
    
    if not generated:
        print("Usage: python generate_arch_review_skeleton.py -w <workload> | -d <decision> | -a <adr_number>")

if __name__ == "__main__":
    main()
