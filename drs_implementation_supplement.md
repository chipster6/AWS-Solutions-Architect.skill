# AWS Elastic Disaster Recovery (DRS) Deep Dive

**Index:** [GOV-ARCH-001](GOV-ARCH-001-Architecture-Documentation-Index.md) | [CROSS_REFERENCE_INDEX.md](CROSS_REFERENCE_INDEX.md)  
**Related:** [AWS Comprehensive Guide](AWS_Solutions_Architect_Comprehensive_Guide.md) Section 8 (Disaster Recovery)  
**Related Supplements:** [Route 53](route53_implementation_supplement.md) (failover) | [Backup](aws_backup_supplement.md) (complementary)  
**Domain:** Design for New Solutions (29%) | Accelerate Migration (20%)

## Overview

AWS Elastic Disaster Recovery (DRS) - formerly CloudEndure Disaster Recovery - provides continuous block-level replication of servers to AWS for rapid recovery with minimal data loss.

### Related Documentation
- **[Migration Patterns](files/migration-patterns.md)** - DRS as a migration strategy
- **[Architecture Patterns](files/architecture-patterns.md)** - DR patterns (Pilot Light, Warm Standby)
- **[Well-Architected Pillars](files/well-architected-pillars.md)** - Reliability pillar (disaster recovery)
- **[Route 53 Supplement](route53_implementation_supplement.md)** - DNS failover integration
- **[Cross-Reference Index](CROSS_REFERENCE_INDEX.md)** - Navigate by DR strategy and RTO/RPO

**Key Differentiator:**
- Traditional DR: Snapshot-based, hours to recover
- DRS: Continuous replication, minutes to recover (RTO: minutes, RPO: seconds)

---

## DRS Architecture

### How It Works

```
Source Environment (On-Premises or Cloud)
    |
    +-- Server A (Production)
    |       |
    |       v
    |   AWS Replication Agent
    |       |
    |       +-- Continuous block-level replication
    |       +-- Compression
    |       +-- Encryption (in transit)
    |           |
    v           v
AWS Staging Area (Low Cost)
    |
    +-- Staging Area Subnet
        |
        +-- Replicated Volume (EBS gp3 - cheap storage)
        +-- Minimal compute (no instances running)
        +-- Point-in-time snapshots

(During Drill or Disaster)
    |
    v
Recovery Instances Launched
    |
    +-- Automatic conversion to AWS-native
    +-- EBS volumes attached
    +-- Boot and run on AWS
```

### Replication Process

**1. Initial Sync:**
- Full replication of source server
- Duration depends on data size and bandwidth
- Can use AWS Snowball for large datasets (>10TB)

**2. Continuous Replication:**
- Block-level changes replicated asynchronously
- RPO typically < 1 minute
- Minimal impact on source server (<5% CPU)

**3. Staging Area:**
- EBS volumes (gp3) - cost-effective storage
- No running instances (major cost savings)
- Automatic snapshots every 5 minutes (configurable)

**4. Recovery:**
- Launch recovery instance from latest state
- Automatic conversion:
  - VMware/Hyper-V → AWS EC2
  - Physical → AWS EC2
  - EC2 → EC2 (cross-region)
- Boot time: typically 5-15 minutes

---

## DRS vs Other DR Strategies

### Comparison Matrix

| Strategy | RTO | RPO | Cost | Complexity |
|----------|-----|-----|------|------------|
| **Backup & Restore** | 4-24 hours | 24+ hours | Low | Low |
| **Pilot Light** | 30-60 min | Minutes-Hours | Medium | Medium |
| **Warm Standby** | 5-15 min | Minutes | Medium-High | Medium |
| **Multi-Site Active-Active** | Seconds | Seconds | High | High |
| **DRS** | 5-15 min | Seconds | Low-Medium | Low |

### When to Choose DRS

**✅ Use DRS When:**
- RTO requirement: < 30 minutes
- RPO requirement: < 1 minute
- Servers can be recovered on AWS (not on-premises)
- Want to avoid running standby instances (cost savings)
- Need to test DR regularly (non-disruptive drills)

**❌ Don't Use DRS When:**
- Need RTO < 5 minutes (use Warm Standby or Active-Active)
- Must recover to on-premises (use VMware Cloud on AWS)
- Simple file-level backup is sufficient
- Database needs active-active (use Aurora Global, DynamoDB Global)

---

## Implementation Guide

### Step 1: Prerequisites

**Network Requirements:**
- VPN or Direct Connect recommended (not required)
- Ports: TCP 443 (HTTPS), TCP 1500 (replication)
- Bandwidth: Minimum 10 Mbps, Recommended 100+ Mbps

**Source Server Requirements:**
- Supported OS: Windows Server, Linux (RHEL, Ubuntu, CentOS, SUSE)
- Minimum 2 GB RAM
- Minimum 10 GB free disk space
- Not supported: Dynamic disks (Windows), encrypted volumes (BitLocker)

**AWS Setup:**
```bash
# Create IAM role for DRS
aws iam create-role \
  --role-name DRSRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "drs.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach required policies
aws iam attach-role-policy \
  --role-name DRSRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSElasticDisasterRecoveryEc2InstancePolicy

# Create staging area VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16
```

### Step 2: Install Replication Agent

**On Source Server:**
```bash
# Download installer from DRS console
wget https://aws-elastic-disaster-recovery-us-east-1.s3.amazonaws.com/latest/aws-replication-agent-installer.py

# Run installer
sudo python3 aws-replication-agent-installer.py \
  --region us-east-1 \
  --aws-access-key-id AKIAXXXXXXXXXXXXXXXX \
  --aws-secret-access-key xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Verify installation
sudo systemctl status aws-replication-agent
```

**Windows:**
```powershell
# Download and run MSI installer
msiexec /i AWSReplicationAgent.msi /qn REGION="us-east-1"

# Verify
Get-Service AWSReplicationAgent
```

### Step 3: Configure Replication Settings

**Launch Template Configuration:**
```json
{
  "LaunchTemplateName": "DRS-Recovery-Template",
  "LaunchTemplateData": {
    "InstanceType": "m5.xlarge",
    "KeyName": "recovery-key",
    "SecurityGroupIds": ["sg-xxxxxxxx"],
    "SubnetId": "subnet-xxxxxxxx",
    "IamInstanceProfile": {
      "Arn": "arn:aws:iam::123456789012:instance-profile/DRS-Recovery"
    },
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [{
        "Key": "Name",
        "Value": "DR-Recovery"
      },{
        "Key": "Environment",
        "Value": "DR"
      }]
    }]
  }
}
```

**Replication Settings:**
```bash
# Update replication configuration
aws drs update-replication-configuration \
  --source-server-id s-xxxxxxxxxxxxxxxxx \
  --replication-configuration '{
    "associateDefaultSecurityGroup": false,
    "bandwidthThrottling": 100,  # Mbps
    "createPublicIP": false,
    "dataPlaneRouting": "PRIVATE_IP",
    "defaultLargeStagingDiskType": "GP3",
    "ebsEncryption": {
      "encrypted": true,
      "kmsKeyId": "arn:aws:kms:us-east-1:123456789012:key/xxxxxxxx"
    },
    "replicationServerInstanceType": "t3.medium",
    "replicationServersSecurityGroupsIDs": ["sg-yyyyyyyy"],
    "stagingAreaSubnetId": "subnet-xxxxxxxx",
    "stagingAreaTags": {
      "Environment": "DR-Staging"
    },
    "useDedicatedReplicationServer": false
  }'
```

### Step 4: Configure Launch Settings

**Launch Settings determine how recovery instances are launched:**
```bash
aws drs update-launch-configuration \
  --source-server-id s-xxxxxxxxxxxxxxxxx \
  --launch-configuration '{
    "copyPrivateIp": true,
    "launchDisposition": "STOPPED",  # Launch in stopped state for testing
    "licensing": {
      "osByol": false  # Use AWS-provided licenses
    },
    "name": "WebServer-DR",
    "targetInstanceTypeRightSizingMethod": "BASIC"
  }'
```

**Launch Disposition Options:**
- **STARTED:** Instance starts immediately (for real DR)
- **STOPPED:** Instance launches in stopped state (for testing)

### Step 5: Monitor Replication

**Check Replication Status:**
```bash
# List source servers
aws drs describe-source-servers

# Get specific server details
aws drs describe-source-servers \
  --filters '{"sourceServerIDs": ["s-xxxxxxxxxxxxxxxxx"]}'
```

**Key Metrics:**
- **Data Replication Lag:** Target < 1 minute
- **Last Snapshot Time:** Should be recent
- **Replication Status:** HEALTHY, ERROR, or INITIAL_SYNC

**CloudWatch Alarms:**
```bash
# Alarm for replication lag
aws cloudwatch put-metric-alarm \
  --alarm-name DRS-Replication-Lag \
  --metric-name DataReplicationLag \
  --namespace AWS/DRS \
  --statistic Average \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 300 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:alerts
```

---

## Performing Disaster Recovery

### Recovery Types

**1. Drill (Non-Disruptive Test):**
```bash
# Initiate drill
aws drs start-replication \
  --source-server-id s-xxxxxxxxxxxxxxxxx \
  --recovery-type DRILL

# Launch recovery instance (stopped state)
aws drs launch-recovery-instances \
  --source-servers '[{
    "serverId": "s-xxxxxxxxxxxxxxxxx",
    "recoverySnapshotID": "snap-xxxxxxxxxxxxxxxxx"
  }]'

# Verify and terminate drill instances
aws dr2 terminate-recovery-instances \
  --recovery-instance-ids r-xxxxxxxxxxxxxxxxx
```

**2. Actual Recovery (Disaster):**
```bash
# Initiate recovery
aws drs launch-recovery-instances \
  --source-servers '[{
    "serverId": "s-xxxxxxxxxxxxxxxxx",
    "recoverySnapshotID": "latest"
  }]'

# Monitor recovery
aws drs describe-recovery-instances
```

### Recovery Procedure (Step-by-Step)

**Step 1: Assessment (0-5 minutes)**
1. Confirm primary site is unavailable
2. Determine scope (partial or full DR)
3. Notify stakeholders
4. Open incident ticket

**Step 2: Launch Recovery Instances (5-15 minutes)**
```bash
# Launch all critical servers
for server_id in s-11111111111111111 s-22222222222222222 s-33333333333333333; do
  aws drs launch-recovery-instances \
    --source-servers "[{\"serverId\": \"$server_id\", \"recoverySnapshotID\": \"latest\"}]"
done
```

**Step 3: Verification (15-30 minutes)**
1. Check instance status checks pass
2. Verify network connectivity
3. Test application functionality
4. Validate data integrity

**Step 4: Update DNS/Traffic Routing (if needed)**
```bash
# Update Route 53 to point to DR site
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "app.example.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z35SXDOTRQ7X7K",
          "DNSName": "dr-alb-123456789.us-west-2.elb.amazonaws.com.",
          "EvaluateTargetHealth": true
        }
      }
    }]
  }'
```

**Step 5: Failback Planning (ongoing)**
1. Document changes made in DR
2. Plan failback to primary when restored
3. Prepare data synchronization strategy

---

## Failback to Primary Site

### When to Failback

- Primary site is fully restored
- All issues resolved
- Sufficient testing completed
- Change window scheduled

### Failback Process

**Step 1: Prepare Primary Site**
```bash
# Ensure primary servers are ready
# Update OS, patches
# Verify connectivity to AWS
```

**Step 2: Install DRS Agent on Primary (Reverse Direction)**
```bash
# Install agent on primary servers
# Configure replication from AWS to on-premises
# Note: This requires AWS to on-premises connectivity
```

**Step 3: Sync Data**
```bash
# Wait for initial sync
# Verify data consistency
# Perform application testing
```

**Step 4: Cutover**
1. Schedule maintenance window
2. Stop writes to DR environment
3. Final sync
4. Switch traffic back to primary
5. Verify functionality

**Step 5: Cleanup**
```bash
# Terminate DR instances
aws drs terminate-recovery-instances \
  --recovery-instance-ids r-xxxxxxxxxxxxxxxxx

# Return to normal replication (on-premises to AWS)
```

---

## Cost Optimization

### Cost Components

**1. Replication Costs:**
- EBS gp3 volumes in staging area: ~$0.08/GB-month
- Data transfer out: ~$0.09/GB (from source to AWS)
- Snapshot storage: ~$0.05/GB-month

**2. Recovery Costs (only during DR):**
- EC2 instances: Pay for usage
- EBS volumes: From snapshots
- Data transfer

### Cost Comparison Example

**Scenario: 10 servers, 100TB total storage**

| Strategy | Monthly Cost | Recovery Cost |
|----------|-------------|---------------|
| Warm Standby | $15,000+ | Minimal |
| DRS | $8,500 | $2,000/hour (if used) |
| Backup & Restore | $3,000 | High (data restore) |

**DRS Cost Breakdown:**
- Staging storage: 100TB × $0.08 = $8,000
- Snapshots: 20TB (20% change rate) × $0.05 = $1,000
- Replication data transfer: ~$500
- **Total: ~$9,500/month**

### Cost Savings Strategies

**1. Right-Sizing Staging Disks:**
```bash
# Use GP3 instead of GP2 or IO1
aws drs update-replication-configuration \
  --source-server-id s-xxxxxxxxxxxxxxxxx \
  --replication-configuration '{
    "defaultLargeStagingDiskType": "GP3"
  }'
```

**2. Compression:**
- DRS automatically compresses data
- Typical compression: 30-50% savings

**3. Bandwidth Throttling:**
```bash
# Limit replication bandwidth during business hours
aws drs update-replication-configuration \
  --source-server-id s-xxxxxxxxxxxxxxxxx \
  --replication-configuration '{
    "bandwidthThrottling": 50  # Mbps
  }'
```

---

## DRS Limitations and Considerations

### Technical Limitations

**Not Supported:**
- Dynamic disks (Windows)
- BitLocker encryption
- iSCSI volumes
- Shared cluster disks
- VMs with snapshots/checkpoints

**Network Requirements:**
- Minimum 10 Mbps bandwidth
- Maximum 1 second latency to AWS
- Stable network connection

**RPO Considerations:**
- Typical RPO: < 1 minute
- Under heavy load: Up to 5 minutes
- Network issues: RPO may increase

### Design Patterns

**Pattern 1: Application-Consistent Recovery**
```
Database Server + App Server
    |
    +-- Use DRS for both
    +-- Launch together
    +-- Application starts cleanly
```

**Pattern 2: Database + DRS Hybrid**
```
Database: Aurora Global / DynamoDB Global (active-active)
Application Servers: DRS (RTO minutes)
    |
    +-- Database always available
    +-- Apps recover quickly
    +-- Best RPO/RTO balance
```

**Pattern 3: Tiered Recovery**
```
Tier 1 (Critical): DRS + Warm Standby (RTO: 5 min)
Tier 2 (Important): DRS only (RTO: 15 min)
Tier 3 (Standard): Backup & Restore (RTO: 4 hours)
```

---

## Integration with Other AWS Services

### DRS + Route 53

**Automated DNS Failover:**
```bash
# CloudWatch alarm triggers Lambda
# Lambda updates Route 53 on DR event

# Lambda function
import boto3

def lambda_handler(event, context):
    route53 = boto3.client('route53')
    
    # Update failover record
    route53.change_resource_record_sets(
        HostedZoneId='Z1234567890ABC',
        ChangeBatch={
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': 'app.example.com',
                    'Type': 'A',
                    'SetIdentifier': 'DR',
                    'Failover': 'PRIMARY',
                    'AliasTarget': {
                        'HostedZoneId': 'Z35SXDOTRQ7X7K',
                        'DNSName': 'dr-alb.amazonaws.com.',
                        'EvaluateTargetHealth': True
                    }
                }
            }]
        }
    )
```

### DRS + Systems Manager

**Automated Post-Recovery Configuration:**
```yaml
# Systems Manager Document for DR recovery
schemaVersion: '2.2'
description: Post-DR recovery configuration
mainSteps:
  - action: aws:runShellScript
    name: configureNetworking
    inputs:
      runCommand:
        - "hostnamectl set-hostname {{Hostname}}"
        - "systemctl restart network"
  
  - action: aws:runShellScript
    name: startApplication
    inputs:
      runCommand:
        - "systemctl start myapp"
        - "systemctl enable myapp"
```

---

## Best Practices

### 1. Regular Testing

**Monthly Drills:**
- Launch recovery instances
- Verify application functionality
- Document any issues
- Terminate drill instances

**Quarterly Full DR Tests:**
- Complete failover simulation
- Update runbooks
- Train team
- Measure RTO/RPO

### 2. Monitoring

**Key Metrics to Watch:**
- Replication lag (should be < 1 minute)
- Snapshot frequency
- Source server health
- Staging area costs

**CloudWatch Dashboard:**
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/DRS", "DataReplicationLag", "SourceServerID", "s-xxxxxxxx"]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "Replication Lag"
      }
    }
  ]
}
```

### 3. Security

**Encryption:**
- Always enable EBS encryption
- Use KMS customer-managed keys
- Encrypt replication in transit (TLS 1.2+)

**Network Security:**
- Place staging area in private subnets
- Use VPC endpoints for AWS service access
- Restrict security groups

### 4. Documentation

**Required Documentation:**
1. Network diagrams (primary and DR)
2. Server inventory with DRS source server IDs
3. Recovery runbook with step-by-step procedures
4. Contact lists and escalation procedures
5. RTO/RPO compliance reports

---

*This section addresses the critical gap in AWS Elastic Disaster Recovery for SA Pro certification. DRS is explicitly mentioned in the exam guide but was missing from the baseline document.*
