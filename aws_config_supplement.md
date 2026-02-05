# AWS Config Implementation Supplement

**Index:** [GOV-ARCH-001](GOV-ARCH-001-Architecture-Documentation-Index.md) | [CROSS_REFERENCE_INDEX.md](CROSS_REFERENCE_INDEX.md)  
**Related:** [AWS Comprehensive Guide](AWS_Solutions_Architect_Comprehensive_Guide.md) Section 7 (Security)  
**Related Supplements:** [Systems Manager](systems_manager_supplement.md) (remediation) | [Security](security_services_supplement.md) (findings)  
**Domain:** Continuous Improvement (25%) | Multi-Account Governance (26%)

## Table of Contents
1. [Overview](#1-overview)
2. [Configuration Recorder Setup](#2-configuration-recorder-setup)
3. [Config Rules](#3-config-rules)
4. [Remediation Actions](#4-remediation-actions)
5. [Compliance Monitoring](#5-compliance-mpliance-monitoring)
6. [Advanced Features](#6-advanced-features)
7. [Integration Patterns](#7-integration-patterns)
8. [Cost Optimization](#8-cost-optimization)
9. [Troubleshooting](#9-troubleshooting)

### Related Documentation
- **[Compliance Framework](files/compliance-framework.md)** - Regulatory compliance mapping
- **[Well-Architected Pillars](files/well-architected-pillars.md)** - Security pillar
- **[Systems Manager Supplement](systems_manager_supplement.md)** - Automated remediation
- **[Cross-Reference Index](CROSS_REFERENCE_INDEX.md)** - Navigate by rule and resource type

---

## 1. Overview

AWS Config provides a detailed view of the configuration of AWS resources in your AWS account, including how resources are related to one another and how configurations change over time.

**Key Capabilities:**
- Configuration history tracking
- Compliance evaluation with rules
- Automated remediation
- Multi-account aggregation
- Change notifications
- Relationship mapping

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS Config Service                       │
├─────────────────────────────────────────────────────────────┤
│  Configuration Recorder  │  Config Rules  │  Remediation    │
├─────────────────────────────────────────────────────────────┤
│           S3 Bucket (Configuration History)                 │
├─────────────────────────────────────────────────────────────┤
│  SNS Topic (Notifications) │ CloudWatch Events/EventBridge  │
└─────────────────────────────────────────────────────────────┘
```

### Use Cases

| Use Case | Description |
|----------|-------------|
| **Compliance Monitoring** | Continuous evaluation against standards |
| **Security Analysis** | Track security group changes, IAM policies |
| **Change Management** | Audit who changed what and when |
| **Troubleshooting** | View last known good configuration |
| **Cost Optimization** | Identify unused or misconfigured resources |

---

## 2. Configuration Recorder Setup

### 2.1 Prerequisites

Before setting up AWS Config:
- S3 bucket for configuration history
- SNS topic (optional, for notifications)
- IAM role with appropriate permissions

### 2.2 Setting Up Configuration Recorder

**AWS Console:**
1. Navigate to AWS Config → Settings
2. Choose resource types to record:
   - All resources in this region
   - Specific resource types
3. Configure S3 bucket
4. Configure SNS topic (optional)
5. Set IAM role
6. Start recorder

**CLI Setup:**
```bash
# Create S3 bucket for Config
aws s3 mb s3://my-config-bucket-123456789 --region us-east-1

# Set bucket policy for Config access
aws s3api put-bucket-policy \
  --bucket my-config-bucket-123456789 \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "AWSConfigBucketPermissionsCheck",
        "Effect": "Allow",
        "Principal": {
          "Service": "config.amazonaws.com"
        },
        "Action": "s3:GetBucketAcl",
        "Resource": "arn:aws:s3:::my-config-bucket-123456789"
      },
      {
        "Sid": "AWSConfigBucketDelivery",
        "Effect": "Allow",
        "Principal": {
          "Service": "config.amazonaws.com"
        },
        "Action": "s3:PutObject",
        "Resource": "arn:aws:s3:::my-config-bucket-123456789/AWSLogs/123456789012/Config/*",
        "Condition": {
          "StringEquals": {
            "s3:x-amz-acl": "bucket-owner-full-control"
          }
        }
      }
    ]
  }'

# Create IAM role for Config
aws iam create-role \
  --role-name ConfigRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "config.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }'

# Attach AWS managed policy
aws iam attach-role-policy \
  --role-name ConfigRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWS_ConfigRole

# Create configuration recorder
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::123456789012:role/ConfigRole \
  --recording-group allSupported=true,includeGlobalResourceTypes=true

# Create delivery channel
aws configservice put-delivery-channel \
  --delivery-channel name=default,s3BucketName=my-config-bucket-123456789

# Start configuration recorder
aws configservice start-configuration-recorder \
  --configuration-recorder-name default
```

### 2.3 Recording Group Configuration

**Record All Resources:**
```bash
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::123456789012:role/ConfigRole \
  --recording-group allSupported=true,includeGlobalResourceTypes=true,recordAllResources=true
```

**Record Specific Resource Types:**
```bash
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::123456789012:role/ConfigRole \
  --recording-group resourceTypes=["AWS::EC2::Instance","AWS::EC2::SecurityGroup","AWS::S3::Bucket"]
```

**Exclude Specific Resources:**
```bash
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::123456789012:role/ConfigRole \
  --recording-group allSupported=true,exclusionByResourceTypes={resourceTypes=["AWS::EC2::Volume"]}
```

---

## 3. Config Rules

### 3.1 Types of Config Rules

| Type | Description | Example |
|------|-------------|---------|
| **Managed Rules** | AWS-provided rules | 200+ available |
| **Custom Lambda Rules** | Lambda-based evaluation | Custom business logic |
| **Custom Policy Rules** | CloudFormation Guard-based | Policy-as-code |
| **Service-Linked Rules** | Created by other services | Security Hub, etc. |

### 3.2 Managed Rules Library

**Common Managed Rules:**

| Rule | Purpose |
|------|---------|
| `s3-bucket-public-read-prohibited` | Detect public S3 buckets |
| `ec2-instance-managed-by-systems-manager` | Verify SSM agent active |
| `iam-password-policy` | Check password requirements |
| `rds-storage-encrypted` | Verify RDS encryption |
| `required-tags` | Enforce tagging standards |
| `vpc-default-security-group-closed` | Check default SG rules |

### 3.3 Creating Config Rules

**Console Steps:**
1. Navigate to AWS Config → Rules
2. Click "Add rule"
3. Search and select rule type
4. Configure rule parameters
5. Set evaluation mode (configuration changes or periodic)
6. Add to conformance pack (optional)
7. Save

**CLI - Managed Rule:**
```bash
# Create S3 public access rule
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "s3-bucket-public-read-prohibited",
    "Description": "Checks that S3 buckets do not allow public read access",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "S3_BUCKET_PUBLIC_READ_PROHIBITED"
    },
    "ConfigRuleState": "ACTIVE"
  }'

# Create EC2 managed by Systems Manager rule
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "ec2-instance-managed-by-systems-manager",
    "Description": "Checks whether EC2 instances are managed by AWS Systems Manager",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "EC2_INSTANCE_MANAGED_BY_SSM"
    },
    "ConfigRuleState": "ACTIVE"
  }'
```

**CLI - Custom Lambda Rule:**
```bash
# First, create the Lambda function for rule evaluation
# Then create the config rule
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "custom-ec2-tag-enforcement",
    "Description": "Custom rule to enforce required tags on EC2 instances",
    "InputParameters": "{\"requiredTags\":\"Environment,Owner,Project\"}",
    "Source": {
      "Owner": "CUSTOM_LAMBDA",
      "SourceIdentifier": "arn:aws:lambda:us-east-1:123456789012:function:config-ec2-tag-check",
      "SourceDetails": [
        {
          "EventSource": "aws.config",
          "MessageType": "ConfigurationItemChangeNotification"
        }
      ]
    },
    "ConfigRuleState": "ACTIVE"
  }'

# Grant Config permission to invoke Lambda
aws lambda add-permission \
  --function-name config-ec2-tag-check \
  --statement-id ConfigPermission \
  --action lambda:InvokeFunction \
  --principal config.amazonaws.com
```

### 3.4 Rule Evaluation Modes

| Mode | Trigger | Use Case |
|------|---------|----------|
| **Configuration Changes** | When resource changes | Real-time compliance |
| **Periodic** | Scheduled interval (1-24 hours) | Cost optimization, comprehensive checks |
| **Both** | Change + periodic | High-security requirements |

**Setting Evaluation Mode:**
```bash
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "s3-bucket-public-write-prohibited",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "S3_BUCKET_PUBLIC_WRITE_PROHIBITED",
      "SourceDetails": [
        {
          "EventSource": "aws.config",
          "MessageType": "ConfigurationItemChangeNotification"
        },
        {
          "EventSource": "aws.config",
          "MessageType": "OversizedConfigurationItemChangeNotification"
        }
      ]
    },
    "MaximumExecutionFrequency": "TwentyFour_Hours",
    "ConfigRuleState": "ACTIVE"
  }'
```

### 3.5 Rule Parameters

Many rules accept parameters for customization:

```bash
# IAM password policy with custom parameters
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "custom-iam-password-policy",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "IAM_PASSWORD_POLICY"
    },
    "InputParameters": "{\"RequireUppercaseCharacters\":\"true\",\"RequireLowercaseCharacters\":\"true\",\"RequireSymbols\":\"true\",\"RequireNumbers\":\"true\",\"MinimumPasswordLength\":\"14\",\"PasswordReusePrevention\":\"24\",\"MaxPasswordAge\":\"90\"}",
    "ConfigRuleState": "ACTIVE"
  }'

# Required tags rule
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "required-tags-check",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "REQUIRED_TAGS"
    },
    "InputParameters": "{\"tag1Key\":\"Environment\",\"tag2Key\":\"Owner\",\"tag3Key\":\"Project\"}",
    "Scope": {
      "ComplianceResourceTypes": ["AWS::EC2::Instance", "AWS::S3::Bucket", "AWS::RDS::DBInstance"]
    },
    "ConfigRuleState": "ACTIVE"
  }'
```

### 3.6 CloudFormation Guard Custom Rules

Create rules using CloudFormation Guard policy-as-code language:

```ruby
# Example Guard rule: Require encryption on S3 buckets
rule s3_bucket_encryption_required {
    AWS::S3::Bucket {
        Properties {
            BucketEncryption.ServerSideEncryptionConfiguration exists
        }
    }
}

# Another rule: Require VPC flow logging
rule vpc_flow_logging_required {
    AWS::EC2::VPC {
        Properties {
            EnableDnsHostnames == true
        }
    }
}
```

**Deploying Guard Rule:**
```bash
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "s3-encryption-guard-rule",
    "Source": {
      "Owner": "CUSTOM_POLICY",
      "SourceIdentifier": "arn:aws:config:us-east-1:123456789012:config-rule/s3-encryption-guard",
      "SourceDetails": [
        {
          "EventSource": "aws.config",
          "MessageType": "ConfigurationItemChangeNotification"
        }
      ]
    },
    "ConfigRuleState": "ACTIVE"
  }'
```

---

## 4. Remediation Actions

### 4.1 Overview

AWS Config can automatically remediate noncompliant resources using Systems Manager Automation documents.

**Remediation Types:**
- **Manual Remediation**: User-triggered via console/CLI
- **Automatic Remediation**: Triggered automatically on noncompliance

### 4.2 Available Remediation Actions

AWS provides managed automation documents for common remediation scenarios:

| Automation Document | Purpose |
|---------------------|---------|
| `AWSConfigRemediation-DeleteUnusedSecurityGroup` | Remove unused security groups |
| `AWSConfigRemediation-EnableS3BucketDefaultEncryption` | Enable S3 encryption |
| `AWSConfigRemediation-RemoveVPCDefaultSecurityGroupRules` | Remove default SG rules |
| `AWSConfigRemediation-EnableEbsEncryptionByDefault` | Enable EBS encryption |
| `AWS-PatchInstance` | Run patch baseline |

### 4.3 Setting Up Auto-Remediation

**Console Steps:**
1. Navigate to AWS Config → Rules
2. Select a rule
3. Click "Manage remediation"
4. Choose remediation action
5. Configure parameters
6. Enable automatic remediation
7. Save

**CLI - Manual Remediation:**
```bash
# Create remediation configuration (manual)
aws configservice put-remediation-configurations \
  --remediation-configurations '[
    {
      "ConfigRuleName": "s3-bucket-public-read-prohibited",
      "TargetType": "SSM_DOCUMENT",
      "TargetId": "AWSConfigRemediation-ConfigureS3BucketPublicAccessBlock",
      "TargetVersion": "1",
      "Parameters": {
        "AutomationAssumeRole": {
          "StaticValue": {
            "Values": ["arn:aws:iam::123456789012:role/ConfigRemediationRole"]
          }
        },
        "BucketName": {
          "ResourceValue": {
            "Value": "RESOURCE_ID"
          }
        }
      },
      "Automatic": false
    }
  ]'
```

**CLI - Automatic Remediation:**
```bash
# Create remediation with automatic execution
aws configservice put-remediation-configurations \
  --remediation-configurations '[
    {
      "ConfigRuleName": "s3-bucket-public-read-prohibited",
      "TargetType": "SSM_DOCUMENT",
      "TargetId": "AWSConfigRemediation-ConfigureS3BucketPublicAccessBlock",
      "TargetVersion": "1",
      "Parameters": {
        "AutomationAssumeRole": {
          "StaticValue": {
            "Values": ["arn:aws:iam::123456789012:role/ConfigRemediationRole"]
          }
        },
        "BucketName": {
          "ResourceValue": {
            "Value": "RESOURCE_ID"
          }
        }
      },
      "Automatic": true,
      "MaximumAutomaticAttempts": 3,
      "RetryAttemptSeconds": 60
    }
  ]'
```

### 4.4 Remediation Parameters

**Parameter Types:**

| Type | Description | Example |
|------|-------------|---------|
| `ResourceValue` | Value from resource (RESOURCE_ID, RESOURCE_NAME) | BucketName from resource |
| `StaticValue` | Fixed value | Role ARN, Tag value |

**Parameter Mapping Examples:**
```json
{
  "Parameters": {
    "AutomationAssumeRole": {
      "StaticValue": {
        "Values": ["arn:aws:iam::123456789012:role/RemediationRole"]
      }
    },
    "ResourceId": {
      "ResourceValue": {
        "Value": "RESOURCE_ID"
      }
    },
    "Region": {
      "StaticValue": {
        "Values": ["us-east-1"]
      }
    }
  }
}
```

### 4.5 Creating Custom Remediation Documents

Create custom SSM Automation document for remediation:

```yaml
schemaVersion: '0.3'
description: Add required tags to non-compliant EC2 instance
assumeRole: '{{AutomationAssumeRole}}'
parameters:
  ResourceId:
    type: String
    description: EC2 instance ID
  RequiredTags:
    type: StringMap
    default:
      Environment: Production
      ManagedBy: AWSConfig
mainSteps:
  - name: addTags
    action: 'aws:createTags'
    inputs:
      ResourceType: ec2:instance
      ResourceIds:
        - '{{ResourceId}}'
      Tags: '{{RequiredTags}}'
```

### 4.6 Remediation Execution Status

**Check Remediation Status:**
```bash
# List remediation executions
aws configservice describe-remediation-execution-status \
  --config-rule-name s3-bucket-public-read-prohibited

# Get details for specific execution
aws configservice describe-remediation-execution-status \
  --config-rule-name s3-bucket-public-read-prohibited \
  --resource-keys resourceType=AWS::S3::Bucket,resourceId=my-bucket
```

---

## 5. Compliance Monitoring

### 5.1 Compliance Dashboard

AWS Config provides a compliance dashboard showing:
- Overall compliance score
- Compliance by resource type
- Non-compliant resources list
- Trend analysis

### 5.2 Viewing Compliance by Resource

```bash
# Get compliance details for a rule
aws configservice get-compliance-details-by-config-rule \
  --config-rule-name s3-bucket-public-read-prohibited \
  --compliance-types NON_COMPLIANT

# Get compliance by resource
aws configservice get-compliance-details-by-resource \
  --resource-type AWS::S3::Bucket \
  --resource-id my-bucket-name

# Get compliance summary
aws configservice get-compliance-summary
```

### 5.3 Compliance Pack (Conformance Packs)

Deploy collections of rules as a single entity:

**Console Steps:**
1. Navigate to AWS Config → Conformance packs
2. Click "Deploy conformance pack"
3. Choose template (AWS best practices, Operational, Security)
4. Configure parameters
5. Deploy

**CLI Deployment:**
```bash
# Deploy operational best practices conformance pack
aws configservice put-conformance-pack \
  --conformance-pack-name Operational-Best-Practices \
  --template-s3-uri s3://my-config-templates/operational-best-practices.yaml \
  --conformance-pack-input-parameters \
    ParameterName=ExcludedResourceTypes,ParameterValue="AWS::CloudFormation::Stack"
```

**Sample Conformance Pack Template:**
```yaml
Resources:
  S3PublicReadRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: s3-bucket-public-read-prohibited
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_PUBLIC_READ_PROHIBITED
        
  S3PublicWriteRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: s3-bucket-public-write-prohibited
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_PUBLIC_WRITE_PROHIBITED
        
  S3EncryptionRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: s3-bucket-server-side-encryption-enabled
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED
```

### 5.4 Compliance Reports

**Generate Compliance Report:**
```bash
# Export compliance report to S3
aws configservice deliver-config-snapshot \
  --delivery-channel-name default

# Query compliance history
aws configservice get-resource-config-history \
  --resource-type AWS::EC2::Instance \
  --resource-id i-0123456789abcdef0
```

---

## 6. Advanced Features

### 6.1 Config Aggregators

Aggregate data from multiple accounts and regions:

**Setting Up Aggregator:**
```bash
# Create aggregator
aws configservice put-configuration-aggregator \
  --configuration-aggregator-name OrganizationAggregator \
  --account-aggregation-sources '{
    "AllAwsRegions": true,
    "AccountIds": ["123456789012", "123456789013"]
  }'

# Or use Organization
aws configservice put-configuration-aggregator \
  --configuration-aggregator-name OrganizationAggregator \
  --organization-aggregation-source '{
    "AllAwsRegions": true,
    "RoleArn": "arn:aws:iam::123456789012:role/ConfigAggregatorRole"
  }'
```

### 6.2 Advanced Queries

Query configuration data using SQL-like syntax:

```bash
# Query all EC2 instances
aws configservice select-resource-config \
  --expression "SELECT resourceId, resourceType, configuration.instanceType, tags WHERE resourceType = 'AWS::EC2::Instance'"

# Query S3 buckets without encryption
aws configservice select-resource-config \
  --expression "SELECT resourceId, resourceName, supplementaryConfiguration.ServerSideEncryptionConfiguration WHERE resourceType = 'AWS::S3::Bucket' AND supplementaryConfiguration.ServerSideEncryptionConfiguration IS NULL"

# Query resources by tag
aws configservice select-resource-config \
  --expression "SELECT * WHERE tags.key = 'Environment' AND tags.value = 'Production'"
```

### 6.3 Configuration Snapshots

**Deliver Snapshot to S3:**
```bash
aws configservice deliver-config-snapshot \
  --delivery-channel-name default
```

Snapshot contains:
- Configuration items for all recorded resources
- Resource relationships
- Configuration history (last known state)

---

## 7. Integration Patterns

### 7.1 EventBridge Integration

**React to Compliance Changes:**
```json
{
  "source": ["aws.config"],
  "detail-type": ["Config Rules Compliance Change"],
  "detail": {
    "newEvaluationResult": {
      "complianceType": ["NON_COMPLIANT"]
    },
    "configRuleName": ["s3-bucket-public-read-prohibited"]
  }
}
```

**Example: Send Slack Alert on Non-Compliance:**
```python
import json
import boto3
import urllib.request

def lambda_handler(event, context):
    rule_name = event['detail']['configRuleName']
    resource_type = event['detail']['newEvaluationResult']['evaluationResultIdentifier']['evaluationResultQualifier']['resourceType']
    resource_id = event['detail']['newEvaluationResult']['evaluationResultIdentifier']['evaluationResultQualifier']['resourceId']
    
    message = {
        "text": f"⚠️ NON_COMPLIANT: {rule_name}\nResource: {resource_type}/{resource_id}"
    }
    
    # Send to Slack webhook
    req = urllib.request.Request(
        'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',
        data=json.dumps(message).encode(),
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)
```

### 7.2 Security Hub Integration

Config findings automatically flow to Security Hub:

**Enable Integration:**
1. Open Security Hub console
2. Navigate to Integrations
3. Enable AWS Config
4. Findings appear in Security Hub dashboard

### 7.3 CloudTrail Integration

All Config API calls are logged to CloudTrail for auditing:

```bash
# Query Config API activity
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventSource,AttributeValue=config.amazonaws.com \
  --max-results 10
```

### 7.4 Systems Manager Integration

Config remediation uses Systems Manager Automation documents.

### 7.5 Organizations Integration

**Multi-Account Setup:**
1. Enable Config in each member account
2. Set up aggregator in management account
3. Use Organizations to enable Config across all accounts
4. Deploy conformance packs organization-wide

```bash
# Enable Config across organization
aws organizations enable-aws-service-access \
  --service-principal config.amazonaws.com

# Deploy conformance pack organization-wide
aws configservice put-organization-conformance-pack \
  --organization-conformance-pack-name Security-Best-Practices \
  --template-s3-uri s3://my-config-templates/security-best-practices.yaml \
  --excluded-accounts ["123456789014"]
```

---

## 8. Cost Optimization

### 8.1 Pricing Components

| Component | Cost | Notes |
|-----------|------|-------|
| **Configuration items** | $0.003 per item | Charged when recorded |
| **Config rules** | $0.001 per evaluation | Per rule evaluation |
| **Conformance packs** | $0.0012 per rule evaluation | Slightly higher than individual rules |
| **Remediation** | Standard SSM pricing | Automation document costs |

### 8.2 Cost Optimization Strategies

**1. Limit Recorded Resource Types**
```bash
# Only record critical resource types
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::123456789012:role/ConfigRole \
  --recording-group resourceTypes=["AWS::EC2::Instance","AWS::S3::Bucket","AWS::IAM::User","AWS::IAM::Role"]
```

**2. Use Periodic Evaluation Wisely**
- Use configuration change triggers for real-time needs
- Use periodic only for compliance reporting
- Choose appropriate frequency (24 hours for cost savings)

**3. Aggregate Multi-Account**
- Use single aggregator instead of multiple recorders
- Reduces redundant storage

**4. Delete Unused Rules**
```bash
# Remove rules that aren't needed
aws configservice delete-config-rule \
  --config-rule-name unused-rule-name
```

### 8.3 Cost Estimation

**Example Monthly Cost:**

| Resource | Quantity | Rate | Monthly Cost |
|----------|----------|------|--------------|
| Config items | 10,000 | $0.003 | $30 |
| Rule evaluations | 50,000 | $0.001 | $50 |
| S3 storage | 50 GB | $0.023/GB | $1.15 |
| **Total** | | | **~$81** |

---

## 9. Troubleshooting

### 9.1 Common Issues

**Configuration Recorder Not Recording**
```bash
# Check recorder status
aws configservice describe-configuration-recorder-status

# Verify IAM permissions
aws iam get-role --role-name ConfigRole

# Check S3 bucket policy
aws s3api get-bucket-policy --bucket my-config-bucket
```

**Rule Evaluation Failures**
```bash
# Get rule evaluation details
aws configservice get-compliance-details-by-config-rule \
  --config-rule-name my-rule \
  --compliance-types INSUFFICIENT_DATA

# Check CloudWatch Logs for Lambda-based rules
aws logs tail /aws/lambda/my-config-rule-function
```

**Remediation Failures**
```bash
# Check remediation execution status
aws configservice describe-remediation-execution-status \
  --config-rule-name my-rule

# View Systems Manager Automation execution
aws ssm describe-automation-executions \
  --filters Key=ExecutionId,Values=execution-id-here
```

### 9.2 Diagnostic Commands

```bash
# List all config rules
aws configservice describe-config-rules

# Get compliance summary
aws configservice get-compliance-summary

# Check resource compliance
aws configservice get-compliance-details-by-resource \
  --resource-type AWS::EC2::Instance \
  --resource-id i-0123456789abcdef0

# View configuration history
aws configservice get-resource-config-history \
  --resource-type AWS::EC2::SecurityGroup \
  --resource-id sg-0123456789abcdef0

# Query configuration items
aws configservice list-discovered-resources \
  --resource-type AWS::EC2::Instance
```

### 9.3 Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "NoAvailableConfigurationRecorder" | Recorder not configured | Create configuration recorder |
| "InsufficientPermissionsException" | IAM permissions missing | Check IAM role policies |
| "MaxNumberOfConfigRulesExceeded" | Too many rules | Request limit increase or remove unused rules |
| "InvalidParameterValueException" | Wrong parameter format | Check JSON formatting |
| "ResourceNotDiscoveredException" | Resource not yet recorded | Wait for initial discovery |

### 9.4 Best Practices

1. **Start with Critical Resources**
   - Focus on security-sensitive resources first
   - Expand coverage gradually

2. **Use Conformance Packs**
   - Standardize rules across accounts
   - Easier to maintain than individual rules

3. **Monitor Costs**
   - Set up billing alerts
   - Review recorded resources regularly

4. **Enable Auto-Remediation Carefully**
   - Test in non-production first
   - Start with manual remediation
   - Use rate limiting

5. **Integrate with Security Hub**
   - Centralized security findings
   - Better visibility across services

6. **Use Tags Effectively**
   - Tag-based rule scoping
   - Easier resource management

---

## Quick Reference

```bash
# Enable Config
aws configservice start-configuration-recorder \
  --configuration-recorder-name default

# Stop Config
aws configservice stop-configuration-recorder \
  --configuration-recorder-name default

# List all compliance
aws configservice get-compliance-summary-by-resource-type

# Get compliance by resource type
aws configservice get-compliance-details-by-resource-type \
  --resource-type AWS::EC2::Instance

# Delete a config rule
aws configservice delete-config-rule \
  --config-rule-name my-rule
```

---

*Last Updated: 2026-02-04*
*Based on AWS Config Documentation*
