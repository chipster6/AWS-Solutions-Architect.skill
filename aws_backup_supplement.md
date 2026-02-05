# AWS Backup Implementation Supplement

**Index:** [GOV-ARCH-001](GOV-ARCH-001-Architecture-Documentation-Index.md) | [CROSS_REFERENCE_INDEX.md](CROSS_REFERENCE_INDEX.md)  
**Related:** [AWS Comprehensive Guide](AWS_Solutions_Architect_Comprehensive_Guide.md) Section 8 (Disaster Recovery)  
**Related Supplements:** [DRS](drs_implementation_supplement.md) (complementary strategies) | [Security](security_services_supplement.md) (encryption)  
**Domain:** Design for New Solutions (29%) | Accelerate Migration (20%)

## Table of Contents
1. [Overview](#1-overview)
2. [Backup Plans](#2-backup-plans)
3. [Backup Vaults](#3-backup-vaults)
4. [Cross-Region Backup](#4-cross-region-backup)
5. [Cross-Account Backup](#5-cross-account-backup)
6. [Supported Resources](#6-supported-resources)
7. [Recovery Procedures](#7-recovery-procedures)
8. [Advanced Features](#8-advanced-features)
9. [Cost Optimization](#9-cost-optimization)
10. [Best Practices](#10-best-practices)

### Related Documentation
- **[Migration Patterns](files/migration-patterns.md)** - Backup for migration scenarios
- **[Architecture Patterns](files/architecture-patterns.md)** - Data protection patterns
- **[Well-Architected Pillars](files/well-architected-pillars.md)** - Reliability pillar (backup)
- **[DRS Supplement](drs_implementation_supplement.md)** - Complementary DR strategies
- **[Cross-Reference Index](CROSS_REFERENCE_INDEX.md)** - Navigate by backup strategy and service

---

## 1. Overview

AWS Backup is a fully managed backup service that makes it easy to centralize and automate data protection across AWS services. It provides policy-based backup management, cross-region/account capabilities, and compliance monitoring.

**Key Capabilities:**
- Centralized backup management
- Policy-based backup automation
- Cross-region and cross-account backup
- Lifecycle management with cold storage
- Point-in-time recovery (PITR)
- Audit and compliance reporting

### Service Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      AWS Backup Service                          │
├─────────────────────────────────────────────────────────────────┤
│  Backup Plans  │  Backup Vaults  │  Cross-Region  │  Audit Mgr  │
├─────────────────────────────────────────────────────────────────┤
│  EC2  │  RDS  │  DynamoDB  │  EFS  │  S3  │  Aurora  │  EBS      │
└─────────────────────────────────────────────────────────────────┘
```

### Use Cases

| Use Case | Description |
|----------|-------------|
| **Disaster Recovery** | Cross-region backup for DR scenarios |
| **Compliance** | Automated backup for regulatory requirements |
| **Data Archival** | Long-term retention with cold storage |
| **Migration** | Cross-account backup for migration |
| **Protection** | Central backup across multiple AWS services |

---

## 2. Backup Plans

### 2.1 Overview

A backup plan defines the backup schedule, retention policy, and lifecycle management for your resources.

### 2.2 Creating Backup Plans

**AWS Console:**
1. Navigate to AWS Backup → Backup plans
2. Click "Create backup plan"
3. Choose start option:
   - Build a new plan
   - Start from existing plan
   - Use CLI
4. Configure backup rules
5. Assign resources
6. Create plan

**AWS CLI:**
```bash
# Create backup plan with JSON file
aws backup create-backup-plan \
  --backup-plan file://backup-plan.json

# Example backup-plan.json
{
  "BackupPlanName": "Production-Backup-Plan",
  "Rules": [
    {
      "RuleName": "Daily-Backup",
      "TargetBackupVaultName": "Production-Vault",
      "ScheduleExpression": "cron(0 2 ? * * *)",
      "StartWindowMinutes": 60,
      "CompletionWindowMinutes": 120,
      "Lifecycle": {
        "MoveToColdStorageAfterDays": 30,
        "DeleteAfterDays": 120
      },
      "RecoveryPointTags": {
        "BackupType": "Automated",
        "Environment": "Production"
      },
      "CopyActions": [
        {
          "DestinationBackupVaultArn": "arn:aws:backup:us-west-2:123456789012:backup-vault:DR-Vault",
          "Lifecycle": {
            "MoveToColdStorageAfterDays": 30,
            "DeleteAfterDays": 120
          }
        }
      ]
    }
  ]
}
```

### 2.3 Backup Rule Configuration

**Schedule Expressions:**

| Frequency | Cron Expression | Description |
|-----------|----------------|-------------|
| Hourly | `cron(0 * * * ? *)` | Every hour |
| Daily | `cron(0 2 * * ? *)` | Daily at 2 AM UTC |
| Weekly | `cron(0 2 ? * SUN *)` | Weekly on Sunday at 2 AM UTC |
| Monthly | `cron(0 2 1 * ? *)` | Monthly on 1st at 2 AM UTC |

**Time Windows:**
- **Start Window**: Time allowed for backup to start (default: 8 hours)
- **Completion Window**: Time allowed for backup to complete (default: 7 days)

**Example with Multiple Rules:**
```json
{
  "BackupPlanName": "Tiered-Backup-Plan",
  "Rules": [
    {
      "RuleName": "Daily-Short-Term",
      "ScheduleExpression": "cron(0 2 * * ? *)",
      "Lifecycle": {
        "DeleteAfterDays": 35
      }
    },
    {
      "RuleName": "Weekly-Long-Term",
      "ScheduleExpression": "cron(0 2 ? * SUN *)",
      "Lifecycle": {
        "MoveToColdStorageAfterDays": 30,
        "DeleteAfterDays": 365
      }
    },
    {
      "RuleName": "Monthly-Archive",
      "ScheduleExpression": "cron(0 2 1 * ? *)",
      "Lifecycle": {
        "MoveToColdStorageAfterDays": 30,
        "DeleteAfterDays": 2555
      }
    }
  ]
}
```

### 2.4 Lifecycle Management

**Storage Tiers:**

| Tier | Description | Use Case |
|------|-------------|----------|
| **Warm** | Standard backup storage | Recent backups, frequent access |
| **Cold** | Lower-cost storage | Older backups, rare access |

**Transition Rules:**
```bash
# Lifecycle: Move to cold after 30 days, delete after 1 year
"Lifecycle": {
  "MoveToColdStorageAfterDays": 30,
  "DeleteAfterDays": 365
}

# Cold storage only for specific resources
# EBS: Archive tier (savings up to 75%)
# EFS: Infrequent Access (savings up to 92%)
# DynamoDB: Not supported for cold
```

### 2.5 Continuous Backups and PITR

Enable point-in-time recovery for supported resources:

```bash
# Enable continuous backups for PITR
aws backup create-backup-plan \
  --backup-plan '{
    "BackupPlanName": "PITR-Plan",
    "Rules": [
      {
        "RuleName": "Continuous-Backup",
        "EnableContinuousBackup": true,
        "Lifecycle": {
          "DeleteAfterDays": 35
        }
      }
    ]
  }'
```

**Supported Resources for PITR:**
- Amazon RDS (Aurora, MySQL, PostgreSQL, etc.)
- Amazon DynamoDB
- Amazon S3 (continuous backups)

---

## 3. Backup Vaults

### 3.1 Overview

Backup vaults are containers that organize and store your backups. Each backup vault has:
- Encryption settings (KMS key)
- Access policies
- Vault locking (compliance)

### 3.2 Creating Backup Vaults

**AWS Console:**
1. Navigate to AWS Backup → Backup vaults
2. Click "Create backup vault"
3. Enter vault name
4. Choose KMS key (or create new)
5. Add tags (optional)
6. Create vault

**AWS CLI:**
```bash
# Create backup vault with default encryption
aws backup create-backup-vault \
  --backup-vault-name Production-Vault \
  --encryption-key-alias alias/aws/backup \
  --tags BackupType=Production,Environment=Primary

# Create vault with customer-managed key
aws backup create-backup-vault \
  --backup-vault-name Compliance-Vault \
  --encryption-key-arn arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012

# List vaults
aws backup list-backup-vaults
```

### 3.3 Vault Access Policies

Control access to backup vaults:

```bash
# Create vault access policy
aws backup put-backup-vault-access-policy \
  --backup-vault-name Production-Vault \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "AllowCrossAccountAccess",
        "Effect": "Allow",
        "Principal": {
          "AWS": "arn:aws:iam::999999999999:root"
        },
        "Action": [
          "backup:CopyIntoBackupVault"
        ],
        "Resource": "*"
      }
    ]
  }'
```

### 3.4 Vault Locking

Prevent backup deletion for compliance:

```bash
# Enable vault lock with governance retention
aws backup put-backup-vault-lock-configuration \
  --backup-vault-name Compliance-Vault \
  --min-retention-days 365 \
  --max-retention-days 2555 \
  --changeable-for-days 3

# Vault lock states
# - Governance: Can be modified with iam:UpdateVaultLock
# - Compliance: Cannot be modified or deleted
```

---

## 4. Cross-Region Backup

### 4.1 Overview

Copy backups to multiple regions for disaster recovery and compliance.

### 4.2 Configuration

**Via Backup Plan:**
```json
{
  "RuleName": "Cross-Region-Backup",
  "CopyActions": [
    {
      "DestinationBackupVaultArn": "arn:aws:backup:us-west-2:123456789012:backup-vault:DR-Vault",
      "Lifecycle": {
        "MoveToColdStorageAfterDays": 30,
        "DeleteAfterDays": 365
      }
    },
    {
      "DestinationBackupVaultArn": "arn:aws:backup:eu-west-1:123456789012:backup-vault:Compliance-Vault",
      "Lifecycle": {
        "DeleteAfterDays": 2555
      }
    }
  ]
}
```

**AWS CLI:**
```bash
# Create backup plan with cross-region copy
aws backup create-backup-plan \
  --backup-plan '{
    "BackupPlanName": "DR-Backup-Plan",
    "Rules": [
      {
        "RuleName": "Primary-to-DR",
        "ScheduleExpression": "cron(0 2 * * ? *)",
        "TargetBackupVaultName": "Primary-Vault",
        "Lifecycle": {
          "DeleteAfterDays": 35
        },
        "CopyActions": [
          {
            "DestinationBackupVaultArn": "arn:aws:backup:us-west-2:123456789012:backup-vault:DR-Vault",
            "Lifecycle": {
              "DeleteAfterDays": 365
            }
          }
        ]
      }
    ]
  }'
```

### 4.3 Cross-Region Considerations

**Data Transfer Costs:**
- Cross-region data transfer charges apply
- Costs vary by source and destination regions
- Consider using S3 cross-region replication for large datasets

**Encryption:**
- Backups are encrypted with destination vault's KMS key
- Ensure KMS key permissions in destination region
- Cross-region KMS key usage may incur additional costs

---

## 5. Cross-Account Backup

### 5.1 Overview

Cross-account backup allows you to "fan in" backups from multiple accounts to a central backup account, providing isolation and protection against account compromise.

### 5.2 Architecture Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│              Central Backup Account (Security OU)               │
│              ┌─────────────────────────────────┐                │
│              │      Central Backup Vault       │                │
│              │  (arn:aws:backup:us-east-1:     │                │
│              │   security:backup-vault:central) │                │
│              └─────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
┌────────▼──────┐    ┌────────▼──────┐    ┌───────▼───────┐
│  Account A    │    │  Account B    │    │  Account C    │
│  (Production) │    │  (Production) │    │  (Development)│
│  IAM Role     │    │  IAM Role     │    │  IAM Role     │
└───────────────┘    └───────────────┘    └───────────────┘
```

### 5.3 Setting Up Cross-Account Backup

**Step 1: Central Account Setup**
```bash
# In central backup account (security account)
# Create backup vault
aws backup create-backup-vault \
  --backup-vault-name Central-Backup-Vault \
  --encryption-key-arn arn:aws:kms:us-east-1:security-account:key/central-key

# Set vault access policy to allow member accounts
aws backup put-backup-vault-access-policy \
  --backup-vault-name Central-Backup-Vault \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "AllowCopyFromMemberAccounts",
        "Effect": "Allow",
        "Principal": {
          "AWS": [
            "arn:aws:iam::account-a:root",
            "arn:aws:iam::account-b:root",
            "arn:aws:iam::account-c:root"
          ]
        },
        "Action": "backup:CopyIntoBackupVault",
        "Resource": "*"
      }
    ]
  }'
```

**Step 2: Member Account Setup**
```bash
# In member account (e.g., Account A)
# Create IAM role for AWS Backup
aws iam create-role \
  --role-name AWSBackupCrossAccountRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "backup.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }'

# Attach required policies
aws iam attach-role-policy \
  --role-name AWSBackupCrossAccountRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup

# Create backup plan with cross-account copy
aws backup create-backup-plan \
  --backup-plan '{
    "BackupPlanName": "Cross-Account-Backup",
    "Rules": [
      {
        "RuleName": "Copy-To-Central",
        "ScheduleExpression": "cron(0 2 * * ? *)",
        "TargetBackupVaultName": "Local-Vault",
        "CopyActions": [
          {
            "DestinationBackupVaultArn": "arn:aws:backup:us-east-1:security-account:backup-vault:Central-Backup-Vault"
          }
        ]
      }
    ]
  }'
```

### 5.4 Organization-Based Cross-Account

**Enable via Organizations:**
```bash
# Enable AWS Backup for organization
aws organizations enable-aws-service-access \
  --service-principal backup.amazonaws.com

# Register delegated administrator
aws backup register-organizaton-admin-account \
  --admin-account-id security-account-id

# Create organization backup plan
aws backup create-backup-plan \
  --backup-plan '{
    "BackupPlanName": "Organization-Backup-Plan",
    "Rules": [...],
    "AdvancedBackupSettings": [
      {
        "ResourceType": "EC2",
        "BackupOptions": {
          "WindowsVSS": "enabled"
        }
      }
    ]
  }'

# Assign to organizational units
aws backup create-backup-selection \
  --backup-plan-id plan-id \
  --backup-selection '{
    "SelectionName": "Production-OU",
    "IamRoleArn": "arn:aws:iam::account:role/service-role/AWSBackupDefaultServiceRole",
    "Resources": [],
    "Conditions": {
      "StringEquals": [
        {"ConditionKey": "aws:ResourceTag/Backup", "ConditionValue": "true"}
      ]
    }
  }'
```

### 5.5 Cross-Account Restore

Restore from central backup vault to member account:

```bash
# In member account, restore from central vault
aws backup start-restore-job \
  --recovery-point-arn "arn:aws:ec2:us-east-1::snapshot/snap-0123456789abcdef0" \
  --metadata '{
    "AvailabilityZone": "us-east-1a",
    "InstanceType": "t3.medium",
    "SubnetId": "subnet-0123456789abcdef0",
    "SecurityGroupIds": "sg-0123456789abcdef0"
  }' \
  --iam-role-arn arn:aws:iam::member-account:role/AWSBackupRestoreRole \
  --resource-type EC2
```

---

## 6. Supported Resources

### 6.1 AWS Backup Supported Services

| Service | Backup Type | Cold Storage | PITR |
|---------|-------------|--------------|------|
| **Amazon EC2** | AMI + EBS snapshots | Yes (EBS) | No |
| **Amazon EBS** | Snapshots | Yes (Archive) | No |
| **Amazon RDS** | Snapshots | Yes | Yes |
| **Amazon Aurora** | Snapshots | Yes | Yes |
| **Amazon DynamoDB** | Table backups | No | Yes |
| **Amazon EFS** | Backups | Yes (IA) | No |
| **Amazon S3** | Backups | Yes | Yes |
| **AWS Storage Gateway** | Volume snapshots | No | No |
| **Amazon DocumentDB** | Snapshots | Yes | Yes |
| **Amazon Neptune** | Snapshots | Yes | Yes |
| **Amazon Timestream** | Backups | No | No |
| **AWS CloudFormation** | Stacks | No | No |

### 6.2 Resource Assignment

**Tag-Based Assignment:**
```bash
# Assign resources by tag
aws backup create-backup-selection \
  --backup-plan-id plan-id \
  --backup-selection '{
    "SelectionName": "Production-Resources",
    "IamRoleArn": "arn:aws:iam::123456789012:role/service-role/AWSBackupDefaultServiceRole",
    "Resources": [],
    "ListOfTags": [
      {
        "ConditionType": "STRINGEQUALS",
        "ConditionKey": "Environment",
        "ConditionValue": "Production"
      }
    ]
  }'
```

**Resource ARN Assignment:**
```bash
# Assign specific resources
aws backup create-backup-selection \
  --backup-plan-id plan-id \
  --backup-selection '{
    "SelectionName": "Critical-Databases",
    "IamRoleArn": "arn:aws:iam::123456789012:role/service-role/AWSBackupDefaultServiceRole",
    "Resources": [
      "arn:aws:rds:us-east-1:123456789012:db:production-db",
      "arn:aws:dynamodb:us-east-1:123456789012:table/orders-table",
      "arn:aws:ec2:us-east-1:123456789012:instance/i-0123456789abcdef0"
    ]
  }'
```

### 6.3 Resource-Specific Considerations

**EC2 Instance Backup:**
- Creates AMI with associated EBS snapshots
- Supports Windows VSS for application consistency
- Excludes instance store volumes

**RDS/Aurora Backup:**
- Creates DB snapshots
- Supports automated backups (daily + transaction logs)
- Cross-region copy creates independent snapshot

**DynamoDB Backup:**
- Full table backup
- No performance impact on table
- PITR allows restore to any second in last 35 days

**S3 Backup:**
- Continuous or periodic backups
- Supports versioning
- Can exclude specific prefixes

---

## 7. Recovery Procedures

### 7.1 Point-in-Time Recovery

**Restore RDS to Specific Time:**
```bash
aws backup start-restore-job \
  --recovery-point-arn arn:aws:backup:us-east-1:123456789012:recovery-point:rp-rds-123 \
  --metadata '{
    "RestoreTime": "2025-01-15T10:30:00Z",
    "DBInstanceIdentifier": "restored-db-instance",
    "DBSubnetGroupName": "my-subnet-group",
    "VpcSecurityGroupIds": "sg-0123456789abcdef0"
  }'
```

**Restore DynamoDB to Point-in-Time:**
```bash
aws backup start-restore-job \
  --recovery-point-arn arn:aws:backup:us-east-1:123456789012:recovery-point:rp-dynamo-456 \
  --metadata '{
    "RestoreDateTime": "2025-01-15T10:30:00Z",
    "TargetTableName": "restored-orders-table"
  }'
```

### 7.2 Cross-Region Restore

```bash
# Restore from DR region to primary region
aws backup start-restore-job \
  --recovery-point-arn arn:aws:backup:us-west-2:123456789012:recovery-point:rp-789 \
  --iam-role-arn arn:aws:iam::123456789012:role/AWSBackupRestoreRole \
  --resource-type EC2 \
  --copy-source-tags \
  --metadata '{
    "AvailabilityZone": "us-east-1a",
    "InstanceType": "t3.medium",
    "SubnetId": "subnet-east-1a",
    "SecurityGroupIds": "sg-east-1a"
  }' \
  --region us-east-1
```

### 7.3 Testing Recovery

**Recovery Testing Best Practices:**
1. **Schedule Regular Tests**
   - Monthly for critical systems
   - Quarterly for non-critical
   - Annually for archival data

2. **Document Procedures**
   - RTO (Recovery Time Objective)
   - RPO (Recovery Point Objective)
   - Step-by-step runbooks

3. **Validate Restored Data**
   - Application connectivity
   - Data integrity checks
   - Performance validation

**Automated Recovery Testing:**
```bash
# Create recovery test plan
aws backup create-restore-testing-plan \
  --restore-testing-plan '{
    "RestoreTestingPlanName": "Monthly-Recovery-Test",
    "ScheduleExpression": "cron(0 2 1 * ? *)",
    "StartWindowHours": 8,
    "RecoveryPointSelection": {
      "Algorithm": "LATEST_WITHIN",
      "IncludeVaults": ["arn:aws:backup:us-east-1:123456789012:backup-vault:Production-Vault"],
      "SelectionWindowDays": 30
    }
  }'
```

### 7.4 Recovery Validation

**Post-Restore Checklist:**
- [ ] Instance/Resource starts successfully
- [ ] Network connectivity established
- [ ] Application starts and functions
- [ ] Data integrity verified
- [ ] Performance within acceptable limits
- [ ] Security groups and IAM permissions correct
- [ ] DNS/Load balancer updated (if needed)
- [ ] Monitoring and logging active

---

## 8. Advanced Features

### 8.1 AWS Backup Audit Manager

Enable compliance monitoring and reporting:

```bash
# Create audit framework
aws backup create-framework \
  --framework-name SOC2-Framework \
  --framework-description "SOC 2 compliance framework" \
  --framework-controls '{
    "FrameworkControls": [
      {
        "ControlName": "BACKUP_PLAN_FREQUENCY",
        "ControlInputParameters": [
          {"ParameterName": "requiredFrequencyValue", "ParameterValue": "1"},
          {"ParameterName": "requiredFrequencyUnit", "ParameterValue": "DAY"}
        ]
      },
      {
        "ControlName": "BACKUP_RECOVERY_POINT_MINIMUM_RETENTION",
        "ControlInputParameters": [
          {"ParameterName": "requiredRetentionDays", "ParameterValue": "35"}
        ]
      }
    ]
  }'

# Create assessment
aws backup create-assessment \
  --assessment-name Monthly-SOC2-Assessment \
  --framework-id framework-id \
  --backup-plan-arns arn:aws:backup:us-east-1:123456789012:backup-plan:production-plan \
  --assessment-tags Compliance=SOC2,Frequency=Monthly
```

### 8.2 Backup Search (Indexing)

Enable backup indexing for searchable backups:

```bash
# Create backup plan with indexing
aws backup create-backup-plan \
  --backup-plan '{
    "BackupPlanName": "Searchable-Backup-Plan",
    "Rules": [
      {
        "RuleName": "Indexed-Backup",
        "ScheduleExpression": "cron(0 2 * * ? *)",
        "IndexActions": {
          "ResourceTypes": ["S3", "EBS"]
        }
      }
    ]
  }'

# Search backups
aws backup start-backup-search-job \
  --search-query '{
    "Filters": {
      "ResourceTypes": ["S3"],
      "BackupVaultArns": ["arn:aws:backup:us-east-1:123456789012:backup-vault:Production-Vault"],
      "CreatedBefore": "2025-01-01T00:00:00Z",
      "CreatedAfter": "2024-01-01T00:00:00Z"
    }
  }'
```

### 8.3 Legal Hold

Prevent backup deletion for legal/compliance:

```bash
# Create legal hold
aws backup create-legal-hold \
  --legal-hold-title "Litigation-Hold-2025-Q1" \
  --legal-hold-description "Legal hold for Q1 litigation case" \
  --idempotency-token 123456789 \
  --resource-arns [
    "arn:aws:backup:us-east-1:123456789012:recovery-point:rp-123",
    "arn:aws:backup:us-east-1:123456789012:recovery-point:rp-456"
  ]

# List legal holds
aws backup list-legal-holds

# Cancel legal hold (when case resolved)
aws backup cancel-legal-hold \
  --legal-hold-id hold-id \
  --cancel-description "Case resolved, hold no longer needed"
```

### 8.4 Report Plan

Create automated compliance reports:

```bash
# Create report plan
aws backup create-report-plan \
  --report-plan-name Monthly-Backup-Report \
  --report-plan-description "Monthly backup compliance report" \
  --report-delivery '{
    "S3BucketName": "my-backup-reports",
    "S3KeyPrefix": "monthly/",
    "Format": "CSV"
  }' \
  --report-setting '{
    "ReportTemplate": "BACKUP_JOB_REPORT",
    "FrameworkArns": ["arn:aws:backup:us-east-1:123456789012:framework/soc2-framework"]
  }' \
  --report-plan-tags BackupReport=true,Frequency=Monthly
```

---

## 9. Cost Optimization

### 9.1 Pricing Components

| Component | Pricing | Notes |
|-----------|---------|-------|
| **Warm storage** | Varies by service | Standard backup storage rates |
| **Cold storage** | 20-90% less than warm | Depends on resource type |
| **Cross-region copy** | Data transfer + storage | Per GB transferred |
| **Cross-account copy** | Storage only | No data transfer within same region |
| **API calls** | Minimal | Usually negligible |

### 9.2 Cost Optimization Strategies

**1. Use Cold Storage**
```bash
# Move backups to cold storage after 30 days
"Lifecycle": {
  "MoveToColdStorageAfterDays": 30,
  "DeleteAfterDays": 365
}
```

**2. Right-Size Retention**
```bash
# Align retention with compliance requirements
# Don't keep backups longer than necessary
"DeleteAfterDays": 90  # Instead of 365 if not required
```

**3. Optimize Cross-Region Strategy**
```bash
# Copy only critical backups cross-region
# Use longer retention in DR region
"CopyActions": [
  {
    "DestinationBackupVaultArn": "arn:aws:backup:us-west-2:...",
    "Lifecycle": {
      "DeleteAfterDays": 365  # Long retention only in DR
    }
  }
]
```

**4. Exclude Test/Dev**
```bash
# Tag-based exclusion
"Conditions": {
  "StringNotEquals": [
    {"ConditionKey": "Environment", "ConditionValue": "Development"}
  ]
}
```

**5. Monitor Usage**
```bash
# Check backup storage costs in Cost Explorer
# Filter by service: AWS Backup
# Group by region, resource type
```

### 9.3 Cost Estimation Example

**Monthly Backup Costs:**

| Resource | Size | Backup Type | Storage | Monthly Cost |
|----------|------|-------------|---------|--------------|
| RDS Prod | 500 GB | Daily | Warm: 30 days | ~$50 |
| EBS Volumes | 1 TB | Daily | Warm: 30d, Cold: 335d | ~$80 |
| DynamoDB | 100 GB | Continuous PITR | PITR enabled | ~$20 |
| Cross-region | 500 GB | Copy to DR | Warm: 365 days | ~$45 + transfer |
| **Total** | | | | **~$195/month** |

---

## 10. Best Practices

### 10.1 3-2-1 Backup Rule Implementation

**Rule:** 3 copies of data, 2 different media, 1 offsite

**AWS Implementation:**
```
Copy 1: Primary (Warm storage in primary region)
Copy 2: Cross-region (DR region)
Copy 3: Cross-account (Central backup account)
```

**Configuration:**
```json
{
  "BackupPlanName": "Three-Two-One-Backup",
  "Rules": [
    {
      "RuleName": "Primary-Backup",
      "ScheduleExpression": "cron(0 2 * * ? *)",
      "TargetBackupVaultName": "Primary-Vault",
      "Lifecycle": {
        "DeleteAfterDays": 35
      }
    },
    {
      "RuleName": "Cross-Region-Copy",
      "ScheduleExpression": "cron(0 2 * * ? *)",
      "TargetBackupVaultName": "Primary-Vault",
      "CopyActions": [
        {
          "DestinationBackupVaultArn": "arn:aws:backup:us-west-2:account:backup-vault:DR-Vault",
          "Lifecycle": {
            "DeleteAfterDays": 365
          }
        }
      ]
    },
    {
      "RuleName": "Cross-Account-Copy",
      "ScheduleExpression": "cron(0 2 * * ? *)",
      "TargetBackupVaultName": "Primary-Vault",
      "CopyActions": [
        {
          "DestinationBackupVaultArn": "arn:aws:backup:us-east-1:security:backup-vault:Central-Vault",
          "Lifecycle": {
            "DeleteAfterDays": 2555
          }
        }
      ]
    }
  ]
}
```

### 10.2 Tagging Strategy

**Standard Backup Tags:**
```yaml
Backup: "true"                    # Include in backup
BackupPlan: "Production"          # Which plan to use
BackupRetention: "365"            # Days to retain
Criticality: "High"               # Recovery priority
Environment: "Production"         # For filtering
Compliance: "SOC2,PCI"            # Compliance requirements
DataClassification: "Confidential" # Security level
```

**Implementation:**
```bash
# Tag resources for backup
aws ec2 create-tags \
  --resources i-0123456789abcdef0 \
  --tags Key=Backup,Value=true Key=BackupPlan,Value=Production

aws rds add-tags-to-resource \
  --resource-name arn:aws:rds:us-east-1:123456789012:db:production-db \
  --tags Key=Backup,Value=true Key=Criticality,Value=High
```

### 10.3 Monitoring and Alerting

**CloudWatch Alarms:**
```bash
# Alarm for failed backup jobs
aws cloudwatch put-metric-alarm \
  --alarm-name Backup-Failure-Alarm \
  --metric-name NumberOfBackupJobsFailed \
  --namespace AWS/Backup \
  --statistic Sum \
  --period 86400 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1

# Alarm for low backup coverage
aws cloudwatch put-metric-alarm \
  --alarm-name Low-Backup-Coverage \
  --metric-name PercentageOfResourcesProtected \
  --namespace AWS/Backup \
  --statistic Average \
  --period 3600 \
  --threshold 95 \
  --comparison-operator LessThanThreshold \
  --evaluation-periods 1
```

**EventBridge Notifications:**
```json
{
  "source": ["aws.backup"],
  "detail-type": ["Backup Job State Change"],
  "detail": {
    "state": ["FAILED", "ABORTED"]
  }
}
```

### 10.4 Security Best Practices

**1. Encryption:**
- Use customer-managed KMS keys
- Enable encryption at rest and in transit
- Separate keys per environment

**2. Access Control:**
- Least privilege IAM policies
- Vault access policies
- Regular access reviews

**3. Audit Logging:**
- Enable CloudTrail for all Backup API calls
- Log all restore operations
- Monitor for unauthorized access

**4. Vault Lock:**
- Enable governance or compliance mode
- Prevent accidental/malicious deletion
- Meet regulatory requirements

### 10.5 Disaster Recovery Planning

**RTO/RPO Definitions:**

| Tier | RTO | RPO | Examples |
|------|-----|-----|----------|
| **Tier 1** | < 4 hours | < 1 hour | Production databases |
| **Tier 2** | < 24 hours | < 24 hours | Application servers |
| **Tier 3** | < 72 hours | < 7 days | Development environments |
| **Tier 4** | Manual | Weekly | Archive data |

**Backup Frequency by Tier:**
- Tier 1: Continuous PITR + hourly snapshots
- Tier 2: Daily backups
- Tier 3: Weekly backups
- Tier 4: Monthly backups

### 10.6 Testing and Validation

**Recovery Test Schedule:**
- **Weekly**: Automated restore tests (non-production)
- **Monthly**: Manual DR drills (production)
- **Quarterly**: Full DR simulation
- **Annually**: Compliance audit recovery

**Test Documentation:**
```
Recovery Test Report
├── Date: 2025-01-15
├── Test Type: Monthly DR Drill
├── Scope: Production database
├── RTO Target: 4 hours
├── RPO Target: 1 hour
├── Results:
│   ├── Actual RTO: 3h 15m ✓
│   ├── Actual RPO: 45m ✓
│   └── Issues Found: None
└── Next Test: 2025-02-15
```

---

## Quick Reference Commands

```bash
# Backup Plans
aws backup list-backup-plans
aws backup get-backup-plan --backup-plan-id <id>
aws backup delete-backup-plan --backup-plan-id <id>

# Backup Jobs
aws backup list-backup-jobs
aws backup describe-backup-job --backup-job-id <id>
aws backup stop-backup-job --backup-job-id <id>

# Recovery Points
aws backup list-recovery-points-by-backup-vault --backup-vault-name <name>
aws backup describe-recovery-point --backup-vault-name <name> --recovery-point-arn <arn>
aws backup delete-recovery-point --backup-vault-name <name> --recovery-point-arn <arn>

# Restore Jobs
aws backup start-restore-job --recovery-point-arn <arn> --metadata {...}
aws backup list-restore-jobs
aws backup describe-restore-job --restore-job-id <id>

# Vaults
aws backup list-backup-vaults
aws backup describe-backup-vault --backup-vault-name <name>

# Audit Manager
aws backup list-frameworks
aws backup list-assessments
```

---

*Last Updated: 2026-02-04*
*Based on AWS Backup Documentation*
