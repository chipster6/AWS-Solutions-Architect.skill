# AWS Security Services Implementation Supplement

**Index:** [GOV-ARCH-001](GOV-ARCH-001-Architecture-Documentation-Index.md) | [CROSS_REFERENCE_INDEX.md](CROSS_REFERENCE_INDEX.md)  
**Related:** [AWS Comprehensive Guide](AWS_Solutions_Architect_Comprehensive_Guide.md) Section 7 (Security Architecture)  
**Related Supplements:** [AWS Config](aws_config_supplement.md) (compliance) | [Systems Manager](systems_manager_supplement.md) (remediation)  
**Domain:** Multi-Account Governance (26%) | Continuous Improvement (25%)

## Table of Contents
1. [Overview](#1-overview)
2. [Amazon GuardDuty](#2-amazon-guardduty)
3. [AWS Security Hub](#3-aws-security-hub)
4. [Amazon Macie](#4-amazon-macie)
5. [Amazon Inspector](#5-amazon-inspector)
6. [IAM Access Analyzer](#6-iam-access-analyzer)
7. [Integration Architecture](#7-integration-architecture)
8. [Cost Optimization](#8-cost-optimization)
9. [Best Practices](#9-best-practices)

### Related Documentation
- **[Well-Architected Pillars](files/well-architected-pillars.md)** - Security pillar
- **[Compliance Framework](files/compliance-framework.md)** - Security compliance requirements
- **[AWS Config Supplement](aws_config_supplement.md)** - Compliance monitoring integration
- **[Cross-Reference Index](CROSS_REFERENCE_INDEX.md)** - Navigate by security service and threat type

---

## 1. Overview

AWS security services provide comprehensive threat detection, vulnerability management, data protection, and compliance monitoring across your AWS environment. These services work together to provide a defense-in-depth security posture.

### Security Services Overview

| Service | Purpose | Key Capabilities |
|---------|---------|------------------|
| **GuardDuty** | Threat detection | ML-based threat detection, multi-account support |
| **Security Hub** | Centralized security posture | Findings aggregation, compliance standards |
| **Macie** | Data protection | S3 data discovery, sensitive data detection |
| **Inspector** | Vulnerability management | EC2/ECR/Lambda scanning, continuous assessment |
| **Access Analyzer** | Access validation | External access detection, zone of trust |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AWS Security Hub (Central)                    │
├─────────────────────────────────────────────────────────────────┤
│  GuardDuty  │    Macie    │  Inspector  │  Config  │  Access    │
│   Findings  │   Findings  │  Findings   │  Findings │  Analyzer  │
├─────────────────────────────────────────────────────────────────┤
│                    EventBridge (Automated Response)              │
├─────────────────────────────────────────────────────────────────┤
│  SNS Notifications  │  Lambda Remediation  │  Ticketing System  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Amazon GuardDuty

### 2.1 Overview

Amazon GuardDuty is a threat detection service that continuously monitors AWS data sources and logs using machine learning, anomaly detection, and threat intelligence feeds to identify suspicious and potentially malicious activity.

**Key Benefits:**
- Continuous threat detection without user configuration
- Multi-account support via Organizations
- Integration with Security Hub and EventBridge
- Protection plans for specialized workloads

### 2.2 Data Sources

GuardDuty analyzes multiple data sources:

| Data Source | Coverage | Enablement |
|-------------|----------|------------|
| **CloudTrail Management Events** | All AWS API calls | Automatic |
| **VPC Flow Logs** | Network traffic analysis | Automatic |
| **DNS Query Logs** | DNS request monitoring | Automatic |
| **EKS Audit Logs** | Kubernetes API activity | Enable EKS Protection |
| **S3 Data Events** | S3 object operations | Enable S3 Protection |
| **EBS Volumes** | Malware scanning | Enable Malware Protection |
| **RDS Login Activity** | Database access monitoring | Enable RDS Protection |
| **Lambda Network Logs** | Function network activity | Enable Lambda Protection |

### 2.3 Protection Plans

**Core Protection (Always Enabled):**
- CloudTrail management events
- VPC Flow Logs
- DNS query logs

**Extended Protection (Optional):**

| Protection Plan | Detects | Cost |
|----------------|---------|------|
| **S3 Protection** | Data exfiltration, unusual access patterns | Per S3 data event |
| **EKS Protection** | Suspicious K8s API activity, crypto-mining | Per EKS audit log |
| **Malware Protection (EC2)** | Malware in EBS volumes | Per GB scanned |
| **Malware Protection (S3)** | Malware in S3 objects | Per object scanned |
| **RDS Protection** | Anomalous DB login activity | Per DB instance |
| **Lambda Protection** | Crypto-mining, malicious communication | Per function |
| **Runtime Monitoring** | OS-level threats on EKS/ECS/EC2 | Per resource-hour |

### 2.4 Setting Up GuardDuty

**Console Setup:**
1. Navigate to GuardDuty console
2. Click "Get Started"
3. Enable GuardDuty
4. Configure protection plans
5. Set up member accounts (for Organizations)

**CLI Setup:**
```bash
# Enable GuardDuty
DETECTOR_ID=$(aws guardduty create-detector --enable --query 'DetectorId' --output text)

# Get detector ID
aws guardduty list-detectors

# Enable S3 Protection
aws guardduty update-detector \
  --detector-id $DETECTOR_ID \
  --finding-publishing-frequency FIFTEEN_MINUTES \
  --data-sources S3Logs={Enable=true}

# Enable EKS Protection
aws guardduty update-detector \
  --detector-id $DETECTOR_ID \
  --data-sources Kubernetes={AuditLogs={Enable=true}}

# Enable Malware Protection for EC2
aws guardduty update-malware-scan-settings \
  --detector-id $DETECTOR_ID \
  --ebs-malware-protection Enable=true
```

### 2.5 Multi-Account Setup

**Architecture:**
- **Master Account**: Central management and findings aggregation
- **Member Accounts**: Report findings to master

**Setup via Organizations:**
```bash
# Designate master account (do this in security account)
aws guardduty create-detector --enable

# Enable GuardDuty for organization (as admin)
aws guardduty enable-organization-admin-account \
  --admin-account-id 123456789012

# Auto-enable for new member accounts
aws guardduty update-organization-configuration \
  --detector-id $DETECTOR_ID \
  --auto-enable-organization-members NEW

# Add existing member accounts
aws guardduty create-members \
  --detector-id $DETECTOR_ID \
  --account-details '[{"AccountId": "123456789013", "Email": "admin@account2.com"}]'
```

### 2.6 Finding Types

GuardDuty finding categories:

| Category | Severity | Examples |
|----------|----------|----------|
| **Backdoor** | High | Compromised EC2 instance, C&C communication |
| **Behavior** | Medium | Unusual API calls, unusual network traffic |
| **CryptoCurrency** | Medium | Crypto-mining activity |
| **DefenseEvasion** | High | CloudTrail tampering, policy changes |
| **Discovery** | Low | Reconnaissance activity |
| **Exfiltration** | High | Data exfiltration attempts |
| **Impact** | High | Resource destruction, ransomware |
| **InitialAccess** | High | Credential compromise, brute force |
| **Persistence** | High | New user creation, role modification |
| **Policy** | Low | AWS security policy violation |
| **PrivilegeEscalation** | High | IAM policy changes, role assumption |
| **Recon** | Low | Port scanning, resource enumeration |
| **Stealth** | Medium | CloudTrail deletion, log tampering |
| **Trojan** | High | Malware detection, backdoor communication |
| **UnauthorizedAccess** | Medium | Unusual access patterns |

### 2.7 Finding Response

**Automated Response via EventBridge:**
```json
{
  "source": ["aws.guardduty"],
  "detail-type": ["GuardDuty Finding"],
  "detail": {
    "severity": [{"numeric": [">", 7]}],
    "type": ["UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration"]
  }
}
```

**Lambda Response Function:**
```python
import boto3
import json

def lambda_handler(event, context):
    finding = event['detail']
    severity = finding['severity']
    finding_type = finding['type']
    
    # High severity findings - immediate action
    if severity >= 7:
        if 'InstanceCredentialExfiltration' in finding_type:
            # Revoke compromised credentials
            iam = boto3.client('iam')
            # Extract and revoke access key
            
        elif 'CryptoCurrency' in finding_type:
            # Isolate instance
            ec2 = boto3.client('ec2')
            # Modify security group to isolate
    
    # Send notification
    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:123456789012:security-alerts',
        Subject=f'GuardDuty Finding: {finding_type}',
        Message=json.dumps(finding, indent=2)
    )
```

### 2.8 Trusted IPs and Threat Lists

**Configure Trusted IPs (Suppress known good activity):**
```bash
# Upload trusted IP list to S3
aws s3 cp trusted-ips.txt s3://my-security-bucket/guardduty/

# Create trusted IP set
aws guardduty create-threat-intel-set \
  --detector-id $DETECTOR_ID \
  --name "Corporate-IPs" \
  --format TXT \
  --location s3://my-security-bucket/guardduty/trusted-ips.txt \
  --activate true

# Create threat intel set (malicious IPs)
aws guardduty create-threat-intel-set \
  --detector-id $DETECTOR_ID \
  --name "Known-Threats" \
  --format TXT \
  --location s3://my-security-bucket/guardduty/threats.txt \
  --activate true
```

### 2.9 Finding Suppression

Create suppression rules to hide expected findings:

```bash
# Suppress findings from known internal scanners
aws guardduty create-filter \
  --detector-id $DETECTOR_ID \
  --name "Internal-Scanning" \
  --action ARCHIVE \
  --rank 1 \
  --finding-criteria '{
    "Criterion": {
      "resource.instanceDetails.tags.key": {
        "Eq": ["Scanner"]
      },
      "type": {
        "Eq": ["Recon:EC2/Portscan"]
      }
    }
  }'
```

---

## 3. AWS Security Hub

### 3.1 Overview

AWS Security Hub provides a comprehensive view of your security state in AWS and helps you assess your AWS environment against security industry standards and best practices.

**Key Benefits:**
- Centralized findings aggregation
- Compliance standards monitoring
- Automated security checks
- Cross-account visibility

### 3.2 Security Standards

Security Hub supports multiple compliance frameworks:

| Standard | Controls | Description |
|----------|----------|-------------|
| **AWS Foundational Security Best Practices** | 200+ | AWS security best practices |
| **CIS AWS Foundations Benchmark** | 50+ | CIS benchmark for AWS |
| **PCI DSS** | 40+ | Payment card industry requirements |
| **NIST SP 800-53** | 100+ | Federal security controls |
| **AFSBP** | 50+ | AWS Foundational Security Best Practices |

### 3.3 Setting Up Security Hub

**Console Setup:**
1. Navigate to Security Hub console
2. Click "Enable Security Hub"
3. Select security standards to enable
4. Configure integrations

**CLI Setup:**
```bash
# Enable Security Hub
aws securityhub enable-security-hub

# Enable AWS Foundational Security Best Practices standard
aws securityhub enable-security-standard \
  --standards-arn arn:aws:securityhub:us-east-1::standards/aws-foundational-security-best-practices/v/1.0.0

# Enable CIS AWS Foundations Benchmark
aws securityhub enable-security-standard \
  --standards-arn arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0

# Check enabled standards
aws securityhub get-enabled-standards
```

### 3.4 Multi-Account Setup

**Architecture:**
- **Administrator Account**: Central management
- **Member Accounts**: Send findings to administrator

**Setup via Organizations:**
```bash
# Designate administrator account (in security account)
aws securityhub enable-organization-admin-account \
  --admin-account-id 123456789012

# Auto-enable Security Hub for organization members
aws securityhub update-organization-configuration \
  --auto-enable-standards "aws-foundational-security-best-practices/v/1.0.0" \
  --auto-enable-default-standards true

# Add existing members
aws securityhub create-members \
  --account-details '[{"AccountId": "123456789013", "Email": "admin@account2.com"}]'
```

### 3.5 Findings Aggregation

**Finding Providers:**
Security Hub aggregates findings from:
- Amazon GuardDuty
- Amazon Inspector
- Amazon Macie
- AWS Config
- AWS Firewall Manager
- AWS IAM Access Analyzer
- AWS Systems Manager Patch Manager
- Partner integrations (50+)

**Finding Format:**
All findings use AWS Security Finding Format (ASFF):
```json
{
  "SchemaVersion": "2018-10-08",
  "Id": "arn:aws:guardduty:us-east-1:123456789012:detector/abc123/finding/def456",
  "ProductArn": "arn:aws:securityhub:us-east-1::product/aws/guardduty",
  "GeneratorId": "arn:aws:guardduty:us-east-1:123456789012:detector/abc123",
  "AwsAccountId": "123456789012",
  "Types": ["TTPs/Initial Access/UnauthorizedAccess:IAMUser-InstanceCredentialExfiltration"],
  "FirstObservedAt": "2025-01-15T10:00:00Z",
  "LastObservedAt": "2025-01-15T10:00:00Z",
  "CreatedAt": "2025-01-15T10:00:00Z",
  "UpdatedAt": "2025-01-15T10:05:00Z",
  "Severity": {
    "Product": 8,
    "Label": "HIGH",
    "Normalized": 80
  },
  "Title": "UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration",
  "Description": "EC2 instance is making API calls using credentials from a different EC2 instance",
  "Resources": [{
    "Type": "AwsEc2Instance",
    "Id": "arn:aws:ec2:us-east-1:123456789012:instance/i-0123456789abcdef0"
  }]
}
```

### 3.6 Automation Rules

Create rules to automatically update findings:

```bash
# Create automation rule to suppress findings from test environment
aws securityhub create-automation-rule \
  --rule-name "Suppress-Test-Environment" \
  --rule-order 1 \
  --rule-status ENABLED \
  --criteria '{
    "AwsAccountId": [{"Value": "123456789012", "Comparison": "EQUALS"}],
    "ResourceTags": [{"Key": "Environment", "Value": "Test", "Comparison": "EQUALS"}]
  }' \
  --actions '[{"Type": "FINDING_FIELDS_UPDATE", "FindingFieldsUpdate": {"Workflow": {"Status": "SUPPRESSED"}, "Severity": {"Label": "INFORMATIONAL"}}}]'
```

### 3.7 Insights

Create custom insights for security monitoring:

```bash
# Create insight for high severity findings
aws securityhub create-insight \
  --name "High-Severity-Findings" \
  --filters '{
    "SeverityLabel": [{"Value": "HIGH", "Comparison": "EQUALS"}],
    "WorkflowStatus": [{"Value": "NEW", "Comparison": "EQUALS"}]
  }' \
  --group-by-attribute ProductName

# Create insight for findings by resource
aws securityhub create-insight \
  --name "Findings-by-Resource" \
  --filters '{}' \
  --group-by-attribute ResourceId
```

### 3.8 Cross-Region Aggregation

Aggregate findings from multiple regions:

```bash
# In each region, set the aggregation region
aws securityhub create-finding-aggregator \
  --region-linking-mode ALL_REGIONS \
  --regions ["us-east-1", "us-west-2", "eu-west-1"]
```

---

## 4. Amazon Macie

### 4.1 Overview

Amazon Macie is a data security service that uses machine learning and pattern matching to discover and protect sensitive data in Amazon S3.

**Key Benefits:**
- Automated sensitive data discovery
- S3 bucket security assessment
- PII and financial data detection
- Integration with Security Hub

### 4.2 Features

**Automated Data Discovery:**
- Continuous S3 bucket inventory
- Automatic sampling and analysis
- ML-based sensitive data detection

**Sensitive Data Discovery Jobs:**
- Deep analysis of S3 objects
- Custom detection criteria
- Scheduled or on-demand execution

**S3 Bucket Assessment:**
- Public access detection
- Encryption status monitoring
- Access control evaluation

### 4.3 Setting Up Macie

**Console Setup:**
1. Navigate to Macie console
2. Click "Get Started"
3. Enable Macie
4. Configure automated discovery
5. Set up classification jobs (optional)

**CLI Setup:**
```bash
# Enable Macie
aws macie2 enable-macie

# Enable automated sensitive data discovery
aws macie2 put-classification-export-configuration \
  --configuration '{"s3Destination": {"bucketName": "my-macie-findings", "keyPrefix": "findings/", "kmsKeyArn": "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012"}}'

# Enable automated discovery
aws macie2 update-macie-session \
  --finding-publishing-frequency FIFTEEN_MINUTES \
  --status ENABLED
```

### 4.4 Managed Data Identifiers

Macie includes built-in identifiers for:

| Category | Examples |
|----------|----------|
| **Financial** | Credit card numbers, bank account numbers |
| **Personal** | Names, addresses, phone numbers |
| **Credentials** | AWS secret keys, private keys, passwords |
| **Medical** | Health insurance numbers (US) |
| **Government IDs** | SSNs, passport numbers, driver's licenses |

**Region-Specific Identifiers:**
- US: SSN, US passport, US driver's license
- EU: VAT numbers, national IDs
- UK: NHS numbers, NI numbers

### 4.5 Custom Data Identifiers

Create custom regex patterns:

```bash
# Create custom data identifier for employee IDs
aws macie2 create-custom-data-identifier \
  --name "Employee-ID" \
  --regex "EMP[0-9]{6}" \
  --description "Company employee ID format" \
  --maximum-match-distance 50

# Create custom identifier for project codes
aws macie2 create-custom-data-identifier \
  --name "Project-Code" \
  --regex "PRJ-[A-Z]{3}-[0-9]{4}" \
  --description "Internal project code format"
```

### 4.6 Sensitive Data Discovery Jobs

**Create One-Time Job:**
```bash
aws macie2 create-classification-job \
  --job-type ONE_TIME \
  --name "Production-S3-Scan" \
  --s3-job-definition '{
    "bucketDefinitions": [
      {
        "accountId": "123456789012",
        "buckets": ["production-data-bucket", "customer-uploads-bucket"]
      }
    ],
    "scoping": {
      "includes": {
        "and": [
          {"simpleScopeTerm": {"comparator": "EQ", "key": "OBJECT_EXTENSION", "values": ["csv", "json", "parquet"]}}
        ]
      }
    }
  }' \
  --managed-data-identifier-selector '{
    "simpleScopeTerm": {"comparator": "EQ", "key": "MANAGED_DATA_IDENTIFIER_TYPE", "values": ["CREDENTIALS", "FINANCIAL_INFORMATION"]}
  }'
```

**Create Scheduled Job:**
```bash
aws macie2 create-classification-job \
  --job-type SCHEDULED \
  --name "Weekly-S3-Scan" \
  --schedule-frequency '{"weeklySchedule": {"dayOfWeek": "SUNDAY"}}' \
  --s3-job-definition '{...}'
```

### 4.7 Allow Lists

Suppress expected data patterns:

```bash
# Create allow list for test data
aws macie2 create-allow-list \
  --name "Test-Data-Patterns" \
  --criteria '{"regex": "TEST-[0-9]{4}-SAMPLE"}' \
  --description "Sample data used for testing"

# Create S3-based allow list
aws macie2 create-allow-list \
  --name "Known-Good-SSNs" \
  --criteria '{"s3WordsList": {"bucketName": "macie-allow-lists", "objectKey": "known-good-ssns.txt"}}'
```

### 4.8 Finding Types

**Policy Findings (Bucket Security):**
- S3 bucket public
- S3 bucket unencrypted
- S3 bucket versioning disabled
- S3 bucket MFA delete disabled

**Sensitive Data Findings:**
- Sensitive data found in object
- Specific data type detected
- Multiple sensitive data types

---

## 5. Amazon Inspector

### 5.1 Overview

Amazon Inspector is an automated vulnerability management service that continually scans AWS workloads for software vulnerabilities and unintended network exposure.

**Key Benefits:**
- Automatic resource discovery
- Continuous vulnerability scanning
- Risk-based findings prioritization
- Integration with Security Hub

### 5.2 Supported Resources

| Resource | Scan Type | Coverage |
|----------|-----------|----------|
| **EC2 Instances** | OS package vulnerabilities, network exposure | Continuous |
| **ECR Container Images** | Package vulnerabilities | On push and continuous |
| **Lambda Functions** | Code and dependency vulnerabilities | Continuous |

### 5.3 Setting Up Inspector

**Console Setup:**
1. Navigate to Inspector console
2. Click "Get Started"
3. Enable Inspector
4. Configure scan settings
5. Set up member accounts (for Organizations)

**CLI Setup:**
```bash
# Enable Inspector
aws inspector2 enable

# Enable for EC2
aws inspector2 enable-scanning \
  --scan-types EC2

# Enable for ECR
aws inspector2 enable-scanning \
  --scan-types ECR

# Enable for Lambda
aws inspector2 enable-scanning \
  --scan-types LAMBDA

# Enable all resource types
aws inspector2 enable-scanning \
  --scan-types EC2 ECR LAMBDA
```

### 5.4 Multi-Account Setup

**Setup via Organizations:**
```bash
# Designate delegated administrator
aws inspector2 enable-delegated-admin \
  --delegated-admin-account-id 123456789012

# Associate member accounts
aws inspector2 associate-member \
  --account-id 123456789013

# Enable auto-activation for organization
aws inspector2 update-organization-configuration \
  --auto-enable-ec2 true \
  --auto-enable-ecr true \
  --auto-enable-lambda true
```

### 5.5 Finding Severity

Inspector uses CVSS v3.1 scoring with environmental context:

| Severity | Score | Action |
|----------|-------|--------|
| **Critical** | 9.0-10.0 | Immediate remediation |
| **High** | 7.0-8.9 | Remediate within 24 hours |
| **Medium** | 4.0-6.9 | Remediate within 7 days |
| **Low** | 0.1-3.9 | Remediate within 30 days |
| **Informational** | 0.0 | Track for awareness |

### 5.6 ECR Scanning

**Enable for Repository:**
```bash
# Enable enhanced scanning for ECR repository
aws ecr put-registry-scanning-configuration \
  --scan-type ENHANCED \
  --rules '[{"scanFrequency": "SCAN_ON_PUSH", "repositoryFilters": [{"filter": "*", "filterType": "WILDCARD"}]}]'

# Or enable for specific repository
aws ecr put-image-scanning-configuration \
  --repository-name my-app \
  --image-scanning-configuration scanOnPush=true
```

### 5.7 Finding Response

**Automated Response Example:**
```python
import boto3

def lambda_handler(event, context):
    finding = event['detail']
    severity = finding['severity']
    
    # Critical findings - immediate action
    if severity >= 9.0:
        instance_id = finding['resources'][0]['id']
        
        # Isolate instance
        ec2 = boto3.client('ec2')
        ec2.modify_instance_attribute(
            InstanceId=instance_id,
            Groups=['sg-isolated']  # Isolated security group
        )
        
        # Send urgent notification
        sns = boto3.client('sns')
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:123456789012:critical-security-alerts',
            Subject=f'CRITICAL: Inspector Finding - {finding["title"]}',
            Message=str(finding)
        )
```

### 5.8 Suppression Rules

Suppress known/accepted findings:

```bash
# Create suppression rule for development instances
aws inspector2 create-filter \
  --name "Dev-Instance-Vulnerabilities" \
  --action SUPPRESS \
  --criteria '{
    "resourceTags": [{"comparison": "EQUALS", "key": "Environment", "value": "Development"}],
    "severity": [{"comparison": "EQUALS", "value": "LOW"}]
  }'
```

---

## 6. IAM Access Analyzer

### 6.1 Overview

IAM Access Analyzer helps identify resources in your organization and accounts that are shared with external entities.

**Key Benefits:**
- External access detection
- Least privilege analysis
- Zone of trust configuration
- Finding archival

### 6.2 Setting Up Access Analyzer

**Console Setup:**
1. Navigate to IAM → Access Analyzer
2. Click "Create analyzer"
3. Choose zone of trust
4. Enable

**CLI Setup:**
```bash
# Create analyzer for account
aws accessanalyzer create-analyzer \
  --analyzer-name AccountAnalyzer \
  --type ACCOUNT \
  --tags Key=Environment,Value=Production

# Create analyzer for organization
aws accessanalyzer create-analyzer \
  --analyzer-name OrganizationAnalyzer \
  --type ORGANIZATION \
  --tags Key=Scope,Value=Organization

# List analyzers
aws accessanalyzer list-analyzers
```

### 6.3 Zone of Trust

**Account Zone:**
- Trust boundary = single AWS account
- External sharing = different account

**Organization Zone:**
- Trust boundary = entire AWS Organization
- External sharing = outside organization

### 6.4 Finding Types

| Resource Type | Example Finding |
|---------------|----------------|
| **S3 Bucket** | Bucket policy allows access from external account |
| **IAM Role** | Trust policy allows external account assumption |
| **KMS Key** | Key policy allows external account usage |
| **Lambda Function** | Resource policy allows external invocation |
| **SQS Queue** | Queue policy allows external account access |
| **Secrets Manager** | Secret policy allows external access |

### 6.5 Archive Rules

Automatically archive expected findings:

```bash
# Create archive rule for known external access
aws accessanalyzer create-archive-rule \
  --analyzer-name AccountAnalyzer \
  --rule-name "Trusted-Vendor-Access" \
  --rule '{
    "resources": ["arn:aws:s3:::vendor-data-bucket/*"],
    "principals": ["arn:aws:iam::999999999999:root"]
  }'

# Archive rule for CloudTrail logs
aws accessanalyzer create-archive-rule \
  --analyzer-name AccountAnalyzer \
  --rule-name "CloudTrail-External" \
  --rule '{
    "resources": ["arn:aws:s3:::cloudtrail-logs-*/*"],
    "actions": ["s3:GetObject"]
  }'
```

### 6.6 Policy Validation

Validate IAM policies before deployment:

```bash
# Validate policy
aws accessanalyzer validate-policy \
  --policy-document file://iam-policy.json \
  --policy-type IDENTITY_POLICY \
  --locale EN_US

# Check for external access in policy
aws accessanalyzer check-access-not-granted \
  --policy-document file://iam-policy.json \
  --access ["s3:GetObject", "s3:PutObject"] \
  --resource-type AWS::S3::Bucket
```

---

## 7. Integration Architecture

### 7.1 Central Security Account Pattern

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│                   Central Security Account                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   GuardDuty  │  │ Security Hub │  │ Access Analyzer  │  │
│  │   (Master)   │  │ (Aggregator) │  │  (Organization)  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
┌────────▼──────┐    ┌────────▼──────┐    ┌───────▼───────┐
│  Account A    │    │  Account B    │    │  Account C    │
│  (Member)     │    │  (Member)     │    │  (Member)     │
└───────────────┘    └───────────────┘    └───────────────┘
```

**Implementation:**
1. Create dedicated security account
2. Enable all services in security account
3. Designate as administrator/aggregator
4. Invite/associate member accounts
5. Configure cross-account IAM roles
6. Set up EventBridge for automated response

### 7.2 EventBridge Integration

**Central Event Bus Pattern:**
```bash
# In member accounts - forward findings to security account
aws events put-rule \
  --name Forward-Security-Findings \
  --event-pattern '{
    "source": ["aws.guardduty", "aws.securityhub", "aws.macie", "aws.inspector"]
  }'

aws events put-targets \
  --rule Forward-Security-Findings \
  --targets '[{
    "Id": "1",
    "Arn": "arn:aws:events:us-east-1:123456789012:event-bus/security-hub",
    "RoleArn": "arn:aws:iam::123456789013:role/EventBridgeCrossAccountRole"
  }]'
```

### 7.3 Automated Response Pipeline

**Event Flow:**
```
Finding Detected → EventBridge → Lambda → Remediation Action
                       ↓
                  SNS → Slack/Email
                       ↓
                  SQS → Ticketing System
```

**Sample Lambda Function:**
```python
import boto3
import json
import os

def lambda_handler(event, context):
    finding = event['detail']
    service = event['source'].split('.')[1]
    severity = finding.get('severity', {}).get('label', 'INFORMATIONAL')
    
    # Route based on severity
    if severity in ['CRITICAL', 'HIGH']:
        # Immediate response
        handle_critical_finding(finding, service)
    elif severity == 'MEDIUM':
        # Alert security team
        notify_security_team(finding)
    else:
        # Log for review
        log_finding(finding)
    
    # Always update Security Hub
    update_security_hub(finding)
    
    return {'statusCode': 200}

def handle_critical_finding(finding, service):
    # Take automated action based on service and finding type
    if service == 'guardduty' and 'CryptoCurrency' in finding.get('type', ''):
        # Isolate EC2 instance
        isolate_instance(finding['resources'][0]['id'])
    elif service == 'inspector' and finding.get('severity', 0) >= 9.0:
        # Quarantine container image
        quarantine_image(finding['resources'][0]['id'])

def notify_security_team(finding):
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=os.environ['SECURITY_ALERTS_TOPIC'],
        Subject=f"Security Finding: {finding.get('title', 'Unknown')}",
        Message=json.dumps(finding, indent=2)
    )
```

---

## 8. Cost Optimization

### 8.1 GuardDuty Costs

| Component | Pricing | Optimization |
|-----------|---------|--------------|
| **CloudTrail analysis** | Free | N/A |
| **VPC Flow Logs** | Free | N/A |
| **DNS logs** | Free | N/A |
| **S3 data events** | $0.0035 per 10,000 events | Limit S3 data event logging |
| **EKS audit logs** | $0.70 per EKS cluster/month | Only enable where needed |
| **Malware Protection (EC2)** | $0.03 per GB scanned | Exclude test/dev instances |
| **Malware Protection (S3)** | $0.03 per object scanned | Limit to production buckets |

**Cost Estimation Example:**
- 10 EC2 instances with Malware Protection: ~$50-100/month
- 100,000 S3 data events/day: ~$10/month
- 5 EKS clusters: ~$3.50/month

### 8.2 Security Hub Costs

| Component | Pricing | Optimization |
|-----------|---------|--------------|
| **Security checks** | $0.0010 per check | Disable unused standards |
| **Finding ingestion** | First 10,000 free, then $0.03 per 1,000 | Archive old findings |
| **Cross-region aggregation** | Standard data transfer rates | Limit to necessary regions |

**Cost Estimation Example:**
- AWS Foundational Security Best Practices (200 checks/day): ~$6/month
- CIS Benchmark (50 checks/day): ~$1.50/month

### 8.3 Macie Costs

| Component | Pricing | Optimization |
|-----------|---------|--------------|
| **Automated discovery** | $0.10 per S3 bucket/month | Focus on sensitive buckets |
| **Data classification** | $1.00 per GB processed | Use sampling, exclude test data |

**Cost Estimation Example:**
- 50 S3 buckets: $5/month base
- 100 GB processed: $100/month

### 8.4 Inspector Costs

| Component | Pricing | Optimization |
|-----------|---------|--------------|
| **EC2 scanning** | $0.03 per EC2 instance/hour | Scan production only |
| **ECR scanning** | $0.03 per image scanned | Use lifecycle policies |
| **Lambda scanning** | $0.03 per function/month | Scan production functions |

**Cost Estimation Example:**
- 20 production EC2 instances (730 hours): ~$438/month
- 100 container images scanned: ~$3/month
- 50 Lambda functions: ~$1.50/month

### 8.5 Cost Optimization Strategies

1. **Staged Rollout**
   - Start with critical production accounts
   - Expand gradually based on findings value

2. **Selective Protection Plans**
   - Only enable protection plans where needed
   - Disable in dev/test environments

3. **Filter Noise**
   - Create suppression rules for expected findings
   - Reduce false positive volume

4. **Consolidate Findings**
   - Use Security Hub aggregation
   - Avoid redundant monitoring

5. **Lifecycle Management**
   - Archive old findings
   - Set retention policies

---

## 9. Best Practices

### 9.1 Enable in Phases

**Phase 1: Foundation (Week 1)**
- Enable GuardDuty in security account
- Enable Security Hub with AWS Foundational standard
- Configure basic alerting

**Phase 2: Coverage (Week 2-3)**
- Roll out GuardDuty to all accounts
- Enable Macie for S3 buckets
- Configure cross-account aggregation

**Phase 3: Advanced (Week 4+)**
- Enable Inspector for EC2/ECR/Lambda
- Implement automated remediation
- Fine-tune suppression rules

### 9.2 Multi-Account Strategy

```
Organization Structure:
├── Management Account
│   └── Security Hub Administrator
├── Security Account (Dedicated)
│   ├── GuardDuty Master
│   ├── Security Hub Aggregator
│   ├── Macie Administrator
│   ├── Inspector Delegated Admin
│   └── Access Analyzer Organization
├── Production OU
│   ├── Account A (Member)
│   ├── Account B (Member)
│   └── Account C (Member)
├── Development OU
│   ├── Dev Account (Member)
│   └── Staging Account (Member)
└── Sandbox OU
    └── Sandbox Account (Member - limited monitoring)
```

### 9.3 Alerting Priority

| Priority | Services | Response Time |
|----------|----------|---------------|
| **P1 - Critical** | GuardDuty (High/Critical), Inspector (Critical) | Immediate |
| **P2 - High** | GuardDuty (Medium), Security Hub (Failed controls) | 1 hour |
| **P3 - Medium** | Macie (Sensitive data), Config (Non-compliant) | 4 hours |
| **P4 - Low** | Inspector (Low), Access Analyzer | 24 hours |

### 9.4 Finding Response Playbooks

**GuardDuty Playbook Example:**
```yaml
Finding: UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration
Severity: High

Response:
  1. Verify finding details
  2. Identify compromised credentials
  3. Revoke access keys immediately
  4. Rotate affected credentials
  5. Investigate instance for compromise
  6. Review CloudTrail for unauthorized API calls
  7. Document incident
  8. Update detection rules if false positive
```

### 9.5 Compliance Mapping

| Compliance Framework | Security Hub Standard | Additional Services |
|---------------------|----------------------|---------------------|
| **PCI DSS** | PCI DSS standard | GuardDuty + Macie |
| **SOC 2** | AWS Foundational | All services |
| **HIPAA** | AWS Foundational + CIS | GuardDuty + Macie + Inspector |
| **FedRAMP** | NIST SP 800-53 | All services |
| **ISO 27001** | AWS Foundational | GuardDuty + Inspector |

### 9.6 Common Integration Patterns

**SIEM Integration:**
- Forward findings to Splunk, Datadog, or ELK
- Use Kinesis Firehose for streaming

**Ticketing Integration:**
- Create Jira/ServiceNow tickets from findings
- Use Lambda for API integration

**ChatOps:**
- Send alerts to Slack/Teams
- Include remediation buttons

**SOAR Integration:**
- Integrate with Palo Alto XSOAR, Splunk SOAR
- Automated playbook triggering

---

## Quick Reference

```bash
# GuardDuty
aws guardduty list-detectors
aws guardduty list-findings --detector-id <id>
aws guardduty get-findings --detector-id <id> --finding-ids <id>

# Security Hub
aws securityhub get-findings
aws securityhub get-compliance-summary
aws securityhub enable-security-standard --standards-arn <arn>

# Macie
aws macie2 list-classification-jobs
aws macie2 list-findings
aws macie2 get-findings --finding-ids <id>

# Inspector
aws inspector2 list-findings
aws inspector2 list-coverage
aws inspector2 create-filter

# Access Analyzer
aws accessanalyzer list-analyzers
aws accessanalyzer list-findings --analyzer-arn <arn>
aws accessanalyzer validate-policy --policy-document <doc>
```

---

*Last Updated: 2026-02-04*
*Based on AWS Security Services Documentation*
