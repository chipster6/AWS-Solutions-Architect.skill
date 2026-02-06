# Disaster Recovery Reference

**Document ID:** ref-disaster-recovery  
**Purpose:** SA Pro-level reference for DR strategies, AWS services, and runbooks

---

## DR Strategies Overview

### Strategy Comparison Matrix

| Strategy | RTO | RPO | Cost | Complexity | Data Loss |
|----------|-----|-----|------|------------|-----------|
| Backup & Restore | Hours | Hours/Days | Low | Low | Potential |
| Pilot Light | 30-60 min | Minutes/Hours | Medium | Medium | Minimal |
| Warm Standby | 10-30 min | Seconds/Minutes | Medium-High | High | Minimal |
| Multi-Site Active/Active | Near-zero | Near-zero | High | Very High | None |

### Strategy Selection Guide

#### Backup and Restore
**Use When:**
- Non-critical workloads
- Budget constraints
- Acceptable data loss (hours/days)
- Recovery time is not urgent

**Architecture:**
```
Primary Region          Secondary Region
┌─────────────┐        ┌─────────────┐
│ Application │ Backup │   S3       │
│   Server    │──────►│  Bucket    │
└─────────────┘        └─────────────┘
                              │
                              ▼
                        ┌─────────────┐
                        │   Restore   │
                        │  Process   │
                        └─────────────┘
```

#### Pilot Light
**Use When:**
- Reproducible workloads
- Cost optimization needed
- Moderate RTO requirements
- Critical data replicated

**Architecture:**
```
Primary Region                    Secondary Region
┌─────────────┐                ┌─────────────┐
│  Full App   │ Replicate      │ Minimal    │
│  Stack      │───────────────►│  Core      │
└─────────────┘                │  Services  │
                               └─────────────┘
                                     │
                                     ▼ Scale-up on failover
```

#### Warm Standby
**Use When:**
- Business-critical applications
- Low RTO requirements
- Regular data synchronization
- Staffed operations team

**Architecture:**
```
Primary Region                    Secondary Region
┌─────────────┐                ┌─────────────┐
│  Full App   │ Sync           │ Scaled-Down │
│  Stack      │───────────────►│  Standby   │
└─────────────┘                └─────────────┘
                                     │
                                     ▼ Scale-up on failover
```

#### Multi-Site Active/Active
**Use When:**
- Mission-critical workloads
- Near-zero RTO/RPO requirements
- High budget available
- Global user base

**Architecture:**
```
us-east-1                      us-west-2
┌─────────────┐               ┌─────────────┐
│  Active    │◄─────────────►│  Active    │
│  App Stack │   Async/Sync  │  App Stack │
└──────┬──────┘               └──────┬──────┘
       │                             │
       └───────────┬─────────────────┘
                   ▼
             Global Load Balancer
```

## AWS Disaster Recovery Services

### AWS Elastic Disaster Recovery (DRS)

#### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Source Site                              │
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │ Server 1│  │ Server 2│  │ Server 3│  │ Server N│     │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘     │
│       │             │             │             │            │
│       └─────┬───────┴─────┬───────┴─────┬────┘            │
│             │             │             │                   │
└─────────────┼─────────────┼─────────────┼─────────────────┘
              │             │             │
              └─────▼─────┴─────▼─────┘
                    │
                    │ Continuous Replication
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    Staging Area (AWS)                         │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              DRS Replication Server                  │   │
│  │                                                      │   │
│  │   ┌─────────────────────────────────────────────┐  │   │
│  │   │           Replicated Volumes                │  │   │
│  │   └─────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│                    │                                    │
│                    ▼ Failover                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Target Instance                       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

#### DRS Configuration
```yaml
drs:
  source_servers:
    - server_id: "s-1234567890abcdef0"
      name: "web-server-01"
      
      replication_settings:
        data_plane_rpo: "1h"
        pit_recording_frequency: "1h"
        
        use_default_replication_server: true
        
      failure_handling:
        strategy: "FAILOVER"
        automatic_failover: true
        
  recovery_instances:
    - source_server_id: "s-1234567890abcdef0"
      recovery_instance_id: "ri-1234567890abcdef0"
      
      target_settings:
        instance_type: "m5.xlarge"
        subnet: "subnet-recovery"
        security_groups:
          - "sg-recovery"
```

### AWS Backup

#### Backup Plan Configuration
```yaml
backup:
  plan:
    name: "CriticalWorkloadsBackup"
    
    rules:
      - name: "daily-backup"
        target_backup_vault_name: "primary-vault"
        
        schedule:
          expression: "cron(0 5 ? * * *)"
          start_window: 60
          completion_window: 180
          
        lifecycle:
          move_to_cold_storage_after: 30
          delete_after: 365
          
        copy_actions:
          - destination_vault_arn: "arn:aws:backup:us-west-2:123456789:backup-vault:dr-vault"
            lifecycle:
              delete_after: 730
              
      - name: "hourly-transaction-logs"
        target_backup_vault_name: "primary-vault"
        
        schedule:
          expression: "cron(0 * ? * * *)"
          start_window: 15
          completion_window: 120
          
        backup_options:
          windows_hour: 0
          
  selections:
    - name: "critical-resources"
      resources:
        - resource_arn: "arn:aws:ec2:us-east-1:123456789:instance/i-*"
        - resource_arn: "arn:aws:rds:us-east-1:123456789:db:*"
        - resource_arn: "arn:aws:efs:us-east-1:123456789:file-system/*"
```

### Database-Specific DR

#### RDS Multi-AZ Configuration
```yaml
rds:
  db_instance:
    db_instance_identifier: "prod-database"
    
    multi_az: true
    
    db_instance_class: "db.r6g.2xlarge"
    
    engine: "postgres"
    engine_version: "15.4"
    
    backup:
      backup_retention_period: 35
      preferred_backup_window: "03:00-04:00"
      automated_backups_replication: true
      
    # Cross-region read replica for additional DR
    db_instance_automated_backups_replication: true
```

#### Aurora Global Database
```yaml
aurora:
  global_database:
    global_cluster_identifier: "prod-global-cluster"
    
    primary_cluster:
      db_cluster_identifier: "prod-primary"
      database_name: "appdb"
      
      db_instance_class: "db.r6g.2xlarge"
      
      backup:
        retention_period: 35
        
    secondary_clusters:
      - db_cluster_identifier: "prod-west"
        region: "us-west-2"
```

## DR Testing & Runbooks

### DR Test Plan Template

#### Pre-Test Checklist
```markdown
## Pre-Test Checklist

### Infrastructure
- [ ] Staging environment ready
- [ ] Network connectivity verified
- [ ] DNS failover configured
- [ ] Firewall rules documented

### Data
- [ ] Latest backup verified
- [ ] Point-in-time recovery tested
- [ ] Cross-region replication lag measured

### Team
- [ ] DR team contacts updated
- [ ] Communication channels confirmed
- [ ] Runbooks reviewed
- [ ] Stakeholders notified
```

#### Test Execution Steps
```markdown
## Test Execution

### Step 1: Failover Initiation
1.1 Verify current system state
1.2 Notify stakeholders
1.3 Initiate DRS failover
1.4 Monitor replication status

### Step 2: Failover Validation
2.1 Verify instance startup
2.2 Check application health endpoints
2.3 Validate database connectivity
2.4 Confirm DNS propagation

### Step 3: User Acceptance
3.1 Execute smoke tests
3.2 Validate key workflows
3.3 Confirm performance baselines
3.4 Document test results

### Step 4: Failback Preparation
4.1 Assess primary site recovery
4.2 Plan data resynchronization
4.3 Schedule failback window
```

### Failover Runbook

#### Failover Execution
```yaml
failover_runbook:
  name: "Production Failover"
  trigger: "DR event or authorized test"
  
  pre_failover:
    - step: "Notify stakeholders"
      action: "Send notification to dr-team@company.com"
      verification: "Confirm receipt"
      
    - step: "Verify DRS status"
      action: "Check replication lag < 1 hour"
      verification: "AWS Console or CLI check"
      
    - step: "Backup current state"
      action: "Create final backup"
      verification: "Backup job status = COMPLETED"
      
  failover:
    - step: "Initiate failover"
      action: "aws drs start-failover --source-server-id s-xxx"
      verification: "Recovery instance status = ACTIVE"
      
    - step: "Update DNS"
      action: "Route 53 health check → Secondary IP"
      verification: "Global DNS resolves to new IP"
      
    - step: "Validate application"
      action: "Execute smoke tests"
      verification: "All tests PASS"
      
  post_failover:
    - step: "Monitor system"
      action: "CloudWatch dashboard review"
      duration: "4 hours"
```

### Failback Runbook

#### Failback Execution
```yaml
failback_runbook:
  name: "Primary Site Restoration"
  trigger: "Primary site recovered and validated"
  
  pre_failback:
    - step: "Assess primary site"
      action: "Verify all services operational"
      verification: "Pre-failback tests PASS"
      
    - step: "Data resynchronization"
      action: "Sync from secondary to primary"
      verification: "Replication lag = 0"
      
    - step: "Schedule maintenance window"
      action: "Coordinate with stakeholders"
      verification: "Approved maintenance ticket"
      
  failback:
    - step: "Notify users"
      action: "Send maintenance notification"
      verification: "User acknowledgment"
      
    - step: "Switch traffic"
      action: "Route 53 → Primary IP"
      verification: "DNS resolves to primary"
      
    - step: "Validate"
      action: "Run validation tests"
      verification: "All tests PASS"
```

## DR Metrics

### RTO/RPO Decision Matrix

| Workload Type | RTO Target | RPO Target | Recommended Strategy |
|---------------|------------|------------|---------------------|
| Transactional DB | 5 min | 0 | Multi-Site Active/Active |
| Customer-Facing App | 30 min | 5 min | Warm Standby |
| Internal Tool | 4 hours | 1 hour | Pilot Light |
| Analytics Pipeline | 24 hours | 24 hours | Backup & Restore |

### DR Coverage Matrix

| Component | Strategy | RTO | RPO | Cost/Month |
|-----------|----------|-----|-----|------------|
| RDS Primary | Multi-AZ + Cross-Region | 30 min | 5 min | $2,000 |
| EC2 Instances | DRS | 1 hour | 1 hour | $1,500 |
| S3 Data | Cross-Region Replication | 0 (restore) | 15 min | $500 |
| DynamoDB | Global Tables | Near-zero | 1 sec | $1,000 |

### DR Runbook Automation
```yaml
# Lambda-based DR automation
dr_automation:
  function_name: "DR-Failover-Handler"
  
  triggers:
    - cloudwatch_event:
        name: "DR-Test-Event"
        
  actions:
    - function: "notifyTeam"
    - function: "checkDRSStatus"
    - function: "initiateFailover"
    - function: "validateFailover"
    - function: "updateDNS"
    - function: "sendCompletionNotification"
```
