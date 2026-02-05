# AWS Systems Manager Implementation Supplement

**Index:** [GOV-ARCH-001](GOV-ARCH-001-Architecture-Documentation-Index.md) | [CROSS_REFERENCE_INDEX.md](CROSS_REFERENCE_INDEX.md)  
**Related:** [AWS Comprehensive Guide](AWS_Solutions_Architect_Comprehensive_Guide.md) Section 2 (Operational Excellence)  
**Related Supplements:** [AWS Config](aws_config_supplement.md) (compliance) | [Security](security_services_supplement.md) (remediation) | [DRS](drs_implementation_supplement.md) (automation)  
**Domain:** Continuous Improvement (25%)

## Table of Contents
1. [Overview](#1-overview)
2. [Patch Manager](#2-patch-manager)
3. [Automation Documents](#3-automation-documents)
4. [Session Manager](#4-session-manager)
5. [Parameter Store](#5-parameter-store)
6. [Run Command](#6-run-command)
7. [Inventory and State Manager](#7-inventory-and-state-manager)
8. [Decision Framework](#8-decision-framework)
9. [Cost Optimization](#9-cost-optimization)
10. [Integration Patterns](#10-integration-patterns)
11. [Troubleshooting](#11-troubleshooting)

### Related Documentation
- **[Well-Architected Pillars](files/well-architected-pillars.md)** - Operational Excellence pillar
- **[Compliance Framework](files/compliance-framework.md)** - Patch compliance requirements
- **[AWS Config Supplement](aws_config_supplement.md)** - Automated remediation integration
- **[Cross-Reference Index](CROSS_REFERENCE_INDEX.md)** - Navigate by Systems Manager capability

---

## 1. Overview

AWS Systems Manager provides centralized node management across AWS, on-premises, and multi-cloud environments. It offers a unified console experience for operational insights, automated administration, and secure remote access without SSH/RDP.

### Key Capabilities

| Capability | Purpose | Use Cases |
|------------|---------|-----------|
| **Patch Manager** | Automated OS and application patching | Security compliance, vulnerability management |
| **Session Manager** | Secure shell access without SSH keys | Audit trails, port forwarding, secure access |
| **Run Command** | Execute commands across fleet | Configuration management, troubleshooting |
| **Automation** | Workflow orchestration | AMI creation, instance management, remediation |
| **Parameter Store** | Secure configuration storage | Secrets management, application configuration |
| **State Manager** | Maintain desired state | Ensure configurations persist across reboots |
| **Inventory** | Collect instance metadata | Asset tracking, compliance reporting |

### Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AWS Systems Manager                       │
├─────────────────────────────────────────────────────────────┤
│  Patch Manager  │ Session Manager │ Run Command │ Automation │
├─────────────────────────────────────────────────────────────┤
│                 Managed Instances (SSM Agent)               │
├─────────────────────────────────────────────────────────────┤
│   EC2   │  On-Premises  │  Edge Devices  │  IoT Greengrass  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Patch Manager

### 2.1 Overview

Patch Manager automates patching of managed nodes with security and other updates. It provides centralized control, flexible operations, compliance reporting, and cross-platform support.

**Key Benefits:**
- Centralized patching across AWS Organizations
- Custom patch baselines defining compliance
- Compliance reporting in CSV format
- Integration with Security Hub and Config
- Cross-platform support (Windows, Linux, macOS)

### 2.2 Patch Baselines

A patch baseline defines what constitutes patch compliance for your organization.

#### Default vs Custom Baselines

| Aspect | AWS-Defined | Custom Baseline |
|--------|-------------|-----------------|
| Approval rules | Pre-configured | Fully customizable |
| Patch lists | Cannot modify | Full control |
| Auto-approval | Fixed delays | Configurable days |
| Use case | Quick start | Production environments |

#### Patch Baseline Components

```
Patch Baseline
├── Operating System (Windows, Amazon Linux, RHEL, etc.)
├── Approval Rules
│   ├── Classification (Security, Bugfix, Enhancement)
│   ├── Severity (Critical, Important, Moderate)
│   └── Auto-approval delay (days after release)
├── Approved Patches (specific patch IDs)
├── Rejected Patches (specific patch IDs)
└── Global Filters (exclude by classification/severity)
```

#### Example: Creating a Custom Patch Baseline

**AWS Console Steps:**
1. Navigate to Systems Manager → Patch Manager
2. Choose "Patch baselines" → "Create patch baseline"
3. Enter name and description
4. Select operating system
5. Configure approval rules:
   - Classification: Security
   - Severity: Critical, Important
   - Auto-approval delay: 7 days
6. Add approved/rejected patches as needed
7. Create baseline

**CLI Example:**
```bash
# Create patch baseline for Amazon Linux 2023
aws ssm create-patch-baseline \
  --name "Production-AL2023-Security" \
  --description "Critical and Important security patches only" \
  --operating-system AMAZON_LINUX_2023 \
  --approval-rules 'PatchRules=[{PatchFilterGroup={PatchFilters=[{Key=CLASSIFICATION,Values=Security},{Key=SEVERITY,Values=Critical,Important}]},ApproveAfterDays=7}]' \
  --tags Key=Environment,Value=Production

# Assign baseline to patch group
aws ssm register-patch-baseline-for-patch-group \
  --baseline-id pb-0123456789abcdef0 \
  --patch-group production-web-servers
```

### 2.3 Patching Operation Methods

Patch Manager offers four methods for running patching operations:

#### Method Comparison

| Method | Scope | Scheduling | Installation | Best For |
|--------|-------|------------|--------------|----------|
| **Patch Policy (Quick Setup)** | Multi-account, Multi-region | Recurring | Yes | Organizations-wide patching |
| **Host Management (Quick Setup)** | Multi-account | Recurring | No (scan only) | Compliance visibility |
| **Maintenance Windows** | Single account/region | Recurring | Yes | Scheduled maintenance |
| **Patch Now** | Single account/region | On-demand | Yes | Emergency patching |

#### Patch Policy Configuration (Recommended)

**Use Case:** Centralized patching across AWS Organization

```yaml
# Patch Policy Structure
PatchPolicy:
  Name: Organization-Security-Patching
  Targets:
    - OrganizationalUnits: ["ou-1234-abcdef"]
    - Accounts: ["123456789012"]
    - Regions: ["us-east-1", "eu-west-1"]
  
  Baselines:
    OperatingSystems:
      - Type: AMAZON_LINUX_2023
        Baseline: pb-production-security
      - Type: WINDOWS
        Baseline: pb-windows-critical
  
  Schedule:
    ScanSchedule: "cron(0 2 ? * SUN *)"  # Weekly scan
    InstallSchedule: "cron(0 4 ? * SUN *)"  # Weekly install
    
  Options:
    RebootOption: RebootIfNeeded
    MaxConcurrency: 10%
    MaxErrors: 5%
```

**Setup Steps:**
1. Open Systems Manager → Quick Setup
2. Choose "Patch Manager"
3. Select configuration type: Patch policy
4. Choose target scope (Organization, OU, or accounts)
5. Select regions
6. Configure baseline and schedule
7. Review and deploy

#### Maintenance Window Patching

**Use Case:** Scheduled patching during maintenance windows

```bash
# Create maintenance window
aws ssm create-maintenance-window \
  --name "Production-Patching-Window" \
  --schedule "cron(0 3 ? * SUN#1 *)" \
  --schedule-timezone "America/New_York" \
  --duration 4 \
  --cutoff 1 \
  --allow-unassociated-targets

# Register targets (instances)
aws ssm register-target-with-maintenance-window \
  --window-id mw-0123456789abcdef0 \
  --resource-type INSTANCE \
  --targets Key=tag:Environment,Values=Production

# Register patch task
aws ssm register-task-with-maintenance-window \
  --window-id mw-0123456789abcdef0 \
  --targets Key=WindowTargetIds,Values=123456789 \
  --task-arn AWS-RunPatchBaseline \
  --service-role-arn arn:aws:iam::123456789012:role/MaintenanceWindowRole \
  --task-type RUN_COMMAND \
  --max-concurrency 10% \
  --max-errors 5% \
  --priority 1 \
  --task-invocation-parameters 'RunCommand={Comment=Security patching,Parameters={Operation=[Install]}}'
```

### 2.4 Compliance Reporting

After scanning operations, view detailed compliance information:

**Compliance Dashboard:**
- Shows non-compliant instances
- Lists missing patches per instance
- Provides overall compliance percentage

**CSV Reports:**
```bash
# Generate compliance report to S3
aws ssm create-report-for-patch-group \
  --patch-group production-web-servers \
  --report-type Compliance \
  --s3-bucket my-patch-reports \
  --s3-prefix reports/
```

**Report Contents:**
- Instance ID and hostname
- Operating system
- Missing patch count
- Specific patch IDs missing
- Severity levels
- Classification (Security, Bugfix, etc.)
- CVE identifiers (if available)

### 2.5 Best Practices

1. **Use Custom Patch Baselines**
   - Define approval delays appropriate for your environment
   - Start with Security classification only
   - Test patches in dev before production

2. **Implement Staged Patching**
   - Dev → Staging → Production
   - Use different schedules per environment
   - Allow rollback window between stages

3. **Monitor Compliance**
   - Set up CloudWatch alarms for compliance drops
   - Export reports to S3 for long-term storage
   - Integrate with Security Hub for centralized visibility

4. **Handle Reboots Appropriately**
   - Use "RebootIfNeeded" for automatic reboots
   - Schedule during maintenance windows
   - Consider using Auto Scaling with health checks

---

## 3. Automation Documents

### 3.1 Overview

Automation documents (SSM documents) define actions performed on managed nodes. They enable workflow orchestration, fleet management, and automated remediation.

### 3.2 Document Types

| Type | Purpose | Example |
|------|---------|---------|
| **Command** | Run commands on instances | Install package, run script |
| **Policy** | Enforce state | Ensure CloudWatch agent installed |
| **Automation** | Multi-step workflows | Create AMI, update ASG |

### 3.3 AWS-Managed Automation Documents

Common automation documents provided by AWS:

| Document | Purpose |
|----------|---------|
| `AWS-CreateImage` | Create AMI from instance |
| `AWS-RestartEC2Instance` | Restart EC2 instance |
| `AWS-StopEC2Instance` | Stop EC2 instance |
| `AWS-StartEC2Instance` | Start EC2 instance |
| `AWS-DetachEBSVolume` | Detach EBS volume |
| `AWS-DeleteSnapshot` | Delete EBS snapshot |
| `AWS-RunPatchBaseline` | Run Patch Manager baseline |

### 3.4 Creating Custom Automation Documents

**Example: Custom AMI Creation Workflow**

```yaml
schemaVersion: '0.3'
description: Create AMI with pre-installed software
assumeRole: '{{AutomationAssumeRole}}'
parameters:
  InstanceId:
    type: String
    description: ID of the source instance
  AMIName:
    type: String
    description: Name for the new AMI
    default: 'CustomAMI-{{global:DATE_TIME}}'
mainSteps:
  - name: stopInstance
    action: 'aws:runCommand'
    inputs:
      DocumentName: AWS-RunShellScript
      InstanceIds:
        - '{{InstanceId}}'
      Parameters:
        commands:
          - sudo yum update -y
          - sudo yum install -y cloudwatch-agent
    onFailure: Abort
    
  - name: createImage
    action: 'aws:createImage'
    inputs:
      InstanceId: '{{InstanceId}}'
      ImageName: '{{AMIName}}'
      NoReboot: false
    onFailure: Abort
    
  - name: verifyImage
    action: 'aws:sleep'
    inputs:
      Duration: PT5M
    onFailure: Continue
    
  - name: startInstance
    action: 'aws:runCommand'
    inputs:
      DocumentName: AWS-RunShellScript
      InstanceIds:
        - '{{InstanceId}}'
      Parameters:
        commands:
          - echo "Instance ready after AMI creation"
    onFailure: Continue
outputs:
  - createImage.ImageId
  - createImage.ImageState
```

**Creating the Document:**
```bash
# Create automation document from YAML file
aws ssm create-document \
  --name CustomAMICreation \
  --content file://custom-ami-automation.yaml \
  --document-type Automation \
  --document-format YAML
```

### 3.5 Rate Control and Error Handling

```bash
# Execute automation with rate control
aws ssm start-automation-execution \
  --document-name CustomAMICreation \
  --parameters InstanceId=i-0123456789abcdef0,AMIName=MyApp-v1.0.0 \
  --target-parameter-name InstanceId \
  --targets Key=tag:Environment,Values=Production \
  --max-concurrency 10% \
  --max-errors 5
```

### 3.6 Lifecycle Hooks in Patching

Run custom scripts before and after patching:

```yaml
mainSteps:
  - name: PrePatchHook
    action: 'aws:runCommand'
    inputs:
      DocumentName: AWS-RunShellScript
      InstanceIds:
        - '{{InstanceId}}'
      Parameters:
        commands:
          - /opt/scripts/pre-patch-checks.sh
          
  - name: ApplyPatches
    action: 'aws:runCommand'
    inputs:
      DocumentName: AWS-RunPatchBaseline
      InstanceIds:
        - '{{InstanceId}}'
      Parameters:
        Operation: Install
        
  - name: PostPatchHook
    action: 'aws:runCommand'
    inputs:
      DocumentName: AWS-RunShellScript
      InstanceIds:
        - '{{InstanceId}}'
      Parameters:
        commands:
          - /opt/scripts/verify-services.sh
          - /opt/scripts/notify-team.sh
```

---

## 4. Session Manager

### 4.1 Overview

Session Manager provides secure shell access to managed nodes without SSH keys, open inbound ports, or bastion hosts. It offers session logging, audit trails, and port forwarding capabilities.

**Key Features:**
- No SSH keys required
- No inbound ports open
- IAM-based access control
- Session logging to S3 or CloudWatch Logs
- Port forwarding support
- Cross-platform (Windows/Linux/macOS)

### 4.2 Prerequisites

1. **SSM Agent installed and running** on target instances
2. **IAM permissions** for Session Manager access
3. **VPC endpoints** (optional but recommended for private subnets)

### 4.3 IAM Permissions

**User/Role Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:StartSession",
        "ssm:ResumeSession",
        "ssm:TerminateSession"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetConnectionStatus"
      ],
      "Resource": "arn:aws:ec2:*:*:instance/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

**Instance Profile Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssmmessages:CreateControlChannel",
        "ssmmessages:CreateDataChannel",
        "ssmmessages:OpenControlChannel",
        "ssmmessages:OpenDataChannel"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetEncryptionConfiguration"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt"
      ],
      "Resource": "arn:aws:kms:region:account-id:key/key-id"
    }
  ]
}
```

### 4.4 Starting Sessions

**Via AWS Console:**
1. Navigate to Systems Manager → Session Manager
2. Click "Start session"
3. Select target instance
4. Click "Start session"

**Via AWS CLI:**
```bash
# Start interactive session
aws ssm start-session --target i-0123456789abcdef0

# Start session with document (port forwarding)
aws ssm start-session \
  --target i-0123456789abcdef0 \
  --document-name AWS-StartPortForwardingSession \
  --parameters '{"portNumber":["80"], "localPortNumber":["8080"]}'
```

**Via Session Manager Plugin:**
```bash
# Connect to instance
session-manager-plugin \
  $(aws ssm start-session \
    --target i-0123456789abcdef0 \
    --document-name AWS-StartSession \
    --parameters '{"Reason":["Troubleshooting"]}' \
    --output json) \
  $(aws configure get region) \
  StartSession \
  $(aws sts get-caller-identity --query Account --output text) \
  i-0123456789abcdef0 \
  session-manager-plugin
```

### 4.5 Port Forwarding

**Use Case:** Access remote services without exposing ports

```bash
# Forward local port 5432 to RDS instance through EC2 bastion
aws ssm start-session \
  --target i-bastion-instance \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{
    "host":["mydb.cluster-xyz.us-east-1.rds.amazonaws.com"],
    "portNumber":["5432"],
    "localPortNumber":["5433"]
  }'

# Now connect locally
psql -h localhost -p 5433 -U dbuser -d mydb
```

### 4.6 Session Logging

**Enable Logging:**

1. **Navigate to:** Systems Manager → Session Manager → Preferences
2. **Configure:**
   - **S3 Logging:** Specify bucket and optional prefix
   - **CloudWatch Logs:** Specify log group
   - **Encryption:** Enable KMS encryption
   - **CloudTrail:** Log API calls

**S3 Bucket Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ssm.amazonaws.com"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::my-session-logs/*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "bucket-owner-full-control"
        }
      }
    }
  ]
}
```

### 4.7 Session Preferences Document

Create custom session preferences:

```json
{
  "schemaVersion": "1.0",
  "description": "Session preferences for production environment",
  "sessionType": "Standard_Stream",
  "inputs": {
    "s3BucketName": "my-session-logs",
    "s3KeyPrefix": "production/",
    "s3EncryptionEnabled": true,
    "cloudWatchLogGroupName": "/aws/ssm/sessions",
    "cloudWatchEncryptionEnabled": true,
    "kmsKeyId": "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012",
    "runAsEnabled": true,
    "runAsDefaultUser": "ssm-user",
    "idleSessionTimeout": "20",
    "maxSessionDuration": "60"
  }
}
```

---

## 5. Parameter Store

### 5.1 Overview

Parameter Store provides secure, hierarchical storage for configuration data management and secrets management. It integrates with AWS services and offers encryption via KMS.

**Key Features:**
- Centralized configuration storage
- Hierarchical organization
- Version tracking
- Integration with Secrets Manager
- Cross-account parameter sharing
- No charge for standard parameters

### 5.2 Parameter Tiers

| Feature | Standard | Advanced |
|---------|----------|----------|
| **Cost** | Free | $0.05 per parameter/month |
| **Max size** | 4 KB | 8 KB |
| **Max parameters** | 10,000 per region | 100,000 per region |
| **Parameter policies** | No | Yes (expiration, notification) |
| **Throughput** | Shared | Higher dedicated |
| **Use case** | Configuration data | Secrets with rotation policies |

### 5.3 Parameter Types

| Type | Description | Example |
|------|-------------|---------|
| **String** | Plain text value | API endpoint URL |
| **StringList** | Comma-separated values | List of security groups |
| **SecureString** | Encrypted with KMS | Database password, API key |

### 5.4 Creating Parameters

**AWS Console:**
1. Navigate to Systems Manager → Parameter Store
2. Click "Create parameter"
3. Enter name (use hierarchical structure: `/app/environment/parameter`)
4. Select type (String, StringList, SecureString)
5. Enter value
6. (Optional) Add tags
7. Create parameter

**AWS CLI:**
```bash
# Create string parameter
aws ssm put-parameter \
  --name /myapp/production/database/host \
  --value "db.example.com" \
  --type String \
  --description "Production database hostname" \
  --tags Key=Environment,Value=Production

# Create secure string parameter
aws ssm put-parameter \
  --name /myapp/production/database/password \
  --value "SuperSecretPassword123!" \
  --type SecureString \
  --key-id alias/aws/ssm \
  --description "Production database password"

# Create string list parameter
aws ssm put-parameter \
  --name /myapp/production/security-groups \
  --value "sg-12345678,sg-87654321" \
  --type StringList \
  --description "Security groups for production"
```

### 5.5 Hierarchical Structure

**Best Practice Naming Convention:**
```
/{application}/{environment}/{resource}/{parameter}

Examples:
/myapp/production/database/host
/myapp/production/database/port
/myapp/production/cache/redis/host
/myapp/staging/api/key
/org/shared/vpc/cidr-block
```

**Retrieving Parameters by Path:**
```bash
# Get all parameters under /myapp/production
aws ssm get-parameters-by-path \
  --path /myapp/production \
  --recursive \
  --with-decryption

# Get only direct children
aws ssm get-parameters-by-path \
  --path /myapp/production \
  --no-recursive
```

### 5.6 Parameter Store vs Secrets Manager

| Aspect | Parameter Store | Secrets Manager |
|--------|-----------------|-----------------|
| **Cost** | Free (Standard), $0.05/Advanced | $0.40/secret/month |
| **Rotation** | Manual or Lambda | Built-in rotation |
| **Replication** | No | Cross-region replication |
| **Size limit** | 4-8 KB | 65,536 bytes |
| **Integration** | Direct service integration | RDS, DocumentDB, Redshift rotation |
| **Use case** | Config data, simple secrets | Database credentials, auto-rotation |

**Decision Matrix:**
- Use **Parameter Store** for: Configuration data, API endpoints, simple secrets, when cost matters
- Use **Secrets Manager** for: Database credentials requiring rotation, cross-region needs, compliance requirements

### 5.7 Advanced Parameter Policies

Only available for Advanced tier:

```bash
# Create parameter with expiration policy
aws ssm put-parameter \
  --name /myapp/temp/api-key \
  --value "temp-key-12345" \
  --type SecureString \
  --policies '[{"Type":"Expiration","Version":"1.0","Attributes":{"Timestamp":"2025-12-31T23:59:59Z"}}]'

# Add notification policy
aws ssm put-parameter \
  --name /myapp/production/database/password \
  --value "new-password" \
  --type SecureString \
  --policies '[{"Type":"NoChangeNotification","Version":"1.0","Attributes":{"After":"30","Unit":"Days"}}]'
```

### 5.8 Using Parameters in Applications

**AWS Lambda (Python):**
```python
import boto3
import os

ssm = boto3.client('ssm')

# Get single parameter
response = ssm.get_parameter(
    Name='/myapp/production/database/host',
    WithDecryption=True
)
db_host = response['Parameter']['Value']

# Get multiple parameters
response = ssm.get_parameters(
    Names=[
        '/myapp/production/database/host',
        '/myapp/production/database/port',
        '/myapp/production/database/password'
    ],
    WithDecryption=True
)
params = {p['Name']: p['Value'] for p in response['Parameters']}
```

**AWS Lambda (Node.js):**
```javascript
const AWS = require('aws-sdk');
const ssm = new AWS.SSM();

async function getParameters() {
  const response = await ssm.getParameter({
    Name: '/myapp/production/database/host',
    WithDecryption: true
  }).promise();
  
  return response.Parameter.Value;
}
```

**CloudFormation:**
```yaml
Resources:
  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      Environment:
        Variables:
          DB_HOST: '{{resolve:ssm-secure:/myapp/production/database/host}}'
          DB_PASSWORD: '{{resolve:ssm-secure:/myapp/production/database/password}}'
```

---

## 6. Run Command

### 6.1 Overview

Run Command allows you to execute commands on managed instances without SSH/RDP. It provides rate control, concurrency management, and output retrieval.

**Common Use Cases:**
- Execute scripts across fleets
- Collect diagnostics
- Install software
- Restart services
- Run troubleshooting commands

### 6.2 AWS-Managed Documents

| Document | Purpose |
|----------|---------|
| `AWS-RunShellScript` | Run shell scripts (Linux/macOS) |
| `AWS-RunPowerShellScript` | Run PowerShell scripts (Windows) |
| `AWS-RunRemoteScript` | Run scripts from S3/GitHub |
| `AWS-UpdateSSMAgent` | Update SSM Agent |
| `AWS-ConfigureAWSPackage` | Install AWS packages |

### 6.3 Executing Commands

**AWS CLI:**
```bash
# Run command on single instance
aws ssm send-command \
  --instance-ids i-0123456789abcdef0 \
  --document-name AWS-RunShellScript \
  --comment "Check disk space" \
  --parameters 'commands=["df -h", "free -m"]'

# Run command on multiple instances by tag
aws ssm send-command \
  --targets Key=tag:Environment,Values=Production \
  --document-name AWS-RunShellScript \
  --parameters 'commands=["yum update -y"]' \
  --max-concurrency 10 \
  --max-errors 2

# Run PowerShell on Windows instances
aws ssm send-command \
  --instance-ids i-windows-instance \
  --document-name AWS-RunPowerShellScript \
  --parameters 'commands=["Get-Process", "Get-Service"]'
```

### 6.4 Rate Control

```bash
# Run command with concurrency control
aws ssm send-command \
  --targets Key=tag:Environment,Values=Production \
  --document-name AWS-RunShellScript \
  --parameters 'commands=["systemctl restart nginx"]' \
  --max-concurrency "10%" \
  --max-errors "5%"
```

**Concurrency Options:**
- `10` - Run on 10 instances at a time
- `10%` - Run on 10% of targets at a time

**Error Handling:**
- Stop after N errors: `--max-errors 5`
- Stop after percentage fails: `--max-errors 10%`

### 6.5 Retrieving Output

```bash
# Get command invocation details
aws ssm list-command-invocations \
  --command-id command-id-here \
  --details

# Get output from specific instance
aws ssm get-command-invocation \
  --command-id command-id-here \
  --instance-id i-0123456789abcdef0
```

**Output to S3:**
```bash
aws ssm send-command \
  --instance-ids i-0123456789abcdef0 \
  --document-name AWS-RunShellScript \
  --parameters 'commands=["cat /var/log/messages"]' \
  --output-s3-bucket-name my-command-output \
  --output-s3-key-prefix logs/
```

---

## 7. Inventory and State Manager

### 7.1 Inventory

Inventory collects metadata from managed instances including:
- Applications
- AWS components
- Files
- Network configurations
- Windows updates
- Instance details

**Setting Up Inventory:**
```bash
# Create association to collect inventory
aws ssm create-association \
  --name AWS-GatherSoftwareInventory \
  --targets Key=InstanceIds,Values=* \
  --schedule-expression "rate(24 hours)"
```

**Querying Inventory:**
```bash
# Get inventory for specific instance
aws ssm get-inventory \
  --filters Key=AWS:InstanceInformation.InstanceId,Values=i-0123456789abcdef0

# Get all installed software
aws ssm get-inventory \
  --result-attributes Key=AWS:Application.Name,Key=AWS:Application.Version
```

### 7.2 State Manager

State Manager ensures instances maintain desired state configurations.

**Use Cases:**
- Ensure CloudWatch agent is installed
- Maintain specific registry settings (Windows)
- Ensure specific users exist
- Configure SSH settings

**Creating an Association:**
```bash
# Ensure CloudWatch agent is installed
aws ssm create-association \
  --name AWS-ConfigureAWSPackage \
  --targets Key=tag:Environment,Values=Production \
  --parameters '{"action":["Install"],"name":["AmazonCloudWatchAgent"]}' \
  --schedule-expression "rate(30 minutes)" \
  --compliance-severity HIGH
```

---

## 8. Decision Framework

### 8.1 Remote Access: Session Manager vs SSH/RDP

| Factor | Session Manager | Traditional SSH/RDP |
|--------|-----------------|---------------------|
| **Security** | No open ports, IAM-based | Requires open ports, key management |
| **Audit trail** | Built-in logging | Manual configuration |
| **Key management** | IAM credentials | SSH keys/passwords |
| **Bastion hosts** | Not required | Often required |
| **Compliance** | Easier to audit | More complex |
| **Cost** | No additional cost | EC2 cost for bastions |

**Recommendation:** Use Session Manager for all production environments.

### 8.2 Configuration Storage: Parameter Store vs Secrets Manager

| Use Case | Parameter Store | Secrets Manager |
|----------|-----------------|-----------------|
| **API endpoints** | ✓ Recommended | ✗ Overkill |
| **Feature flags** | ✓ Recommended | ✗ Overkill |
| **Database passwords (no rotation)** | ✓ Acceptable | ✓ Recommended |
| **Database passwords (auto-rotation)** | ✗ Not supported | ✓ Required |
| **Third-party API keys** | ✓ Acceptable | ✓ Recommended |
| **Cost-sensitive** | ✓ Free tier | ✗ Higher cost |

### 8.3 Patching Strategy Selection

| Environment | Method | Schedule |
|-------------|--------|----------|
| **Development** | Patch Now | Ad-hoc |
| **Staging** | Maintenance Window | Weekly |
| **Production** | Patch Policy | Monthly (cautious) |
| **Critical** | Manual + Maintenance Window | Quarterly + emergency |

---

## 9. Cost Optimization

### 9.1 Parameter Store

- Use **Standard tier** for most parameters (free)
- Only use **Advanced tier** when needed:
  - Parameter policies required
  - Larger than 4 KB
  - Higher throughput needed

### 9.2 Session Manager

- No additional cost for Session Manager itself
- Data transfer costs apply:
  - Inbound: Free
  - Outbound: Standard EC2 data transfer rates
- Log storage costs:
  - S3: Standard S3 pricing
  - CloudWatch Logs: Ingestion and storage costs

### 9.3 Patch Manager

- No additional cost for Patch Manager
- EC2 instance costs during patching
- Consider maintenance windows to minimize disruption
- Use patch policies for efficient multi-account management

### 9.4 Automation

- No cost for automation documents
- EC2 API call charges apply
- Step Functions integration has standard Step Functions pricing

---

## 10. Integration Patterns

### 10.1 EventBridge Integration

**Automated Response to Patch Compliance Events:**
```json
{
  "source": ["aws.ssm"],
  "detail-type": ["Configuration Compliance State Change"],
  "detail": {
    " compliance-type": ["Patch"],
    "status": ["NON_COMPLIANT"]
  }
}
```

**Action:** Trigger Lambda to create Jira ticket or send Slack notification.

### 10.2 Security Hub Integration

Patch compliance findings automatically flow to Security Hub when enabled.

### 10.3 Config Integration

Use AWS Config rules to validate Systems Manager associations:
- `ec2-instance-managed-by-systems-manager`
- `ec2-instance-patch-compliance-check`

### 10.4 CloudWatch Integration

**Metrics Available:**
- `CommandsFailed`
- `CommandsSucceeded`
- `CommandsDeliveryTimedOut`
- `AutomationExecutionsFailed`

**Alarms:**
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name HighPatchFailureRate \
  --metric-name CommandsFailed \
  --namespace AWS/SSM-RunCommand \
  --statistic Sum \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1
```

---

## 11. Troubleshooting

### 11.1 SSM Agent Issues

**Verify Agent Status:**
```bash
# Linux
sudo systemctl status amazon-ssm-agent
sudo amazon-ssm-agent -version

# Windows (PowerShell)
Get-Service AmazonSSMAgent
Get-Command AmazonSSMAgent.exe
```

**Common Issues:**

| Issue | Cause | Solution |
|-------|-------|----------|
| Agent not running | Service stopped | `sudo systemctl start amazon-ssm-agent` |
| No IAM permissions | Missing instance profile | Attach AmazonSSMManagedInstanceCore policy |
| Can't reach endpoints | VPC configuration | Configure VPC endpoints or NAT Gateway |
| Old agent version | Outdated | `sudo yum update amazon-ssm-agent` |

### 11.2 Session Manager Troubleshooting

**Check Session Manager Plugin:**
```bash
session-manager-plugin --version
```

**Common Errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| "SessionManagerPlugin is not found" | Plugin not installed | Install Session Manager plugin |
| "TargetNotConnected" | Instance not registered | Verify SSM Agent is running |
| "AccessDenied" | IAM permissions | Check user has ssm:StartSession permission |
| "InvalidDocument" | Wrong document | Use AWS-StartSession document |

### 11.3 Patch Manager Troubleshooting

**Check Patch Compliance:**
```bash
aws ssm describe-instance-patch-states \
  --instance-id i-0123456789abcdef0
```

**View Patch Baseline:**
```bash
aws ssm get-patch-baseline \
  --baseline-id pb-0123456789abcdef0
```

**Common Issues:**

| Issue | Cause | Solution |
|-------|-------|----------|
| Patches not installing | Wrong baseline | Verify patch baseline approval rules |
| Instance not scanning | Not in patch group | Register instance to patch group |
| Maintenance window not running | Wrong schedule | Verify cron expression |
| Reboot not occurring | Reboot option set to Never | Change to RebootIfNeeded |

### 11.4 Parameter Store Troubleshooting

**Check Parameter Access:**
```bash
aws ssm get-parameter \
  --name /myapp/production/database/host \
  --with-decryption
```

**Common Issues:**

| Issue | Cause | Solution |
|-------|-------|----------|
| "ParameterNotFound" | Wrong path | Verify full parameter name |
| Decryption failed | KMS access denied | Grant kms:Decrypt permission |
| Throttling | Too many requests | Implement caching, use Advanced tier |

---

## Quick Reference Commands

```bash
# Check instance SSM registration
aws ssm describe-instance-information

# List available documents
aws ssm list-documents

# Get document details
aws ssm get-document --name AWS-RunShellScript

# List parameters
aws ssm describe-parameters

# Get patch compliance summary
aws ssm describe-patch-groups

# List associations
aws ssm list-associations

# Check automation executions
aws ssm describe-automation-executions
```

---

*Last Updated: 2026-02-04*
*Based on AWS Systems Manager Documentation*
