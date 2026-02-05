---
id: CROSS-REF-001
title: Cross-Reference Index - AWS Solutions Architect Documentation
owner: AWS Solutions Architect Team
status: Active
last_reviewed: 2026-02-04
---

# Cross-Reference Index - AWS Solutions Architect Documentation

Status: Active  
Owner: AWS Solutions Architect Team  
Last Updated: 2026-02-04  
Governance: GOV-ARCH-001  
Related: docs/index.md, AGENTS.md

---

**Purpose:** Navigate between related concepts across all documentation files  
**Governance Reference:** [GOV-ARCH-001-Architecture-Documentation-Index.md](./GOV-ARCH-001-Architecture-Documentation-Index.md) for master catalog

---

## Quick Navigation

- [By SA Pro Domain](#by-sa-pro-domain)
- [By AWS Service](#by-aws-service)
- [By Topic/Concept](#by-topicconcept)
- [By Architecture Pattern](#by-architecture-pattern)
- [Supplement Cross-Reference](#supplement-cross-reference)
- [Implementation Guides Index](#implementation-guides-index)

---

## By SA Pro Domain

### Domain 1: Multi-Account Governance (26%)

| Topic | Primary Document | Supplement | Key Sections |
|-------|-----------------|------------|--------------|
| AWS Organizations | Comprehensive Guide | - | Section 14 (Multi-Account) |
| Service Control Policies (SCPs) | Comprehensive Guide | - | Section 14.3 - Enhanced with evaluation logic |
| AWS Control Tower | Comprehensive Guide | - | Section 14.4 |
| IAM Identity Center | Comprehensive Guide | - | Section 7.4 |
| Cross-Account Networking | Comprehensive Guide | container_networking_supplement.md | Transit Gateway patterns |
| Centralized Logging | Comprehensive Guide | - | Section 14.6 |
| Cost Allocation | Comprehensive Guide | - | Section 11 |
| GuardDuty Multi-Account | security_services_supplement.md | - | Multi-account setup section |
| Security Hub Aggregation | security_services_supplement.md | - | Cross-account aggregation |
| Access Analyzer | security_services_supplement.md | - | External access analysis |

### Domain 2: Design for New Solutions (29%)

| Topic | Primary Document | Supplement | Key Sections |
|-------|-----------------|------------|--------------|
| High Availability | Comprehensive Guide | - | Section 8 |
| Disaster Recovery | Comprehensive Guide | drs_implementation_supplement.md | DRS architecture |
| Auto Scaling | Comprehensive Guide | - | Section 9 |
| Container Networking | container_networking_supplement.md | - | ECS/EKS networking modes |
| CI/CD Pipelines | cicd_implementation_supplement.md | - | Complete implementation |
| Blue/Green Deployment | cicd_implementation_supplement.md | - | Deployment strategies |
| Canary Deployment | cicd_implementation_supplement.md | - | Auto-rollback patterns |
| Route 53 Failover | route53_implementation_supplement.md | - | Health checks, routing |
| Security Architecture | Comprehensive Guide | security_services_supplement.md | Defense in depth |
| Cost Optimization | Comprehensive Guide | - | Section 11 |

### Domain 3: Continuous Improvement (25%)

| Topic | Primary Document | Supplement | Key Sections |
|-------|-----------------|------------|--------------|
| Systems Manager | systems_manager_supplement.md | - | Complete coverage |
| Patch Manager | systems_manager_supplement.md | - | Automated patching |
| AWS Config | aws_config_supplement.md | - | Compliance monitoring |
| Config Rules | aws_config_supplement.md | - | Managed & custom rules |
| Automated Remediation | aws_config_supplement.md | systems_manager_supplement.md | Config + Automation |
| AWS Backup | aws_backup_supplement.md | - | Central backup policies |
| Monitoring | Comprehensive Guide | - | Section 8.5 |
| CloudWatch | Comprehensive Guide | - | Section 8.5 |
| Security Improvements | security_services_supplement.md | aws_config_supplement.md | Continuous monitoring |

### Domain 4: Accelerate Migration (20%)

| Topic | Primary Document | Supplement | Key Sections |
|-------|-----------------|------------|--------------|
| 7 R's Migration Strategy | Comprehensive Guide | - | Section 10.1 (now includes Relocate) |
| AWS DRS | drs_implementation_supplement.md | - | Complete implementation |
| Application Migration | Comprehensive Guide | - | Section 16 |
| AWS MGN | Comprehensive Guide | - | Section 16.2 |
| AWS Backup for Migration | aws_backup_supplement.md | - | Cross-account backup |
| DataSync | Comprehensive Guide | - | Section 16.3 |
| Snow Family | Comprehensive Guide | - | Section 16.4 |

---

## By AWS Service

### A-B

| Service | Documentation Location | Key Topics |
|---------|----------------------|------------|
| **API Gateway** | Comprehensive Guide | REST vs WebSocket, throttling, caching |
| **Access Analyzer** | security_services_supplement.md | External access, zone of trust |
| **Application Load Balancer** | Comprehensive Guide | Layer 7 routing, health checks |
| **Aurora** | Comprehensive Guide | Storage architecture, Global DB, Serverless |
| **Auto Scaling** | Comprehensive Guide | Policies, lifecycle hooks, predictive |
| **AWS Backup** | aws_backup_supplement.md | Plans, vaults, cross-region/account |
| **AWS Config** | aws_config_supplement.md | Rules, remediation, compliance |
| **AWS Organizations** | Comprehensive Guide | SCPs, consolidated billing, OU structure |

### C-D

| Service | Documentation Location | Key Topics |
|---------|----------------------|------------|
| **CloudFormation** | Comprehensive Guide | Templates, StackSets, drift detection |
| **CloudFront** | Comprehensive Guide | Caching, edge locations, signed URLs |
| **CloudTrail** | Comprehensive Guide | Management events, data events, insights |
| **CloudWatch** | Comprehensive Guide | Metrics, alarms, logs, dashboards |
| **CodeBuild** | cicd_implementation_supplement.md | Buildspec, artifacts, caching |
| **CodeDeploy** | cicd_implementation_supplement.md | Deployment strategies, hooks |
| **CodePipeline** | cicd_implementation_supplement.md | Stages, actions, approvals |
| **Cognito** | Comprehensive Guide | User pools, identity pools, MFA |
| **DynamoDB** | Comprehensive Guide | Data model, DAX, streams, global tables |
| **DMS** | Comprehensive Guide | CDC, replication types, SCT |
| **DRS** | drs_implementation_supplement.md | Architecture, failover, failback |

### E-G

| Service | Documentation Location | Key Topics |
|---------|----------------------|------------|
| **EBS** | Comprehensive Guide | Volume types, snapshots, encryption |
| **EC2** | Comprehensive Guide | Instance types, purchasing options |
| **ECS** | container_networking_supplement.md | awsvpc mode, service discovery |
| **EFS** | Comprehensive Guide | Performance modes, lifecycle |
| **EKS** | container_networking_supplement.md | VPC CNI, network policies |
| **ElastiCache** | Comprehensive Guide | Redis vs Memcached, cluster mode |
| **EventBridge** | Comprehensive Guide | Rules, buses, schema registry |
| **Fargate** | container_networking_supplement.md | Serverless containers |
| **GuardDuty** | security_services_supplement.md | Threat detection, findings |
| **Global Accelerator** | Comprehensive Guide | Static IPs, health checks |

### I-M

| Service | Documentation Location | Key Topics |
|---------|----------------------|------------|
| **IAM** | Comprehensive Guide | Policies, roles, federation |
| **Inspector** | security_services_supplement.md | Vulnerability scanning |
| **Kinesis** | Comprehensive Guide | Streams, Firehose, Analytics |
| **KMS** | Comprehensive Guide | Key policies, envelope encryption |
| **Lambda** | Comprehensive Guide | Runtime, layers, event sources |
| **Macie** | security_services_supplement.md | Sensitive data discovery |
| **NAT Gateway** | container_networking_supplement.md | Egress control, costs |

### N-R

| Service | Documentation Location | Key Topics |
|---------|----------------------|------------|
| **NLB** | Comprehensive Guide | Layer 4, static IPs, TLS |
| **Parameter Store** | systems_manager_supplement.md | Hierarchies, SecureString |
| **Patch Manager** | systems_manager_supplement.md | Baselines, compliance |
| **RDS** | Comprehensive Guide | Multi-AZ, read replicas, encryption |
| **Route 53** | route53_implementation_supplement.md | Health checks, failover |
| **S3** | Comprehensive Guide | Storage classes, replication, encryption |
| **Secrets Manager** | Comprehensive Guide | Rotation, cross-account access |
| **Security Hub** | security_services_supplement.md | Findings aggregation, standards |
| **Session Manager** | systems_manager_supplement.md | Secure access, port forwarding |
| **SNS** | Comprehensive Guide | Topics, subscriptions, filtering |
| **SQS** | Comprehensive Guide | Queues, DLQs, FIFO |
| **SSM (Systems Manager)** | systems_manager_supplement.md | Complete coverage |
| **Step Functions** | Comprehensive Guide | Workflows, error handling |

### T-Z

| Service | Documentation Location | Key Topics |
|---------|----------------------|------------|
| **Transit Gateway** | Comprehensive Guide | Routing, attachments, peering |
| **VPC** | Comprehensive Guide | Subnets, routing, security groups |
| **VPC Endpoints** | container_networking_supplement.md | PrivateLink, Gateway endpoints |
| **WAF** | Comprehensive Guide | Rules, rate limiting, managed rules |

---

## By Topic/Concept

### High Availability

| Concept | Document | Section |
|---------|----------|---------|
| Multi-AZ | Comprehensive Guide | Section 8.2 |
| Multi-Region | Comprehensive Guide | Section 8.3 |
| Auto Scaling | Comprehensive Guide | Section 9 |
| Health Checks | route53_implementation_supplement.md | Health check types |
| Failover Patterns | drs_implementation_supplement.md | Automated failover |

### Disaster Recovery

| Concept | Document | Section |
|---------|----------|---------|
| RTO/RPO Definitions | Comprehensive Guide | Section 8.1 |
| DR Strategies | Comprehensive Guide | Section 8.4 |
| AWS DRS | drs_implementation_supplement.md | Complete guide |
| Backup Strategies | aws_backup_supplement.md | 3-2-1 rule |
| Pilot Light | Comprehensive Guide | Section 8.4 |
| Warm Standby | Comprehensive Guide | Section 8.4 |

### Security

| Concept | Document | Section |
|---------|----------|---------|
| Defense in Depth | Comprehensive Guide | Section 7 |
| IAM Best Practices | Comprehensive Guide | Section 7.1 |
| Encryption | Comprehensive Guide | Section 7.2 |
| VPC Security | container_networking_supplement.md | Security boundaries |
| Threat Detection | security_services_supplement.md | GuardDuty |
| Vulnerability Mgmt | security_services_supplement.md | Inspector |
| Compliance Monitoring | aws_config_supplement.md | Conformance packs |

### Networking

| Concept | Document | Section |
|---------|----------|---------|
| VPC Design | Comprehensive Guide | Section 5 |
| Subnetting | Comprehensive Guide | Section 5.1 |
| Routing | Comprehensive Guide | Section 5.2 |
| Container Networking | container_networking_supplement.md | ECS/EKS modes |
| Service Discovery | container_networking_supplement.md | Cloud Map |
| Load Balancing | Comprehensive Guide | Section 5.3 |

### Cost Optimization

| Concept | Document | Section |
|---------|----------|---------|
| Compute Savings | Comprehensive Guide | Section 11.1 |
| Storage Tiers | Comprehensive Guide | Section 11.2 |
| Network Costs | Comprehensive Guide | Section 11.3 |
| RI & Savings Plans | Comprehensive Guide | Section 11.1 |

### Migration

| Concept | Document | Section |
|---------|----------|---------|
| 7 R's Strategy | Comprehensive Guide | Section 10.1 |
| DMS Migration | Comprehensive Guide | Section 16.1 |
| Server Migration | Comprehensive Guide | Section 16.2 |
| Data Migration | Comprehensive Guide | Section 16.3-16.4 |

---

## By Architecture Pattern

### Serverless

| Pattern | Document | Section |
|---------|----------|---------|
| Lambda Functions | Comprehensive Guide | Section 9.1 |
| API Gateway + Lambda | Comprehensive Guide | Section 9.1 |
| Event-Driven | Comprehensive Guide | Section 9.2 |
| Step Functions | Comprehensive Guide | Section 9.3 |

### Container-Based

| Pattern | Document | Section |
|---------|----------|---------|
| ECS awsvpc Mode | container_networking_supplement.md | ECS networking |
| EKS VPC CNI | container_networking_supplement.md | EKS networking |
| Service Mesh | container_networking_supplement.md | App Mesh |
| Fargate | container_networking_supplement.md | Serverless containers |

### Multi-Tier

| Pattern | Document | Section |
|---------|----------|---------|
| Web-App-DB | Comprehensive Guide | Section 12.1 |
| Load Balancer Patterns | Comprehensive Guide | Section 5.3 |
| Auto Scaling | Comprehensive Guide | Section 9 |

### Event-Driven

| Pattern | Document | Section |
|---------|----------|---------|
| EventBridge | Comprehensive Guide | Section 9.2 |
| SQS + Lambda | Comprehensive Guide | Section 9.2 |
| SNS Fan-Out | Comprehensive Guide | Section 9.2 |

### Disaster Recovery

| Pattern | Document | Section |
|---------|----------|---------|
| Backup & Restore | Comprehensive Guide | Section 8.4 |
| Pilot Light | Comprehensive Guide | Section 8.4 |
| Warm Standby | Comprehensive Guide | Section 8.4 |
| Active-Active | Comprehensive Guide | Section 8.4 |
| AWS DRS | drs_implementation_supplement.md | Implementation |

---

## Supplement Cross-Reference

### Container Networking Supplement Links

| References | Target Document |
|------------|----------------|
| ECS Service Discovery | aws_backup_supplement.md (cross-account patterns) |
| EKS Load Balancing | route53_implementation_supplement.md (failover) |
| Network Policies | security_services_supplement.md (defense in depth) |

### Security Services Supplement Links

| References | Target Document |
|------------|----------------|
| GuardDuty → Security Hub | Already integrated |
| Inspector Remediation | systems_manager_supplement.md (Automation) |
| Access Analyzer → Config | aws_config_supplement.md (compliance) |
| Security Hub → Config | aws_config_supplement.md (conformance packs) |

### CI/CD Supplement Links

| References | Target Document |
|------------|----------------|
| Blue/Green + Route 53 | route53_implementation_supplement.md (routing) |
| Canary + CloudWatch | Comprehensive Guide (monitoring) |
| Multi-Account Pipeline | security_services_supplement.md (cross-account) |

### Systems Manager Links

| References | Target Document |
|------------|----------------|
| Patch Manager → Config | aws_config_supplement.md (compliance) |
| Automation → DRS | drs_implementation_supplement.md (recovery) |
| Session Manager → Security | security_services_supplement.md (access) |

### DRS Supplement Links

| References | Target Document |
|------------|----------------|
| DRS + Route 53 | route53_implementation_supplement.md (failover) |
| DRS + Backup | aws_backup_supplement.md (complementary strategies) |

### Route 53 Links

| References | Target Document |
|------------|----------------|
| Failover + DRS | drs_implementation_supplement.md (automated DR) |
| Health Checks + ALB | container_networking_supplement.md (ingress) |

---

## Implementation Guides Index

### Step-by-Step Configuration Guides

| Task | Document | Section |
|------|----------|---------|
| Configure Systems Manager Patch Manager | systems_manager_supplement.md | Section 2 |
| Set up Patch Baselines | systems_manager_supplement.md | Section 2.2 |
| Create Custom Automation Document | systems_manager_supplement.md | Section 3.4 |
| Configure Session Manager Logging | systems_manager_supplement.md | Section 4.6 |
| Create Parameter Store Hierarchy | systems_manager_supplement.md | Section 5.4 |
| Set up AWS Config Recorder | aws_config_supplement.md | Section 2 |
| Create Config Rule | aws_config_supplement.md | Section 3.3 |
| Configure Auto-Remediation | aws_config_supplement.md | Section 4.3 |
| Enable GuardDuty | security_services_supplement.md | Section 2.4 |
| Set up GuardDuty Multi-Account | security_services_supplement.md | Section 2.5 |
| Enable Security Hub | security_services_supplement.md | Section 3.3 |
| Enable Macie | security_services_supplement.md | Section 4.3 |
| Enable Inspector | security_services_supplement.md | Section 5.3 |
| Create Backup Plan | aws_backup_supplement.md | Section 2 |
| Configure Cross-Region Backup | aws_backup_supplement.md | Section 4 |
| Set up Cross-Account Backup | aws_backup_supplement.md | Section 5 |
| Configure DRS | drs_implementation_supplement.md | Section 3 |
| Set up Route 53 Failover | route53_implementation_supplement.md | Section 3 |
| Configure ECS awsvpc Mode | container_networking_supplement.md | Section 2 |
| Configure EKS VPC CNI | container_networking_supplement.md | Section 3 |
| Set up CI/CD Pipeline | cicd_implementation_supplement.md | Section 2 |
| Configure Blue/Green Deployment | cicd_implementation_supplement.md | Section 3 |
| Configure Canary Deployment | cicd_implementation_supplement.md | Section 4 |

### Decision Trees

| Decision | Document | Location |
|----------|----------|----------|
| ECS vs EKS vs Lambda | container_networking_supplement.md | Section 8 |
| Parameter Store vs Secrets Manager | systems_manager_supplement.md | Section 5.6 |
| Patch Policy vs Maintenance Window | systems_manager_supplement.md | Section 2.3 |
| Session Manager vs SSH | systems_manager_supplement.md | Section 8.1 |
| Backup Storage Tier Selection | aws_backup_supplement.md | Section 2.4 |
| When to Use Security Hub | security_services_supplement.md | Section 8.2 |
| Security Services Selection | security_services_supplement.md | Section 8.2 |

### Troubleshooting Guides

| Issue | Document | Section |
|-------|----------|---------|
| SSM Agent Issues | systems_manager_supplement.md | Section 11.1 |
| Session Manager Connection | systems_manager_supplement.md | Section 11.2 |
| Patch Manager Failures | systems_manager_supplement.md | Section 11.3 |
| Config Recorder Issues | aws_config_supplement.md | Section 9.1 |
| Remediation Failures | aws_config_supplement.md | Section 9.4 |
| Backup Job Failures | aws_backup_supplement.md | Section 10 |

---

## Document Summary

| Document | Lines | Primary Focus | Key Supplements Referenced |
|----------|-------|---------------|---------------------------|
| AWS_Solutions_Architect_Comprehensive_Guide.md | 4,426 | Foundation | All supplements |
| container_networking_supplement.md | 559 | ECS/EKS networking | Route 53, DRS |
| route53_implementation_supplement.md | 609 | DNS failover | DRS, Container |
| drs_implementation_supplement.md | 651 | Disaster recovery | Route 53, Backup |
| cicd_implementation_supplement.md | 877 | CI/CD pipelines | Route 53, Security |
| systems_manager_supplement.md | 1,179 | Operations | Config, Security |
| aws_config_supplement.md | 954 | Compliance | Systems Manager |
| security_services_supplement.md | 1,154 | Security monitoring | Config, Systems Manager |
| aws_backup_supplement.md | 1,106 | Data protection | DRS |

**Total Documentation:** 12,115 lines of validated content (measured 2026-02-04)

---

*Last Updated: 2026-02-04*
