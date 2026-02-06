---
title: AWS Architecture Patterns
type: pattern-catalog
version: 1.0
provider: aws
last_updated: "2024-01-01"
---

# AWS Architecture Patterns Catalog

## Serverless Patterns

### Event-Driven Architecture
```mermaid
graph LR
    A[Source] --> B[Event Bus]
    B --> C[Lambda 1]
    B --> D[Lambda 2]
    C --> E[(DynamoDB)]
    D --> F[(S3)]
```

**Components:**
- Event Source: S3, DynamoDB, SNS, etc.
- Event Bus: EventBridge, SNS
- Processing: Lambda functions
- Storage: DynamoDB, S3

**Best Practices:**
- Use dead-letter queues for failed events
- Implement idempotency in Lambda handlers
- Use EventBridge for complex routing

### API Gateway + Lambda
```mermaid
graph LR
    A[Client] --> B[API Gateway]
    B --> C[Lambda]
    C --> D[(DynamoDB)]
    C --> E[(S3 Presigned URL)]
```

**Components:**
- API Gateway (REST or HTTP)
- Lambda functions
- DynamoDB or other storage
- IAM roles for authorization

**Best Practices:**
- Use API keys or Cognito for auth
- Implement caching at API Gateway
- Use Lambda Power Tools for observability

## Microservices Patterns

### ECS Microservices
```mermaid
graph TB
    subgraph VPC
        A[ALB] --> B[Service A]
        A --> C[Service B]
        B --> D[(RDS)]
        C --> E[(Redis)]
    end
```

**Components:**
- Application Load Balancer
- ECS services
- RDS/Aurora databases
- ElastiCache Redis

**Best Practices:**
- Use service discovery
- Implement health checks
- Use Fargate for serverless containers

### EKS with Service Mesh
```mermaid
graph TB
    subgraph EKS
        A[Ingress] --> B[Mesh Gateway]
        B --> C[Service A]
        B --> D[Service B]
        C --> E[(Database)]
    end
```

**Components:**
- AWS Load Balancer Controller
- Istio or App Mesh
- EKS cluster
- Kubernetes services

**Best Practices:**
- Use IAM roles for service accounts
- Implement network policies
- Use Karpenter for auto-scaling

## Data Patterns

### Data Lake Landing + Curated
```mermaid
graph LR
    A[Raw S3] --> B[Glue ETL]
    B --> C[Curated S3]
    C --> D[Athena]
    C --> E[Lake Formation]
```

**Components:**
- S3 buckets (raw, curated, analytics)
- AWS Glue (ETL, crawlers, Data Catalog)
- Athena (SQL queries)
- Lake Formation (governance)

**Best Practices:**
- Use Lake Formation for fine-grained access
- Implement partition strategies
- Use columnar formats (Parquet, ORC)

### Real-Time Streaming
```mermaid
graph LR
    A[Kinesis Data Streams] --> B[Lambda]
    B --> C[DynamoDB Streams]
    C --> D[Lambda Consumer]
    D --> E[(S3)]
```

**Components:**
- Kinesis Data Streams
- Lambda or Kinesis Data Analytics
- DynamoDB Streams
- S3 for batch processing

**Best Practices:**
- Use enhanced monitoring
- Implement retry mechanisms
- Use Kinesis Producer Library for high throughput

## Network Patterns

### Hub-and-Spoke with TGW
```mermaid
graph TB
    subgraph Hub
        A[TGW] --> B[Inspection VPC]
        A --> C[Shared Services]
    end
    subgraph Spokes
        D[VPC 1] --> A
        E[VPC 2] --> A
    end
```

**Components:**
- Transit Gateway
- VPC attachments
- Route tables
- Security groups

**Best Practices:**
- Use separate route tables per attachment
- Implement TGW Network Manager
- Use AWS Firewall Manager for policies

### Multi-Region Active-Active
```mermaid
graph TB
    subgraph "us-east-1"
        A[Route 53] --> B[Primary LB]
        B --> C[EC2/VPC 1]
    end
    subgraph "us-west-2"
        A --> D[Secondary LB]
        D --> E[EC2/VPC 2]
    end
```

**Components:**
- Route 53 with health checks
- Global Accelerator
- CloudFront CDN
- Multiple region deployments

**Best Practices:**
- Use R53 latency-based routing
- Implement active-active failover
- Use CloudFront for static assets

## AI/ML Patterns

### RAG Architecture
```mermaid
graph TB
    subgraph "Knowledge Base"
        A[S3 Documents] --> B[Embedding Model]
        B --> C[Vector DB]
    end
    subgraph "Generation"
        D[User Query] --> E[Embedding]
        E --> F[Similarity Search]
        F --> G[Prompt Engineering]
        G --> H[Bedrock Claude]
        H --> I[Response]
    end
```

**Components:**
- S3 for document storage
- Titan Embedding model
- OpenSearch/Pinecone vector DB
- Bedrock Claude for generation

**Best Practices:**
- Implement chunking strategies
- Use guardrails for content filtering
- Cache frequently accessed embeddings

### SageMaker MLOps Pipeline
```mermaid
graph LR
    A[S3 Data] --> B[SageMaker Processing]
    B --> C[SageMaker Training]
    C --> D[Model Registry]
    D --> E[Endpoint Deployment]
    E --> F[CloudWatch Monitoring]
```

**Components:**
- S3 for data/artifacts
- SageMaker Processing
- SageMaker Training
- SageMaker Endpoints
- CloudWatch Model Monitor

**Best Practices:**
- Use Spot instances for training
- Implement CI/CD for models
- Use Model Monitor for drift detection

## Serverless Data Processing
```mermaid
graph LR
    A[S3 Event] --> B[Lambda Trigger]
    B --> C[Step Functions]
    C --> D[DynamoDB]
    D --> E[AppSync]
    E --> F[React App]
```

**Components:**
- S3 event notifications
- Lambda functions
- Step Functions workflows
- DynamoDB tables
- AppSync GraphQL API

**Best Practices:**
- Use Step Functions for complex workflows
- Implement state machines with callbacks
- Use AppSync for real-time subscriptions
