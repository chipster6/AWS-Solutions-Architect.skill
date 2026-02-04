# GitHub - scheema/AWS-SAP-C02: AWS Solution Architect Certification Notes

> Source: https://github.com/scheema/AWS-SAP-C02
> Cached: 2026-02-04T21:56:30.731Z

---

## AWS-SAP-C02

[](#aws-sap-c02)
# AWS Solution Architect Certification Exam Guide Reference

[](#aws-solution-architect-certification-exam-guide-reference)
## Domain 1: Design Solutions for Organizational Complexity 26%

[](#domain-1-design-solutions-for-organizational-complexity-26)
### Task Statement 1: Architect network connectivity strategies.

[](#task-statement-1-architect-network-connectivity-strategies)
#### Knowledge of:

[](#knowledge-of)

- AWS global infrastructure

- AWS networking concepts (for example, Amazon VPC, AWS Direct Connect, AWS VPN, transitive routing, AWS container services)

- Hybrid DNS concepts (for example, Amazon Route 53 Resolver, on-premises DNS integration )

- Network segmentation (for example, subnetting, IP addressing, connectivity among VPCs)

- Network traffic monitoring

#### Skills in:

[](#skills-in)

- Evaluating connectivity options for multiple VPCs

- Evaluating connectivity options for on-premises, co-location, and cloud integration

- Selecting AWS Regions and Availability Zones based on network and latency requirements

- Troubleshooting traffic flows by using AWS tools

- Utilizing service endpoints for service integrations

### Task Statement 2: Prescribe security controls.

[](#task-statement-2-prescribe-security-controls)
#### Knowledge of:

[](#knowledge-of-1)

- AWS Identity and Access Management (IAM) and AWS Single Sign-On

- Route tables, security groups, and network ACLs

Encryption keys and certificate management (for example, AWS Key Management Service
[AWS KMS], AWS Certificate Manager [ACM])
- AWS security, identity, and compliance tools (for example, AWS CloudTrail, AWS Identity and Access Management Access Analyzer, AWS Security Hub, Amazon Inspector) 1

#### Skills in:

[](#skills-in-1)

- Evaluating cross-account access management

- Integrating with third-party identity providers

- Deploying encryption strategies for data at rest and data in transit

- Developing a strategy for centralized security event notifications and auditing

### Task Statement 3: Design reliable and resilient architectures.

[](#task-statement-3-design-reliable-and-resilient-architectures)
#### Knowledge of:

[](#knowledge-of-2)

- Recovery time objectives (RTOs) and recovery point objectives (RPOs)

Disaster recovery strategies (for example, using AWS Elastic Disaster Recovery [CloudEndure
Disaster Recovery], pilot light, warm standby, and multi-site)
- Data backup and restoration

#### Skills in:

[](#skills-in-2)

- Designing disaster recovery solutions based on RTO and RPO requirements

- Implementing architectures to automatically recover from failure

- Developing the optimal architecture by considering scale-up and scale-out options

Designing an effective backup and restoration strategy
Task Statement 4: Design a multi-account AWS environment.

#### Knowledge of:

[](#knowledge-of-3)

- AWS Organizations and AWS Control Tower

- Multi-account event notifications

- AWS resource sharing across environments

#### Skills in:

[](#skills-in-3)

- Evaluating the most appropriate account structure for organizational requirements

- Recommending a strategy for central logging and event notifications

- Developing a multi-account governance model

### Task Statement 5: Determine cost optimization and visibility strategies.

[](#task-statement-5-determine-cost-optimization-and-visibility-strategies)
#### Knowledge of:

[](#knowledge-of-4)

AWS cost and usage monitoring tools (for example, AWS Trusted Advisor, AWS Pricing
Calculator, AWS Cost Explorer, AWS Budgets)
- AWS purchasing options (for example, Reserved Instances, Savings Plans, Spot Instances)

AWS right-sizing visibility tools (for example, AWS Compute Optimizer, Amazon S3 Storage
Lens)

#### Skills in:

[](#skills-in-4)

- Monitoring cost and usage with AWS tools

- Developing an effective tagging strategy that maps costs to business units

- Understanding how purchasing options affect cost and performance

## Domain 2: Design for New Solutions 29%

[](#domain-2-design-for-new-solutions-29)
### Task Statement 1: Design a deployment strategy to meet business requirements.

[](#task-statement-1-design-a-deployment-strategy-to-meet-business-requirements)
#### Knowledge of:

[](#knowledge-of-5)

- Infrastructure as code (IaC) (for example, AWS CloudFormation)

- Continuous integration/continuous delivery (CI/CD)

- Change management processes

- Configuration management tools (for example, AWS Systems Manager)

#### Skills in:

[](#skills-in-5)

- Determining an application or upgrade path for new services and features

- Selecting services to develop deployment strategies and implement appropriate rollback mechanisms

- Adopting managed services as needed to reduce infrastructure provisioning and patching overhead

- Making advanced technologies accessible by delegating complex development and deployment tasks to AWSVersion

### Task Statement 2: Design a solution to ensure business continuity.

[](#task-statement-2-design-a-solution-to-ensure-business-continuity)
#### Knowledge of:

[](#knowledge-of-6)

- AWS global infrastructure

- AWS networking concepts (for example, Route 53, routing methods)

- RTOs and RPOs

- Disaster recovery scenarios (for example, backup and restore, pilot light, warm standby, multi-site)

- Disaster recovery solutions on AWS

#### Skills in:

[](#skills-in-6)

- Configuring disaster recovery solutions

- Configuring data and database replication

- Performing disaster recovery testing

- Architecting a backup solution that is automated, is cost-effective, and supports business continuity across multiple Availability Zones and/or AWS Regions

- Designing an architecture that provides application and infrastructure availability in the event of a disruption

- Leveraging processes and components for centralized monitoring to proactively recover from system failures

### Task Statement 3: Determine security controls based on requirements.

[](#task-statement-3-determine-security-controls-based-on-requirements)
#### Knowledge of:

[](#knowledge-of-7)

- IAM

- Route tables, security groups, and network ACLs

- Encryption options for data at rest and data in transit

- AWS service endpoints

- Credential management services

- AWS managed security services (for example, AWS Shield, AWS WAF, Amazon GuardDuty, AWS Security Hub)

#### Skills in:

[](#skills-in-7)

- Specifying IAM users and IAM roles that adhere to the principle of least privilege access

- Specifying inbound and outbound network flows by using security group rules and network ACL rules

- Developing attack mitigation strategies for large-scale web applications

- Developing encryption strategies for data at rest and data in transit

- Specifying service endpoints for service integrations

- Developing strategies for patch management to remain compliant with organizational standards

### Task Statement 4: Design a strategy to meet reliability requirements.

[](#task-statement-4-design-a-strategy-to-meet-reliability-requirements)
#### Knowledge of:

[](#knowledge-of-8)

- AWS global infrastructure

- AWS storage services and replication strategies (for example Amazon S3, Amazon RDS, Amazon ElastiCache)

- Multi-AZ and multi-Region architectures

- Auto scaling policies and events

- Application integration (for example, Amazon Simple Notification Service [Amazon SNS], Amazon Simple Queue Service [Amazon SQS], AWS Step Functions)

- Service quotas and limits

#### Skills in:

[](#skills-in-8)

- Designing highly available application environments based on business requirements

- Leveraging advanced techniques to design for failure and ensure seamless system recoverability

- Implementing loosely coupled dependencies

- Operating and maintaining high-availability architectures (for example, application failovers, database failovers)

- Leveraging AWS managed services for high availability

Implementing DNS routing policies (for example, Route 53 latency-based routing, geolocation routing, simple routing)
Task Statement 5: Design a solution to meet performance objectives.

#### Knowledge of:

[](#knowledge-of-9)

- Performance monitoring technologies

- Storage options on AWS

- Instance families and use cases

- Purpose-built databases

#### Skills in:

[](#skills-in-9)

- Designing large-scale application architectures for a variety of access patterns

- Designing an elastic architecture based on business objectives

- Applying design patterns to meet performance objectives with caching, buffering, and replicas

- Developing a process methodology for selecting purpose-built services for required tasks

- Designing a right-sizing strategy

### Task Statement 6: Determine a cost optimization strategy to meet solution goals and objectives.

[](#task-statement-6-determine-a-cost-optimization-strategy-to-meet-solution-goals-and-objectives)
#### Knowledge of:

[](#knowledge-of-10)

- AWS cost and usage monitoring tools (for example, Cost Explorer, Trusted Advisor, AWS Pricing Calculator)

- Pricing models (for example, Reserved Instances, Savings Plans)

- Storage tiering

- Data transfer costs

- AWS managed service offerings

#### Skills in:

[](#skills-in-10)

- Identifying opportunities to select and right size infrastructure for cost-effective resources

- Identifying appropriate pricing models

- Performing data transfer modeling and selecting services to reduce data transfer costs

- Developing a strategy and implementing controls for expenditure and usage awareness

## Domain 3: Continuous Improvement for Existing Solutions 25%

[](#domain-3-continuous-improvement-for-existing-solutions-25)
### Task Statement 1: Determine a strategy to improve overall operational excellence.

[](#task-statement-1-determine-a-strategy-to-improve-overall-operational-excellence)
#### Knowledge of:

[](#knowledge-of-11)

- Alerting and automatic remediation strategies

Disaster recovery planning
• Monitoring and logging solutions (for example, Amazon CloudWatch)
- CI/CD pipelines and deployment strategies (for example, blue/green, all-at-once, rolling)

- Configuration management tools (for example, Systems Manager)

#### Skills in:

[](#skills-in-11)

- Determining the most appropriate logging and monitoring strategy

- Evaluating current deployment processes for improvement opportunities

- Prioritizing opportunities for automation within a solution stack

- Recommending the appropriate AWS solution to enable configuration management automation

- Engineering failure scenario activities to support and exercise an understanding of recovery actions

### Task Statement 2: Determine a strategy to improve security.

[](#task-statement-2-determine-a-strategy-to-improve-security)
#### Knowledge of:

[](#knowledge-of-12)

- Data retention, data sensitivity, and data regulatory requirements

- Automated monitoring and remediation strategies (for example, AWS Config rules)

- Secrets management (for example, Systems Manager, AWS Secrets Manager)

- Principle of least privilege access

- Security-specific AWS solutions

- Patching practices

- Backup practices and methods

#### Skills in:

[](#skills-in-12)

- Evaluating a strategy for the secure management of secrets and credentials

- Auditing an environment for least privilege access

- Reviewing implemented solutions to ensure security at every layer

- Reviewing comprehensive traceability of users and services

- Prioritizing automated responses to the detection of vulnerabilities

- Designing and implementing a patch and update process

- Designing and implementing a backup process

- Employing remediation techniques

### Task Statement 3: Determine a strategy to improve performance.

[](#task-statement-3-determine-a-strategy-to-improve-performance)
#### Knowledge of:

[](#knowledge-of-13)

- High-performing systems architectures (for example, auto scaling, instance fleets, and placement groups)

- Global service offerings (for example, AWS Global Accelerator, Amazon CloudFront, and edge computing services)Version 1.0 SAP-C02 8 | PAGE

- Monitoring tool sets and services (for example, CloudWatch)

- Service level agreements (SLAs) and key performance indicators (KPIs)

#### Skills in:

[](#skills-in-13)

- Translating business requirements to measurable metrics

- Testing potential remediation solutions and making recommendations

- Proposing opportunities for the adoption of new technologies and managed services

- Assessing solutions and applying right sizing based on requirements

- Identifying and examining performance bottlenecks

### Task Statement 4: Determine a strategy to improve reliability.

[](#task-statement-4-determine-a-strategy-to-improve-reliability)
#### Knowledge of:

[](#knowledge-of-14)

- AWS global infrastructure

- Data replication methods

- Scaling methodologies (for example, load balancing, auto scaling)

- High availability and resiliency

- Disaster recovery methods and tools

- Service quotas and limits

#### Skills in:

[](#skills-in-14)

- Understanding application growth and usage trends

- Evaluating existing architecture to determine areas that are not sufficiently reliable

- Remediating single points of failure

- Enabling data replication, self-healing, and elastic features and services

### Task Statement 5: Identify opportunities for cost optimizations.

[](#task-statement-5-identify-opportunities-for-cost-optimizations)
#### Knowledge of:

[](#knowledge-of-15)

- Cost-conscious architecture choices (for example, utilizing Spot Instances, scaling policies, and right-sizing resources)

- Price model adoptions (for example, Reserved Instances, Savings Plans)

- Networking and data transfer costs

- Cost management, alerting, and reporting

#### Skills in:

[](#skills-in-15)

- Analyzing usage reports to identify underutilized and overutilized resources

- Utilizing AWS solutions to identify unused resources

- Designing billing alarms based on expected usage patterns

- Investigating AWS Cost and Usage Reports at a granular level

- Utilizing tagging for cost allocation and reporting

## Domain 4: Accelerate Workload Migration and Modernization 20%

[](#domain-4-accelerate-workload-migration-and-modernization-20)
### Task Statement 1: Select existing workloads and processes for potential migration.

[](#task-statement-1-select-existing-workloads-and-processes-for-potential-migration)
#### Knowledge of:

[](#knowledge-of-16)

- Migration assessment and tracking tools (for example, AWS Migration Hub)

- Portfolio assessment

- Asset planning

- Prioritization and migration of workloads (for example, wave planning)

#### Skills in:

[](#skills-in-16)

- Completing an application migration assessment

- Evaluating applications according to the seven common migration strategies (7Rs)

- Evaluating total cost of ownership (TCO)

### Task Statement 2: Determine the optimal migration approach for existing workloads.

[](#task-statement-2-determine-the-optimal-migratio

... [Content truncated]