# Migration Patterns Reference

## Purpose

This reference provides guidance on migrating workloads to AWS using the 6 R's migration strategy. Always consult AWS Migration documentation via MCP for current best practices.

## The 6 R's Migration Strategy

### 1. Rehost ("Lift and Shift")

**What it is**: Move applications to AWS with minimal changes

**When to use**:
- Quick migration needed
- Minimize initial changes/risks
- Prove business case for cloud
- Legacy applications without source code
- Want to optimize later after migration

**How it works**:
- Use AWS Application Migration Service (MGN)
- Or manual EC2 deployment
- Minimal application changes
- Keep same architecture initially

**Benefits**:
- Fastest migration path
- Lowest initial risk
- Immediate cloud benefits (elasticity, global reach)
- Can optimize post-migration

**Drawbacks**:
- Doesn't leverage cloud-native features
- May not be cost-optimized
- Technical debt carried forward
- Limited immediate improvements

**Typical Timeline**: Weeks to months

**MCP Lookup**: "AWS rehost migration best practices"

---

### 2. Replatform ("Lift, Tinker, and Shift")

**What it is**: Make minimal cloud optimizations during migration

**When to use**:
- Want some cloud benefits without full re-architecture
- Database migration opportunity (to RDS, Aurora)
- Application server modernization
- Balance speed with optimization

**How it works**:
- Migrate to AWS with targeted improvements
- Example: Move database to RDS instead of EC2
- Example: Use Elastic Beanstalk instead of custom servers
- Keep core application logic same

**Benefits**:
- Faster than refactoring
- Some immediate cloud benefits
- Reduced operational burden (managed services)
- Foundation for future optimization

**Drawbacks**:
- Still carrying some technical debt
- Not fully cloud-native
- May need future optimization
- Requires testing of changes

**Typical Timeline**: Months

**Examples**:
- SQL Server on EC2 → RDS SQL Server
- Self-managed Postgres → Aurora PostgreSQL
- Custom web servers → Elastic Beanstalk
- Self-managed Redis → ElastiCache

**MCP Lookup**: "AWS replatform migration strategies"

---

### 3. Repurchase ("Drop and Shop")

**What it is**: Move to a different product, usually SaaS

**When to use**:
- Commercial software with cloud version available
- Want to reduce maintenance burden
- Legacy licensing costs too high
- Willing to accept product differences

**How it works**:
- Move from on-premises to SaaS
- Example: Exchange Server → Microsoft 365
- Example: On-premises CRM → Salesforce
- Requires data migration and user training

**Benefits**:
- Reduced operational burden
- Always up-to-date
- Predictable pricing
- Vendor manages infrastructure

**Drawbacks**:
- May require business process changes
- Data migration complexity
- New vendor lock-in
- User retraining needed
- Potential feature differences

**Typical Timeline**: Months (including vendor selection)

**Examples**:
- On-premises email → Microsoft 365, Google Workspace
- On-premises CRM → Salesforce
- On-premises HR system → Workday
- Custom BI tool → AWS QuickSight, Tableau

**MCP Lookup**: "AWS marketplace migration SaaS"

---

### 4. Refactor / Re-architect

**What it is**: Re-imagine application using cloud-native features

**When to use**:
- Need significant improvements (scale, performance, cost)
- Modernization is strategic priority
- Willing to invest in transformation
- Want to leverage cloud-native capabilities
- Current architecture limits business agility

**How it works**:
- Decompose monoliths into microservices
- Adopt serverless architectures
- Implement event-driven patterns
- Use managed services extensively

**Benefits**:
- Maximum cloud benefits
- Improved scalability and resilience
- Better cost optimization opportunities
- Modern development practices
- Competitive advantage

**Drawbacks**:
- Highest cost and effort
- Longest timeline
- Requires skilled team
- Higher initial risk
- Business disruption possible

**Typical Timeline**: 6 months to 2+ years

**Common Patterns**:
- Monolith → Microservices (ECS/EKS)
- Traditional app → Serverless (Lambda)
- Batch processing → Event-driven (EventBridge, SQS)
- Self-managed → Managed services

**MCP Lookup**: "AWS refactoring migration modernization"

---

### 5. Retire

**What it is**: Decommission applications no longer needed

**When to use**:
- Application no longer provides business value
- Replaced by other systems
- Duplicate functionality exists
- Cost of migration exceeds value

**How it works**:
- Identify candidates during discovery
- Document dependencies
- Plan decommissioning
- Archive data if needed
- Shut down systems

**Benefits**:
- Reduce complexity
- Lower costs immediately
- Reduce attack surface
- Free up team resources

**Key Considerations**:
- Verify truly not needed
- Document dependencies
- Plan data archival
- Communicate to stakeholders
- Have rollback plan

**Typical Savings**: 10-20% of portfolio

**MCP Lookup**: "AWS migration portfolio rationalization"

---

### 6. Retain (Revisit)

**What it is**: Keep on-premises for now, revisit later

**When to use**:
- Not ready for migration (technical/business reasons)
- Recently invested in on-premises infrastructure
- Complex dependencies not yet resolved
- Regulatory/compliance blockers
- Waiting for other migrations to complete

**How it works**:
- Document reason for retaining
- Set review date
- Plan future migration path
- May still use AWS for DR or dev/test

**Strategy**:
- Not a permanent decision
- Keep on migration roadmap
- Address blockers over time
- Re-evaluate periodically

**Common Reasons**:
- Mainframe applications (complex migration)
- Recently purchased hardware
- Compliance requirements (being addressed)
- Dependencies on other systems
- Performance concerns (need more analysis)

**MCP Lookup**: "AWS hybrid cloud architecture"

---

## Migration Phases

### Phase 1: Assessment & Planning

**Activities**:
1. **Discover**:
   - Inventory applications
   - Map dependencies
   - Assess complexity
   - Gather performance data

2. **Prioritize**:
   - Score applications (business value, migration complexity)
   - Identify quick wins
   - Plan wave order
   - Create migration roadmap

3. **Plan**:
   - Choose R strategy per application
   - Estimate effort and cost
   - Identify risks
   - Resource planning

**Tools**:
- AWS Application Discovery Service
- Migration Evaluator
- Migration Hub

**Duration**: 1-3 months

**MCP Lookup**: "AWS migration assessment planning"

---

### Phase 2: Design

**Activities**:
1. **Target Architecture**:
   - Design AWS architecture
   - Choose services
   - Plan networking
   - Security design

2. **Migration Approach**:
   - Cutover strategy
   - Data migration plan
   - Testing approach
   - Rollback plan

3. **Landing Zone**:
   - Account structure
   - Network design
   - Security baseline
   - Operational readiness

**Best Practices**:
- Start with pilot workloads
- Use Well-Architected Framework
- Plan for Day 2 operations
- Document everything

**Duration**: 1-2 months per wave

**MCP Lookup**: "AWS landing zone migration"

---

### Phase 3: Migration Execution

**Activities**:
1. **Pilot Migration**:
   - Choose low-risk application
   - Test migration process
   - Validate procedures
   - Learn and refine

2. **Wave Migrations**:
   - Execute per wave plan
   - Monitor closely
   - Document issues/learnings
   - Adjust next waves

3. **Data Migration**:
   - Use AWS DMS for databases
   - Use DataSync for file data
   - Use Snowball for large datasets
   - Plan for minimal downtime

**Tools**:
- AWS Application Migration Service
- AWS Database Migration Service
- AWS DataSync
- AWS Snow Family

**Duration**: Varies by complexity

**MCP Lookup**: "AWS migration execution best practices"

---

### Phase 4: Optimization

**Activities**:
1. **Right-Sizing**:
   - Analyze actual usage
   - Optimize instance types
   - Review data storage tiers
   - Implement auto-scaling

2. **Cost Optimization**:
   - Purchase Reserved Instances/Savings Plans
   - Delete unused resources
   - Optimize data transfer
   - Review pricing models

3. **Modernization**:
   - Adopt managed services
   - Implement automation
   - Enhance monitoring
   - Improve security posture

**Best Practices**:
- Establish regular review cadence
- Use AWS Cost Explorer
- Implement tagging strategy
- Continuous optimization

**Duration**: Ongoing

**MCP Lookup**: "AWS migration optimization best practices"

---

## Migration Wave Planning

### Wave Strategy

**Wave 1 - Pilot**:
- Simple, low-risk applications
- Learn migration process
- Build confidence
- Refine procedures

**Wave 2-3 - Foundation**:
- Critical infrastructure services
- Shared services (DNS, monitoring)
- Developer tools
- Build operational muscle

**Wave 4+ - Business Applications**:
- Customer-facing applications
- Core business systems
- Higher complexity workloads
- Leverage lessons learned

### Wave Criteria

**Good Early Wave Candidates**:
- Simple architecture
- Well-documented
- Low business risk
- Few dependencies
- Good for learning

**Later Wave Candidates**:
- Complex architectures
- Many dependencies
- Business-critical
- Poorly documented
- Require specialized expertise

---

## Common Migration Patterns

### Pattern 1: Database Migration

**Approach**:
1. **Assess**:
   - Database size, type, version
   - Schema complexity
   - Performance requirements

2. **Choose Target**:
   - Same engine → RDS (rehost/replatform)
   - Engine change → Aurora (replatform)
   - NoSQL fit → DynamoDB (refactor)

3. **Migrate**:
   - Use AWS DMS
   - Test thoroughly
   - Plan cutover
   - Monitor performance

**MCP Lookup**: "AWS database migration DMS"

---

### Pattern 2: Application Server Migration

**Approach**:
1. **Assess Complexity**:
   - Stateless vs stateful
   - Dependencies
   - Configuration needs

2. **Choose Approach**:
   - Rehost → EC2
   - Replatform → Elastic Beanstalk, ECS
   - Refactor → Lambda, ECS/EKS

3. **Plan Networking**:
   - VPC design
   - Load balancing
   - DNS cutover

**MCP Lookup**: "AWS application migration server"

---

### Pattern 3: Storage Migration

**Approach**:
1. **Assess Data**:
   - Volume, type, access patterns
   - Performance requirements
   - Compliance needs

2. **Choose Service**:
   - Object storage → S3
   - Block storage → EBS
   - File storage → EFS, FSx
   - Tape → S3 Glacier

3. **Transfer Method**:
   - < 10 TB → DataSync, S3 Transfer Acceleration
   - 10-100 TB → Snowball
   - > 100 TB → Snowmobile

**MCP Lookup**: "AWS storage migration data transfer"

---

## Migration Best Practices

### 1. Start with Assessment
- Discover all applications
- Understand dependencies
- Map data flows
- Identify risks early

### 2. Pilot First
- Choose simple application
- Test migration process
- Validate procedures
- Build team skills

### 3. Automate When Possible
- Use migration tools
- Script repetitive tasks
- Infrastructure as Code
- Reduce human error

### 4. Plan for Rollback
- Document rollback procedures
- Test rollback plans
- Have contingency for issues
- Don't burn bridges too soon

### 5. Communicate Extensively
- Keep stakeholders informed
- Document decisions
- Share learnings
- Manage expectations

### 6. Monitor Closely Post-Migration
- Application performance
- User experience
- Costs
- Security posture

### 7. Optimize After Stabilization
- Don't optimize during migration
- Stabilize first
- Then right-size and optimize
- Continuous improvement

---

## Migration Risks and Mitigation

### Risk 1: Underestimated Complexity
**Mitigation**:
- Thorough discovery
- Proof of concepts
- Expert consultation
- Buffer in timeline/budget

### Risk 2: Dependency Surprises
**Mitigation**:
- Detailed dependency mapping
- Test thoroughly
- Gradual migration
- Maintain fallback options

### Risk 3: Data Loss/Corruption
**Mitigation**:
- Multiple backups
- Validation procedures
- Gradual cutover
- Rollback capability

### Risk 4: Performance Issues
**Mitigation**:
- Performance testing
- Capacity planning
- Gradual traffic shift
- Monitoring and alerts

### Risk 5: Cost Overruns
**Mitigation**:
- Detailed cost estimation
- Budget controls
- Regular cost reviews
- Optimization focus post-migration

---

## Using AWS Migration Services

### AWS Application Migration Service (MGN)
**Purpose**: Lift-and-shift migrations
**Use for**: Rehost migrations, minimize downtime
**MCP Lookup**: "AWS MGN application migration service"

### AWS Database Migration Service (DMS)
**Purpose**: Database migrations with minimal downtime
**Use for**: Homogeneous and heterogeneous database migrations
**MCP Lookup**: "AWS DMS database migration"

### AWS DataSync
**Purpose**: Automated data transfer
**Use for**: File data migrations, ongoing replication
**MCP Lookup**: "AWS DataSync data transfer"

### AWS Snow Family
**Purpose**: Offline data transfer for large datasets
**Use for**: TB to PB scale migrations with limited bandwidth
**MCP Lookup**: "AWS Snow Family data migration"

### Migration Hub
**Purpose**: Track migrations across tools
**Use for**: Portfolio view, progress tracking
**MCP Lookup**: "AWS Migration Hub tracking"

---

## Getting Current Migration Guidance

Before planning migrations:

1. **Check migration strategies**:
   ```
   MCP_DOCKER:search_documentation "AWS migration strategies 6 Rs"
   ```

2. **Review service-specific migration**:
   ```
   MCP_DOCKER:search_documentation "migrating [technology] to AWS"
   ```

3. **Get tool documentation**:
   ```
   MCP_DOCKER:search_documentation "AWS [migration tool] best practices"
   ```

4. **Find reference architectures**:
   ```
   MCP_DOCKER:search_documentation "AWS migration reference architecture"
   ```

This ensures migration plans reflect current AWS guidance and leverage latest migration capabilities.
