# Service Decision Trees Reference

## Purpose

This reference provides frameworks for choosing between AWS services. Always consult AWS Decision Guides via MCP for current, detailed guidance.

## Compute Service Selection

### Decision Framework

**Start with these questions**:
1. Do you want to manage servers? (Yes → EC2 path, No → Serverless/Container path)
2. Is this containerized? (Yes → Container path, No → Serverless/VM path)
3. How predictable is the load? (Predictable → EC2/Fargate, Variable → Lambda)
4. What's the execution duration? (<15 min → Lambda possible, >15 min → Other options)

### Compute Decision Tree

```
Application Compute Need
│
├─ Serverless Preferred?
│  ├─ Yes, Event-driven → Lambda
│  ├─ Yes, HTTP APIs → Lambda + API Gateway
│  └─ Yes, Long-running → Fargate or App Runner
│
├─ Containerized?
│  ├─ Need Kubernetes? → EKS
│  ├─ Want simplicity? → ECS Fargate
│  ├─ Need EC2 control? → ECS on EC2
│  └─ Simple container app? → App Runner
│
└─ Traditional VMs?
   ├─ Specialized workload → Purpose-built (HPC, Graphics)
   ├─ High performance → EC2 (optimize instance type)
   ├─ Batch processing → AWS Batch
   └─ Standard → EC2 with Auto Scaling
```

### Service Comparison

| Service | When to Use | Avoid When |
|---------|-------------|------------|
| **Lambda** | Event-driven, variable load, <15 min execution | Long-running, need custom OS, consistent heavy load |
| **Fargate** | Containers without managing servers, variable load | Need spot instances, very cost-sensitive |
| **ECS on EC2** | Containers with cost optimization, predictable load | Don't want to manage capacity |
| **EKS** | Need Kubernetes, multi-cloud portability | Simple app, small team |
| **EC2** | Custom requirements, specialized hardware, >15 min jobs | Want to minimize operations |
| **App Runner** | Simple containerized web apps | Complex networking, need custom domain config |
| **Batch** | Scheduled jobs, large-scale batch processing | Real-time processing |

**MCP Lookup**: "choosing AWS compute service decision guide"

## Database Service Selection

### Decision Framework

**Start with these questions**:
1. What's your data model? (Relational, Key-Value, Document, Graph, etc.)
2. What's your consistency requirement? (Strong vs. Eventual)
3. What's your query pattern? (OLTP vs. OLAP)
4. What's your scale? (GB, TB, PB)
5. Do you need managed or more control?

### Database Decision Tree

```
Data Storage Need
│
├─ Relational Data?
│  ├─ PostgreSQL-compatible?
│  │  ├─ Serverless scaling → Aurora Serverless (PostgreSQL)
│  │  ├─ High performance → Aurora PostgreSQL
│  │  └─ Cost-conscious → RDS PostgreSQL
│  │
│  └─ MySQL-compatible?
│     ├─ Serverless scaling → Aurora Serverless (MySQL)
│     ├─ High performance → Aurora MySQL
│     └─ Cost-conscious → RDS MySQL
│
├─ NoSQL Data?
│  ├─ Key-Value, Microsecond latency → DynamoDB
│  ├─ Document (MongoDB) → DocumentDB
│  ├─ Graph → Neptune
│  ├─ Time-series → Timestream
│  ├─ Ledger → QLDB
│  └─ Wide-column → Keyspaces (Cassandra)
│
├─ Data Warehouse?
│  ├─ Serverless, pay-per-query → Athena
│  ├─ Traditional DW → Redshift
│  └─ Real-time analytics → Redshift Streaming
│
├─ Caching?
│  ├─ In-memory, advanced features → ElastiCache (Redis)
│  └─ Simple caching → ElastiCache (Memcached)
│
└─ File Storage?
   ├─ Shared file system → EFS
   ├─ High-performance computing → FSx (Lustre)
   ├─ Windows file shares → FSx (Windows)
   └─ Object storage → S3
```

### Database Comparison

| Service | Use Case | Scale | Consistency |
|---------|----------|-------|-------------|
| **Aurora** | Relational, high performance | Multi-TB | Strong |
| **RDS** | Relational, standard | Up to 64 TB | Strong |
| **DynamoDB** | Key-value, high scale | Unlimited | Eventual (configurable) |
| **DocumentDB** | MongoDB-compatible docs | TB scale | Strong |
| **Neptune** | Graph relationships | Billions of relationships | Strong |
| **Redshift** | Data warehouse, analytics | PB scale | Strong |
| **Athena** | Serverless SQL on S3 | Exabyte scale | N/A (query engine) |

**MCP Lookup**: "choosing AWS database service decision guide"

## Storage Service Selection

### Decision Framework

**Start with these questions**:
1. What type of data? (Objects, Blocks, Files)
2. How is it accessed? (Frequently, Infrequently, Archive)
3. What performance needed? (Throughput, IOPS, Latency)
4. Is it shared across instances?

### Storage Decision Tree

```
Storage Need
│
├─ Object Storage?
│  ├─ Frequent access → S3 Standard
│  ├─ Infrequent access → S3 IA or S3 One Zone-IA
│  ├─ Archive → S3 Glacier or Glacier Deep Archive
│  └─ Intelligent tiering → S3 Intelligent-Tiering
│
├─ Block Storage (EC2 volumes)?
│  ├─ High IOPS, low latency → EBS io2/io2 Block Express
│  ├─ Balanced → EBS gp3
│  ├─ Throughput-optimized → EBS st1
│  └─ Cold storage → EBS sc1
│
├─ File Storage (Shared)?
│  ├─ Linux/POSIX → EFS
│  ├─ Windows → FSx for Windows
│  ├─ High-performance compute → FSx for Lustre
│  └─ NetApp enterprise → FSx for NetApp ONTAP
│
└─ Hybrid Storage?
   ├─ File gateway → Storage Gateway (File)
   ├─ Volume gateway → Storage Gateway (Volume)
   └─ Tape gateway → Storage Gateway (Tape)
```

### Storage Tier Selection

| Access Pattern | Recommended S3 Tier | Use Case |
|----------------|--------------------|-----------| 
| Daily access | S3 Standard | Active data, frequently accessed |
| Weekly/monthly | S3 IA | Backups, older data |
| Quarterly/yearly | S3 Glacier Flexible | Compliance archives |
| Multi-year retention | S3 Glacier Deep Archive | Long-term archives |
| Unknown/changing | S3 Intelligent-Tiering | Unpredictable access |

**MCP Lookup**: "AWS storage services comparison"

## Networking Service Selection

### Decision Framework

**Start with these questions**:
1. What are you connecting? (VPCs, On-premises, Users, Services)
2. What's the use case? (Routing, Load balancing, CDN, API management)
3. What protocol? (HTTP/S, TCP, UDP)
4. Global or regional?

### Networking Decision Tree

```
Networking Need
│
├─ Content Delivery?
│  ├─ Global CDN → CloudFront
│  ├─ Regional edge → CloudFront with Regional Edge Caches
│  └─ API caching → API Gateway with caching
│
├─ Load Balancing?
│  ├─ HTTP/HTTPS (Layer 7) → Application Load Balancer (ALB)
│  ├─ TCP/UDP (Layer 4) → Network Load Balancer (NLB)
│  └─ Legacy/EC2-Classic → Classic Load Balancer (deprecated)
│
├─ DNS?
│  ├─ Public DNS → Route 53
│  ├─ Private DNS → Route 53 Private Hosted Zones
│  └─ Traffic routing → Route 53 with routing policies
│
├─ API Management?
│  ├─ REST APIs → API Gateway (REST)
│  ├─ WebSocket → API Gateway (WebSocket)
│  ├─ HTTP APIs (simple) → API Gateway (HTTP)
│  └─ GraphQL → AppSync
│
├─ VPC Connectivity?
│  ├─ Within AWS (many VPCs) → Transit Gateway
│  ├─ VPC to VPC → VPC Peering
│  ├─ To on-premises (dedicated) → Direct Connect
│  ├─ To on-premises (encrypted) → Site-to-Site VPN
│  └─ Remote user access → Client VPN
│
└─ Private Connectivity?
   ├─ To AWS services → VPC Endpoints (PrivateLink)
   └─ To SaaS providers → PrivateLink connections
```

**MCP Lookup**: "AWS networking services comparison"

## Integration Service Selection

### Decision Framework

**Start with these questions**:
1. Synchronous or asynchronous?
2. Point-to-point or fan-out?
3. Message ordering required?
4. Message durability needed?

### Integration Decision Tree

```
Integration Need
│
├─ Asynchronous Messaging?
│  ├─ Queue (point-to-point) → SQS
│  ├─ Pub/Sub (fan-out) → SNS
│  ├─ Event bus (routing) → EventBridge
│  └─ Data streaming → Kinesis or MSK
│
├─ Workflow Orchestration?
│  ├─ Serverless workflows → Step Functions
│  ├─ Managed workflows → Managed Workflows for Apache Airflow (MWAA)
│  └─ Simple state machine → Step Functions Express
│
├─ API Integration?
│  ├─ REST API gateway → API Gateway
│  ├─ GraphQL → AppSync
│  └─ WebSocket → API Gateway WebSocket
│
└─ Data Integration?
   ├─ Database replication → DMS
   ├─ ETL → Glue
   ├─ Data transfer → DataSync, Transfer Family
   └─ Application integration → AppFlow
```

### Messaging Service Comparison

| Service | Pattern | Ordering | Durability | Use Case |
|---------|---------|----------|------------|-----------|
| **SQS** | Queue | FIFO optional | Yes | Decoupling, work queues |
| **SNS** | Pub/Sub | No | No (delivers once) | Fan-out notifications |
| **EventBridge** | Event bus | No | Retries | Event-driven architectures |
| **Kinesis** | Stream | Yes (per shard) | 1-365 days | Real-time data streams |
| **MSK** | Kafka-compatible | Yes (per partition) | Configurable | Enterprise messaging |

**MCP Lookup**: "AWS integration services comparison"

## Service Selection Best Practices

### 1. Start with Managed Services
- Less operational overhead
- Built-in best practices
- Automatic scaling and patching
- Focus on business logic

**Exception**: When you need specific control or customization that managed services don't provide

### 2. Prefer Serverless When Possible
- Pay for actual usage
- Auto-scaling built-in
- No capacity planning
- Reduced operations

**Exception**: Predictable, constant high load where reserved capacity is more cost-effective

### 3. Use Purpose-Built Databases
- Don't try to fit all data into one database type
- Choose database based on access patterns
- Consider using multiple database types

**Exception**: When operational complexity of multiple databases outweighs benefits

### 4. Consider Total Cost of Ownership
- Not just service costs
- Include operational costs
- Factor in team learning curve
- Consider hidden costs (data transfer, API calls)

### 5. Match Service to Team Capabilities
- Can team operate this service?
- Is training/hiring needed?
- What's the operational burden?
- Is there adequate documentation?

## Using AWS Decision Guides

AWS provides official decision guides. Always consult these via MCP:

**Compute**: 
- Search: "choosing AWS compute service"
- Specific: "AWS Fargate or Lambda decision guide"

**Databases**:
- Search: "choosing AWS database service"
- Specific: "AWS RDS or DynamoDB"

**Containers**:
- Search: "choosing AWS container service"
- Specific: "ECS or EKS decision guide"

**Storage**:
- Search: "AWS storage services comparison"

**Networking**:
- Search: "AWS networking services comparison"

## Decision Documentation Template

When making service decisions, document:

```
## Service Decision: [Decision Name]

### Context
[What problem are we solving?]

### Requirements
- Functional: [What it must do]
- Non-functional: [Performance, scale, etc.]
- Constraints: [Budget, timeline, team]

### Options Considered
1. **[Service A]**
   - Pros: [Benefits]
   - Cons: [Drawbacks]
   - Cost: [Estimate]
   
2. **[Service B]**
   - Pros: [Benefits]
   - Cons: [Drawbacks]
   - Cost: [Estimate]

### Decision
**Selected**: [Chosen service]

**Rationale**: [Why this choice]

**Trade-offs Accepted**: [What we're giving up]

### Review Criteria
[When should we revisit this decision?]
```

## Getting Current Service Information

Before recommending services:

1. **Check service capabilities**:
   ```
   MCP_DOCKER:search_documentation "[service name] features"
   ```

2. **Review best practices**:
   ```
   MCP_DOCKER:search_documentation "[service name] best practices"
   ```

3. **Compare services**:
   ```
   MCP_DOCKER:search_documentation "comparison [service A] [service B]"
   ```

4. **Get decision guidance**:
   ```
   MCP_DOCKER:search_documentation "choosing [category] AWS"
   ```

This ensures recommendations reflect current service capabilities and AWS guidance.
