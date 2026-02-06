# Well-Architected Framework Pillars Reference

**Document ID:** workflow-review  
**Index:** [GOV-ARCH-001](../GOV-ARCH-001-Architecture-Documentation-Index.md)  
**Router:** [docs/workflows/review.md](../docs/workflows/review.md)  
**Related:** [discovery-questions-enhanced.md](discovery-questions-enhanced.md), [architecture-patterns.md](architecture-patterns.md), [CROSS_REFERENCE_INDEX.md](../CROSS_REFERENCE_INDEX.md)

## Purpose

This reference provides guidance on conducting Well-Architected Framework reviews across all 6 pillars. For detailed, current best practices, always consult AWS documentation via MCP before conducting reviews.

### Related Documents
- **[Discovery Process](discovery-questions-enhanced.md)** - Use discovery questions before conducting reviews
- **[Architecture Patterns](architecture-patterns.md)** - Review patterns against Well-Architected principles
- **[Service Decisions](service-decisions-enhanced.md)** - Validate service selections against pillars
- **[Compliance Framework](compliance-framework.md)** - Security pillar alignment with compliance
- **[Cross-Reference Index](../CROSS_REFERENCE_INDEX.md)** - Navigate by pillar and topic

## The 6 Pillars

### 1. Operational Excellence (OPS)

**Focus**: Run and monitor systems to deliver business value and continually improve

**Key Areas to Review**:
- **Organization**: How teams are structured and empowered
- **Prepare**: Design for operations, implement observability
- **Operate**: Understand workload health, respond to events
- **Evolve**: Learn from experience, share knowledge

**Design Principles**:
- Organize teams around business outcomes
- Implement observability for actionable insights
- Safely automate where possible
- Make frequent, small, reversible changes
- Refine operations procedures frequently
- Anticipate failure
- Learn from all operational events

**Questions to Ask**:
- How do you determine workload health?
- How do you understand operational health?
- How do you manage workload and operations events?
- How do you evolve operations?

**MCP Lookup**: Search for "operational excellence best practices"

### 2. Security (SEC)

**Focus**: Protect information, systems, and assets

**Key Areas to Review**:
- **Identity and Access Management**: Who can access what
- **Detection**: Identify security events
- **Infrastructure Protection**: Network and host-level defenses
- **Data Protection**: Encrypt and classify data
- **Incident Response**: Respond to and recover from incidents

**Design Principles**:
- Implement strong identity foundation
- Enable traceability
- Apply security at all layers
- Automate security best practices
- Protect data in transit and at rest
- Keep people away from data
- Prepare for security events

**Questions to Ask**:
- How do you securely operate your workload?
- How do you manage identities for people and machines?
- How do you detect and investigate security events?
- How do you protect your network resources?
- How do you protect your compute resources?
- How do you classify your data?
- How do you protect your data at rest?
- How do you protect your data in transit?
- How do you anticipate, respond to, and recover from incidents?

**MCP Lookup**: Search for "security pillar best practices"

### 3. Reliability (REL)

**Focus**: Workload performs intended function correctly and consistently

**Key Areas to Review**:
- **Foundations**: Network topology, service quotas
- **Workload Architecture**: Service-oriented architecture, distributed system design
- **Change Management**: Monitor workload resources, implement change
- **Failure Management**: Backup, resilience, disaster recovery

**Design Principles**:
- Automatically recover from failure
- Test recovery procedures
- Scale horizontally
- Stop guessing capacity
- Manage change through automation

**Questions to Ask**:
- How do you manage service quotas and constraints?
- How do you plan your network topology?
- How do you design your workload service architecture?
- How do you design interactions to prevent failures?
- How do you design interactions to mitigate failures?
- How do you monitor workload resources?
- How do you design your workload to adapt to changes in demand?
- How do you implement change?
- How do you back up data?
- How do you use fault isolation to protect your workload?
- How do you design your workload to withstand component failures?
- How do you test reliability?
- How do you plan for disaster recovery?

**MCP Lookup**: Search for "reliability pillar best practices"

### 4. Performance Efficiency (PERF)

**Focus**: Use computing resources efficiently

**Key Areas to Review**:
- **Selection**: Choose right resource types and sizes
- **Review**: Ensure architecture remains optimal
- **Monitoring**: Track performance metrics
- **Trade-offs**: Balance consistency, durability, latency, throughput

**Design Principles**:
- Democratize advanced technologies
- Go global in minutes
- Use serverless architectures
- Experiment more often
- Consider mechanical sympathy

**Questions to Ask**:
- How do you select appropriate cloud resources and architecture patterns?
- How do you select your compute solution?
- How do you select your storage solution?
- How do you select your database solution?
- How do you configure your networking solution?
- How do you evolve your workload to take advantage of new releases?
- How do you monitor your resources?
- How do you use tradeoffs to improve performance?

**MCP Lookup**: Search for "performance efficiency best practices"

### 5. Cost Optimization (COST)

**Focus**: Avoid unnecessary costs

**Key Areas to Review**:
- **Practice Cloud Financial Management**: Establish governance
- **Expenditure and Usage Awareness**: Track and attribute costs
- **Cost-Effective Resources**: Use right-sized resources
- **Manage Demand and Supply**: Match supply to demand
- **Optimize Over Time**: Adopt new services and features

**Design Principles**:
- Implement cloud financial management
- Adopt consumption model
- Measure overall efficiency
- Stop spending on undifferentiated heavy lifting
- Analyze and attribute expenditure

**Questions to Ask**:
- How do you implement cloud financial management?
- How do you govern usage?
- How do you monitor usage and cost?
- How do you decommission resources?
- How do you evaluate cost when selecting services?
- How do you meet cost targets with resource type, size, and number?
- How do you use pricing models to reduce cost?
- How do you plan for data transfer charges?
- How do you manage demand and supply resources?
- How do you evaluate new services?

**MCP Lookup**: Search for "cost optimization best practices"

### 6. Sustainability (SUS)

**Focus**: Minimize environmental impact

**Key Areas to Review**:
- **Region Selection**: Choose regions wisely
- **User Behavior Patterns**: Align resources with usage
- **Software and Architecture Patterns**: Optimize code and architecture
- **Data Patterns**: Manage data efficiently
- **Hardware Patterns**: Select efficient hardware
- **Development and Deployment**: Sustainable practices

**Design Principles**:
- Understand your impact
- Establish sustainability goals
- Maximize utilization
- Anticipate and adopt new efficient offerings
- Use managed services
- Reduce downstream impact

**Questions to Ask**:
- How do you select Regions for your workload?
- How do you take advantage of user behavior patterns?
- How do you take advantage of software and architecture patterns?
- How do you take advantage of data access and usage patterns?
- How do you take advantage of hardware and services?
- How do you manage development and deployment processes?

**MCP Lookup**: Search for "sustainability pillar best practices"

## Conducting a Well-Architected Review

### Step 1: Understand Workload Context
- What does the workload do?
- What are the business requirements?
- What is the current architecture?

### Step 2: Select Pillars to Review
- All 6 pillars for comprehensive review
- Specific pillars for targeted assessment
- Prioritize based on business concerns

### Step 3: Ask Pillar-Specific Questions
- Use the questions above as starting point
- Consult AWS documentation MCP for detailed questions
- Adapt questions to workload context

### Step 4: Identify Issues
- **High Risk Issues (HRIs)**: Critical problems that must be addressed
- **Medium Risk Issues (MRIs)**: Important improvements
- **Best Practices Met**: Areas already well-architected

### Step 5: Provide Recommendations
- Prioritize by business impact
- Provide prescriptive solutions
- Include implementation guidance
- Estimate effort and impact

### Step 6: Create Improvement Plan
- Quick wins (low effort, high impact)
- Medium-term improvements
- Long-term optimizations

## Review Report Structure

```
# Well-Architected Review: [Workload Name]

## Executive Summary
- Overall assessment
- Critical issues found
- Key recommendations

## Pillar Assessments

### Operational Excellence
- Issues Found: [HRI count] High, [MRI count] Medium
- Key Findings:
  1. [Issue description]
  2. [Issue description]
- Recommendations:
  1. [Recommendation with priority]
  2. [Recommendation with priority]

[Repeat for each pillar]

## Improvement Plan
- Phase 1 (0-3 months): [Quick wins]
- Phase 2 (3-6 months): [Medium-term]
- Phase 3 (6-12 months): [Long-term]

## Next Steps
[Actions to take]
```

## Using MCP Documentation for Reviews

For each pillar, before conducting review:

1. **Search for current best practices**:
   ```
   MCP_DOCKER:search_documentation "security pillar best practices"
   ```

2. **Read specific guidance**:
   ```
   MCP_DOCKER:read_documentation [URL from search results]
   ```

3. **Get detailed questions**:
   ```
   MCP_DOCKER:search_documentation "[pillar] questions well-architected"
   ```

This ensures recommendations are based on current AWS guidance, not outdated information.

## Common Review Findings by Pillar

### Operational Excellence
- Lack of observability and monitoring
- No automated deployment pipelines
- Missing runbooks and incident response procedures
- No regular operations reviews

### Security
- Overly permissive IAM policies
- No encryption at rest for sensitive data
- Missing MFA for privileged accounts
- No security event logging and monitoring
- Exposed credentials in code

### Reliability
- Single points of failure
- No disaster recovery plan
- No backup strategy
- No health checks or auto-recovery
- Manual scaling processes

### Performance Efficiency
- Over-provisioned resources
- Using wrong service types for workload
- No performance testing
- Not leveraging caching
- Inefficient data access patterns

### Cost Optimization
- Resources running 24/7 when not needed
- No Reserved Instances or Savings Plans
- Oversized instances
- Expensive data transfer patterns
- No cost monitoring or allocation

### Sustainability
- Inefficient resource utilization
- Not using latest generation instances
- Running in carbon-intensive regions
- No consideration of sustainability goals
- Wasteful data storage practices

## Anti-Patterns in Reviews

❌ **Don't**:
- Review without understanding business context
- Focus only on one pillar
- Recommend changes without trade-off analysis
- Provide vague recommendations ("improve security")
- Ignore operational capabilities of team

✅ **Do**:
- Understand business impact of issues
- Balance across all pillars
- Explain trade-offs explicitly
- Provide specific, actionable recommendations
- Consider team's ability to implement changes
