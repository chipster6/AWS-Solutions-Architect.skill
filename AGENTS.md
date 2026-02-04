# AWS Well-Architected Agent Skill Repository

This repository contains the source content for the `aws-solution-architect` agent skill, providing decision frameworks, patterns, and workflows aligned with AWS's 6 Well-Architected Pillars:

1. **Operational Excellence** - Run and monitor systems to deliver business value
2. **Security** - Protect information and systems
3. **Reliability** - Ensure systems recover from failures and meet demand
4. **Performance Efficiency** - Use resources efficiently to meet requirements
5. **Cost Optimization** - Avoid unnecessary costs
6. **Sustainability** - Minimize environmental impacts

## Skill Overview

The skill gives agents precise decision frameworks and domain knowledge to create well-architected AWS solutions. It covers:

- **Discovery Process** - Systematic requirements gathering with Well-Architected integration
- **Architecture Reviews** - Assessment against the 6 pillars
- **Service Decisions** - Decision trees for choosing between AWS services
- **Migration Planning** - 6 R's migration strategies
- **Cost Optimization** - Real-time estimation and optimization
- **Compliance** - Regulatory requirement mapping

## Build/Lint/Test Commands

### Python (Validation)
```bash
# Validate documentation registry sync
python scripts/validate_docs.py

# Run with explicit Python 3
python3 scripts/validate_docs.py

# Use virtual environment
source .venv/bin/activate && python scripts/validate_docs.py
```

### Bun/Node.js (OpenCode Plugins)
```bash
# Install skill dependencies
bun install

# Update plugins
bun update
```

## Code Style Guidelines

### Python (Validation Scripts)
- **Type hints**: Use `from __future__ import annotations` with full type annotations
- **Imports**: Standard library → third-party → local; prefer `pathlib` over `os.path`
- **Naming**: snake_case (functions/variables), PascalCase (classes), UPPER_CASE (constants)
- **Functions**: Docstrings for public functions, type hints for all parameters/returns
- **Error handling**: Use specific exceptions, `raise SystemExit` for CLI errors, collect errors in lists
- **Formatting**: 4-space indentation, 88 character line length, double quotes for strings
- **Strings**: f-strings for interpolation

### Markdown (Documentation)
- **Headers**: ATX style (#) with hierarchical structure (h1 → h2 → h3)
- **Frontmatter**: Required for router files with `title`, `source`, `type`, `description`
- **Links**: Relative paths with `.md` extension, include line numbers for precision
- **Code blocks**: Always specify language for syntax highlighting
- **Lists**: Dashes (-) for unordered lists with consistent indentation

### YAML (Registry)
- **Indentation**: 2 spaces
- **Quotes**: Quote strings with special characters only
- **Structure**: Group entries under descriptive category keys

## Repository Structure

```
/
├── docs/                    # Router files (skill entry points)
│   ├── index.md            # Main navigation hub
│   ├── workflows/          # Discovery, Review, Decisions, Migration
│   ├── patterns/           # Architecture, Compliance, Migration, Services
│   ├── tools/              # Cost Estimator, Team Assessment, etc.
│   └── reference/          # Well-Architected, Decision Trees, Best Practices
├── files/                  # Canonical content (decision frameworks)
│   ├── discovery-questions-enhanced.md
│   ├── well-architected-pillars.md
│   ├── service-decisions-enhanced.md
│   ├── migration-patterns.md
│   ├── architecture-patterns.md
│   └── compliance-framework.md
├── tools/                  # Interactive tool documentation
│   ├── cost-estimator.md
│   ├── team-assessment.md
│   └── implementation-guide.md
├── scripts/                # Validation and utilities
│   ├── validate_docs.py    # Registry validator
│   └── workflow_registry.yaml  # Source of truth
└── .opencode/              # OpenCode plugin configuration
```

## Skill Usage Patterns

### For Architecture Design
Agents should follow this workflow:

1. **Discovery** → Use `files/discovery-questions-enhanced.md`
   - Gather business context, technical requirements, constraints
   - Extract industry, scale, compliance needs, success metrics

2. **Service Selection** → Use `files/service-decisions-enhanced.md`
   - Apply decision trees for compute, storage, database, messaging
   - Consider trade-offs: cost vs performance, managed vs self-hosted

3. **Architecture Review** → Use `files/well-architected-pillars.md`
   - Validate against 6 pillars
   - Identify risks and improvement opportunities

4. **Pattern Matching** → Use `files/architecture-patterns.md`
   - Match requirements to proven patterns (serverless, microservices, 3-tier)
   - Apply appropriate anti-patterns avoidance

### For Migration Projects
1. **Assessment** → Use `files/migration-patterns.md`
   - Apply 6 R's framework (Rehost, Replatform, Repurchase, Refactor, Retire, Retain)
   - Evaluate migration complexity and risk

2. **Planning** → Use `files/discovery-questions-enhanced.md` Phase 4
   - Define migration waves, rollback procedures
   - Establish success criteria

### For Compliance Requirements
1. **Framework Mapping** → Use `files/compliance-framework.md`
   - Map regulatory requirements (GDPR, HIPAA, SOC2, PCI-DSS)
   - Identify compliant service selections

### For Cost Optimization
1. **Estimation** → Reference `tools/cost-estimator.md`
2. **Optimization** → Apply patterns from `files/architecture-patterns.md`
   - Right-sizing, reserved capacity, lifecycle policies

## Content Maintenance

### Adding New Decision Frameworks

```bash
# 1. Add to registry
echo "  new-framework:
    router: docs/category/new-framework.md
    canonical: files/new-framework.md" >> scripts/workflow_registry.yaml

# 2. Create router file with frontmatter:
# ---
# title: framework-name
# source: ../../files/new-framework.md
# type: pattern|workflow|tool|reference
# description: Brief description
# ---

# 3. Create canonical content in files/
# 4. Update docs/index.md with navigation link
# 5. Validate
python scripts/validate_docs.py
```

### Registry Validation
Always run validation after content changes:
```bash
python scripts/validate_docs.py
```

Checks:
- Router files exist and reference correct canonical sources
- Canonical files exist
- docs/index.md contains navigation links

## Common Tasks

### Running Tests (if added)
```bash
# Install pytest if needed
pip install pytest

# Run specific test
pytest tests/test_validate_docs.py::test_function_name -v

# Run test module
pytest tests/test_validate_docs.py -v
```

### Updating Skill Content
1. Edit canonical files in `files/` or `tools/`
2. Update router metadata if needed
3. Run validation: `python scripts/validate_docs.py`
4. Commit with message format: `type: description`
   - `docs: add migration patterns`
   - `fix: update service decision tree`
   - `refactor: reorganize compliance framework`

## Dependencies

### Python (.venv)
- PyYAML for registry parsing
- Install additional packages as needed

### Bun/Node.js
- `@opencode-ai/plugin`: Agent framework integration
- `@kilocode/plugin`: Additional agent capabilities

## Key Principles

### Decision Framework Quality
- **Specificity**: Provide concrete criteria, not vague guidance
- **Context-aware**: Include industry, scale, and compliance considerations
- **Trade-off clarity**: Explicitly state pros/cons of each option
- **Actionable**: Give clear next steps, not just theory

### Documentation Standards
- **Router files**: Minimal, just frontmatter + links to canonical
- **Canonical files**: Comprehensive, detailed, decision-oriented
- **Line number references**: Enable precise agent navigation
- **Consistent terminology**: Align with AWS documentation

### Skill Integration
- This repo's content is consumed by `~/.config/opencode/skills/aws-solution-architect/`
- Changes here affect how agents design architectures
- Test skill behavior after significant content updates
