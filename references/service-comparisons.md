# Service Comparisons Reference

**Document ID:** ref-service-comparisons  
**Purpose:** Quick reference for comparing AWS services across dimensions

---

## Compute Services Comparison

| Service | Managed Level | Pricing Model | Best For |
|---------|---------------|---------------|----------|
| Lambda | Full | Request + GB-s | Event-driven, variable workloads |
| ECS Fargate | High | vCPU + GB | Container workloads without cluster management |
| EKS | Medium | Cluster resources + EKS fee | Kubernetes workloads, complex orchestration |
| EC2 | Low | Instance + storage | Full control requirements, specialized workloads |
| App Runner | High | Instance + GB | Containerized web apps, simple deployments |
| Lightsail | High | Fixed monthly | Simple workloads, predictable pricing |

### Compute Decision Matrix

| Criterion | Lambda | ECS Fargate | EKS | EC2 |
|-----------|--------|------------|-----|-----|
| Ops overhead | Very Low | Low | High | Very High |
| Scalability | Automatic | Automatic | Manual/Auto | Manual |
| Cost for variable | Excellent | Good | Moderate | Poor |
| Cost for steady | Poor | Good | Good | Excellent |
| Flexibility | Low | Medium | High | Very High |
| Learning curve | Low | Medium | High | Medium |

## Database Services Comparison

### Relational Databases

| Service | Type | Pricing Model | Best For |
|---------|------|---------------|----------|
| Amazon RDS | Relational | Instance + storage | General purpose relational |
| Amazon Aurora | Relational | Serverless + provisioned | High performance, MySQL/PostgreSQL |
| Amazon Redshift | Data Warehouse | Node-based | Analytics, large-scale aggregations |
| Amazon Aurora Serverless v2 | Relational | ACU-based | Variable workloads, cost optimization |

### NoSQL Databases

| Service | Type | Pricing Model | Best For |
|---------|------|---------------|----------|
| Amazon DynamoDB | NoSQL (key-value) | On-demand + provisioned | Serverless, high scale, low latency |
| Amazon DocumentDB | Document | Instance + storage | MongoDB compatible |
| Amazon Keyspaces | Wide-column | Throughput-based | Apache Cassandra compatible |
| Amazon Neptune | Graph | Instance + storage | Graph workloads, relationships |

### Database Selection Guide

| Use Case | Recommended Service | Alternative |
|----------|---------------------|--------------|
| OLTP transactional | Aurora PostgreSQL | RDS PostgreSQL |
| High-scale key-value | DynamoDB | None |
| Document storage | DocumentDB | DynamoDB |
| Data warehousing | Redshift | Snowflake |
| Graph relationships | Neptune | None |
| Time series | Timestream | InfluxDB |
| In-memory cache | ElastiCache Redis | DynamoDB Accelerator |

## Storage Services Comparison

| Service | Access Pattern | Durability | Best For |
|---------|----------------|------------|----------|
| S3 Standard | Frequent access | 99.999999999% | General purpose |
| S3 Intelligent-Tiering | Unknown access | 99.999999999% | Variable access patterns |
| S3 Standard-IA | Infrequent access | 99.999999999% | Long-term storage, infrequent access |
| S3 Glacier | Archive | 99.999999999% | Long-term archival |
| S3 Glacier Deep Archive | Archive | 99.999999999% | Compliance, rarely accessed |
| EFS | File system | 99.999999999% | Shared file access, POSIX |
| FSx for Windows | File system | 99.999999999% | Windows file shares |
| FSx for Lustre | File system | 99.999999999% | HPC, performance computing |
| EBS | Block storage | 99.999999999% | EC2 boot volumes, databases |

### Storage Decision Matrix

| Criterion | S3 | EFS | EBS | FSx |
|-----------|-----|-----|-----|-----|
| File system interface | No | Yes | No | Yes |
| Shared access | Limited | Yes | No | Yes |
| Performance | Variable | Moderate | High | Very High |
| Cost/GB | Low | Medium | Medium | High |
| Scalability | Unlimited | Elastic | Limited | Scalable |

## Integration Services Comparison

| Service | Pattern | Delivery | Best For |
|---------|---------|----------|----------|
| Amazon SQS | Queue | At-least-once | Decoupling, async processing |
| Amazon SNS | Pub/Sub | Fire-and-forget | Fan-out, notifications |
| Amazon EventBridge | Event bus | At-least-once | Event filtering, cross-account |
| Amazon Kinesis | Stream | Sharded | Real-time analytics, high throughput |
| Amazon MQ | Queue | Managed ActiveMQ | Migration from on-premises |

### Integration Pattern Selection

| Pattern | Service | Use Case |
|---------|---------|----------|
| Point-to-point | SQS | Task queues, job processing |
| Fan-out | SNS + SQS | Multiple consumers, different processing |
| Event routing | EventBridge | Complex event pipelines, SaaS integration |
| Real-time streaming | Kinesis | Analytics, IoT, clickstream |
| Legacy migration | Amazon MQ | ActiveMQ, RabbitMQ migration |

## Network Services Comparison

### Load Balancing

| Service | Type | Use Case | Pricing |
|---------|------|----------|---------|
| ALB | Layer 7 | HTTP/HTTPS, microservices | LCU + hourly |
| NLB | Layer 4 | TCP/UDP, high throughput | LCU + hourly |
| GWLB | Layer 3/4 | Security appliances | Hourly + hourly |
| CLB | Legacy | Simple HTTP/HTTPS | Hourly + GB |

### DNS Services

| Service | Features | Pricing |
|---------|----------|---------|
| Route 53 | DNS, health checks, routing | Query + hosted zone |
| Route 53 Resolver | Hybrid DNS | Hourly + queries |

### VPC Connectivity

| Service | Type | Use Case | Max Throughput |
|---------|------|----------|----------------|
| VPC Peering | Direct | VPC-to-VPC | 100 Gbps |
| Transit Gateway | Hub-and-spoke | Multi-VPC, cross-account | 100 Gbps per attachment |
| Direct Connect | Dedicated | On-premises to AWS | 1-100 Gbps |
| VPN | Encrypted | Hybrid, backup | 1.25 Gbps per tunnel |
| PrivateLink | Interface | Service sharing | 10 Gbps per endpoint |

## Analytics Services Comparison

| Service | Use Case | Pricing | Real-time |
|---------|----------|---------|-----------|
| Athena | SQL queries on S3 | Query + TB scanned | No |
| Redshift | Data warehouse | Node-based | Near real-time |
| EMR | Big data processing | Instance + EMR fee | No |
| Glue | ETL | DPU + job duration | No |
| QuickSight | BI/dashboards | User + SPICE | No |
| OpenSearch | Search + analytics | Instance + storage | Yes |

## AI/ML Services Comparison

### Foundation Models

| Service | Models | Pricing | Best For |
|---------|--------|---------|----------|
| Amazon Bedrock | Claude, Titan, Jurassic, Stable Diffusion | Request + tokens | Generative AI applications |
| SageMaker JumpStart | Open source models | Instance + training | Custom model development |

### ML Platforms

| Service | Use Case | Pricing | Managed Level |
|---------|----------|---------|---------------|
| SageMaker Training | Custom training | Instance + ML hours | High |
| SageMaker Inference | Model deployment | Instance + invocation | High |
| SageMaker Ground Truth | Data labeling | Human + storage | Medium |
| Comprehend | NLP | Per document | Full |
| Rekognition | Computer vision | Per image | Full |
| Polly | Text-to-speech | Per character | Full |
| Translate | Translation | Per character | Full |

---

## Service Selection Quick Reference

### When to Use Serverless

- Variable/unpredictable traffic
- Infrequent or bursty workloads
- Pay-per-use cost model preferred
- No infrastructure management desired
- **Services**: Lambda, Fargate, Aurora Serverless, DynamoDB, S3

### When to Use Managed Services

- Operational overhead concern
- Well-defined patterns
- Cost optimization for steady state
- **Services**: RDS, ElastiCache, DocumentDB, EKS, EMR

### When to Use Self-Managed

- Maximum control required
- Custom configurations
- Specialized workloads
- **Services**: EC2, Self-managed databases, Self-managed Kubernetes

---

## Cost Optimization Decision Matrix

| Service | Low Usage | Medium Usage | High Usage |
|---------|-----------|--------------|------------|
| Lambda | Excellent | Good | Poor |
| Fargate | Good | Excellent | Good |
| EC2 | Poor | Good | Excellent |
| RDS | Poor | Good | Excellent |
| DynamoDB | Excellent | Good | Good |
| S3 | Excellent | Excellent | Excellent |
