---
id: GOV-ARCH-001
title: Architecture Documentation Index
owner: AWS Solutions Architect Team
status: Active
last_reviewed: 2026-02-04
---

# GOV-ARCH-001 Architecture Documentation Index

Status: Active  
Owner: AWS Solutions Architect Team  
Approvers: Architecture Review Board  
Last updated: 2026-02-04  
Applies to: All AWS solution architecture documentation  
Related: REF-001, REF-002, CROSS_REFERENCE_INDEX.md

---

## 1. Purpose

This document serves as the master catalog and cross-reference index for all AWS Solutions Architect documentation. It provides:

- **Centralized navigation** between all documentation files
- **Dependency mapping** showing relationships between documents
- **Quick lookup** by topic, service, pattern, and domain
- **Documentation coverage** assessment across the Well-Architected Framework

## 2. Scope

### In Scope

- All canonical decision frameworks in `files/`
- All workflow routers in `docs/workflows/`
- All pattern documentation in `docs/patterns/`
- All tool documentation in `docs/tools/` and `tools/`
- All reference materials in `docs/reference/`
- All implementation supplements
- Cross-references to external AWS documentation

### Out of Scope

- Generated documentation artifacts
- Deprecated/legacy documentation versions
- Third-party integrations not maintained by this team
- Runtime configuration files

## 3. Documentation Catalog

### 3.1 Tier 1 - Foundation Documents

| ID | Document | Location | Tier | Purpose |
|----|----------|----------|------|---------|
| REF-001 | Glossary and Standards Catalog | N/A (to be created) | 1 | Canonical terminology and naming conventions |
| REF-002 | Platform Constants | N/A (to be created) | 1 | Environment values and service identifiers |
| GOV-ARCH-001 | Architecture Documentation Index | CROSS_REFERENCE_INDEX.md | 1 | This master catalog |

### 3.2 Workflows (Discovery → Review → Decision → Migration)

| Workflow | Router File | Canonical File | Description | Domain |
|----------|-------------|----------------|-------------|--------|
| Discovery | `docs/workflows/discovery.md` | `files/discovery-questions-enhanced.md` | Systematic requirements gathering | Multi-Account (26%) |
| Review | `docs/workflows/review.md` | `files/well-architected-pillars.md` | Well-Architected assessments | All Domains |
| Decisions | `docs/workflows/decisions.md` | `files/service-decisions-enhanced.md` | Service selection frameworks | Design (29%) |
| Migration | `docs/workflows/migration.md` | `files/migration-patterns.md` | 6 R's migration strategy | Migration (20%) |

### 3.3 Patterns (Architecture, Compliance, Migration, Services)

| Pattern | Router File | Canonical File | Focus Area | Domain |
|---------|-------------|----------------|------------|--------|
| Architecture | `docs/patterns/architecture.md` | `files/architecture-patterns.md` | Design patterns & anti-patterns | Design (29%) |
| Compliance | `docs/patterns/compliance.md` | `files/compliance-framework.md` | Regulatory mapping | Security/All |
| Migration | `docs/patterns/migration.md` | `files/migration-patterns.md` | Migration strategies | Migration (20%) |
| Services | `docs/patterns/services.md` | `files/service-decisions-enhanced.md` | Service selection | Design (29%) |

### 3.4 Tools (Cost, Assessment, Implementation)

| Tool | Router File | Canonical File | Purpose |
|------|-------------|----------------|---------|
| Cost Estimator | `docs/tools/cost-estimator.md` | `tools/cost-estimator.md` | Real-time cost estimation |
| Team Assessment | `docs/tools/team-assessment.md` | `tools/team-assessment.md` | Capability evaluation |
| Implementation Guide | `docs/tools/implementation-guide.md` | `tools/implementation-guide.md` | Guided implementation |
| Compliance Checker | `docs/tools/compliance-checker.md` | `files/compliance-framework.md` | Regulatory assessment |

### 3.5 Reference Materials

| Reference | Router File | Canonical File | Content Type |
|-----------|-------------|----------------|--------------|
| Well-Architected | `docs/reference/well-architected.md` | `files/well-architected-pillars.md` | 6 Pillars deep dive |
| Decision Trees | `docs/reference/decision-trees.md` | `files/service-decisions-enhanced.md` | Service selection |
| Best Practices | `docs/reference/best-practices.md` | `files/architecture-patterns.md` | Patterns & practices |

### 3.6 Implementation Supplements

| Supplement | Focus Area | Lines | Primary Use Case |
|------------|------------|-------|------------------|
| `AWS_Solutions_Architect_Comprehensive_Guide.md` | Foundation | ~2,500 | All SA Pro domains |
| `container_networking_supplement.md` | ECS/EKS networking | ~2,500 | Container orchestration |
| `route53_implementation_supplement.md` | DNS & failover | ~2,000 | Routing & health checks |
| `drs_implementation_supplement.md` | Disaster recovery | ~2,200 | DR implementation |
| `cicd_implementation_supplement.md` | CI/CD pipelines | ~2,800 | Deployment automation |
| `systems_manager_supplement.md` | Operations | ~2,400 | Patch & automation |
| `aws_config_supplement.md` | Compliance | ~2,200 | Configuration monitoring |
| `security_services_supplement.md` | Security monitoring | ~2,600 | Threat detection |
| `aws_backup_supplement.md` | Data protection | ~2,000 | Backup strategies |

**Total Implementation Supplement Coverage**: ~21,200 lines

## 4. Cross-Reference Matrix

### 4.1 By SA Pro Domain

#### Domain 1: Multi-Account Governance (26%)

| Topic | Primary Document | Supplement | Cross-References |
|-------|-----------------|------------|------------------|
| AWS Organizations | Comprehensive Guide | - | SCPs, Control Tower |
| Service Control Policies | Comprehensive Guide | - | Identity Center |
| AWS Control Tower | Comprehensive Guide | - | Landing Zone |
| IAM Identity Center | Comprehensive Guide | - | SSO, Federation |
| Cross-Account Networking | Comprehensive Guide | container_networking_supplement.md | Transit Gateway |
| Centralized Logging | Comprehensive Guide | - | CloudTrail, Config |
| Cost Allocation | Comprehensive Guide | - | Budgets, CUR |
| GuardDuty Multi-Account | security_services_supplement.md | - | Security Hub |
| Security Hub Aggregation | security_services_supplement.md | - | Config |
| Access Analyzer | security_services_supplement.md | - | IAM, Organizations |

**Related Workflows**: Discovery, Review  
**Related Patterns**: Architecture, Compliance  
**Related Tools**: Compliance Checker

#### Domain 2: Design for New Solutions (29%)

| Topic | Primary Document | Supplement | Cross-References |
|-------|-----------------|------------|------------------|
| High Availability | Comprehensive Guide | - | Auto Scaling, Multi-AZ |
| Disaster Recovery | Comprehensive Guide | drs_implementation_supplement.md | Backup, Route 53 |
| Auto Scaling | Comprehensive Guide | - | EC2, ECS, EKS |
| Container Networking | container_networking_supplement.md | - | ECS, EKS, Fargate |
| CI/CD Pipelines | cicd_implementation_supplement.md | - | CodePipeline, CodeDeploy |
| Blue/Green Deployment | cicd_implementation_supplement.md | - | Route 53, ALB |
| Canary Deployment | cicd_implementation_supplement.md | - | CloudWatch, Auto Scaling |
| Route 53 Failover | route53_implementation_supplement.md | - | Health checks, DRS |
| Security Architecture | Comprehensive Guide | security_services_supplement.md | Defense in depth |
| Cost Optimization | Comprehensive Guide | - | RI, Savings Plans |

**Related Workflows**: Decisions, Discovery  
**Related Patterns**: Architecture, Services  
**Related Tools**: Cost Estimator, Implementation Guide

#### Domain 3: Continuous Improvement (25%)

| Topic | Primary Document | Supplement | Cross-References |
|-------|-----------------|------------|------------------|
| Systems Manager | systems_manager_supplement.md | - | Automation, Session |
| Patch Manager | systems_manager_supplement.md | - | Compliance, Config |
| AWS Config | aws_config_supplement.md | - | Rules, Remediation |
| Config Rules | aws_config_supplement.md | - | Security Hub |
| Automated Remediation | aws_config_supplement.md | systems_manager_supplement.md | Config + Automation |
| AWS Backup | aws_backup_supplement.md | - | Cross-region/account |
| Monitoring | Comprehensive Guide | - | CloudWatch, X-Ray |
| CloudWatch | Comprehensive Guide | - | Metrics, Alarms, Logs |
| Security Improvements | security_services_supplement.md | aws_config_supplement.md | Continuous monitoring |

**Related Workflows**: Review, Migration  
**Related Patterns**: Compliance, Architecture  
**Related Tools**: Compliance Checker, Team Assessment

#### Domain 4: Accelerate Migration (20%)

| Topic | Primary Document | Supplement | Cross-References |
|-------|-----------------|------------|------------------|
| 7 R's Migration Strategy | Comprehensive Guide | - | MGN, DMS, DRS |
| AWS DRS | drs_implementation_supplement.md | - | Failover, failback |
| Application Migration | Comprehensive Guide | - | MGN, Server Migration |
| AWS MGN | Comprehensive Guide | - | Server migration |
| AWS Backup for Migration | aws_backup_supplement.md | - | Cross-account backup |
| DataSync | Comprehensive Guide | - | Data transfer |
| Snow Family | Comprehensive Guide | - | Offline transfer |

**Related Workflows**: Migration, Discovery  
**Related Patterns**: Migration, Architecture  
**Related Tools**: Implementation Guide

### 4.2 By AWS Service (Alphabetical)

#### A-B

| Service | Primary Location | Key Topics | Related Documents |
|---------|-----------------|------------|-------------------|
| API Gateway | Comprehensive Guide | REST vs WebSocket, throttling | cicd_implementation_supplement.md |
| Access Analyzer | security_services_supplement.md | External access, zone of trust | Comprehensive Guide, Config |
| Application Load Balancer | Comprehensive Guide | Layer 7, health checks | container_networking_supplement.md |
| Aurora | Comprehensive Guide | Storage architecture, Global DB | Comprehensive Guide |
| Auto Scaling | Comprehensive Guide | Policies, lifecycle hooks | cicd_implementation_supplement.md |
| AWS Backup | aws_backup_supplement.md | Plans, vaults, cross-region | drs_implementation_supplement.md |
| AWS Config | aws_config_supplement.md | Rules, remediation | systems_manager_supplement.md |
| AWS Organizations | Comprehensive Guide | SCPs, consolidated billing | security_services_supplement.md |

#### C-D

| Service | Primary Location | Key Topics | Related Documents |
|---------|-----------------|------------|-------------------|
| CloudFormation | Comprehensive Guide | Templates, StackSets | Comprehensive Guide |
| CloudFront | Comprehensive Guide | Caching, edge locations | Comprehensive Guide |
| CloudTrail | Comprehensive Guide | Management events, insights | aws_config_supplement.md |
| CloudWatch | Comprehensive Guide | Metrics, alarms, logs | cicd_implementation_supplement.md |
| CodeBuild | cicd_implementation_supplement.md | Buildspec, artifacts | cicd_implementation_supplement.md |
| CodeDeploy | cicd_implementation_supplement.md | Deployment strategies | cicd_implementation_supplement.md |
| CodePipeline | cicd_implementation_supplement.md | Stages, actions | cicd_implementation_supplement.md |
| Cognito | Comprehensive Guide | User pools, identity pools | Comprehensive Guide |
| DynamoDB | Comprehensive Guide | Data model, DAX, streams | Comprehensive Guide |
| DMS | Comprehensive Guide | CDC, replication | Comprehensive Guide |
| DRS | drs_implementation_supplement.md | Architecture, failover | route53_implementation_supplement.md |

#### E-G

| Service | Primary Location | Key Topics | Related Documents |
|---------|-----------------|------------|-------------------|
| EBS | Comprehensive Guide | Volume types, snapshots | Comprehensive Guide |
| EC2 | Comprehensive Guide | Instance types, purchasing | Comprehensive Guide |
| ECS | container_networking_supplement.md | awsvpc mode, service discovery | container_networking_supplement.md |
| EFS | Comprehensive Guide | Performance modes | Comprehensive Guide |
| EKS | container_networking_supplement.md | VPC CNI, network policies | container_networking_supplement.md |
| ElastiCache | Comprehensive Guide | Redis vs Memcached | Comprehensive Guide |
| EventBridge | Comprehensive Guide | Rules, buses, schemas | Comprehensive Guide |
| Fargate | container_networking_supplement.md | Serverless containers | container_networking_supplement.md |
| GuardDuty | security_services_supplement.md | Threat detection | security_services_supplement.md |
| Global Accelerator | Comprehensive Guide | Static IPs, health checks | Comprehensive Guide |

#### I-M

| Service | Primary Location | Key Topics | Related Documents |
|---------|-----------------|------------|-------------------|
| IAM | Comprehensive Guide | Policies, roles, federation | Comprehensive Guide |
| Inspector | security_services_supplement.md | Vulnerability scanning | systems_manager_supplement.md |
| Kinesis | Comprehensive Guide | Streams, Firehose, Analytics | Comprehensive Guide |
| KMS | Comprehensive Guide | Key policies, encryption | Comprehensive Guide |
| Lambda | Comprehensive Guide | Runtime, layers, events | cicd_implementation_supplement.md |
| Macie | security_services_supplement.md | Sensitive data discovery | security_services_supplement.md |
| NAT Gateway | container_networking_supplement.md | Egress control | container_networking_supplement.md |

#### N-R

| Service | Primary Location | Key Topics | Related Documents |
|---------|-----------------|------------|-------------------|
| NLB | Comprehensive Guide | Layer 4, static IPs | container_networking_supplement.md |
| Parameter Store | systems_manager_supplement.md | Hierarchies, SecureString | systems_manager_supplement.md |
| Patch Manager | systems_manager_supplement.md | Baselines, compliance | aws_config_supplement.md |
| RDS | Comprehensive Guide | Multi-AZ, read replicas | Comprehensive Guide |
| Route 53 | route53_implementation_supplement.md | Health checks, failover | drs_implementation_supplement.md |
| S3 | Comprehensive Guide | Storage classes, replication | aws_backup_supplement.md |
| Secrets Manager | Comprehensive Guide | Rotation, cross-account | systems_manager_supplement.md |
| Security Hub | security_services_supplement.md | Findings aggregation | aws_config_supplement.md |
| Session Manager | systems_manager_supplement.md | Secure access | security_services_supplement.md |
| SNS | Comprehensive Guide | Topics, subscriptions | Comprehensive Guide |
| SQS | Comprehensive Guide | Queues, DLQs, FIFO | Comprehensive Guide |
| SSM | systems_manager_supplement.md | Complete coverage | aws_config_supplement.md |
| Step Functions | Comprehensive Guide | Workflows, errors | Comprehensive Guide |

#### T-Z

| Service | Primary Location | Key Topics | Related Documents |
|---------|-----------------|------------|-------------------|
| Transit Gateway | Comprehensive Guide | Routing, attachments | container_networking_supplement.md |
| VPC | Comprehensive Guide | Subnets, routing, security | container_networking_supplement.md |
| VPC Endpoints | container_networking_supplement.md | PrivateLink, Gateway | container_networking_supplement.md |
| WAF | Comprehensive Guide | Rules, rate limiting | security_services_supplement.md |

### 4.3 By Architecture Pattern

| Pattern Category | Pattern | Document | Section | Domain |
|-----------------|---------|----------|---------|--------|
| Serverless | Lambda Functions | Comprehensive Guide | Section 9.1 | Design |
| Serverless | API Gateway + Lambda | Comprehensive Guide | Section 9.1 | Design |
| Serverless | Event-Driven | Comprehensive Guide | Section 9.2 | Design |
| Serverless | Step Functions | Comprehensive Guide | Section 9.3 | Design |
| Container-Based | ECS awsvpc Mode | container_networking_supplement.md | ECS networking | Design |
| Container-Based | EKS VPC CNI | container_networking_supplement.md | EKS networking | Design |
| Container-Based | Service Mesh | container_networking_supplement.md | App Mesh | Design |
| Container-Based | Fargate | container_networking_supplement.md | Serverless containers | Design |
| Multi-Tier | Web-App-DB | Comprehensive Guide | Section 12.1 | Design |
| Multi-Tier | Load Balancer Patterns | Comprehensive Guide | Section 5.3 | Design |
| Multi-Tier | Auto Scaling | Comprehensive Guide | Section 9 | Design |
| Event-Driven | EventBridge | Comprehensive Guide | Section 9.2 | Design |
| Event-Driven | SQS + Lambda | Comprehensive Guide | Section 9.2 | Design |
| Event-Driven | SNS Fan-Out | Comprehensive Guide | Section 9.2 | Design |
| Disaster Recovery | Backup & Restore | Comprehensive Guide | Section 8.4 | Design |
| Disaster Recovery | Pilot Light | Comprehensive Guide | Section 8.4 | Design |
| Disaster Recovery | Warm Standby | Comprehensive Guide | Section 8.4 | Design |
| Disaster Recovery | Active-Active | Comprehensive Guide | Section 8.4 | Design |
| Disaster Recovery | AWS DRS | drs_implementation_supplement.md | Implementation | Design |

### 4.4 By Topic/Concept

#### High Availability

| Concept | Document | Section | Service Mapping |
|---------|----------|---------|-----------------|
| Multi-AZ | Comprehensive Guide | Section 8.2 | RDS, Aurora, ElastiCache |
| Multi-Region | Comprehensive Guide | Section 8.3 | Global Accelerator, Route 53 |
| Auto Scaling | Comprehensive Guide | Section 9 | EC2, ECS, EKS |
| Health Checks | route53_implementation_supplement.md | Health check types | Route 53, ALB, NLB |
| Failover Patterns | drs_implementation_supplement.md | Automated failover | DRS, Route 53 |

#### Disaster Recovery

| Concept | Document | Section | Related Patterns |
|---------|----------|---------|------------------|
| RTO/RPO Definitions | Comprehensive Guide | Section 8.1 | All DR patterns |
| DR Strategies | Comprehensive Guide | Section 8.4 | Pilot Light, Warm Standby |
| AWS DRS | drs_implementation_supplement.md | Complete guide | Failover, failback |
| Backup Strategies | aws_backup_supplement.md | 3-2-1 rule | Cross-region/account |
| Pilot Light | Comprehensive Guide | Section 8.4 | RDS, Aurora replicas |
| Warm Standby | Comprehensive Guide | Section 8.4 | Auto Scaling groups |

#### Security

| Concept | Document | Section | Related Services |
|---------|----------|---------|------------------|
| Defense in Depth | Comprehensive Guide | Section 7 | All security services |
| IAM Best Practices | Comprehensive Guide | Section 7.1 | IAM, Identity Center |
| Encryption | Comprehensive Guide | Section 7.2 | KMS, CloudHSM |
| VPC Security | container_networking_supplement.md | Security boundaries | Security groups, NACLs |
| Threat Detection | security_services_supplement.md | GuardDuty | Security Hub |
| Vulnerability Mgmt | security_services_supplement.md | Inspector | Systems Manager |
| Compliance Monitoring | aws_config_supplement.md | Conformance packs | Config Rules |

#### Networking

| Concept | Document | Section | Service Mapping |
|---------|----------|---------|-----------------|
| VPC Design | Comprehensive Guide | Section 5 | VPC, subnets, routing |
| Subnetting | Comprehensive Guide | Section 5.1 | Public/private, CIDR |
| Routing | Comprehensive Guide | Section 5.2 | Route tables, TGW |
| Container Networking | container_networking_supplement.md | ECS/EKS modes | awsvpc, CNI |
| Service Discovery | container_networking_supplement.md | Cloud Map | ECS, EKS |
| Load Balancing | Comprehensive Guide | Section 5.3 | ALB, NLB, CLB |

#### Cost Optimization

| Concept | Document | Section | Strategies |
|---------|----------|---------|------------|
| Compute Savings | Comprehensive Guide | Section 11.1 | RI, Savings Plans, Spot |
| Storage Tiers | Comprehensive Guide | Section 11.2 | S3 lifecycle, EFS IA |
| Network Costs | Comprehensive Guide | Section 11.3 | VPC endpoints, TGW |
| RI & Savings Plans | Comprehensive Guide | Section 11.1 | Compute, RDS |

#### Migration

| Concept | Document | Section | Tools/Services |
|---------|----------|---------|----------------|
| 7 R's Strategy | Comprehensive Guide | Section 10.1 | Rehost, Replatform, Refactor |
| DMS Migration | Comprehensive Guide | Section 16.1 | Database migration |
| Server Migration | Comprehensive Guide | Section 16.2 | AWS MGN |
| Data Migration | Comprehensive Guide | Section 16.3-16.4 | DataSync, Snow Family |

## 5. Implementation Guides Index

### 5.1 Step-by-Step Configuration Guides

| Task | Document | Section | Domain |
|------|----------|---------|--------|
| Configure Systems Manager Patch Manager | systems_manager_supplement.md | Section 2 | Continuous Improvement |
| Set up Patch Baselines | systems_manager_supplement.md | Section 2.2 | Continuous Improvement |
| Create Custom Automation Document | systems_manager_supplement.md | Section 3.4 | Continuous Improvement |
| Configure Session Manager Logging | systems_manager_supplement.md | Section 4.6 | Multi-Account |
| Create Parameter Store Hierarchy | systems_manager_supplement.md | Section 5.4 | Continuous Improvement |
| Set up AWS Config Recorder | aws_config_supplement.md | Section 2 | Continuous Improvement |
| Create Config Rule | aws_config_supplement.md | Section 3.3 | Continuous Improvement |
| Configure Auto-Remediation | aws_config_supplement.md | Section 4.3 | Continuous Improvement |
| Enable GuardDuty | security_services_supplement.md | Section 2.4 | Multi-Account |
| Set up GuardDuty Multi-Account | security_services_supplement.md | Section 2.5 | Multi-Account |
| Enable Security Hub | security_services_supplement.md | Section 3.3 | Multi-Account |
| Enable Macie | security_services_supplement.md | Section 4.3 | Multi-Account |
| Enable Inspector | security_services_supplement.md | Section 5.3 | Continuous Improvement |
| Create Backup Plan | aws_backup_supplement.md | Section 2 | Design |
| Configure Cross-Region Backup | aws_backup_supplement.md | Section 4 | Design |
| Set up Cross-Account Backup | aws_backup_supplement.md | Section 5 | Multi-Account |
| Configure DRS | drs_implementation_supplement.md | Section 3 | Design |
| Set up Route 53 Failover | route53_implementation_supplement.md | Section 3 | Design |
| Configure ECS awsvpc Mode | container_networking_supplement.md | Section 2 | Design |
| Configure EKS VPC CNI | container_networking_supplement.md | Section 3 | Design |
| Set up CI/CD Pipeline | cicd_implementation_supplement.md | Section 2 | Design |
| Configure Blue/Green Deployment | cicd_implementation_supplement.md | Section 3 | Design |
| Configure Canary Deployment | cicd_implementation_supplement.md | Section 4 | Design |

### 5.2 Decision Trees

| Decision | Document | Location | Related Documents |
|----------|----------|----------|-------------------|
| ECS vs EKS vs Lambda | container_networking_supplement.md | Section 8 | Comprehensive Guide |
| Parameter Store vs Secrets Manager | systems_manager_supplement.md | Section 5.6 | Comprehensive Guide |
| Patch Policy vs Maintenance Window | systems_manager_supplement.md | Section 2.3 | Comprehensive Guide |
| Session Manager vs SSH | systems_manager_supplement.md | Section 8.1 | Comprehensive Guide |
| Backup Storage Tier Selection | aws_backup_supplement.md | Section 2.4 | Comprehensive Guide |
| When to Use Security Hub | security_services_supplement.md | Section 8.2 | Comprehensive Guide |
| Security Services Selection | security_services_supplement.md | Section 8.2 | All security supplements |

### 5.3 Troubleshooting Guides

| Issue | Document | Section | Common Causes |
|-------|----------|---------|---------------|
| SSM Agent Issues | systems_manager_supplement.md | Section 11.1 | IAM, network, endpoints |
| Session Manager Connection | systems_manager_supplement.md | Section 11.2 | IAM, VPC endpoints |
| Patch Manager Failures | systems_manager_supplement.md | Section 11.3 | Baseline, permissions |
| Config Recorder Issues | aws_config_supplement.md | Section 9.1 | IAM, S3, delivery |
| Remediation Failures | aws_config_supplement.md | Section 9.4 | Automation, IAM |
| Backup Job Failures | aws_backup_supplement.md | Section 10 | IAM, vault access |

## 6. Supplement Cross-Reference Matrix

### 6.1 Container Networking Supplement Links

| Source Concept | Target Document | Target Concept |
|----------------|-----------------|----------------|
| ECS Service Discovery | aws_backup_supplement.md | Cross-account patterns |
| EKS Load Balancing | route53_implementation_supplement.md | Failover routing |
| Network Policies | security_services_supplement.md | Defense in depth |
| VPC CNI | container_networking_supplement.md | Custom networking |
| Service Mesh | container_networking_supplement.md | App Mesh implementation |

### 6.2 Security Services Supplement Links

| Source Concept | Target Document | Target Concept |
|----------------|-----------------|----------------|
| GuardDuty → Security Hub | Already integrated | Findings ingestion |
| Inspector Remediation | systems_manager_supplement.md | Automation documents |
| Access Analyzer → Config | aws_config_supplement.md | Compliance rules |
| Security Hub → Config | aws_config_supplement.md | Conformance packs |
| Macie Findings | security_services_supplement.md | EventBridge integration |

### 6.3 CI/CD Supplement Links

| Source Concept | Target Document | Target Concept |
|----------------|-----------------|----------------|
| Blue/Green + Route 53 | route53_implementation_supplement.md | Routing policies |
| Canary + CloudWatch | Comprehensive Guide | Monitoring metrics |
| Multi-Account Pipeline | security_services_supplement.md | Cross-account IAM |
| CodeDeploy Hooks | cicd_implementation_supplement.md | Lifecycle events |
| Pipeline Approvals | cicd_implementation_supplement.md | Manual gates |

### 6.4 Systems Manager Links

| Source Concept | Target Document | Target Concept |
|----------------|-----------------|----------------|
| Patch Manager → Config | aws_config_supplement.md | Compliance monitoring |
| Automation → DRS | drs_implementation_supplement.md | Recovery workflows |
| Session Manager → Security | security_services_supplement.md | Access auditing |
| Parameter Store → Security | security_services_supplement.md | Secret rotation |
| Run Command → Config | aws_config_supplement.md | Remediation |

### 6.5 DRS Supplement Links

| Source Concept | Target Document | Target Concept |
|----------------|-----------------|----------------|
| DRS + Route 53 | route53_implementation_supplement.md | Automated failover |
| DRS + Backup | aws_backup_supplement.md | Complementary strategies |
| Failover Testing | drs_implementation_supplement.md | DR drills |
| Failback Procedures | drs_implementation_supplement.md | Recovery validation |

### 6.6 Route 53 Links

| Source Concept | Target Document | Target Concept |
|----------------|-----------------|----------------|
| Failover + DRS | drs_implementation_supplement.md | Automated DR |
| Health Checks + ALB | container_networking_supplement.md | Ingress routing |
| Geolocation + CloudFront | Comprehensive Guide | Edge optimization |
| Latency + Global Accelerator | Comprehensive Guide | Performance routing |

## 7. Navigation Quick Reference

### 7.1 Start Here - By Role

| Role | Start With | Next Steps |
|------|-----------|------------|
| **New Architect** | `docs/index.md` | Discovery → Review → Decisions |
| **Experienced SA** | `CROSS_REFERENCE_INDEX.md` | Service-specific supplements |
| **DevOps Engineer** | `cicd_implementation_supplement.md` | Systems Manager, Config |
| **Security Engineer** | `security_services_supplement.md` | Config, IAM guides |
| **Migration Lead** | `files/migration-patterns.md` | DRS, MGN supplements |
| **Compliance Officer** | `files/compliance-framework.md` | Config, Security Hub |
| **Cost Optimizer** | `tools/cost-estimator.md` | Architecture patterns |

### 7.2 By Exam Domain

| SA Pro Domain | Primary Documents | Supporting Supplements |
|--------------|-------------------|----------------------|
| **Domain 1: Multi-Account (26%)** | Discovery workflow, Compliance framework | Security services, Config |
| **Domain 2: Design (29%)** | Service decisions, Architecture patterns | Container networking, CI/CD, DRS, Route 53 |
| **Domain 3: Continuous Improvement (25%)** | Well-Architected review | Systems Manager, Config, Backup |
| **Domain 4: Migration (20%)** | Migration patterns | DRS, Backup, Comprehensive Guide |

### 7.3 By Task Type

| Task | Go To | Tools |
|------|-------|-------|
| **Design Architecture** | `files/service-decisions-enhanced.md` | Cost Estimator |
| **Review Architecture** | `files/well-architected-pillars.md` | Team Assessment |
| **Plan Migration** | `files/migration-patterns.md` | Implementation Guide |
| **Ensure Compliance** | `files/compliance-framework.md` | Compliance Checker |
| **Gather Requirements** | `files/discovery-questions-enhanced.md` | - |
| **Implement Solution** | `tools/implementation-guide.md` | - |
| **Estimate Costs** | `tools/cost-estimator.md` | - |
| **Assess Team** | `tools/team-assessment.md` | - |

## 8. Documentation Maintenance

### 8.1 Adding New Documents

When adding new documentation:

1. **Update Registry** (`scripts/workflow_registry.yaml`):
   ```yaml
   new_category:
     new_document:
       router: docs/category/document.md
       canonical: files/document.md
   ```

2. **Create Router File** (`docs/category/document.md`):
   ```markdown
   ---
   title: document-name
   source: ../../files/document.md
   type: pattern|workflow|tool|reference
   description: Brief description
   ---
   ```

3. **Create Canonical Content** (`files/document.md`)

4. **Update Navigation** (`docs/index.md`):
   Add link to new router file

5. **Update This Index**: Add entry to appropriate section

6. **Validate**:
   ```bash
   python scripts/validate_docs.py
   ```

### 8.2 Validation Checklist

- [ ] New router file created with proper frontmatter
- [ ] Canonical file created in `files/` or `tools/`
- [ ] Registry entry added to `workflow_registry.yaml`
- [ ] Navigation link added to `docs/index.md`
- [ ] Cross-references identified and documented
- [ ] Related documents linked in content
- [ ] Validation script passes: `python scripts/validate_docs.py`
- [ ] This index updated with new document entry

### 8.3 Document Tiers

| Tier | Definition | Examples |
|------|-----------|----------|
| **Tier 1** | Implementation blocking | REF-001, GOV-ARCH-001, Workflows, Patterns |
| **Tier 2** | Integration blocking | API specs, Data models, Service architecture |
| **Tier 3** | Production blocking | Security controls, Observability, DR |
| **Tier 4** | Operational maturity | Runbooks, Capacity planning |

**Prioritization Rule**: Always complete Tier 1 before Tier 2, etc.

## 9. Governance Invariants

### 9.1 Documentation Structure Invariants

1. **Router/Canonical Separation**
   - Router files in `docs/` must only contain frontmatter and navigation links
   - Canonical content must reside in `files/` or `tools/`
   - Never duplicate content between router and canonical

2. **Registry Consistency**
   - Every document must have an entry in `workflow_registry.yaml`
   - Router paths must be relative to repository root
   - Canonical paths must be accurate and exist

3. **Cross-Reference Integrity**
   - All cross-references must use valid document IDs
   - Bidirectional links preferred (A references B, B references A)
   - Links must include line numbers where applicable

### 9.2 Content Quality Invariants

1. **No Orphaned Documents**
   - Every document must be reachable from `docs/index.md`
   - Every supplement must be cross-referenced from at least one workflow or pattern

2. **Frontmatter Completeness**
   - All router files must have complete YAML frontmatter
   - Required fields: `title`, `source`, `type`, `description`

3. **Naming Conventions**
   - Files use kebab-case: `service-decisions-enhanced.md`
   - Directories use lowercase: `workflows/`, `patterns/`
   - No spaces in file or directory names

## 10. References

### 10.1 Internal Documents

| Document ID | Description | Location |
|-------------|-------------|----------|
| CROSS_REFERENCE_INDEX.md | Detailed cross-reference by domain/service | Repository root |
| AGENTS.md | Repository setup and build instructions | Repository root |
| workflow_registry.yaml | Source of truth for document mapping | `scripts/` |

### 10.2 External Resources

- **AWS Well-Architected Framework**: https://aws.amazon.com/architecture/well-architected/
- **AWS Documentation**: https://docs.aws.amazon.com/
- **AWS Prescriptive Guidance**: https://aws.amazon.com/prescriptive-guidance/
- **AWS Architecture Center**: https://aws.amazon.com/architecture/

### 10.3 Architecture Documentation Standards

- **REF-001**: Glossary and Standards Catalog (to be created)
- **REF-002**: Platform Constants (to be created)
- **Skill**: `aws-solution-architect` - Agent skill for architecture design

## 11. Acceptance Criteria

This documentation index is considered complete and maintained when:

1. **Coverage**: All existing documents are catalogued in Section 3
2. **Cross-References**: All major cross-reference relationships documented in Section 4
3. **Navigation**: Users can find any document within 3 clicks from this index
4. **Validation**: `python scripts/validate_docs.py` passes without errors
5. **Currency**: Index reviewed and updated within 30 days of any document addition
6. **Accuracy**: All document locations and links verified quarterly

## 12. Change Control

### 12.1 Change Approval

- **Minor updates** (typos, broken links): Any team member
- **Document additions**: Architecture Review Board approval required
- **Structure changes**: Architecture Review Board + Documentation Lead
- **Tier changes**: Architecture Review Board + Product Owner

### 12.2 Change Process

1. Create feature branch from `main`
2. Make changes following Section 8.1 guidelines
3. Run validation: `python scripts/validate_docs.py`
4. Update this index with changes
5. Submit PR with clear description of changes
6. Request review from Documentation Lead
7. Merge after approval

### 12.3 Waiver Mechanism

Emergency changes that violate invariants require:
- Written justification in PR description
- Architecture Review Board approval
- Follow-up ticket to resolve technical debt
- Must be remediated within 30 days

---

*Last Updated: 2026-02-04*  
*Document Version: 1.0.0*  
*Governance Version: GOV-ARCH-001*
