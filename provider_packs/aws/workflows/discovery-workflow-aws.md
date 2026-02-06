---
title: AWS Discovery Workflow
type: workflow
version: 1.0
provider: aws
last_updated: "2024-01-01"
---

# AWS Discovery Workflow

## Purpose
Extract AWS-specific requirements during discovery phase

## AWS-Specific Discovery Questions

### Account Structure
1. How many AWS accounts do you currently have?
2. Are you using AWS Organizations?
3. What's your desired account structure?
4. Do you have existing Control Tower?
5. What is your OU structure?

### Networking
1. Do you have existing VPCs?
2. What are your hybrid connectivity requirements?
3. What are your CIDR block constraints?
4. Do you need multi-region architecture?
5. What are your security group policies?

### Compliance
1. Which AWS regions are approved for your workloads?
2. Are there data residency requirements?
3. What compliance frameworks apply (HIPAA, PCI-DSS, SOC2)?
4. Do you need encryption at rest and in transit?
5. What are your logging/audit requirements?

### Existing AWS Services
1. What AWS services are currently in use?
2. What's your current Well-Architected maturity?
3. Do you have existing CloudFormation/Terraform?
4. What is your CI/CD pipeline setup?
5. What monitoring tools are you using?

## AWS-Specific Outputs
- Account architecture recommendation
- Regional deployment strategy
- Compliance mapping
- Existing service integration plan

## Discovery Templates

### Account Assessment Template
```yaml
account_assessment:
  current_state:
    account_count: 0
    organizations_enabled: false
    control_tower_enabled: false
    existing_ous: []
    
  target_state:
    account_count: 0
    organization_structure: ""
    guardrails_required: []
    
  gaps:
    - gap_1: ""
    - gap_2: ""
    
  recommendations:
    - rec_1: ""
    - rec_2: ""
```

### Networking Assessment Template
```yaml
networking_assessment:
  current_state:
    vpc_count: 0
    cidr_blocks: []
    connectivity: []
    
  requirements:
    hybrid_connectivity: false
    multi_region: false
    new_cidr_needed: false
    
  constraints:
    reserved_cidrs: []
    security_requirements: []
    
  recommendations:
    - tgw_recommended: false
    - vpc_design: ""
```

## Service Selection Decision Tree

### Compute Selection
```
Need Compute?
    │
    ├─ Serverless preferred?
    │   ├─ Yes → Event-driven? → Lambda
    │   │   └─ No → HTTP APIs? → Lambda + API Gateway
    │   └─ No → Containerized?
    │       ├─ Yes → Kubernetes needed? → EKS
    │       │   └─ No → ECS Fargate
    │       └─ No → VM needed?
    │           ├─ Yes → EC2
    │           └─ No → Consider serverless alternatives
```

### Database Selection
```
Need Database?
    │
    ├─ Relational data?
    │   ├─ Yes → ACID required? → RDS/Aurora
    │   └─ No → NoSQL needed?
    │       ├─ Yes → Key-value access? → DynamoDB
    │       └─ No → Document? → DocumentDB
    └─ No → Analytics needed?
        ├─ Yes → Data warehouse? → Redshift
        └─ No → Search? → OpenSearch
```

## Well-Architected Pillar Mapping

| Pillar | AWS Services | Key Questions |
|--------|--------------|---------------|
| Operational Excellence | CloudWatch, Lambda, Step Functions | How do you monitor? What's your CI/CD? |
| Security | IAM, KMS, Shield, WAF | What's your encryption strategy? |
| Reliability | S3, DynamoDB, Lambda | What's your RTO/RPO? |
| Performance Efficiency | Lambda, RDS, ElastiCache | What's your scaling strategy? |
| Cost Optimization | Cost Explorer, Savings Plans | What's your budgeting process? |
| Sustainability | Lambda, Graviton | What's your optimization strategy? |
