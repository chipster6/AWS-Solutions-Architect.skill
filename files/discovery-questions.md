# AWS Solutions Architect Skill - Discovery Process Framework

> ⚠️ **DEPRECATED**: This document has been superseded by [`discovery-questions-enhanced.md`](discovery-questions-enhanced.md) which includes Well-Architected Framework integration and enhanced decision criteria. Please use the enhanced version for all new work.

## Overview

This framework guides the systematic discovery process that Solutions Architects use to understand requirements before designing architectures. It ensures no critical aspect is overlooked and provides a structured conversation flow.

---

## Discovery Phase Structure

### Phase 1: Business Context Discovery
**Goal**: Understand the "why" before the "what"

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
    - Network segmentation requirements
    
    Incident Response:
    - Incident detection requirements
    - Response time targets
    - Forensic capabilities
    - Notification procedures

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