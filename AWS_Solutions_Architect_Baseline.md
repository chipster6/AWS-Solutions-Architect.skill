# AWS Solutions Architect: Comprehensive Knowledge Baseline

**Version:** 1.0.0  
**Last Updated:** 2026-02-04  
**Scope:** Certification preparation (SAA-C03) and enterprise architecture practices

---

## Table of Contents

1. [AWS Well-Architected Framework](#1-aws-well-architected-framework)
2. [Compute Services](#2-compute-services)
3. [Storage Services](#3-storage-services)
4. [Networking & VPC](#4-networking--vpc)
5. [Database Services](#5-database-services)
6. [Security & Identity](#6-security--identity)
7. [High Availability & Disaster Recovery](#7-high-availability--disaster-recovery)
8. [Monitoring & Observability](#8-monitoring--observability)
9. [Load Balancing & Auto Scaling](#9-load-balancing--auto-scaling)
10. [DNS & Content Delivery](#10-dns--content-delivery)
11. [Serverless Architecture](#11-serverless-architecture)
12. [Migration & Data Transfer](#12-migration--data-transfer)
13. [Cost Optimization](#13-cost-optimization)
14. [Exam Strategies](#14-exam-strategies)

---

## 1. AWS Well-Architected Framework

### The Six Pillars

The AWS Well-Architected Framework provides architectural best practices for designing and operating reliable, secure, efficient, and cost-effective systems.

#### 1.1 Operational Excellence
- **Design Principles:**
  - Perform operations as code (IaC, automation)
  - Annotate documentation (comments, README, runbooks)
  - Make frequent, small, reversible changes
  - Refine operations procedures frequently
  - Anticipate failure
  - Learn from all operational failures
- **Key Services:** CloudWatch, CloudFormation, AWS Config, Systems Manager
- **Best Practices:**
  - Implement CI/CD pipelines
  - Create runbooks for common scenarios
  - Use infrastructure as code for all resources
  - Monitor operational health with dashboards

#### 1.2 Security
- **Design Principles:**
  - Implement strong identity foundation (IAM, least privilege)
  - Enable traceability (CloudTrail, logs)
  - Apply security at all layers
  - Automate security best practices
  - Protect data in transit and at rest
  - Keep people away from data
  - Prepare for security events
- **Key Services:** IAM, KMS, WAF, Shield, Secrets Manager, GuardDuty
- **Best Practices:**
  - Use IAM roles, not access keys
  - Enable MFA for root and privileged users
  - Encrypt everything by default
  - Implement defense in depth
  - Regular security audits

#### 1.3 Reliability
- **Design Principles:**
  - Automatically recover from failure
  - Test recovery procedures (chaos engineering)
  - Scale horizontally to increase aggregate workload availability
  - Stop guessing capacity
  - Manage change in automation
- **Key Services:** Auto Scaling, Multi-AZ RDS, S3, Route 53 health checks
- **Best Practices:**
  - Design for failure (everything fails eventually)
  - Implement multi-AZ and multi-region architectures
  - Use health checks and automatic failover
  - Decouple components with queues
  - Regular DR testing

#### 1.4 Performance Efficiency
- **Design Principles:**
  - Democratize advanced technologies (managed services)
  - Go global in minutes
  - Use serverless architectures
  - Experiment more often
  - Consider mechanical sympathy (understand how services work)
- **Key Services:** Lambda, DynamoDB, ElastiCache, CloudFront
- **Best Practices:**
  - Right-size instances based on actual usage
  - Use caching at multiple layers
  - Optimize database queries
  - Use read replicas for read-heavy workloads
  - Leverage managed services

#### 1.5 Cost Optimization
- **Design Principles:**
  - Implement cloud financial management
  - Adopt a consumption model (pay-as-you-go)
  - Measure overall efficiency
  - Stop spending money on undifferentiated heavy lifting
  - Analyze and attribute expenditure
- **Key Services:** Cost Explorer, Budgets, Savings Plans, Reserved Instances
- **Best Practices:**
  - Tag everything for cost allocation
  - Use lifecycle policies for S3
  - Purchase Reserved Instances for predictable workloads
  - Right-size continuously
  - Delete unused resources

#### 1.6 Sustainability
- **Design Principles:**
  - Understand your impact
  - Establish sustainability goals
  - Maximize utilization
  - Use efficient hardware and software offerings
  - Use managed services
  - Reduce downstream impact
- **Key Services:** Graviton instances, Spot instances, S3 Intelligent-Tiering
- **Best Practices:**
  - Use ARM-based Graviton processors
  - Implement load smoothing
  - Use Spot instances for fault-tolerant workloads
  - Right-size to reduce waste
  - Remove unused resources

---

## 2. Compute Services

### 2.1 Amazon EC2 (Elastic Compute Cloud)

**Key Concepts:**
- **Instance Types:**
  - **General Purpose (T3, T4g, M6i, M7g):** Balanced compute, memory, networking
  - **Compute Optimized (C6i, C7g):** High-performance processors (gaming, ML)
  - **Memory Optimized (R6i, X2idn):** In-memory databases, real-time big data
  - **Accelerated Computing (P4, G6):** GPU instances (ML, graphics)
  - **Storage Optimized (I4i, Im4gn):** High IOPS (databases, data warehouses)

- **Purchase Options:**
  - **On-Demand:** Pay by second, no commitment, highest cost
  - **Reserved Instances (1-3 years):** 40-72% discount, predictable workloads
  - **Savings Plans:** Flexible commitment ($/hour), compute or EC2 specific
  - **Spot Instances:** Up to 90% discount, interruptible, fault-tolerant workloads
  - **Dedicated Hosts:** Physical servers, software licensing requirements

- **Key Features:**
  - **EBS:** Persistent block storage (gp3, io2, st1, sc1)
  - **Instance Store:** Ephemeral SSD storage (highest performance)
  - **AMI:** Amazon Machine Images for launching instances
  - **Placement Groups:** Cluster, spread, partition for performance
  - **ENI:** Elastic Network Interfaces for networking

**Best Practices:**
- Use latest generation instance types for better price/performance
- Choose Graviton (ARM) instances for better sustainability and cost
- Use gp3 volumes instead of gp2 for predictable performance
- Enable detailed monitoring for production workloads
- Use AWS Systems Manager Session Manager instead of SSH keys

### 2.2 AWS Lambda (Serverless Compute)

**Key Concepts:**
- **Execution Model:** Event-driven, stateless functions
- **Runtime Support:** Node.js, Python, Java, Go, Ruby, .NET, custom runtimes
- **Limits:**
  - 15-minute timeout
  - 10 GB memory
  - 6 MB payload (sync), 256 KB (async)
  - 1000 concurrent executions (soft limit)
- **Triggers:** API Gateway, S3, EventBridge, SNS, SQS, DynamoDB Streams
- **Layers:** Share common code across functions

**Best Practices:**
- Keep functions small and focused (single responsibility)
- Use environment variables for configuration
- Implement proper error handling and retries
- Use Lambda Powertools for observability
- Optimize cold starts (provisioned concurrency for critical paths)
- Use Step Functions for orchestrating multiple Lambdas

### 2.3 Amazon ECS (Elastic Container Service)

**Launch Types:**
- **Fargate:** Serverless containers, no EC2 management
- **EC2:** Full control over instances, cost-effective at scale
- **External:** On-premises container orchestration

**Key Concepts:**
- **Task Definition:** Blueprint for tasks (containers, volumes, networking)
- **Service:** Maintains desired count of tasks, handles deployments
- **Cluster:** Logical grouping of tasks or services
- **Capacity Providers:** Auto Scaling integration

### 2.4 AWS Fargate

**Use Cases:**
- Microservices architecture
- Batch processing
- Machine learning inference
- Web applications and APIs

**Benefits:**
- No server management
- Pay per use (vCPU and memory)
- Automatic scaling
- Isolated environments

### 2.5 AWS Batch

**Key Concepts:**
- Fully managed batch processing
- Dynamically provisions optimal compute resources
- Supports EC2 and Fargate
- Job queues, compute environments, job definitions

**Best Practices:**
- Use Spot instances for cost savings on fault-tolerant workloads
- Configure job retry strategies
- Use job dependencies for complex workflows

### 2.6 AWS Elastic Beanstalk

**Use Cases:**
- Quick deployment of web applications
- Managed platform for developers
- Supports multiple platforms (Java, .NET, PHP, Node.js, Python, Ruby, Go, Docker)

**Key Concepts:**
- Application: Container for environments
- Environment: Collection of AWS resources running application
- Version: Specific code deployment
- Platform: OS, web server, runtime

---

## 3. Storage Services

### 3.1 Amazon S3 (Simple Storage Service)

**Key Concepts:**
- **Object Storage:** Unlimited storage, 99.999999999% (11 9's) durability
- **Buckets:** Global unique namespace, region-specific
- **Objects:** Data + metadata (up to 5 TB per object)
- **Versioning:** Keep multiple versions, recover from deletion

**Storage Classes:**

| Class | Use Case | Durability | Availability | Min Duration |
|-------|----------|------------|--------------|--------------|
| S3 Standard | Frequently accessed | 99.999999999% | 99.99% | None |
| Intelligent-Tiering | Unknown/variable access | 99.999999999% | 99.9% | None |
| Standard-IA | Infrequent access | 99.999999999% | 99.9% | 30 days |
| One Zone-IA | Infrequent, non-critical | 99.999999999% | 99.5% | 30 days |
| Glacier Instant | Archive, millisecond access | 99.999999999% | 99.9% | 90 days |
| Glacier Flexible | Archive, minutes access | 99.999999999% | 99.99% | 90 days |
| Glacier Deep Archive | Archive, hours access | 99.999999999% | 99.9% | 180 days |
| Express One Zone | High-performance, single AZ | 99.999999999% | 99.95% | None |

**Key Features:**
- **Lifecycle Policies:** Automate transitions, expiration
- **Cross-Region Replication (CRR):** Async replication between regions
- **Same-Region Replication (SRR):** Replication within same region
- **Event Notifications:** Trigger Lambda, SQS, SNS on object events
- **S3 Select:** Query data in place (SQL-like)
- **Access Points:** Manage access at scale
- **Object Lock:** WORM (Write Once Read Many) for compliance
- **Pre-Signed URLs:** Temporary access for private objects

**Security Best Practices:**
- Block public access by default
- Use bucket policies and IAM policies
- Enable versioning and MFA delete
- Use server-side encryption (SSE-S3, SSE-KMS, SSE-C)
- Enable CloudTrail logging for object-level events
- Use VPC endpoints to keep traffic within AWS

### 3.2 Amazon EBS (Elastic Block Store)

**Volume Types:**

| Type | Use Case | IOPS | Throughput | Max Size |
|------|----------|------|------------|----------|
| gp3 | General purpose | 16,000 | 1,000 MB/s | 16 TiB |
| gp2 | General purpose (legacy) | 16,000 | 250 MB/s | 16 TiB |
| io2 | I/O intensive, critical apps | 256,000 | 4,000 MB/s | 64 TiB |
| io1 | I/O intensive (legacy) | 256,000 | 1,000 MB/s | 16 TiB |
| st1 | Throughput optimized | 500 | 500 MB/s | 16 TiB |
| sc1 | Cold HDD | 250 | 250 MB/s | 16 TiB |

**Key Features:**
- **Snapshots:** Incremental backups to S3
- **Multi-Attach:** Attach single io1/io2 volume to multiple EC2 instances (clustered apps)
- **Encryption:** KMS encryption at rest
- **Elastic Volumes:** Modify size, type, IOPS without detaching

**Best Practices:**
- Use gp3 for new workloads (better price/performance than gp2)
- Use io2 Block Express for most demanding workloads
- Take frequent snapshots for backup
- Use EBS-optimized instances for consistent performance
- Separate data volumes from root volumes

### 3.3 Amazon EFS (Elastic File System)

**Key Concepts:**
- Fully managed NFS service
- Multiple EC2 instances can access simultaneously
- Automatic scaling (petabytes)
- Region-wide availability

**Storage Classes:**
- **Standard:** Frequently accessed files
- **Infrequent Access (IA):** Cost-optimized for less accessed files
- **Archive:** Rarely accessed files

**Performance Modes:**
- **General Purpose:** Latency-sensitive (web serving, CMS)
- **Max I/O:** High aggregate throughput/high IOPS (big data, media)

**Throughput Modes:**
- **Bursting:** Scales with file system size
- **Provisioned:** Fixed throughput regardless of size
- **Elastic:** Automatically scales based on workload

### 3.4 Amazon FSx

**Variants:**
- **FSx for Windows File Server:** SMB protocol, Windows workloads, AD integration
- **FSx for Lustre:** High-performance computing (HPC), ML, analytics
- **FSx for NetApp ONTAP:** Hybrid cloud with NetApp features
- **FSx for OpenZFS:** Managed OpenZFS (NFS, SMB, iSCSI)

### 3.5 Storage Gateway

**Types:**
- **File Gateway:** NFS/SMB to S3, local caching
- **Volume Gateway:** iSCSI block storage, backed by S3
- **Tape Gateway:** Virtual tape library (VTL), backup software compatible

**Use Cases:**
- Hybrid cloud storage
- Backup and archival
- Disaster recovery
- Cloud migration

---

## 4. Networking & VPC

### 4.1 Amazon VPC (Virtual Private Cloud)

**Key Concepts:**
- **CIDR Blocks:** IP address ranges (e.g., 10.0.0.0/16)
- **Subnets:** Subdivisions of VPC CIDR, tied to AZ
  - Public subnets: Route to Internet Gateway
  - Private subnets: No direct internet route
  - VPN-only: Route to VGW, not IGW
- **Route Tables:** Define traffic routing rules
- **Internet Gateway (IGW):** VPC attachment for internet access
- **NAT Gateway:** Allow private subnets outbound internet (not inbound)
- **Egress-Only Gateway:** IPv6 outbound only (no inbound)

**VPC Components:**
- **Security Groups:** Stateful firewall (instance level), allow rules only
- **Network ACLs:** Stateless firewall (subnet level), allow/deny rules
- **VPC Peering:** Connect two VPCs (same or different accounts/regions)
- **VPC Endpoints:** Private connectivity to AWS services
  - Gateway Endpoints: S3, DynamoDB (free, route table)
  - Interface Endpoints: Most AWS services (ENI-based, paid)
- **Transit Gateway:** Hub-and-spoke VPC and network connectivity
- **PrivateLink:** Private connectivity to services (VPC endpoints)

**VPC Design Best Practices:**
- Use multiple AZs (minimum 2, preferably 3) for high availability
- Separate public and private subnets
- Use NAT Gateway for outbound internet from private subnets
- Use VPC Flow Logs for network monitoring
- Implement least privilege security groups
- Use VPC endpoints to reduce data transfer costs and improve security
- Avoid overlapping CIDRs in peered VPCs

### 4.2 Direct Connect

**Key Concepts:**
- Dedicated network connection from on-premises to AWS
- Private connectivity (not over internet)
- Consistent network performance
- Port speeds: 1 Gbps, 10 Gbps, 100 Gbps
- Connection types: Dedicated, Hosted

**Components:**
- **Virtual Interfaces (VIF):**
  - Private VIF: Connect to VPC (Direct Connect Gateway)
  - Public VIF: Connect to AWS public services (S3, DynamoDB)
  - Transit VIF: Connect to Transit Gateway

### 4.3 VPN (Virtual Private Network)

**Types:**
- **Site-to-Site VPN:** Encrypted connection between on-premises and VPC
- **Client VPN:** Remote users to VPC (OpenVPN based)

**Components:**
- **Virtual Private Gateway (VGW):** VPC side of VPN
- **Customer Gateway (CGW):** On-premises side of VPN
- **Transit Gateway:** Can terminate multiple VPN connections

**Best Practices:**
- Use VPN for backup to Direct Connect
- Enable route propagation
- Use Accelerated Site-to-Site VPN for better performance

### 4.4 PrivateLink

**Key Concepts:**
- Private connectivity between VPCs and AWS services
- No internet gateway, NAT, VPN, or public IP required
- Interface VPC endpoints (powered by PrivateLink)
- PrivateLink services (expose your service to other VPCs)

### 4.5 AWS App Mesh

**Key Concepts:**
- Service mesh for microservices
- Standardizes service communication
- Observability and traffic control
- Works with ECS, EKS, EC2, Fargate

### 4.6 AWS Cloud Map

**Key Concepts:**
- Service discovery for cloud resources
- Register resources with custom names
- Health checking
- Integrates with ECS, EKS

---

## 5. Database Services

### 5.1 Amazon RDS (Relational Database Service)

**Supported Engines:**
- MySQL, PostgreSQL, MariaDB
- Oracle, SQL Server (bring your own license or license included)

**Key Features:**
- **Multi-AZ:** Synchronous replication to standby in different AZ
  - Automatic failover
  - No manual intervention
  - Used for high availability, not scaling
- **Read Replicas:** Asynchronous replication for read scaling
  - Up to 15 replicas
  - Can be in different regions
  - Automatic failover promotion
- **Aurora:** AWS-optimized database (see 5.2)
- **Parameter Groups:** Database configuration
- **Option Groups:** Additional features (Oracle, SQL Server)

**Instance Types:**
- **db.t3/t4g:** Burstable, dev/test
- **db.m6i/m7g:** General purpose
- **db.r6i/r7g:** Memory optimized

**Storage:**
- General Purpose (SSD) - gp3
- Provisioned IOPS (SSD) - io1/io2
- Magnetic (legacy)

**Backup:**
- Automated backups (1-35 days retention)
- Manual snapshots (unlimited retention)
- Point-in-time recovery

**Best Practices:**
- Enable Multi-AZ for production
- Use read replicas for read-heavy workloads
- Enable encryption at rest
- Use IAM database authentication when possible
- Enable Enhanced Monitoring and Performance Insights
- Use RDS Proxy for connection pooling

### 5.2 Amazon Aurora

**Key Concepts:**
- MySQL and PostgreSQL compatible
- 5x (MySQL) or 3x (PostgreSQL) performance improvement
- Auto-scaling storage (up to 128 TB)
- 15 read replicas (same region), minimal lag
- Continuous backup to S3
- Cross-region replication (Aurora Global Database)

**Aurora Architecture:**
- **Storage Layer:** Distributed across 3 AZs, 6 copies
- **Compute Layer:** Primary instance + read replicas
- **Shared Storage:** All instances access same storage

**Aurora Serverless:**
- v1: Auto-scales based on demand
- v2: Fine-grained scaling, instant scaling

**Aurora Global Database:**
- Cross-region replication (< 1 second lag)
- Disaster recovery with < 1 minute RPO
- Read scaling across regions

### 5.3 Amazon DynamoDB

**Key Concepts:**
- Fully managed NoSQL database
- Single-digit millisecond latency
- Unlimited throughput and storage
- Serverless (no capacity planning)

**Data Model:**
- **Tables:** Collection of items
- **Items:** Collection of attributes (max 400 KB per item)
- **Primary Key:**
  - Partition Key (single attribute)
  - Composite Key (partition + sort key)
- **Attributes:** Name-value pairs

**Capacity Modes:**
- **On-Demand:** Pay per request, unpredictable workloads
- **Provisioned:** RCU (read capacity units), WCU (write capacity units)
  - Auto Scaling adjusts capacity based on utilization
  - Reserved capacity for predictable workloads

**Indexes:**
- **Local Secondary Index (LSI):** Same partition key, different sort key (table creation only)
- **Global Secondary Index (GSI):** Different partition/sort keys (can add later)

**Features:**
- **DAX (DynamoDB Accelerator):** In-memory cache, microsecond latency
- **Streams:** Capture item-level changes
- **Global Tables:** Multi-region, multi-master replication
- **Transactions:** ACID transactions across multiple items
- **TTL:** Automatic item expiration
- **On-Demand Backup:** Point-in-time recovery (35 days)

**Best Practices:**
- Design for partition key distribution (avoid hot partitions)
- Use GSIs for alternate query patterns
- Use DAX for read-heavy, cacheable workloads
- Implement exponential backoff for throttling
- Use transactions only when necessary (2x cost)
- Enable point-in-time recovery

### 5.4 Amazon ElastiCache

**Engines:**
- **Redis:** Data structures, pub/sub, persistence
- **Memcached:** Simple key-value, multi-threaded

**Use Cases:**
- Session storage
- Real-time analytics
- Leaderboards
- Geospatial data
- Caching database queries

**Features:**
- Multi-AZ with auto-failover (Redis)
- Read replicas (Redis)
- Cluster mode (sharding)
- Backup and restore

### 5.5 Amazon DocumentDB

**Key Concepts:**
- MongoDB-compatible document database
- JSON data model
- Up to 15 read replicas
- Auto-scaling storage

### 5.6 Amazon Neptune

**Key Concepts:**
- Fully managed graph database
- Supports Property Graph and RDF
- SPARQL and Gremlin query languages
- Read replicas for query scaling

### 5.7 Amazon Timestream

**Key Concepts:**
- Fully managed time series database
- IoT, operational metrics, analytics
- Auto-scaling
- Built-in analytics functions

### 5.8 Amazon Keyspaces (for Apache Cassandra)

**Key Concepts:**
- Managed Cassandra-compatible database
- Serverless (on-demand or provisioned)
- Continuous backups
- Up to 3 read replicas per table

---

## 6. Security & Identity

### 6.1 AWS IAM (Identity and Access Management)

**Key Concepts:**
- **Users:** Individual identities (avoid long-term credentials)
- **Groups:** Collection of users with shared permissions
- **Roles:** Temporary credentials, assumed by users/services
- **Policies:** JSON documents defining permissions
  - Identity-based: Attached to users, groups, roles
  - Resource-based: Attached to resources (S3, SNS, SQS)
  - Trust policies: Define who can assume roles

**Policy Structure:**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow|Deny",
    "Action": "service:action",
    "Resource": "arn:aws:service:region:account:resource",
    "Condition": {
      "ConditionOperator": {"ConditionKey": "ConditionValue"}
    }
  }]
}
```

**Best Practices:**
- **Root Account:**
  - Don't use for day-to-day operations
  - Enable MFA
  - Lock away credentials
  - Don't share
- **Users & Roles:**
  - Use roles for applications (EC2, Lambda, ECS)
  - Use IAM Identity Center for workforce
  - Apply least privilege
  - Use managed policies as starting point
  - Regularly rotate credentials
  - Remove unused users/roles
  - Use Access Analyzer to identify unused permissions
- **Conditions:**
  - Source IP restrictions
  - VPC endpoint restrictions
  - MFA requirements
  - Time-based restrictions
  - Encryption requirements

### 6.2 AWS KMS (Key Management Service)

**Key Concepts:**
- Managed service for creating and controlling encryption keys
- FIPS 140-2 Level 2 validated HSMs
- Integrated with most AWS services

**Key Types:**
- **Symmetric:** Single key for encrypt/decrypt (AES-256)
  - Used by most AWS services
- **Asymmetric:** Key pairs (RSA, ECC)
  - Signing/verification
  - Encryption/decryption

**Key Material Origin:**
- **AWS Managed:** AWS creates and manages key material
- **Customer Managed:** You create and manage key material in KMS
- **External:** You import key material
- **CloudHSM:** Custom key store backed by CloudHSM

**Key Policies:**
- Required for customer managed keys
- Define who can use and manage keys
- Cannot be deleted without key policy allowing it

**Best Practices:**
- Enable key rotation (automatic for AWS managed)
- Use aliases for key management
- Separate keys by application/environment
- Use grants for temporary permissions
- Monitor CloudTrail logs for key usage

### 6.3 AWS CloudHSM

**Key Concepts:**
- Dedicated hardware security modules (HSMs)
- FIPS 140-2 Level 3 validated
- Full control over keys
- No AWS access to keys

**Use Cases:**
- Compliance requirements (FIPS 140-2 Level 3)
- Keys not exportable from HSM
- High-performance cryptographic operations

### 6.4 AWS Secrets Manager

**Key Concepts:**
- Store and rotate secrets (credentials, API keys, tokens)
- Automatic rotation with Lambda
- Cross-account access
- Versioning

**Best Practices:**
- Use for database credentials, API keys
- Enable automatic rotation
- Don't hardcode secrets in code
- Use IAM policies to control access

### 6.5 AWS Certificate Manager (ACM)

**Key Concepts:**
- Provision, manage, deploy SSL/TLS certificates
- Free public certificates
- Automatic renewal
- Integration with CloudFront, ALB, API Gateway

**Limitations:**
- Cannot export private keys for public certificates
- Use IAM Certificate Store or import for external use

### 6.6 AWS WAF (Web Application Firewall)

**Key Concepts:**
- Protect web applications from common exploits
- Integration with CloudFront, ALB, API Gateway, AppSync
- Managed rule sets (OWASP, IP reputation)
- Rate limiting
- Geo-blocking
- Custom rules

### 6.7 AWS Shield

**Shield Standard:**
- Free, automatic protection
- Protection against common DDoS attacks

**Shield Advanced:**
- Enhanced DDoS protection
- Cost protection (reimbursement for scaling charges)
- 24/7 DDoS Response Team (DRT)
- Application-layer protection with WAF

### 6.8 AWS GuardDuty

**Key Concepts:**
- Intelligent threat detection
- Uses machine learning
- Analyzes CloudTrail, VPC Flow Logs, DNS logs
- Finds compromised instances, reconnaissance, unauthorized access

### 6.9 AWS Security Hub

**Key Concepts:**
- Centralized security findings
- Aggregates from GuardDuty, Inspector, Macie, etc.
- Automated compliance checks
- Insights and prioritization

### 6.10 AWS Config

**Key Concepts:**
- Configuration history and change management
- Compliance monitoring
- Config rules (managed and custom)
- Remediation actions

**Use Cases:**
- Audit resource configurations
- Detect compliance violations
- Troubleshoot configuration changes
- Security analysis

### 6.11 AWS CloudTrail

**Key Concepts:**
- Audit logs of AWS API calls
- Account activity history
- Log file integrity validation
- Integration with CloudWatch Logs

**Types:**
- **Management Events:** Control plane operations (default enabled)
- **Data Events:** Data plane operations (S3 object-level, Lambda)
- **Insights Events:** Unusual API activity (additional cost)

**Best Practices:**
- Enable CloudTrail in all regions
- Enable log file validation
- Enable S3 bucket MFA delete
- Use organization trail for multi-account
- Enable Insights for anomaly detection

---

## 7. High Availability & Disaster Recovery

### 7.1 High Availability (HA) Patterns

**Multi-AZ Deployment:**
- Distribute resources across multiple Availability Zones
- Automatic failover within region
- Synchronous replication (databases)

**Multi-Region Deployment:**
- Active-active or active-passive
- Asynchronous replication
- Route 53 for traffic routing
- Lower latency for global users

### 7.2 Disaster Recovery (DR) Strategies

| Strategy | RTO | RPO | Cost | Complexity |
|----------|-----|-----|------|------------|
| **Backup & Restore** | Hours | 24+ hours | Low | Low |
| **Pilot Light** | Minutes-hours | Minutes | Medium | Medium |
| **Warm Standby** | Minutes | Minutes | Medium-High | Medium |
| **Active-Active** | Seconds-minutes | Near zero | High | High |

**Backup & Restore:**
- Regular backups to S3
- Cross-region replication
- Infrastructure as Code for quick provisioning
- Documented restoration procedures

**Pilot Light:**
- Minimal resources always running (core components)
- Scale up when needed
- RDS read replica in DR region
- S3 cross-region replication

**Warm Standby:**
- Scaled-down but fully functional environment
- Faster recovery than pilot light
- Regular data synchronization
- Automated failover possible

**Active-Active:**
- Full production environment in multiple regions
- Traffic distributed across regions
- Real-time data synchronization
- Automatic failover
- Highest availability, highest cost

### 7.3 Key DR Services

**AWS Elastic Disaster Recovery (DRS):**
- Automated recovery of on-premises and cloud workloads
- Continuous replication
- Point-in-time recovery
- Non-disruptive testing

**AWS Backup:**
- Centralized backup management
- Cross-region and cross-account backup
- Automated backup policies
- Compliance monitoring

### 7.4 RTO and RPO

**Recovery Time Objective (RTO):**
- Maximum acceptable downtime after disaster
- Time to restore service

**Recovery Point Objective (RPO):**
- Maximum acceptable data loss
- Time between last backup and disaster

**Calculation:**
- RTO drives architectural decisions
- RPO drives backup frequency
- Balance between cost and requirements

### 7.5 DR Best Practices

1. **Regular Testing:**
   - Test failover procedures
   - Validate data restoration
   - Document lessons learned
   - Update runbooks

2. **Automation:**
   - Automate failover where possible
   - Use Route 53 health checks
   - Lambda for automation
   - CloudFormation for infrastructure

3. **Documentation:**
   - Maintain runbooks
   - Document decision trees
   - Keep contact lists updated
   - Store documentation in multiple locations

4. **Monitoring:**
   - Set up CloudWatch alarms
   - Use Route 53 health checks
   - Monitor replication lag
   - Alert on backup failures

---

## 8. Monitoring & Observability

### 8.1 Amazon CloudWatch

**Key Concepts:**
- **Metrics:** Time-ordered data points (default 5-minute, detailed 1-minute)
- **Alarms:** Watch metrics and trigger actions
- **Logs:** Centralized log management
- **Events (EventBridge):** Near real-time event stream
- **Dashboards:** Customizable visualization
- **Insights:** Automated log analysis

**Features:**
- **Custom Metrics:** Publish application metrics
- **Alarms:**
  - Threshold-based (CPU > 80%)
  - Anomaly detection
  - Composite alarms
  - Actions: SNS, Lambda, EC2 Auto Scaling
- **Logs:**
  - Log groups and streams
  - Log retention policies
  - Log Insights (query language)
  - Metric filters
  - Subscription filters (Kinesis, Lambda)

**Best Practices:**
- Enable detailed monitoring for critical resources
- Set appropriate retention periods
- Use CloudWatch Agent for custom metrics
- Create dashboards for operational visibility
- Set alarms with appropriate thresholds
- Use anomaly detection for dynamic thresholds

### 8.2 AWS X-Ray

**Key Concepts:**
- Distributed tracing
- Request flow visualization
- Performance bottlenecks identification
- Service map generation

**Integration:**
- Lambda, API Gateway, ECS, EKS
- SDKs for Java, Node.js, Python, .NET, Go
- OpenTelemetry support

### 8.3 AWS CloudTrail

**Key Concepts:**
- Audit trail of AWS API calls
- Account activity history
- Security analysis
- Compliance auditing

**Features:**
- Management events (default)
- Data events (opt-in, additional cost)
- Insights events (anomaly detection)
- Log file integrity validation

### 8.4 Amazon CloudWatch Logs

**Key Concepts:**
- Centralized logging
- Log groups and streams
- Metric filters
- Subscription filters
- Live Tail

**Integration:**
- CloudWatch Logs Insights (query language)
- Export to S3
- Stream to Elasticsearch/OpenSearch
- Lambda for processing

### 8.5 AWS Distro for OpenTelemetry

**Key Concepts:**
- OpenTelemetry collector for AWS
- Collect traces and metrics
- Integration with X-Ray, CloudWatch, Prometheus
- Vendor-neutral instrumentation

### 8.6 Third-Party Monitoring

**Options:**
- Datadog
- New Relic
- Splunk
- Dynatrace
- AppDynamics

---

## 9. Load Balancing & Auto Scaling

### 9.1 Elastic Load Balancing (ELB)

**Types:**

#### Application Load Balancer (ALB)
- **Layer 7 (HTTP/HTTPS)**
- Content-based routing (host, path, headers)
- WebSocket and HTTP/2 support
- Lambda target groups (invoke functions)
- Containerized application support (ECS, EKS)
- Authentication (OIDC, SAML, Cognito)

**Features:**
- Target groups
- Health checks (HTTP/HTTPS)
- SSL/TLS termination
- Sticky sessions
- Slow start
- Redirects and fixed responses

**Use Cases:**
- Microservices
- Container-based applications
- Advanced routing requirements

#### Network Load Balancer (NLB)
- **Layer 4 (TCP, UDP, TLS)**
- Ultra-low latency
- Millions of requests per second
- Static IP per AZ
- Preserve source IP

**Features:**
- Target groups
- Health checks (TCP/HTTP/HTTPS)
- Cross-zone load balancing
- Preserve client IP
- TLS termination

**Use Cases:**
- High-performance applications
- Gaming
- IoT
- Financial applications
- When source IP preservation needed

#### Gateway Load Balancer (GWLB)
- **Layer 3 (IP packets)**
- Deploy and manage virtual appliances
- Transparent inline inspection

**Use Cases:**
- Firewalls
- Intrusion detection/prevention
- Deep packet inspection

### 9.2 Amazon EC2 Auto Scaling

**Key Concepts:**
- **Auto Scaling Groups (ASG):** Collection of EC2 instances
- **Launch Templates/Configurations:** Instance blueprint
- **Scaling Policies:** When and how to scale

**Scaling Types:**

**Manual Scaling:**
- Change desired capacity manually

**Dynamic Scaling:**
- **Target Tracking:** Maintain metric at target value (e.g., CPU = 50%)
- **Step Scaling:** Scale by amount based on CloudWatch alarm
- **Simple Scaling:** Scale by fixed amount (legacy, not recommended)

**Scheduled Scaling:**
- Scale based on predictable schedule
- Time-based actions

**Predictive Scaling:**
- ML-based prediction
- Scale before anticipated load

**Scaling Components:**
- **Minimum:** Minimum instances to maintain
- **Maximum:** Maximum instances allowed
- **Desired:** Current target number

**Health Checks:**
- EC2 status checks (default)
- ELB health checks
- Custom health checks

**Best Practices:**
- Use multiple AZs
- Enable ELB health checks
- Use target tracking for most use cases
- Set appropriate cooldown periods
- Use mixed instances policy (Spot + On-Demand)
- Configure instance refresh for updates

### 9.3 AWS Auto Scaling

**Key Concepts:**
- Unified scaling for multiple resources
- Application Auto Scaling for individual services

**Supported Resources:**
- EC2 Auto Scaling Groups
- ECS services
- DynamoDB tables and indexes
- Aurora replicas
- Spot Fleet
- EMR clusters
- AppStream 2.0 fleets

---

## 10. DNS & Content Delivery

### 10.1 Amazon Route 53

**Key Concepts:**
- Highly available DNS service
- Domain registration
- Health checking
- Traffic management

**Routing Policies:**

| Policy | Description | Use Case |
|--------|-------------|----------|
| **Simple** | Single resource | Single endpoint |
| **Weighted** | Split traffic by percentage | A/B testing, migration |
| **Latency** | Route to lowest latency region | Global applications |
| **Geolocation** | Route based on user location | Content localization |
| **Geoproximity** | Route based on resource location | Shift traffic between regions |
| **Failover** | Primary/secondary configuration | Disaster recovery |
| **Multivalue** | Return multiple values | Load balancing, failover |

**Alias Records:**
- Route 53-specific, maps to AWS resources
- Supports: ELB, CloudFront, S3, API Gateway, VPC endpoints
- Free (no charge for DNS queries)
- Automatic health checks

**Health Checks:**
- HTTP/HTTPS/TCP health checks
- CloudWatch metric-based
- Calculated (composite)
- Automated failover

**Private DNS:**
- Internal DNS within VPC
- Integrates with on-premises DNS

### 10.2 Amazon CloudFront

**Key Concepts:**
- Global content delivery network (CDN)
- Edge locations worldwide
- Caches content close to users
- Reduces latency and origin load

**Origins:**
- S3 buckets
- Custom origins (HTTP servers)
- ELB (Application/Classic Load Balancers)
- API Gateway
- MediaStore, MediaPackage

**Features:**
- **Caching:** TTL-based, query string, cookie, header control
- **Security:**
  - SSL/TLS encryption
  - Field-level encryption
  - Origin Access Identity (OAI) / Origin Access Control (OAC)
  - AWS WAF integration
  - DDoS protection (Shield)
- **Edge Functions:**
  - Lambda@Edge (run Lambda at edge locations)
  - CloudFront Functions (lightweight JavaScript)
- **Origin Shield:** Centralized caching layer
- **Signed URLs/Cookies:** Restrict access to content
- **Real-time Logs:** Kinesis Data Streams integration

**Cache Behaviors:**
- Path patterns (/images/*, /api/*)
- TTL settings (min, max, default)
- Forwarded values (headers, cookies, query strings)
- Viewer protocol policy (HTTP/HTTPS redirect)
- Allowed HTTP methods
- Lambda@Edge functions

**Best Practices:**
- Use CloudFront in front of S3 for security and performance
- Set appropriate cache TTLs
- Enable compression (Gzip, Brotli)
- Use Origin Shield for high cache hit ratio
- Configure alternate domain names (CNAMEs)
- Use signed URLs for restricted content

### 10.3 AWS Global Accelerator

**Key Concepts:**
- Network layer acceleration
- Static anycast IP addresses
- Direct traffic over AWS global network
- Health checks and automatic failover

**Benefits:**
- Lower latency for global users
- Instant failover (faster than DNS)
- TCP and UDP support
- Client IP preservation

**Use Cases:**
- Gaming
- VoIP
- IoT
- Financial applications
- Applications requiring static IP

---

## 11. Serverless Architecture

### 11.1 AWS Lambda

(See section 2.2 for details)

### 11.2 Amazon API Gateway

**Types:**
- **REST API:** Full-featured, cache, throttling, request/response transformation
- **HTTP API:** Lower cost, simplified, JWT authorizers
- **WebSocket API:** Real-time bidirectional communication

**Features:**
- **Endpoints:** Regional, Edge-optimized, Private
- **Integration:**
  - Lambda proxy
  - HTTP proxy
  - AWS services (SQS, Step Functions, etc.)
  - Mock
- **Authorization:**
  - IAM
  - Cognito User Pools
  - Lambda authorizers
  - JWT (HTTP API)
- **Throttling:** Rate limits, burst limits
- **Caching:** TTL-based response caching
- **Request/Response:** Transformation, validation
- **Deployment:** Stages, canary releases

**Best Practices:**
- Use HTTP API for cost savings when features sufficient
- Enable caching for read-heavy workloads
- Use private APIs for internal services
- Implement proper error handling
- Enable CloudWatch logs and metrics

### 11.3 AWS Step Functions

**Key Concepts:**
- Workflow orchestration service
- State machines (JSON definition)
- Visual workflow designer

**State Types:**
- **Task:** Single unit of work (Lambda, ECS, Batch, etc.)
- **Choice:** Branch based on condition
- **Wait:** Delay execution
- **Parallel:** Execute branches simultaneously
- **Map:** Iterate over collection
- **Pass:** Pass input to output
- **Succeed/Fail:** End states

**Workflow Types:**
- **Standard:** Exactly-once processing, 1-year duration
- **Express:** At-least-once processing, 5-minute duration, high throughput

**Features:**
- Error handling (Retry, Catch)
- Service integrations (140+ AWS services)
- Distributed tracing (X-Ray)
- Callback patterns
- Human-in-the-loop (approval workflows)

### 11.4 Amazon EventBridge

**Key Concepts:**
- Serverless event bus
- Event routing
- Schema registry

**Event Buses:**
- **Default:** AWS service events
- **Custom:** Application events
- **Partner:** SaaS application events (Datadog, PagerDuty, etc.)

**Features:**
- **Rules:** Pattern matching for event routing
- **Targets:** Lambda, SQS, SNS, Kinesis, Step Functions, etc.
- **Archive and Replay:** Store and replay events
- **Schema Registry:** Auto-discover and validate event schemas

**Use Cases:**
- Event-driven architectures
- Decoupling microservices
- Real-time data processing
- SaaS integration

### 11.5 Amazon SQS (Simple Queue Service)

**Queue Types:**

**Standard Queue:**
- Unlimited throughput
- At-least-once delivery
- Best-effort ordering
- Use case: Decoupling, buffering

**FIFO Queue:**
- High throughput (batch: 3,000 msg/sec, single: 300 msg/sec)
- Exactly-once processing
- First-in-first-out ordering
- Use case: Order critical, deduplication

**Features:**
- **Visibility Timeout:** Time to process before message visible again
- **Dead Letter Queue (DLQ):** Store failed messages for analysis
- **Message Retention:** 1 minute to 14 days (default 4 days)
- **Maximum Message Size:** 256 KB
- **Long Polling:** Reduce empty responses (cost saving)
- **Delay Queue:** Postpone message delivery

**Best Practices:**
- Use separate queues for different priorities
- Enable DLQ for error handling
- Use batch operations for efficiency
- Monitor queue depth with CloudWatch

### 11.6 Amazon SNS (Simple Notification Service)

**Key Concepts:**
- Pub/Sub messaging service
- Fan-out pattern
- Push-based delivery

**Topics:**
- **Standard:** High throughput, at-least-once delivery
- **FIFO:** Exactly-once, ordering (SQS FIFO subscribers only)

**Subscribers:**
- Lambda
- SQS
- HTTP/S endpoints
- Email
- SMS
- Mobile push

**Features:**
- **Message Filtering:** Filter based on message attributes
- **Message Attributes:** Metadata for filtering
- **Delivery Policies:** Retry logic for HTTP/S
- **Delivery Status:** Track message delivery

**Use Cases:**
- Fan-out to multiple subscribers
- Mobile push notifications
- Email alerts
- SMS notifications

### 11.7 Amazon Kinesis

**Services:**

**Kinesis Data Streams:**
- Real-time streaming data ingestion
- Custom applications process data
- Retention: 24 hours to 1 year
- Shards for throughput scaling

**Kinesis Data Firehose:**
- Load streaming data to AWS data stores
- S3, Redshift, OpenSearch, Splunk
- Automatic scaling
- Transformation (Lambda)

**Kinesis Data Analytics:**
- Real-time SQL streaming analytics
- Apache Flink applications
- Process Kinesis and Kafka streams

**Kinesis Video Streams:**
- Video streaming for analytics, ML
- WebRTC support

### 11.8 AWS AppSync

**Key Concepts:**
- Managed GraphQL service
- Real-time subscriptions
- Offline data synchronization

**Data Sources:**
- DynamoDB
- Lambda
- RDS (HTTP endpoints)
- OpenSearch
- HTTP endpoints
- None (local resolvers)

**Features:**
- Automatic scaling
- DynamoDB batch operations
- Pipeline resolvers (chaining)
- Caching
- Authorization (API key, IAM, Cognito, OIDC)
- Real-time subscriptions (WebSocket)

---

## 12. Migration & Data Transfer

### 12.1 AWS Migration Hub

**Key Concepts:**
- Central tracking of migration progress
- Integration with SMS, DMS, Application Discovery Service
- Single pane of glass for migrations

### 12.2 AWS Application Discovery Service

**Key Concepts:**
- Discover on-premises infrastructure
- Server utilization data
- Dependency mapping
- Agent-based and agentless discovery

### 12.3 AWS Application Migration Service (MGN)

**Key Concepts:**
- Lift-and-shift migrations to AWS
- Agent-based replication
- Non-disruptive testing
- Cutover automation
- Replaces AWS SMS (Server Migration Service)

### 12.4 AWS Database Migration Service (DMS)

**Key Concepts:**
- Migrate databases to AWS
- Homogeneous (same engine) and heterogeneous (different engine)
- Continuous replication (CDC - Change Data Capture)
- Minimal downtime migrations

**Sources & Targets:**
- Oracle, SQL Server, MySQL, PostgreSQL, MariaDB
- MongoDB, Amazon DocumentDB
- S3, Redshift, DynamoDB
- Kafka, Kinesis

**Replication Types:**
- Full load
- Full load + CDC
- CDC only

**Schema Conversion Tool (SCT):**
- Convert database schemas
- Heterogeneous migrations
- Assess migration complexity

### 12.5 AWS DataSync

**Key Concepts:**
- Online data transfer service
- On-premises to AWS, AWS to AWS
- NFS, SMB, HDFS, S3, EFS, FSx
- Encrypted and optimized transfer

### 12.6 AWS Transfer Family

**Key Concepts:**
- Managed file transfer services
- SFTP, FTPS, FTP
- Integration with S3 and EFS
- Identity providers (Directory Service, custom)

### 12.7 AWS Snow Family

**Devices:**

**Snowcone:**
- 8 TB usable storage
- Edge computing
- Offline shipping

**Snowball Edge Storage Optimized:**
- 80 TB usable storage
- 40 vCPU, 80 GB RAM
- S3-compatible endpoint

**Snowball Edge Compute Optimized:**
- 42 TB usable storage
- 52 vCPU, 208 GB RAM
- GPU option
- EC2 instances

**Snowmobile:**
- Exabyte-scale data transfer
- 45-foot shipping container
- Up to 100 PB per device

**Use Cases:**
- Large-scale data migration
- Edge computing
- Remote site data collection
- Disaster recovery

### 12.8 6 R's of Migration

1. **Rehost (Lift-and-Shift):**
   - Move application without changes
   - Fastest migration method
   - Tools: AWS MGN, VM Import/Export

2. **Replatform (Lift-Tinker-and-Shift):**
   - Minor optimizations
   - Example: Migrate to RDS, use Elastic Beanstalk

3. **Repurchase (Drop-and-Shop):**
   - Move to SaaS or different software
   - Example: Migrate to Salesforce, Workday

4. **Refactor/Re-architect:**
   - Major architectural changes
   - Example: Monolith to microservices, serverless
   - Highest effort, highest benefit

5. **Retire:**
   - Decommission applications
   - Cost savings

6. **Retain (Revisit):**
   - Keep on-premises
   - Hybrid cloud
   - Example: Legacy systems, regulatory requirements

---

## 13. Cost Optimization

### 13.1 AWS Pricing Models

**Compute:**
- On-Demand (highest cost, most flexible)
- Reserved Instances (1-3 years, 40-72% discount)
- Savings Plans (1-3 years, flexible commitment)
- Spot Instances (up to 90% discount, interruptible)
- Dedicated Hosts (physical servers)

**Storage:**
- S3 tiers (Standard, IA, Glacier)
- EBS volume types
- Data transfer costs (inbound free, outbound charged)

**Database:**
- Reserved capacity
- On-demand vs provisioned

### 13.2 Cost Management Tools

**AWS Cost Explorer:**
- Analyze costs and usage
- Filter by service, tag, region
- Forecast future costs
- Reserved Instance recommendations

**AWS Budgets:**
- Set budget thresholds
- Alert on forecasted and actual costs
- Tag-based budgets

**AWS Cost Anomaly Detection:**
- ML-powered anomaly detection
- Alert unusual spending

**AWS Pricing Calculator:**
- Estimate costs before deployment
- Compare service options

**AWS Billing Conductor:**
- Custom pricing and billing rules
- Chargeback/showback for enterprise

### 13.3 Cost Optimization Strategies

**Compute:**
- Use Graviton instances (ARM-based, 20% cheaper, better performance)
- Purchase Reserved Instances or Savings Plans for predictable workloads
- Use Spot Instances for fault-tolerant workloads
- Right-size instances (use Compute Optimizer)
- Use serverless (Lambda) for variable workloads

**Storage:**
- Use S3 Intelligent-Tiering for unknown access patterns
- Implement lifecycle policies
- Delete incomplete multipart uploads
- Compress data before storage
- Use EFS Infrequent Access for less accessed files

**Database:**
- Use Reserved Instances for production databases
- Scale read replicas based on demand
- Use DynamoDB on-demand for unpredictable workloads
- Enable TTL to delete expired data

**Networking:**
- Use VPC endpoints instead of NAT Gateway where possible
- Use CloudFront to reduce data transfer costs
- Keep traffic within same AZ when possible
- Use Direct Connect for high-volume data transfer

**Other:**
- Tag everything for cost allocation
- Delete unused resources
- Use CloudWatch retention policies to control log costs
- Monitor and optimize with Trusted Advisor

### 13.4 AWS Trusted Advisor

**Categories:**
- Cost Optimization
- Performance
- Security
- Fault Tolerance
- Service Limits
- Operational Excellence

**Levels:**
- **Basic:** Limited checks
- **Developer:** All checks for single account
- **Business/Enterprise:** Multi-account support, programmatic access

---

## 14. Exam Strategies

### 14.1 AWS Solutions Architect Associate (SAA-C03)

**Exam Format:**
- 65 questions
- 130 minutes
- Multiple choice and multiple response
- Passing score: 720/1000

**Domains:**

| Domain | Weight | Topics |
|--------|--------|--------|
| Domain 1 | 30% | Design Secure Architectures |
| Domain 2 | 26% | Design Resilient Architectures |
| Domain 3 | 24% | Design High-Performing Architectures |
| Domain 4 | 20% | Design Cost-Optimized Architectures |

### 14.2 Key Exam Strategies

**1. Read Carefully:**
- Identify keywords: "most cost-effective", "highly available", "secure", "serverless"
- Note constraints: budget, RTO/RPO, compliance
- Understand the scenario completely

**2. Elimination:**
- Eliminate obviously wrong answers
- Compare remaining options
- Choose the best fit

**3. Service Selection:**
- Know when to use managed vs unmanaged
- Understand service limitations
- Know service integrations

**4. Common Patterns:**
- **High Availability:** Multi-AZ, Auto Scaling, ELB
- **Disaster Recovery:** Multi-region, backups, pilot light
- **Security:** Encryption, least privilege, VPC
- **Cost:** Reserved instances, S3 tiers, lifecycle policies
- **Performance:** Caching, read replicas, CloudFront

**5. Remember:**
- IAM roles > access keys for applications
- S3 for object storage, EBS for block storage, EFS for file storage
- RDS for relational, DynamoDB for NoSQL
- ALB for HTTP/HTTPS, NLB for TCP/UDP
- Use managed services when possible

### 14.3 Common Mistakes to Avoid

**1. Choosing Wrong Storage:**
- S3 for archives vs EBS for databases
- EFS for shared access vs EBS for single instance

**2. Security Misconfigurations:**
- Public S3 buckets
- Overly permissive IAM policies
- Not encrypting data

**3. Cost Mistakes:**
- Not using Reserved Instances
- Wrong S3 storage class
- Data transfer costs

**4. High Availability:**
- Single AZ deployments
- No health checks
- No backup strategy

**5. Performance:**
- Wrong instance types
- No caching
- Database bottlenecks

### 14.4 Practice Areas

**Focus on:**
- VPC design (subnets, routing, security)
- EC2 pricing and features
- S3 storage classes and features
- RDS and DynamoDB differences
- Load balancer types and use cases
- Auto Scaling policies
- IAM best practices
- Disaster recovery strategies
- Cost optimization techniques
- Migration strategies (6 R's)

---

## Appendix A: Service Comparison Tables

### Storage Services

| Service | Type | Use Case | Durability | Max Size |
|---------|------|----------|------------|----------|
| S3 | Object | Static files, backups | 99.999999999% | 5 TB/object |
| EBS | Block | EC2 storage, databases | 99.8-99.9% | 64 TB |
| EFS | File | Shared storage, CMS | 99.999999999% | Petabytes |
| FSx Windows | File | Windows apps, SMB | 99.999999999% | 64 TB |
| FSx Lustre | File | HPC, ML | 99.999999999% | Petabytes |
| Glacier | Archive | Long-term storage | 99.999999999% | Unlimited |

### Database Services

| Service | Type | Use Case | Scaling |
|---------|------|----------|---------|
| RDS | Relational | OLTP, traditional apps | Vertical, read replicas |
| Aurora | Relational | High-performance OLTP | Auto-scaling, 15 replicas |
| DynamoDB | NoSQL | Key-value, document | Automatic, unlimited |
| ElastiCache | In-memory | Caching, session store | Vertical, clusters |
| DocumentDB | Document | MongoDB workloads | Horizontal, replicas |
| Neptune | Graph | Relationships, networks | Read replicas |
| Keyspaces | Wide-column | Cassandra workloads | Serverless |
| Timestream | Time series | IoT, metrics | Auto-scaling |

### Compute Services

| Service | Type | Management | Use Case |
|---------|------|------------|----------|
| EC2 | Virtual machines | Self-managed | Full control needed |
| Lambda | Serverless | Fully managed | Event-driven, short tasks |
| ECS | Containers | Managed orchestration | Container workloads |
| Fargate | Serverless containers | Fully managed | Containers without servers |
| EKS | Kubernetes | Managed control plane | Kubernetes workloads |
| Batch | Batch processing | Fully managed | Batch jobs, HPC |
| Elastic Beanstalk | PaaS | Managed platform | Quick web app deployment |

### Load Balancers

| Type | Layer | Protocols | Use Case |
|------|-------|-----------|----------|
| ALB | 7 | HTTP/HTTPS | Web apps, microservices |
| NLB | 4 | TCP/UDP/TLS | High performance, gaming |
| GWLB | 3 | IP | Virtual appliances |

---

## Appendix B: Important Limits and Defaults

### EC2
- Instances per region: 20 (on-demand), adjustable
- EBS volumes per instance: Depends on instance type
- EBS volume size: 8 GiB - 16 TiB (64 TiB for io2 Block Express)

### S3
- Object size: 0 bytes - 5 TB
- Upload: 5 GB (single operation), 10,000 parts (multipart)
- Buckets per account: 100 (soft limit)

### RDS
- Max instance size: db.x2iedn.32xlarge
- Storage: Up to 64 TiB (Aurora up to 128 TiB)
- Read replicas: 5 (MySQL, PostgreSQL), 15 (Aurora)

### DynamoDB
- Item size: 400 KB
- Partition key: Min 1 byte, max 2048 bytes
- Sort key: Min 1 byte, max 1024 bytes

### Lambda
- Memory: 128 MB - 10,240 MB (10 GB)
- Timeout: 900 seconds (15 minutes)
- Deployment package: 50 MB (zipped), 250 MB (unzipped)
- Concurrent executions: 1000 (soft limit)

### VPC
- VPCs per region: 5 (adjustable)
- Subnets per VPC: 200 (adjustable)
- Security groups per VPC: 300 (adjustable)
- Rules per security group: 60 inbound + 60 outbound

---

## Appendix C: Quick Reference Decision Trees

### When to Use Which Compute Service

```
Do you need full OS control?
├── YES → EC2
└── NO → Is it event-driven/short duration?
    ├── YES → Lambda
    └── NO → Do you need containers?
        ├── YES → Fargate or ECS/EKS
        └── NO → Elastic Beanstalk
```

### When to Use Which Storage Service

```
What type of data?
├── Files → EFS (shared) or FSx (Windows/Lustre)
├── Block storage → EBS
├── Objects/Backup → S3
│   ├── Frequently accessed → S3 Standard
│   ├── Unknown pattern → S3 Intelligent-Tiering
│   ├── Infrequently accessed → S3 Standard-IA
│   └── Archive → S3 Glacier
└── Cache → ElastiCache
```

### When to Use Which Database

```
Relational data?
├── YES → RDS (standard) or Aurora (high-performance)
└── NO → Key-value or document?
    ├── Key-value → DynamoDB
    ├── Document → DocumentDB (MongoDB) or DynamoDB
    ├── Graph → Neptune
    ├── Time series → Timestream
    └── Cache → ElastiCache
```

---

## Document Maintenance

**Validation Sources:**
- AWS Well-Architected Framework (Official Documentation)
- AWS Solutions Architect Associate Exam Guide
- AWS Service Documentation
- Context7 AWS Libraries
- AWS Whitepapers and Best Practices

**Review Schedule:**
- Quarterly: Update for new services and features
- Annually: Comprehensive review against certification updates
- As needed: Corrections and clarifications

**Contributing:**
This document serves as the authoritative baseline for the AWS Solution Architect agent skill. All skill content should align with this document's definitions and best practices.

---

*This document represents a comprehensive synthesis of AWS Solutions Architect certification requirements and real-world architecture best practices, validated against official AWS documentation.*
