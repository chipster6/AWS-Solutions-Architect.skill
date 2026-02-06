#!/usr/bin/env python3
"""
Validate that workflow execution produced required outputs.

This script checks that a skill run produced all expected artifacts
with the correct structure.
"""

import sys
from pathlib import Path
from datetime import datetime

OUTPUT_ARTIFACTS = {
    "discovery": {
        "required_fields": [
            "business_context",
            "technical_requirements", 
            "constraints",
            "success_metrics"
        ],
        "filename_pattern": "discovery-output-*.md"
    },
    "architecture": {
        "required_fields": [
            "components",
            "data_flow",
            "service_selections",
            "well_architected_review"
        ],
        "filename_pattern": "architecture-rec-*.md"
    },
    "waf_review": {
        "required_fields": [
            "operational_excellence",
            "security",
            "reliability",
            "performance_efficiency",
            "cost_optimization",
            "sustainability"
        ],
        "filename_pattern": "waf-review-*.md"
    },
    "decision_matrix": {
        "required_fields": [
            "options_evaluated",
            "criteria_weights",
            "scores",
            "recommendation"
        ],
        "filename_pattern": "decision-matrix-*.md"
    },
    "migration_plan": {
        "required_fields": [
            "current_state",
            "migration_strategy",
            "phase_roadmap",
            "rollback_procedures"
        ],
        "filename_pattern": "migration-plan-*.md"
    }
}

def validate_output_file(filepath, artifact_type):
    """Validate a single output file has required structure."""
    content = Path(filepath).read_text()
    artifact_config = OUTPUT_ARTIFACTS[artifact_type]
    
    missing_fields = []
    for field in artifact_config["required_fields"]:
        if field.lower() not in content.lower():
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, f"Valid {artifact_type} output"

def main():
    """Validate workflow outputs in current directory."""
    output_dir = Path(".")
    
    print("Validating workflow outputs...")
    
    all_passed = True
    for artifact_type, config in OUTPUT_ARTIFACTS.items():
        pattern = config["filename_pattern"]
        files = list(output_dir.glob(pattern))
        
        if not files:
            print(f"FAIL: {artifact_type} - No output file found matching {pattern}")
            all_passed = False
            continue
        
        for filepath in files:
            passed, message = validate_output_file(filepath, artifact_type)
            status = "PASS" if passed else "FAIL"
            print(f"{status}: {filepath.name} - {message}")
            if not passed:
                all_passed = False
    
    if all_passed:
        print()
        print("All workflow outputs validated!")
        return 0
    else:
        print()
        print("Some outputs failed validation")
        return 1

if __name__ == "__main__":
    sys.exit(main())
