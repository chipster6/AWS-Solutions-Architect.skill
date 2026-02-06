# Architecture Patterns Reference

**Document ID:** pattern-architecture  
**Index:** [GOV-ARCH-001](../GOV-ARCH-001-Architecture-Documentation-Index.md)  
**Router:** [docs/patterns/architecture.md](../docs/patterns/architecture.md)  
**Related:** [service-decisions-enhanced.md](service-decisions-enhanced.md), [well-architected-pillars.md](well-architected-pillars.md), [CROSS_REFERENCE_INDEX.md](../CROSS_REFERENCE_INDEX.md)

## Purpose

This reference provides common AWS architecture patterns. Always consult AWS Prescriptive Guidance via MCP for current implementation details and official patterns.

### Related Documents
- **[Service Decisions](service-decisions-enhanced.md)** - Select services to implement these patterns
- **[Well-Architected Pillars](well-architected-pillars.md)** - Review patterns against all 6 pillars
- **[Discovery Process](discovery-questions-enhanced.md)** - Use Phase 2 technical discovery for pattern selection
- **[Migration Patterns](migration-patterns.md)** - Patterns for migrated workloads
- **[Cross-Reference Index](../CROSS_REFERENCE_INDEX.md)** - Navigate by pattern type and service

## Pattern Categories

### 1. Serverless Web Application
**Pattern**: CloudFront + S3 (static) + API Gateway + Lambda + DynamoDB

**When to Use**:
- Variable/unpredictable traffic
- Want to minimize operational overhead
- Pay-per-use cost model preferred
- Don't need long-running processes

**Benefits**:
- Auto-scaling built-in
- Pay only for actual usage
- No server management
- High availability by default

**Trade-offs**:
- Cold start latency
- 15-minute Lambda timeout
- Limited control over infrastructure
- Vendor lock-in considerations

**MCP Lookup**: "serverless web application architecture AWS"

### 2. Microservices with Containers
**Pattern**: ALB + ECS/EKS + Service Mesh + RDS/DynamoDB + SQS/SNS

**When to Use**:
- Need fine-grained scalability
- Multiple teams, independent deployments
- Polyglot technology requirements
- Complex application with many services

**Benefits**:
- Independent scaling per service
- Technology flexibility
- Fault isolation
- Team autonomy

**Trade-offs**:
- Increased operational complexity
- Network latency between services
- Distributed tracing needed
- More complex testing

**MCP Lookup**: "microservices architecture patterns AWS"

### 3. Data Lake Architecture
**Pattern**: S3 (raw/processed/curated) + Glue + Athena + Lake Formation + QuickSight

**When to Use**:
- Store diverse data types
- Need schema-on-read flexibility
- Separate storage from compute
- Cost-effective analytics at scale

**Benefits**:
- Centralized data repository
- Scale storage and compute independently
- Support multiple analytics tools
- Cost-effective storage

**Trade-offs**:
- Requires data governance
- Can become data swamp without proper management
- Query performance depends on data organization
- Requires data cataloging effort

**MCP Lookup**: "data lake architecture AWS best practices"

### 4. Event-Driven Architecture
**Pattern**: EventBridge + Lambda + SQS + DynamoDB Streams + SNS

**When to Use**:
- Loosely coupled systems
- Asynchronous processing
- Fan-out to multiple consumers
- Event sourcing pattern

**Benefits**:
- Loose coupling
- Scalability
- Easy to add new event consumers
- Replay capability

**Trade-offs**:
- Eventually consistent
- Debugging complexity
- Message ordering challenges
- Requires idempotency

**MCP Lookup**: "event-driven architecture AWS patterns"

### 5. Hybrid Cloud Architecture
**Pattern**: Direct Connect + Transit Gateway + VPN + AWS Outposts

**When to Use**:
- Gradual cloud migration
- Data residency requirements
- Low-latency on-premises access needed
- Existing on-premises investments

**Benefits**:
- Flexibility in migration
- Leverage existing investments
- Meet compliance requirements
- Consistent experience

**Trade-offs**:
- Increased complexity
- Network dependency
- Higher costs
- Requires hybrid operations expertise

**MCP Lookup**: "hybrid cloud architecture AWS"

### 6. Real-Time Streaming Analytics
**Pattern**: Kinesis Data Streams + Kinesis Analytics + Lambda + S3 + Athena

**When to Use**:
- Real-time data processing
- IoT data ingestion
- Clickstream analytics
- Time-series data

**Benefits**:
- Sub-second latency
- Scalable ingestion
- Real-time insights
- Durable storage

**Trade-offs**:
- Higher complexity
- Costs for continuous processing
- Requires stream processing expertise
- Handling late-arriving data

**MCP Lookup**: "real-time streaming analytics AWS"

### 7. Machine Learning Pipeline
**Pattern**: S3 + SageMaker + Lambda + Step Functions + Model Registry

**When to Use**:
- ML model training and deployment
- Automated retraining pipelines
- Model versioning needed
- MLOps practices

**Benefits**:
- Managed ML infrastructure
- Experiment tracking
- Model versioning
- Easy deployment

**Trade-offs**:
- SageMaker costs
- Learning curve
- May be overkill for simple models
- Lock-in to AWS ML services

**MCP Lookup**: "machine learning pipeline architecture AWS"

### 8. Batch Processing Pipeline
**Pattern**: S3 + Glue + EMR/Batch + Athena + Step Functions

**When to Use**:
- Large-scale data transformations
- Scheduled processing jobs
- ETL workloads
- Non-time-critical processing

**Benefits**:
- Cost-effective for large datasets
- Parallel processing
- Managed services available
- Pay for compute only when running

**Trade-offs**:
- Not real-time
- Requires job orchestration
- Debugging batch jobs can be complex
- Resource sizing challenges

**MCP Lookup**: "batch processing architecture AWS"

## AWS Prescriptive Guidance Design Patterns

AWS provides official patterns via Prescriptive Guidance. Always consult these before recommending:

### Microservices Patterns
- **Anti-Corruption Layer**: Isolate legacy systems
- **Circuit Breaker**: Handle service failures gracefully
- **Saga Pattern**: Manage distributed transactions
- **Strangler Fig**: Gradually migrate monoliths

### Integration Patterns
- **API Routing**: Hostname, path, header-based
- **Publish-Subscribe**: Event-driven communication
- **Scatter-Gather**: Parallel processing with aggregation
- **Transactional Outbox**: Ensure message delivery

### Reliability Patterns
- **Retry with Backoff**: Handle transient failures
- **Bulkhead**: Isolate resources
- **Health Checks**: Automated recovery
- **Multi-Region Active-Active**: Geographic resilience

**MCP Lookup**: "AWS Prescriptive Guidance cloud design patterns"

## Pattern Selection Framework

### Step 1: Understand Requirements
- Scale (current and projected)
- Latency sensitivity
- Consistency requirements
- Operational complexity tolerance
- Team expertise

### Step 2: Identify Constraints
- Budget
- Timeline
- Compliance requirements
- Existing technology
- Team capabilities

### Step 3: Map to Patterns
- Match requirements to pattern characteristics
- Consider hybrid patterns when needed
- Balance trade-offs

### Step 4: Validate with AWS Documentation
- Use MCP to get current best practices
- Check for new services/features
- Review reference architectures

## Anti-Patterns to Avoid

### 1. One-Size-Fits-All
❌ Using the same architecture pattern for all workloads
✅ Choose pattern based on specific requirements

### 2. Over-Engineering
❌ Using microservices for small, simple applications
✅ Start simple, evolve as needed

### 3. Ignoring Operational Complexity
❌ Choosing complex patterns without operations expertise
✅ Match pattern to team capabilities

### 4. Premature Optimization
❌ Optimizing for scale before proving business model
✅ Build for current needs, design for evolution

### 5. Technology-Driven Decisions
❌ "Let's use Kubernetes because it's popular"
✅ Choose based on actual requirements

## Pattern Evolution

### MVP Phase
- Start simple
- Monolith or simple serverless
- Managed services preferred
- Quick to market

### Growth Phase
- Identify bottlenecks
- Introduce caching
- Consider breaking into services
- Optimize costs

### Scale Phase
- Multi-region if needed
- Advanced patterns (CQRS, Event Sourcing)
- Sophisticated observability
- Cost optimization focus

### Maturity Phase
- Platform thinking
- Self-service infrastructure
- Advanced automation
- Continuous optimization

## Getting Current Pattern Details

When recommending a pattern, always:

1. Search AWS Prescriptive Guidance:
   ```
   MCP_DOCKER:search_documentation "[pattern name] AWS architecture"
   ```

2. Get implementation details:
   ```
   MCP_DOCKER:read_documentation [URL from search]
   ```

3. Check for reference architectures:
   ```
   MCP_DOCKER:search_documentation "[pattern name] reference architecture"
   ```

4. Review service best practices:
   ```
   MCP_DOCKER:search_documentation "[service name] best practices"
   ```

This ensures recommendations are based on current AWS guidance and account for latest service features.
