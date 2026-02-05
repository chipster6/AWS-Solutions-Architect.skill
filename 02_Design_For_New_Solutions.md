# AWS Design for New Solutions Documentation

## Canonical Reference for Architecture Design, Patterns, and Best Practices

**Version:** 1.0  
**Last Updated:** 2026-02-04  
**Purpose:** Comprehensive guide for designing new AWS solutions, consolidating all design methodology, patterns, anti-patterns, and best practices

---

## Table of Contents

1. [Role of a Solutions Architect](#1-role-of-a-solutions-architect)
2. [Architecture Design Process](#2-architecture-design-process)
3. [Discovery Framework](#3-discovery-framework)
4. [AWS Well-Architected Framework](#4-aws-well-architected-framework)
5. [Operational Excellence Design Principles](#5-operational-excellence-design-principles)
6. [Architecture Patterns](#6-architecture-patterns)
7. [Anti-Patterns and Failure Modes](#7-anti-patterns-and-failure-modes)
8. [Trade-offs and Considerations](#8-trade-offs-and-considerations)
9. [Architecture Review Process](#9-architecture-review-process)
10. [Decision Frameworks](#10-decision-frameworks)
11. [Implementation Guidelines](#11-implementation-guidelines)
12. [Exam Scenarios and Validation](#12-exam-scenarios-and-validation)

---

## 1. Role of a Solutions Architect

A Solutions Architect bridges business requirements with technical implementation. Unlike developers who focus on code or system administrators who focus on operations, Solutions Architects design systems that meet business goals while adhering to technical constraints.

### Core Responsibilities

1. **Requirement Translation:** Understanding business needs and translating them into technical specifications. This involves asking the right questions: What problem are we solving? Who are the users? What does success look like?

2. **Technology Selection:** Choosing the right tools for the job. AWS offers 200+ services, and selecting the wrong one can lead to cost overruns, performance issues, or operational complexity.

3. **Risk Management:** Identifying and mitigating risks before they become problems. This includes security vulnerabilities, single points of failure, and scalability limitations.

4. **Cost Optimization:** Balancing performance requirements with budget constraints. Often, the most expensive solution isn't the best one.

5. **Stakeholder Communication:** Explaining complex technical concepts to non-technical stakeholders and justifying architectural decisions.

### Key Architectural Principles

**1. Design for Failure**

Everything fails eventually. AWS regions can go down, instances can crash, networks can partition. Good architecture assumes failure and designs around it.

**2. Loose Coupling**

Components should be independent. If Service A depends on Service B, and Service B goes down, Service A should degrade gracefully, not fail completely.

**3. Elasticity**

Systems should scale automatically based on demand. Don't provision for peak capacity 24/7—scale up when needed, scale down when not.

**4. Automation**

Manual processes are error-prone and don't scale. Automate deployments, testing, monitoring, and recovery.

**5. Security at Every Layer**

Don't rely on a single security control. Implement defense in depth with multiple security layers.

---

## 2. Architecture Design Process

Effective architecture design follows a systematic process:

### Phase 1: Discovery

- Gather business requirements (functional and non-functional)
- Understand constraints (budget, timeline, compliance, existing systems)
- Define success metrics and KPIs
- Identify risks and assumptions

### Phase 2: Conceptual Design

- Create high-level architecture diagrams
- Select major components and services
- Define integration points
- Estimate costs

### Phase 3: Detailed Design

- Specify configurations and parameters
- Design data models and flows
- Plan for security and compliance
- Create runbooks and operational procedures

### Phase 4: Validation

- Review against best practices (Well-Architected Framework)
- Conduct threat modeling
- Perform cost analysis
- Get peer reviews

### Phase 5: Implementation Support

- Guide development teams
- Troubleshoot issues
- Iterate based on feedback
- Document lessons learned

---

## 3. Discovery Framework

### Purpose

The discovery framework guides systematic discovery process that Solutions Architects use to understand requirements before designing architectures. It integrates Well-Architected Framework questions directly into discovery to ensure architectures align with AWS best practices from the start.

### Discovery Categories

**Business Requirements**

- Primary business objectives and success criteria
- User base size and geographic distribution
- Compliance and regulatory requirements
- Budget constraints and cost sensitivity
- Timeline and milestone requirements

**Technical Requirements**

- Performance requirements (latency, throughput, response time)
- Availability and durability requirements
- Scalability requirements (peak load, growth projections)
- Integration requirements (existing systems, APIs)
- Data requirements (volume, velocity, variety, veracity)

**Security Requirements**

- Data classification and protection requirements
- Access control and authentication requirements
- Encryption requirements (at rest, in transit)
- Compliance framework requirements (PCI-DSS, HIPAA, GDPR)
- Audit and logging requirements

**Operational Requirements**

- Monitoring and alerting requirements
- Deployment and release procedures
- Incident response procedures
- Disaster recovery requirements
- Operational hours and support constraints

### Discovery Artifacts

- Requirements document with prioritized features
- Risk register with mitigation strategies
- Assumptions document
- Constraints matrix
- Success criteria and KPIs

---

## 4. AWS Well-Architected Framework

The AWS Well-Architected Framework helps you understand the pros and cons of decisions you make while building systems on AWS. By using the Framework you will learn architectural best practices for designing and operating reliable, secure, efficient, cost-effective, and sustainable systems in the cloud.

### The Six Pillars

#### 4.1 Operational Excellence

The focus of the operational excellence pillar is running and monitoring systems to deliver business value, and continually improving processes and procedures.

Key questions:
- How do you design your workload so that you can understand its health?
- How do you reduce, and how do you design your workload to, mitigate the impact of issues?
- How do you meet operational requirements?

#### 4.2 Security

The security pillar focuses on protecting information and systems. Key areas include confidentiality and integrity of data, identifying and managing who can do what with privilege management, protecting systems, and establishing security controls.

Key questions:
- How do you protect your data at rest and in transit?
- How do you manage identities and permissions?
- How do you detect security events?

#### 4.3 Reliability

The reliability pillar focuses on ensuring a workload performs its intended function correctly and consistently when it's expected to. This includes the ability to recover from infrastructure or service disruptions, dynamically acquire computing resources to meet demand, and mitigate disruptions such as misconfiguration or transient network issues.

Key questions:
- How do you design your workload to prevent and recover from failures?
- How do you handle recovery procedures?
- How do you test reliability?

#### 4.4 Performance Efficiency

The performance efficiency pillar focuses on using computing resources efficiently to meet system requirements, and maintaining that efficiency as demand changes and technologies evolve.

Key questions:
- How do you select the best performing architecture for your workload?
- How do you monitor your workload to ensure it continues to operate as designed?
- How do you evolve your workload to take advantage of new releases?

#### 4.5 Cost Optimization

The cost optimization pillar focuses on avoiding unnecessary costs. Key topics include understanding and controlling where money is being spent, selecting the most appropriate and right number of resource types, analyzing spend over time, and scaling to meet business needs without overspending.

Key questions:
- How do you govern consumption?
- How do you monitor cost and usage?
- How do you select resources?

#### 4.6 Sustainability

The sustainability pillar focuses on minimizing the environmental impacts of running cloud workloads. Key areas include understanding impact, maximizing utilization, and measuring and improving efficiency.

Key questions:
- How do you understand your workload's environmental impact?
- How do you maximize utilization of your resources?
- How do you measure and improve sustainability outcomes?

---

## 5. Operational Excellence Design Principles

The following are design principles for operational excellence in the cloud. These principles are foundational to operating well-architected workloads.

### Principle 1: Organize Teams Around Business Outcomes

The ability of a team to achieve business outcomes comes from leadership vision, effective operations, and a business-aligned operating model. Leadership should be fully invested and committed to a CloudOps transformation with a suitable cloud operating model that incentivizes teams to operate in the most efficient way and meet business outcomes.

The right operating model uses people, process, and technology capabilities to scale, optimize for productivity, and differentiate through agility, responsiveness, and adaptation. The organization's long-term vision is translated into goals that are communicated across the enterprise to stakeholders and consumers of your cloud services. Goals and operational KPIs are aligned at all levels.

### Principle 2: Implement Observability for Actionable Insights

Gain a comprehensive understanding of workload behavior, performance, reliability, cost, and health. Establish key performance indicators (KPIs) and leverage observability telemetry to make informed decisions and take prompt action when business outcomes are at risk. Proactively improve performance, reliability, and cost based on actionable observability data.

Implementation approach:
- Instrument applications with detailed logging
- Collect metrics at appropriate granularity
- Create dashboards for operational visibility
- Set up alerts for anomaly detection
- Correlate logs, metrics, and traces

### Principle 3: Safely Automate Where Possible

In the cloud, you can apply the same engineering discipline that you use for application code to your entire environment. You can define your entire workload and its operations (applications, infrastructure, configuration, and procedures) as code, and update it. You can then automate your workload's operations by initiating them in response to events.

In the cloud, you can employ automation safety by configuring guardrails, including rate control, error thresholds, and approvals. Through effective automation, you can achieve consistent responses to events, limit human error, and reduce operator toil.

Implementation approach:
- Infrastructure as Code (CloudFormation, Terraform)
- Automated deployment pipelines (CodePipeline, CodeBuild)
- Automated testing and validation
- Self-healing infrastructure
- Automated scaling policies

### Principle 4: Make Frequent, Small, Reversible Changes

Design workloads that are scalable and loosely coupled to permit components to be updated regularly. Automated deployment techniques together with smaller, incremental changes reduces the blast radius and allows for faster reversal when failures occur. This increases confidence to deliver beneficial changes to your workload while maintaining quality and adapting quickly to changes in market conditions.

Implementation approach:
- Feature flags for controlled rollout
- Blue-green deployments
- Canary releases
- Automated rollback capabilities
- Trunk-based development

### Principle 5: Refine Operations Procedures Frequently

As you evolve your workloads, evolve your operations appropriately. As you use operations procedures, look for opportunities to improve them. Hold regular reviews and validate that all procedures are effective and that teams are familiar with them. Where gaps are identified, update procedures accordingly. Communicate procedural updates to all stakeholders and teams.

Implementation approach:
- Runbook reviews and updates
- Post-incident reviews with action items
- Regular game day exercises
- Knowledge sharing sessions
- Procedure testing and validation

### Principle 6: Anticipate Failure

Maximize operational success by driving failure scenarios to understand the workload's risk profile and its impact on your business outcomes. Test the effectiveness of your procedures and your team's response against these simulated failures. Make informed decisions to manage open risks that are identified by your testing.

Implementation approach:
- Chaos engineering experiments
- Disaster recovery testing
- Failure mode analysis
- Capacity testing
- Security penetration testing

### Principle 7: Learn from All Operational Events and Metrics

Drive improvement through lessons learned from all operational events and failures. Share what is learned across teams and through the entire organization. Learnings should highlight data and anecdotes on how operations contribute to business outcomes.

Implementation approach:
- Blameless post-mortems
- Knowledge base creation
- Trend analysis and patterns
- Continuous improvement metrics
- Cross-team learning sessions

### Principle 8: Use Managed Services

Reduce operational burden by using AWS managed services where possible. Build operational procedures around interactions with those services.

Implementation approach:
- Evaluate managed vs self-managed trade-offs
- Understand shared responsibility model
- Monitor service health and SLAs
- Leverage service quotas and limits
- Plan for service deprecations

---

## 6. Architecture Patterns

### 6.1 Three-Tier Web Application

**Classic Pattern:**

```
Internet
    |
    v
Presentation Tier (Web)
    - CloudFront (CDN)
    - S3 (Static website)
    
Application Tier (Logic)
    - ALB (Load balancing)
    - EC2/ECS/EKS (Application servers)
    - Auto Scaling (Dynamic scaling)
    
Data Tier (Storage)
    - RDS/Aurora (Database)
    - ElastiCache (Session store)
```

**When to Use:**
- Traditional web applications
- Well-understood pattern
- Easy to implement

### 6.2 Serverless Microservices

**Modern Pattern:**

```
Internet
    |
    v
API Gateway
    |
    v
Lambda Functions (Per microservice)
    |
    +-- Lambda: User Service
    +-- Lambda: Order Service
    +-- Lambda: Payment Service
    |
    v
DynamoDB (Per-service tables)
```

**When to Use:**
- Variable workloads
- Cost optimization priority
- Rapid development needed
- Independent deployment needed

### 6.3 Event-Driven Architecture

Event-driven architectures communicate across different systems using networks, which introduce variable latency. For workloads that require very low latency, such as real-time trading systems, this design might not be the best choice. However, for highly scalable and available workloads, or those with unpredictable traffic patterns, event-driven architectures can provide an effective way to meet these demands.

**Key Components:**

1. **Direct invocation (push method):** AWS services trigger Lambda functions directly
   - Amazon S3 triggers a function when a file is uploaded
   - API Gateway triggers a function when it receives an HTTP request

2. **Event source mapping (pull method):** Lambda retrieves events and invokes functions
   - Lambda retrieves messages from an Amazon SQS queue and invokes a function
   - Lambda reads records from a DynamoDB stream and invokes a function

**Event-Driven Pattern Example:**

```
S3 Bucket (Event Source)
    |
    v
Lambda: Process Upload
    |
    +-- Publishes event to EventBridge/SNS
         |
         +-- Lambda: Process Image
         +-- Lambda: Send Notification
         +-- Lambda: Update Analytics
```

**Benefits:**
- Replacing polling and webhooks with events
- Reducing complexity
- Improving scalability and extensibility
- Near-real-time processing
- Loose coupling between services

### 6.4 Microservices with Lambda

Typical monolithic applications consist of different layers: a presentation layer, an application layer, and a data layer. Microservices architectures separate functionalities into cohesive "verticals" according to specific domains, rather than technological layers.

**Recommended Approach:**

Break down monolithic Lambda functions into individual microservices, mapping a single Lambda function to a single, well-defined task.

```
API Gateway
    |
    v
Microservices Layer
    |
    +-- Lambda: Create User (handles /users POST)
    +-- Lambda: Get User (handles /users/{id} GET)
    +-- Lambda: Update User (handles /users/{id} PUT)
    +-- Lambda: Delete User (handles /users/{id} DELETE)
    |
    v
Per-Service Data Stores
```

### 6.5 Step Functions Orchestration

For complex processes with multiple types of failure and retry logic, Step Functions can help reduce the amount of custom code needed to orchestrate the workflow. Step Functions orchestrates the work and robustly handles errors and retries, and the Lambda functions contain only business logic.

**Pattern:**

```
Start
    |
    v
Step Function Workflow
    |
    +-- Task: Validate Order
    |       |
    |       v
    +-- Task: Reserve Inventory (with retry)
    |       |
    |       v
    +-- Task: Process Payment (with compensation)
    |       |
    |       v
    +-- Task: Create Invoice
    |
    v
End (Success or Failure)
```

**Benefits:**
- Visual workflow management
- Built-in error handling and retries
- State management
- Durability and persistence
- Audit trail

### 6.6 SQS Buffering Between Services

If a downstream process is slower than an upstream process, the queue durably persists messages and decouples the two functions.

```
Lambda: Create Order
    |
    v
SQS Queue (Buffer)
    |
    v
Lambda: Process Payment (slower)
```

**Benefits:**
- Decoupling producers and consumers
- Load leveling
- Message durability
- Error handling via dead letter queues
- Cost optimization

### 6.7 CQRS Pattern

Command Query Responsibility Segregation separates read and write operations into different models.

```
Commands (Writes)
    |
    v
Command Handler Lambda
    |
    v
Write Database (Authoritative)
    |
    +-- Event sourcing
    |       |
    |       v
    |   Event Store
    |
    +-- Async propagation
            |
            v
        Read Database (Optimized for queries)
                |
                v
            Query API
```

**Benefits:**
- Optimized read and write performance
- Scalability of read and write paths independently
- Flexibility in query models
- Audit trail for writes

---

## 7. Anti-Patterns and Failure Modes

When building event-driven architectures with Lambda, avoid the following common anti-patterns.

### 7.1 The Lambda Monolith

In many applications migrated from traditional servers, developers "lift and shift" existing code. Frequently, this results in a single Lambda function that contains all of the application logic that is triggered for all events. For a basic web application, a monolithic Lambda function would handle all API Gateway routes and integrate with all necessary downstream resources.

**Drawbacks:**

- **Package size:** The Lambda function might be much larger because it contains all possible code for all paths, which makes it slower for the Lambda service to run.
- **Hard to enforce least privilege:** The function's execution role must allow permissions to all resources needed for all paths, making the permissions very broad.
- **Harder to upgrade:** Any upgrades to the single function are more risky and could break the entire application.
- **Harder to maintain:** It's more difficult to have multiple developers working on the service since it's a monolithic code repository.
- **Harder to reuse code:** It's harder to separate reusable libraries from monoliths, making code reuse more difficult.
- **Harder to test:** As the lines of code increase, it becomes harder to unit test all the possible combinations of inputs.

**Solution:** Break down the monolithic Lambda function into individual microservices, mapping a single Lambda function to a single, well-defined task.

### 7.2 Recursive Patterns Causing Runaway Lambda Functions

AWS services generate events that invoke Lambda functions, and Lambda functions can send messages to AWS services. Generally, the service or resource that invokes a Lambda function should be different to the service or resource that the function outputs to. Failure to manage this can result in infinite loops.

**Example:**

```
Lambda Function
    |
    v
Write to S3 bucket
    |
    v
S3 trigger
    |
    v
Same Lambda Function ← LOOP!
```

**Consequences:**
- Lambda scales to consume all available concurrency
- S3 continues to write objects and generate more events
- Significant cost implications
- Potential service disruption

**Solution:** Use recursive loop detection to find and avoid this anti-pattern. Ensure that the output resource is different from the input trigger.

### 7.3 Lambda Functions Calling Lambda Functions Synchronously

Functions enable encapsulation and code re-use. Most programming languages support the concept of code synchronously calling functions within a code base. While Lambda functions directly calling other Lambda functions is generally an anti-pattern due to cost and complexity concerns, this doesn't apply to durable functions, which are specifically designed to orchestrate multi-step workflows.

**Problems:**

- **Cost:** With Lambda, you pay for the duration of an invocation. When one function calls another synchronously, both functions are billed for the entire duration.
- **Error handling:** In nested invocations, error handling can become much more complex.
- **Tight coupling:** The availability of the entire workflow is limited by the slowest function.
- **Scaling:** The concurrency of all three functions must be equal, using more concurrency than would otherwise be needed.

**Example Problem:**

```
Create Order Lambda
    |
    v (waits)
Process Payment Lambda
    |
    v (waits)
Create Invoice Lambda
    |
    v
Return to caller
(all three billed during wait time)
```

**Solutions:**

1. Use an Amazon SQS queue between Lambda functions
2. Use AWS Step Functions for complex orchestration

### 7.4 Synchronous Waiting Within a Single Lambda Function

Make sure that any potentially concurrent activities are not scheduled synchronously within a single Lambda function.

**Problem:**

```
Lambda Function
    |
    +-- Write to S3 bucket (waits)
    +-- Write to DynamoDB table (waits)
    +-- Call external API (waits)
    |
    v
Return response
```

This increases latency unnecessarily and can cause timeouts if any downstream service is slow.

**Solution:** Use asynchronous patterns:
- EventBridge for fan-out
- SQS for buffering
- Step Functions for orchestration

### 7.5 Nested Function Calls Anti-Pattern

Similar to Lambda calling Lambda, nested function calls within a synchronous workflow create tight coupling and increase the blast radius of failures.

**Problem:**

```
Parent Function
    |
    v
Child Function 1
    |
    v
Grandchild Function 1.1
    |
    v
Grandchild Function 1.2
    |
    v
Child Function 2
```

**Solutions:**
- Flatten the call hierarchy
- Use asynchronous messaging
- Implement circuit breaker patterns
- Consider Step Functions for complex workflows

---

## 8. Trade-offs and Considerations

### 8.1 Variable Latency

Unlike monolithic applications, which might process everything within the same memory space on a single device, event-driven applications communicate across networks. This design introduces variable latency. While it's possible to engineer applications to minimize latency, monolithic applications can almost always be optimized for lower latency at the expense of scalability and availability.

**Workloads NOT suitable for event-driven architecture:**
- High-frequency trading applications
- Sub-millisecond robotics automation
- Real-time gaming systems
- Low-latency financial systems

### 8.2 Eventual Consistency

An event represents a change in state, and with many events flowing through different services in an architecture at any given point of time, such workloads are often eventually consistent.

**Challenges:**
- Processing transactions becomes more complex
- Handling duplicates requires additional logic
- Determining the exact overall state of a system is harder

**Patterns to Address:**
- DynamoDB strongly consistent reads (higher latency, more throughput)
- DynamoDB transactions for ACID properties
- Amazon RDS for ACID compliance
- Amazon RDS Proxy for connection management

### 8.3 Cost Implications

**Lambda Duration Billing:**
- Pay per millisecond of execution
- Synchronous waiting consumes billed time
- Nested invocations multiply costs

**Cost Optimization Strategies:**
- Right-size memory and timeout settings
- Use provisioned concurrency for predictable workloads
- Implement proper error handling to avoid retries
- Monitor and optimize cold start frequency

### 8.4 Error Handling Complexity

In nested invocations, error handling can become much more complex. For example, an error in a downstream function might require upstream functions to reverse their work (compensation).

**Solutions:**
- Implement retry with exponential backoff
- Use dead letter queues for failed events
- Implement circuit breaker patterns
- Use Step Functions for built-in error handling
- Design compensation transactions for rollback

### 8.5 Tight Coupling

Processing dependencies can create tight coupling between services. In synchronous patterns, the availability of the entire workflow is limited by the slowest function.

**Solutions:**
- Use asynchronous messaging for loose coupling
- Implement timeouts and circuit breakers
- Design for graceful degradation
- Use bulkhead patterns for isolation

### 8.6 Debugging Across Services

Debugging event-driven systems is different compared to a monolithic application. With different systems and services passing events, it's not possible to record and reproduce the exact state of multiple services when errors occur.

**Requirements for Successful Debugging:**
1. **Robust logging system:** Critical, provided by CloudWatch
2. **Transaction identifiers:** Every event should have a unique ID logged at each step
3. **Automated log analysis:** Use X-Ray for distributed tracing

**Tools:**
- AWS X-Ray for distributed tracing
- CloudWatch Logs Insights for log analysis
- ServiceLens for unified observability
- CloudWatch Metrics for performance monitoring

---

## 9. Architecture Review Process

The review of architectures must be done in a consistent manner, with a blame-free approach that encourages diving deep. It should be a lightweight process (hours not days) that is a conversation and not an audit.

### 9.1 Review Principles

1. **Consistent approach:** Use the same methodology for every review
2. **Blame-free environment:** Focus on systems, not people
3. **Dive deep:** Don't surface-level reviews; understand the details
4. **Conversation, not audit:** Collaborative exploration, not checklist completion
5. **Identify critical issues:** Focus on high-impact problems first

### 9.2 Review Frequency

**Nearly Continuous Approach:**

The recommended approach is for team members who build an architecture to use the Well-Architected Framework to continually review their architecture, rather than holding a formal review meeting. A nearly continuous approach permits team members to update answers as the architecture evolves, and improve the architecture as they deliver features.

**Milestone-Based Reviews:**

Reviews should be applied at key milestones:
- Early in the design phase (before one-way doors)
- Before the go-live date
- After significant architecture changes
- Periodically in production (quarterly)

### 9.3 One-Way vs Two-Way Doors

**Two-Way Doors:**

Many decisions are reversible. These decisions can use a lightweight process.
- Feature flags enable easy reversibility
- Canary deployments limit blast radius
- Database schema changes with backward compatibility

**One-Way Doors:**

One-way doors are hard or impossible to reverse and require more inspection before making them.
- Region selection
- Database engine choice
- Core data model changes
- Security architecture changes
- Pricing model commitments

### 9.4 Review Meeting Facilitation

**Suggested Items:**

- Meeting room with whiteboards
- Printouts of any diagrams or design notes
- Action list of questions requiring out-of-band research
- Well-Architected Tool export or checklist

### 9.5 Handling Team Objections

**"We are too busy!"**

If you are getting ready for a big launch, you will want it to go smoothly. The review will permit you to understand any problems you might encounter before they become emergencies.

**"This will slow us down!"**

The review is meant to be lightweight (hours, not days). The goal is to identify critical issues early when they're cheaper to fix.

**"Our architecture is simple, we don't need this."**

Simple architectures can hide complex problems. Even simple systems benefit from systematic review.

### 9.6 Post-Review Actions

After you have done a review, you should have a list of issues that you can prioritize based on your business context. Take into account the impact of those issues on the day-to-day work of your team. If you address these issues early, you could free up time to work on creating business value rather than solving recurring problems.

**Prioritization Criteria:**

- Risk to business outcomes
- Effort to remediate
- Frequency of impact
- Dependencies on other changes
- Compliance requirements

---

## 10. Decision Frameworks

### 10.1 Compute Selection Framework

| Requirement | Recommended Service | Alternative |
|-------------|-------------------|-------------|
| Serverless, event-driven | Lambda | Step Functions |
| Container orchestration | EKS | ECS |
| Virtual machines | EC2 | Lightsail |
| Batch processing | Batch | Lambda (for short jobs) |
| High performance computing | EC2 Spot | Lambda (limited) |

### 10.2 Database Selection Framework

| Requirement | Recommended Service | Consideration |
|-------------|-------------------|---------------|
| Relational data | RDS/Aurora | Strong consistency, ACID |
| Key-value, high scale | DynamoDB | Eventual consistency, serverless |
| In-memory cache | ElastiCache | Low latency reads |
| Document store | DynamoDB | Flexible schema |
| Time series | Timestream | Optimized for time-series data |
| Graph | Neptune | Relationship traversal |

### 10.3 Storage Selection Framework

| Requirement | Recommended Service | Consideration |
|-------------|-------------------|---------------|
| Object storage | S3 | Durability, scalability |
| Block storage | EBS | EC2-optimized |
| File storage | EFS/FSx | Shared access |
| Data lake | S3 + Lake Formation | Analytics |
| Archive | S3 Glacier | Cost optimization |

### 10.4 Architecture Pattern Selection

| Requirement | Pattern | When to Use |
|-------------|---------|------------|
| Rapid development, variable load | Serverless | Microservices, event-driven |
| Complex business logic | Step Functions | Multi-step workflows |
| High throughput, low latency | Three-tier | Traditional web apps |
| Real-time processing | Event-driven | Async workflows |
| Read-heavy workloads | CQRS | Separate read/write optimization |

### 10.5 Migration Strategy Selection (6 R's)

1. **Rehost:** Lift and shift (no changes)
2. **Replatform:** Minor optimizations (managed services)
3. **Repurchase:** Move to SaaS product
4. **Refactor:** Application modernization
5. **Retire:** Decommission legacy systems
6. **Retain:** Keep on-premises for now

---

## 11. Implementation Guidelines

### 11.1 Infrastructure as Code

Define your entire workload and its operations as code:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Production workload infrastructure

Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.micro
      ImageId: ami-12345678
      SecurityGroupIds:
        - !Ref MySecurityGroup
      Tags:
        - Key: Environment
          Value: Production
```

### 11.2 CI/CD Pipeline Implementation

```yaml
Pipeline:
  Source Stage:
    - CodeCommit Repository
    - Webhook trigger on push
  
  Build Stage:
    - CodeBuild Project
    - Build artifacts
    - Run tests
  
  Deploy Stage:
    - CodeDeploy Application
    - Deploy to ECS/EC2/Lambda
```

### 11.3 Security Implementation

**Principle of Least Privilege:**

```json
// GOOD: Only permissions needed for the job
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": "arn:aws:s3:::my-bucket/uploads/*"
}
```

**Enable Traceability:**
- Implement detailed logging
- Use CloudTrail for API calls
- Enable VPC Flow Logs
- Use X-Ray for tracing

### 11.4 Monitoring and Observability

**CloudWatch Dashboard:**

```yaml
Resources:
  MyDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: Production-Dashboard
      DashboardBody: |
        {
          "widgets": [
            {
              "type": "metric",
              "x": 0,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "title": "CPU Utilization",
                "metrics": [["AWS/EC2", "CPUUtilization", "InstanceId", "i-12345678"]],
                "period": 300,
                "stat": "Average"
              }
            }
          ]
        }
```

### 11.5 Disaster Recovery Implementation

**Recovery Objectives:**
- RTO (Recovery Time Objective): Maximum acceptable downtime
- RPO (Recovery Point Objective): Maximum acceptable data loss

**Implementation:**

| Strategy | RTO | RPO | Use Case |
|----------|-----|-----|----------|
| Backup & Restore | 4-24 hours | 24+ hours | Non-critical workloads |
| Pilot Light | 30-60 min | Minutes-Hours | Low RTO tolerance |
| Warm Standby | 5-15 min | Minutes | Medium RTO tolerance |
| Multi-Site Active-Active | Seconds | Seconds | Mission critical |

---

## 12. Exam Scenarios and Validation

### Scenario 1: Event-Driven Architecture Design

**Question:**

A company wants to process uploaded images asynchronously. When images are uploaded to S3, they should be:
1. Resized into multiple versions
2. Analyzed for content moderation
3. Metadata extracted and stored
4. Notifications sent to users

What is the recommended approach?

**Answer:**

Use an event-driven architecture with S3 triggers and Lambda functions for each processing step, connected through EventBridge or SNS for fan-out.

```
S3 Bucket (upload)
    |
    v
Lambda: Trigger Processor
    |
    v
EventBridge/SNS (fan-out)
    |
    +-- Lambda: Resize Images
    +-- Lambda: Content Moderation
    +-- Lambda: Extract Metadata
    |
    v
Results stored in DynamoDB/S3
Notifications sent via SNS
```

**Key Points:**
- Decoupled processing steps
- Independent scaling of each processor
- Fault isolation (one failure doesn't block others)
- Easy to add new processors

### Scenario 2: Anti-Pattern Recognition

**Question:**

A developer has created a Lambda function that processes orders. The function:
1. Validates the order
2. Calls another Lambda to process payment
3. Calls another Lambda to create an invoice
4. Calls another Lambda to send confirmation

All calls are synchronous. What is the problem and solution?

**Problem:**

This is the "Lambda calling Lambda synchronously" anti-pattern.

Issues:
- Cost: All functions billed during waiting time
- Tight coupling: Failure in any step fails the entire chain
- Scaling: All functions must scale together
- Error handling: Complex compensation logic needed

**Solution:**

Use Step Functions or SQS for orchestration:

```
Start → Validate Order → SQS Queue → Process Payment
                                    ↓
                            Success: Create Invoice
                                    ↓
                            Success: Send Confirmation
                                    
Alternative: Use Step Functions with built-in error handling
```

### Scenario 3: Architecture Review Process

**Question:**

A team is about to launch a new critical application. They say they're too busy for a Well-Architected review. How do you respond?

**Answer:**

The review is meant to be lightweight (hours, not days). If they're getting ready for a big launch, they want it to go smoothly. The review will permit them to understand any problems they might encounter before they become emergencies.

**Approach:**

1. Frame it as risk mitigation, not overhead
2. Offer a focused review (2-3 hours)
3. Prioritize critical path components
4. Use findings as action items, not blockers
5. Schedule follow-up reviews for non-critical items

**Key Points:**
- One-way door decisions need review before commitment
- Early issue detection is cheaper than production fixes
- Team ownership of quality, not external audit

### Scenario 4: Trade-off Analysis

**Question:**

A financial services company needs sub-millisecond latency for trading decisions. They're considering event-driven architecture. What trade-offs should you discuss?

**Answer:**

Event-driven architectures introduce variable latency due to network communication between services. For sub-millisecond requirements, this pattern is not suitable.

**Trade-offs to Discuss:**

1. **Latency vs Scalability:** Event-driven provides scalability but adds network latency
2. **Consistency vs Performance:** Eventual consistency may not meet financial requirements
3. **Cost vs Control:** Serverless is cost-effective but less predictable performance

**Alternative Approaches:**

- Monolithic architecture within a single instance
- In-memory processing (ElastiCache)
- Direct database access instead of service calls
- Consider EC2 with custom optimization

### Scenario 5: Operational Excellence Implementation

**Question:**

How would you implement the "Learn from all operational events" principle?

**Answer:**

1. **Blameless Post-Mortems:**
   - Focus on system improvements, not blame
   - Document what happened, why, and how to prevent
   - Share learnings across teams

2. **Metrics-Driven Improvement:**
   - Track MTTR (Mean Time to Recovery)
   - Monitor error rates and trends
   - Set improvement targets

3. **Knowledge Sharing:**
   - Regular show-and-tell sessions
   - Centralized documentation
   - Runbook maintenance

4. **Continuous Validation:**
   - Chaos engineering experiments
   - Regular game days
   - Failure mode testing

---

## Conclusion

This document provides comprehensive coverage of AWS architecture design for new solutions. It consolidates:

- Architecture design methodology
- Discovery framework
- Well-Architected Framework integration
- Operational Excellence design principles (all 8 from AWS)
- Architecture patterns (microservices, serverless, event-driven)
- Anti-patterns (all 5 Lambda anti-patterns from AWS)
- Trade-offs documentation
- Architecture review process
- Decision frameworks
- Implementation guidelines

Use this document as the canonical reference for designing new AWS solutions aligned with AWS best practices.

---

## References

- AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- Operational Excellence Design Principles: https://docs.aws.amazon.com/wellarchitected/latest/framework/oe-design-principles.html
- Architecture Selection: https://docs.aws.amazon.com/wellarchitected/2023-10-03/framework/perf-arch.html
- Event-Driven Architecture Anti-Patterns: https://docs.aws.amazon.com/lambda/latest/dg/concepts-event-driven-architectures.html
- Architecture Review Process: https://docs.aws.amazon.com/wellarchitected/latest/framework/the-review-process.html
- Microservices on AWS: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/simple-microservices-architecture-on-aws.html

---

*Document Version: 1.0*  
*Last Updated: 2026-02-04*  
*Status: Canonical Reference*