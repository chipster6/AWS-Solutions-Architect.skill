# Enhanced Discovery Process with Well-Architected Integration

**Document ID:** workflow-discovery  
**Index:** [GOV-ARCH-001](../GOV-ARCH-001-Architecture-Documentation-Index.md)  
**Router:** [docs/workflows/discovery.md](../docs/workflows/discovery.md)  
**Related:** [well-architected-pillars.md](well-architected-pillars.md), [service-decisions-enhanced.md](service-decisions-enhanced.md), [CROSS_REFERENCE_INDEX.md](../CROSS_REFERENCE_INDEX.md)

## Overview

This framework guides systematic discovery process that Solutions Architects use to understand requirements before designing architectures. It integrates Well-Architected Framework questions directly into discovery to ensure architectures align with AWS best practices from the start.

### Related Documents
- **[Service Decisions](service-decisions-enhanced.md)** - Use after discovery to select appropriate services
- **[Architecture Patterns](architecture-patterns.md)** - Reference for pattern selection based on discovered requirements
- **[Compliance Framework](compliance-framework.md)** - Use when compliance requirements are identified
- **[Migration Patterns](migration-patterns.md)** - For migration project discovery phase
- **[Cross-Reference Index](../CROSS_REFERENCE_INDEX.md)** - Navigate to related topics

---

## Discovery Phase Structure

### Phase 1: Business Context Discovery
**Goal**: Understand "why" before "what"

#### Core Questions
1. **Problem Statement**
   - What business problem are you solving?
   - Who are the end users/customers?
   - What does success look like?

2. **Current State**
   - What exists today? (existing systems, processes, infrastructure)
   - What's working? What's not?
   - Why change now?

3. **Business Drivers**
   - Time to market requirements
   - Competitive pressures
   - Regulatory/compliance mandates
   - Cost reduction goals
   - Innovation/experimentation needs

4. **Success Metrics**
   - How will you measure success?
   - What are the KPIs?
   - What would constitute failure?

#### Information to Extract
- **Industry/Domain**: Healthcare, FinTech, Gaming, E-commerce, SaaS, etc.
- **Company Stage**: Startup, Growth, Enterprise
- **Business Model**: B2B, B2C, B2B2C, Platform, Marketplace
- **Revenue Impact**: Revenue-generating, cost center, enablement

---

### Phase 2: Technical Requirements Discovery
**Goal**: Understand what the system must do

#### Functional Requirements

1. **Core Capabilities**
   - What does the system need to do?
   - What are the main user workflows?
   - What data needs to be processed/stored?

2. **Integration Requirements**
   - What systems must this integrate with?
   - What APIs need to be exposed/consumed?
   - Data sources and destinations?

3. **Data Characteristics**
   ```
   Data Volume:
   - Current: [amount] per [timeframe]
   - 6-month projection: [amount]
   - 2-year projection: [amount]
   
   Data Types:
   - Structured, semi-structured, unstructured
   - Real-time vs batch
   - Transactional vs analytical
   
   Data Sensitivity:
   - PII, PHI, PCI, confidential, public
   - Retention requirements
   - Data residency requirements
   ```

4. **User/Traffic Patterns**
   ```
   Current Users:
   - Active users: [number]
   - Concurrent users (peak): [number]
   - Geographic distribution: [regions/countries]
   
   Growth Projection:
   - 6 months: [percentage increase]
   - 12 months: [percentage increase]
   - 24 months: [percentage increase]
   
   Usage Patterns:
   - Traffic distribution (steady, spiky, seasonal)
   - Peak hours/days
   - Expected request rate (requests/second)
   ```

#### Non-Functional Requirements

1. **Performance Requirements**
   - Response time targets (p50, p95, p99)
   - Throughput requirements
   - Latency sensitivity
   - Batch processing windows

2. **Availability Requirements**
   ```
   Target Uptime: [percentage] (e.g., 99.9%, 99.99%)
   Downtime Tolerance: [minutes/hours per month]
   Maintenance Windows: [acceptable times]
   Geographic Redundancy: [required/not required]
   ```

3. **Scalability Requirements**
   ```
   Scaling Triggers:
   - User growth
   - Data volume
   - Transaction volume
   - Geographic expansion
   
   Scaling Type:
   - Horizontal vs Vertical
   - Auto-scaling requirements
   - Manual scaling acceptable?
   ```

4. **Security Requirements**
   ```
   Authentication:
   - User types (customers, employees, partners)
   - Authentication methods (SSO, MFA, federated)
   
   Authorization:
   - Role-based access control
   - Attribute-based access control
   - Resource-level permissions
   
   Data Protection:
   - Encryption at rest (required/optional)
   - Encryption in transit (required/optional)
   - Key management requirements
   
   Network Security:
   - VPC requirements
   - Firewall rules
   - DDoS protection needs
   ```

5. **Compliance Requirements**
   ```
   Regulatory Frameworks:
   - HIPAA (Healthcare)
   - PCI-DSS (Payments)
   - SOX (Financial reporting)
   - GDPR (Data privacy)
   - FedRAMP (Government)
   
   Data Residency:
   - Data must stay within [country/region]
   - Sovereignty requirements
   
   Audit Requirements:
   - Logging requirements
   - Monitoring requirements
   - Reporting frequency
   ```

6. **Sustainability Requirements**
   ```
   Carbon Footprint Goals:
   - Renewable energy usage target
   - Carbon reduction targets
   - Sustainability reporting needs
   
   Resource Efficiency:
   - Energy efficiency requirements
   - Resource utilization goals
   - Waste reduction targets
   ```

---

### Phase 3: Well-Architected Assessment During Discovery

**Goal**: Evaluate requirements against AWS best practices during discovery, not after architecture is designed

#### Operational Excellence Assessment

**Key Questions to Ask During Discovery**:
1. How will you monitor workload health and performance?
2. What processes will you use for managing changes?
3. How will you respond to operational events?
4. What's your team's operational capability level?

**Scoring Framework** (0-5 points each):
- **5**: Comprehensive monitoring and automated operations
- **3-4**: Basic monitoring and some automation
- **1-2**: Minimal monitoring, mostly manual
- **0**: No operational planning

#### Security Assessment

**Key Questions to Ask During Discovery**:
1. Who needs access to what data and resources?
2. How will you protect data at rest and in transit?
3. How will you detect and respond to security events?
4. How will you manage identities and permissions?

**Scoring Framework** (0-5 points each):
- **5**: Zero-trust architecture, automated security
- **3-4**: Strong security practices, some automation
- **1-2**: Basic security measures
- **0**: No security planning

#### Reliability Assessment

**Key Questions to Ask During Discovery**:
1. What are your availability and recovery requirements?
2. How will you handle component failures?
3. What's your disaster recovery plan?
4. How will you test reliability?

**Scoring Framework** (0-5 points each):
- **5**: Multi-region, automated failover, comprehensive testing
- **3-4**: High availability, basic disaster recovery
- **1-2**: Single region, basic backups
- **0**: No reliability planning

#### Performance Efficiency Assessment

**Key Questions to Ask During Discovery**:
1. What are your performance targets?
2. How will you right-size resources?
3. How will you optimize performance over time?
4. What's your performance testing approach?

**Scoring Framework** (0-5 points each):
- **5**: Comprehensive performance optimization and testing
- **3-4**: Basic performance monitoring and optimization
- **1-2**: Minimal performance planning
- **0**: No performance requirements

#### Cost Optimization Assessment

**Key Questions to Ask During Discovery**:
1. What's your budget and cost targets?
2. How will you track and optimize costs?
3. What's your pricing model preference?
4. How will you right-size resources for cost?

**Scoring Framework** (0-5 points each):
- **5**: Comprehensive cost management and optimization
- **3-4**: Basic cost tracking and some optimization
- **1-2**: Minimal cost consideration
- **0**: No cost planning

#### Sustainability Assessment

**Key Questions to Ask During Discovery**:
1. What are your sustainability goals?
2. How will you measure environmental impact?
3. What's your preference for carbon-efficient regions?
4. How will you optimize resource utilization?

**Scoring Framework** (0-5 points each):
- **5**: Comprehensive sustainability planning and measurement
- **3-4**: Basic sustainability considerations
- **1-2**: Minimal sustainability planning
- **0**: No sustainability goals

---

### Phase 4: Discovery Documentation Template

**Use this template to document discovery findings**:

```
# Discovery Results: [Project Name]

## Executive Summary
- Business Problem: [one-sentence description]
- Success Criteria: [what success looks like]
- Timeline: [expected delivery timeline]
- Budget Range: [estimated cost range]

## Business Context
### Current State
- Existing Systems: [what exists today]
- Pain Points: [what's not working]
- Change Drivers: [why change now]

### Success Metrics
- Primary KPIs: [key metrics]
- Secondary Metrics: [supporting metrics]
- Failure Criteria: [what constitutes failure]

## Technical Requirements

### Functional Requirements
#### Core Capabilities
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

#### Integration Requirements
- External Systems: [systems to integrate with]
- APIs to Expose: [APIs needed]
- Data Sources: [where data comes from]

#### Data Characteristics
- Volume: Current [amount], 1-year [projected amount]
- Types: [structured/unstructured/etc.]
- Sensitivity: [PII/PHI/etc.]
- Retention: [how long to keep data]

#### User & Traffic Patterns
- Current Users: [number]
- Projected Growth: [percentage/timeframe]
- Traffic Pattern: [steady/spiky/seasonal]
- Geographic Distribution: [regions/countries]

### Non-Functional Requirements

#### Performance
- Response Time: p50 [target], p95 [target], p99 [target]
- Throughput: [transactions/second]
- Batch Windows: [time limits]

#### Availability
- Target Uptime: [percentage]
- RTO: [Recovery Time Objective]
- RPO: [Recovery Point Objective]
- Maintenance Windows: [acceptable times]

#### Security
- Authentication: [methods required]
- Authorization: [access control model]
- Data Protection: [encryption requirements]
- Compliance: [regulatory frameworks]

#### Scalability
- Scaling Type: [horizontal/vertical]
- Auto-scaling: [required/not required]
- Peak Multiplier: [expected peak vs baseline]

#### Cost
- Budget Constraints: [monthly/yearly limits]
- Pricing Preference: [fixed/variable consumption]
- Optimization Goals: [cost reduction targets]

#### Sustainability
- Carbon Goals: [renewable energy targets]
- Region Preference: [carbon-efficient regions]
- Resource Efficiency: [utilization goals]

## Well-Architected Assessment

### Scores (0-5 each)
- Operational Excellence: [score] - [summary]
- Security: [score] - [summary]
- Reliability: [score] - [summary]
- Performance Efficiency: [score] - [summary]
- Cost Optimization: [score] - [summary]
- Sustainability: [score] - [summary]

### Overall Assessment
- Average Score: [calculated average]
- Strengths: [pillars with high scores]
- Areas of Concern: [pillars with low scores]
- Immediate Focus: [top 2-3 priorities]

## Architecture Implications

### Required AWS Services
Based on discovery, the architecture will likely need:
- Compute: [AWS compute services]
- Storage: [AWS storage services]
- Database: [AWS database services]
- Networking: [AWS networking services]
- Security: [AWS security services]
- Monitoring: [AWS monitoring services]

### Key Architectural Decisions Needed
1. [Decision 1] - impacted by [requirement]
2. [Decision 2] - impacted by [requirement]
3. [Decision 3] - impacted by [requirement]

### Constraints and Trade-offs
- Primary Constraint: [most limiting factor]
- Trade-offs to Consider: [what we might sacrifice]
- Risk Factors: [potential risks]

## Next Steps
1. [Action 1] - [timeline]
2. [Action 2] - [timeline]
3. [Action 3] - [timeline]
```

---

## Discovery Integration with AWS Documentation

**Before finalizing discovery, always verify requirements against current AWS guidance**:

1. **Check Well-Architected questions**:
   ```
   MCP_DOCKER:search_documentation "Well-Architected review questions [pillar name]"
   ```

2. **Verify service capabilities**:
   ```
   MCP_DOCKER:search_documentation "[service name] capabilities limits"
   ```

3. **Check compliance requirements**:
   ```
   MCP_DOCKER:search_documentation "[compliance standard] AWS requirements"
   ```

4. **Review best practices**:
   ```
   MCP_DOCKER:search_documentation "[architecture pattern] best practices AWS"
   ```

This ensures discovery outcomes align with current AWS capabilities and best practices.