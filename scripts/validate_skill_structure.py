#!/usr/bin/env python3
"""
Validate AWS Solutions Architect Skill structure.

Checks:
1. SKILL.md exists at root
2. All referenced files in SKILL.md exist
3. references/ directory contains expected files
4. assets/ directory contains expected templates
5. scripts/ directory contains expected validators
"""

import sys
from pathlib import Path

SKILL_REQUIRED_FRONTFIELDS = ["name", "description"]
REFERENCES_DIR = Path("references")
ASSETS_DIR = Path("assets")
SCRIPTS_DIR = Path("scripts")

REQUIRED_REFERENCE_FILES = [
    "discovery-questions-enhanced.md",
    "well-architected-pillars.md",
    "service-decisions-enhanced.md",
    "service-comparisons.md",
    "migration-patterns.md",
    "architecture-patterns.md",
    "compliance-framework.md",
]

REQUIRED_ASSET_FILES = [
    "ADR_TEMPLATE.md",
    "WAF_REVIEW_REPORT_TEMPLATE.md",
    "ARCH_DECISION_MATRIX_TEMPLATE.md",
    "DIAGRAM_SPEC_TEMPLATE.md",
    "SERVICE_SELECTION_SCORECARD_TEMPLATE.yml",
]

REQUIRED_SCRIPT_FILES = [
    "validate_skill_structure.py",
    "validate_workflow_outputs.py",
    "generate_arch_review_skeleton.py",
]

def validate_skill_md():
    """Validate SKILL.md exists and has required frontmatter."""
    skill_path = Path("SKILL.md")
    if not skill_path.exists():
        return False, "SKILL.md not found at root"
    
    content = skill_path.read_text()
    if not content.startswith("---"):
        return False, "SKILL.md missing YAML frontmatter"
    
    # Parse frontmatter
    lines = content.split("\n")
    in_frontmatter = False
    frontmatter_content = []
    for line in lines:
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                break
        if in_frontmatter:
            frontmatter_content.append(line)
    
    frontmatter = "\n".join(frontmatter_content)
    for field in SKILL_REQUIRED_FRONTFIELDS:
        if f"{field}:" not in frontmatter:
            return False, f"SKILL.md missing {field} in frontmatter"
    
    return True, "SKILL.md valid"

def validate_references():
    """Validate all required reference files exist."""
    missing = []
    for ref_file in REQUIRED_REFERENCE_FILES:
        if not (REFERENCES_DIR / ref_file).exists():
            missing.append(str(REFERENCES_DIR / ref_file))
    
    if missing:
        return False, f"Missing reference files: {', '.join(missing)}"
    return True, f"All {len(REQUIRED_REFERENCE_FILES)} reference files present"

def validate_assets():
    """Validate all required asset templates exist."""
    missing = []
    for asset_file in REQUIRED_ASSET_FILES:
        if not (ASSETS_DIR / asset_file).exists():
            missing.append(str(ASSETS_DIR / asset_file))
    
    if missing:
        return False, f"Missing asset files: {', '.join(missing)}"
    return True, f"All {len(REQUIRED_ASSET_FILES)} asset templates present"

def validate_scripts():
    """Validate all required scripts exist."""
    missing = []
    for script_file in REQUIRED_SCRIPT_FILES:
        if not (SCRIPTS_DIR / script_file).exists():
            missing.append(str(SCRIPTS_DIR / script_file))
    
    if missing:
        return False, f"Missing scripts: {', '.join(missing)}"
    return True, f"All {len(REQUIRED_SCRIPT_FILES)} scripts present"

def validate_references_in_skill():
    """Validate all file references in SKILL.md point to existing files."""
    skill_content = Path("SKILL.md").read_text()
    import re
    # Match markdown links like [text](references/file.md)
    references = re.findall(r"\[([^\]]+)\]\((references/[^)]+)\.md\)", skill_content)
    
    missing = []
    for text, ref in references:
        ref_path = Path(ref + ".md")
        if not ref_path.exists():
            missing.append(ref + ".md")
    
    if missing:
        return False, f"Broken references in SKILL.md: {', '.join(missing)}"
    return True, "All references in SKILL.md are valid"

def main():
    """Run all validations and report results."""
    validators = [
        ("SKILL.md structure", validate_skill_md),
        ("Reference files", validate_references),
        ("Asset templates", validate_assets),
        ("Validation scripts", validate_scripts),
        ("SKILL.md references", validate_references_in_skill),
    ]
    
    all_passed = True
    for name, validator in validators:
        try:
            passed, message = validator()
            status = "PASS" if passed else "FAIL"
            print(f"{status}: {name} - {message}")
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"ERROR: {name} - {str(e)}")
            all_passed = False
    
    if all_passed:
        print()
        print("All validations passed!")
        return 0
    else:
        print()
        print("Some validations failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
