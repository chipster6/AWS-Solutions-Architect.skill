# Phase 0: AWS Account Setup and Configuration Guide

## Overview

This guide provides comprehensive instructions for setting up AWS accounts for testing and development for the AWS Solutions Architect skill enhancement project. It covers account creation, IAM configuration, security setup, and governance frameworks.

## Account Architecture

### 1. Account Structure

#### 1.1 Multi-Account Strategy
```markdown
# Multi-Account Strategy
- **Master Account**: Central management and billing account
- **Development Account**: Development and testing environment
- **Staging Account**: Pre-production and integration testing
- **Production Account**: Live production environment
- **Sandbox Account**: Experimental and learning environment
- **Shared Services Account**: Shared services and tools
- **Logging Account**: Centralized logging and monitoring
- **Security Account**: Security and compliance management
```

#### 1.2 Account Organization
```markdown
# Account Organization
- **AWS Organizations**: Centralized account management
- **Organizational Units**: Logical grouping of accounts
- **Service Control Policies**: Centralized policy management
- **Tagging Strategy**: Consistent resource tagging
- **Cost Allocation**: Cost allocation and tracking
- **Security Baselines**: Security baselines and standards
- **Compliance Frameworks**: Compliance frameworks and controls
- **Governance Policies**: Governance policies and procedures
```

### 2. Account Creation

#### 2.1 Master Account Setup
```bash
# Create Master Account
aws organizations create-account \
  --email devops@yourcompany.com \
  --account-name "AWS Solutions Architect - Master"

# Enable AWS Organizations
aws organizations enable-all-features

# Create Organizational Units
aws organizations create-organizational-unit \
  --parent-id r-examplerootid \
  --name "Development"

aws organizations create-organizational-unit \
  --parent-id r-examplerootid \
  --name "Production"
```

#### 2.2 Development Account Setup
```bash
# Create Development Account
aws organizations create-account \
  --email dev@yourcompany.com \
  --account-name "AWS Solutions Architect - Development"

# Move to Development OU
aws organizations move-account \
  --account-id 123456789012 \
  --source-parent-id r-examplerootid \
  --destination-parent-id ou-examplerootid-development

# Enable CloudTrail
aws cloudtrail create-trail \
  --name development-cloudtrail \
  --s3-bucket-name development-logs \
  --is-multi-region-trail
```

#### 2.3 Production Account Setup
```bash
# Create Production Account
aws organizations create-account \
  --email prod@yourcompany.com \
  --account-name "AWS Solutions Architect - Production"

# Move to Production OU
aws organizations move-account \
  --account-id 123456789013 \
  --source-parent-id r-examplerootid \
  --destination-parent-id ou-examplerootid-production

# Enable Config
aws configservice put-configuration-recorder \
  --configuration-recorder-name default \
  --role-arn arn:aws:iam::123456789013:role/config-role \
  --recording-group AllSupported=true IncludeGlobalResourceTypes=true
```

## IAM Configuration

### 1. Identity and Access Management

#### 1.1 IAM Users and Groups
```bash
# Create IAM Users
aws iam create-user --user-name solutions-architect
aws iam create-user --user-name developer
aws iam create-user --user-name qa-engineer
aws iam create-user --user-name operations-engineer

# Create IAM Groups
aws iam create-group --group-name administrators
aws iam create-group --group-name developers
aws iam create-group --group-name qa-engineers
aws iam create-group --group-name operations-engineers

# Add Users to Groups
aws iam add-user-to-group --user-name solutions-architect --group-name administrators
aws iam add-user-to-group --user-name developer --group-name developers
aws iam add-user-to-group --user-name qa-engineer --group-name qa-engineers
aws iam add-user-to-group --user-name operations-engineer --group-name operations-engineers
```

#### 1.2 IAM Policies
```bash
# Create Custom Policies
aws iam create-policy \
  --policy-name SolutionsArchitectFullAccess \
  --policy-document file://solutions-architect-policy.json

aws iam create-policy \
  --policy-name DeveloperAccess \
  --policy-document file://developer-policy.json

aws iam create-policy \
  --policy-name QAAccess \
  --policy-document file://qa-policy.json

aws iam create-policy \
  --policy-name OperationsAccess \
  --policy-document file://operations-policy.json

# Attach Policies to Groups
aws iam attach-group-policy \
  --group-name administrators \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

aws iam attach-group-policy \
  --group-name developers \
  --policy-arn arn:aws:iam::123456789012:policy/DeveloperAccess

aws iam attach-group-policy \
  --group-name qa-engineers \
  --policy-arn arn:aws:iam::123456789012:policy/QAAccess

aws iam attach-group-policy \
  --group-name operations-engineers \
  --policy-arn arn:aws:iam::123456789012:policy/OperationsAccess
```

### 2. Role-Based Access Control

#### 2.1 Service Roles
```bash
# Create Service Roles
aws iam create-role \
  --role-name CodePipelineServiceRole \
  --assume-role-policy-document file://codepipeline-trust-policy.json

aws iam create-role \
  --role-name CodeBuildServiceRole \
  --assume-role-policy-document file://codebuild-trust-policy.json

aws iam create-role \
  --role-name LambdaExecutionRole \
  --assume-role-policy-document file://lambda-trust-policy.json

aws iam create-role \
  --role-name EC2InstanceRole \
  --assume-role-policy-document file://ec2-trust-policy.json

# Attach Service Policies
aws iam attach-role-policy \
  --role-name CodePipelineServiceRole \
  --policy-arn arn:aws:iam::aws:policy/AWSCodePipelineServiceRole

aws iam attach-role-policy \
  --role-name CodeBuildServiceRole \
  --policy-arn arn:aws:iam::aws:policy/AWSCodeBuildDeveloperAccess

aws iam attach-role-policy \
  --role-name LambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name EC2InstanceRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
```

#### 2.2 Cross-Account Roles
```bash
# Create Cross-Account Roles
aws iam create-role \
  --role-name CrossAccountAccess \
  --assume-role-policy-document file://cross-account-trust-policy.json

# Attach Cross-Account Policies
aws iam attach-role-policy \
  --role-name CrossAccountAccess \
  --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess

# Create Trust Relationship
aws iam update-assume-role-policy \
  --role-name CrossAccountAccess \
  --policy-document file://cross-account-trust-policy.json
```

## Security Configuration

### 1. Security Baselines

#### 1.1 Security Groups
```bash
# Create Security Groups
aws ec2 create-security-group \
  --group-name DevelopmentSecurityGroup \
  --description "Security group for development resources"

aws ec2 create-security-group \
  --group-name ProductionSecurityGroup \
  --description "Security group for production resources"

# Configure Security Group Rules
aws ec2 authorize-security-group-ingress \
  --group-name DevelopmentSecurityGroup \
  --protocol tcp \
  --port 22 \
  --cidr 192.168.1.0/24

aws ec2 authorize-security-group-ingress \
  --group-name ProductionSecurityGroup \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

#### 1.2 Network ACLs
```bash
# Create Network ACLs
aws ec2 create-network-acl \
  --vpc-id vpc-12345678 \
  --network-acl-name DevelopmentNetworkACL

aws ec2 create-network-acl \
  --vpc-id vpc-12345678 \
  --network-acl-name ProductionNetworkACL

# Configure Network ACL Rules
aws ec2 create-network-acl-entry \
  --network-acl-id acl-12345678 \
  --rule-number 100 \
  --protocol tcp \
  --port-range From=22,To=22 \
  --cidr-block 192.168.1.0/24 \
  --rule-action allow
```

### 2. Compliance Configuration

#### 2.1 Config Rules
```bash
# Create Config Rules
aws configservice put-config-rule \
  --config-rule file://restricted-common-ports-rule.json

aws configservice put-config-rule \
  --config-rule file://restricted-ssh-rule.json

aws configservice put-config-rule \
  --config-rule file://restricted-egress-rule.json

aws configservice put-config-rule \
  --config-rule file://restricted-encrypted-volumes-rule.json

# Enable Config Recording
aws configservice start-configuration-recorder \
  --configuration-recorder-name default
```

#### 2.2 Compliance Standards
```bash
# Implement Compliance Standards
aws configservice put-compliance-by-config-rule \
  --config-rule-name restricted-common-ports-rule \
  --compliance-resource-type AWS::EC2::SecurityGroup

aws configservice put-compliance-by-config-rule \
  --config-rule-name restricted-ssh-rule \
  --compliance-resource-type AWS::EC2::SecurityGroup

aws configservice put-compliance-by-config-rule \
  --config-rule-name restricted-egress-rule \
  --compliance-resource-type AWS::EC2::SecurityGroup

aws configservice put-compliance-by-config-rule \
  --config-rule-name restricted-encrypted-volumes-rule \
  --compliance-resource-type AWS::EC2::Volume
```

## Governance and Monitoring

### 1. Cost Management

#### 1.1 Cost Allocation Tags
```bash
# Create Cost Allocation Tags
aws ce create-cost-category-definition \
  --name Environment \
  --rule file://environment-cost-category-rule.json

aws ce create-cost-category-definition \
  --name Project \
  --rule file://project-cost-category-rule.json

aws ce create-cost-category-definition \
  --name Team \
  --rule file://team-cost-category-rule.json

# Enable Cost Allocation Tags
aws ce enable-cost-allocation-tags \
  --region us-east-1
```

#### 1.2 Budget Configuration
```bash
# Create Budgets
aws ce create-budget \
  --account-id 123456789012 \
  --budget file://monthly-budget.json

aws ce create-budget \
  --account-id 123456789012 \
  --budget file://quarterly-budget.json

aws ce create-budget \
  --account-id 123456789012 \
  --budget file://yearly-budget.json

# Configure Budget Alerts
aws ce create-budget-alert \
  --account-id 123456789012 \
  --budget-name MonthlyBudget \
  --alert file://monthly-budget-alert.json
```

### 2. Monitoring and Logging

#### 2.1 CloudWatch Configuration
```bash
# Create CloudWatch Alarms
aws cloudwatch put-metric-alarm \
  --alarm-name DevelopmentCPUUtilization \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:alert-topic

aws cloudwatch put-metric-alarm \
  --alarm-name ProductionErrorRate \
  --metric-name ErrorRate \
  --namespace AWS/Application \
  --statistic Average \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:alert-topic
```

#### 2.2 CloudTrail Configuration
```bash
# Create CloudTrail Trail
aws cloudtrail create-trail \
  --name organization-trail \
  --s3-bucket-name organization-logs \
  --is-multi-region-trail \
  --include-global-service-events

# Enable CloudTrail Logging
aws cloudtrail start-logging \
  --name organization-trail

# Create CloudTrail Insights
aws cloudtrail put-insight-selectors \
  --trail-name organization-trail \
  --insight-selectors ApiCallRateInsight
```

## Automation and Infrastructure as Code

### 1. CloudFormation Templates

#### 1.1 Account Structure Template
```yaml
# CloudFormation Template for Account Structure
AWSTemplateFormatVersion: '2010-09-09'
Description: AWS Solutions Architect Account Structure

Resources:
  MasterAccount:
    Type: AWS::Organizations::Account
    Properties:
      Email: master@yourcompany.com
      AccountName: "AWS Solutions Architect - Master"
      Tags:
        - Key: Environment
          Value: Master
        - Key: Project
          Value: AWS-Solutions-Architect

  DevelopmentAccount:
    Type: AWS::Organizations::Account
    Properties:
      Email: dev@yourcompany.com
      AccountName: "AWS Solutions Architect - Development"
      Tags:
        - Key: Environment
          Value: Development
        - Key: Project
          Value: AWS-Solutions-Architect

  ProductionAccount:
    Type: AWS::Organizations::Account
    Properties:
      Email: prod@yourcompany.com
      AccountName: "AWS Solutions Architect - Production"
      Tags:
        - Key: Environment
          Value: Production
        - Key: Project
          Value: AWS-Solutions-Architect

Outputs:
  MasterAccountId:
    Description: Master Account ID
    Value: !Ref MasterAccount
  DevelopmentAccountId:
    Description: Development Account ID
    Value: !Ref DevelopmentAccount
  ProductionAccountId:
    Description: Production Account ID
    Value: !Ref ProductionAccount
```

#### 1.2 IAM Configuration Template
```yaml
# CloudFormation Template for IAM Configuration
AWSTemplateFormatVersion: '2010-09-09'
Description: IAM Configuration for AWS Solutions Architect

Resources:
  SolutionsArchitectGroup:
    Type: AWS::IAM::Group
    Properties:
      GroupName: SolutionsArchitects
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AdministratorAccess

  DeveloperGroup:
    Type: AWS::IAM::Group
    Properties:
      GroupName: Developers
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AWSDeveloperAccess

  QAGroup:
    Type: AWS::IAM::Group
    Properties:
      GroupName: QAEngineers
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AWSQAEngineerAccess

  OperationsGroup:
    Type: AWS::IAM::Group
    Properties:
      GroupName: OperationsEngineers
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AWSOperationsAccess

Outputs:
  SolutionsArchitectGroup:
    Description: Solutions Architect Group
    Value: !Ref SolutionsArchitectGroup
  DeveloperGroup:
    Description: Developer Group
    Value: !Ref DeveloperGroup
  QAGroup:
    Description: QA Engineer Group
    Value: !Ref QAGroup
  OperationsGroup:
    Description: Operations Engineer Group
    Value: !Ref OperationsGroup
```

### 2. Automation Scripts

#### 2.1 Account Creation Script
```bash
#!/bin/bash
# create-accounts.sh

# Set Variables
MASTER_EMAIL="master@yourcompany.com"
DEV_EMAIL="dev@yourcompany.com"
PROD_EMAIL="prod@yourcompany.com"

# Create Master Account
aws organizations create-account \
  --email "$MASTER_EMAIL" \
  --account-name "AWS Solutions Architect - Master"

# Create Development Account
aws organizations create-account \
  --email "$DEV_EMAIL" \
  --account-name "AWS Solutions Architect - Development"

# Create Production Account
aws organizations create-account \
  --email "$PROD_EMAIL" \
  --account-name "AWS Solutions Architect - Production"

echo "Account creation completed successfully!"
```

#### 2.2 Security Configuration Script
```bash
#!/bin/bash
# configure-security.sh

# Set Variables
DEV_SECURITY_GROUP="DevelopmentSecurityGroup"
PROD_SECURITY_GROUP="ProductionSecurityGroup"

# Create Security Groups
aws ec2 create-security-group \
  --group-name "$DEV_SECURITY_GROUP" \
  --description "Security group for development resources"

aws ec2 create-security-group \
  --group-name "$PROD_SECURITY_GROUP" \
  --description "Security group for production resources"

# Configure Security Group Rules
aws ec2 authorize-security-group-ingress \
  --group-name "$DEV_SECURITY_GROUP" \
  --protocol tcp \
  --port 22 \
  --cidr 192.168.1.0/24

aws ec2 authorize-security-group-ingress \
  --group-name "$PROD_SECURITY_GROUP" \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

echo "Security configuration completed successfully!"
```

## Next Steps

### Immediate Actions
1. Create AWS Organizations master account
2. Set up organizational units and service control policies
3. Create development and production accounts
4. Configure IAM users, groups, and policies
5. Set up security groups and network ACLs

### Short-term Actions (Week 1)
1. Complete account creation and organization setup
2. Configure IAM roles and cross-account access
3. Set up compliance and security configurations
4. Implement cost management and budgeting
5. Configure monitoring and logging

### Long-term Actions (Week 2-3)
1. Complete automation and infrastructure as code setup
2. Implement advanced security and compliance controls
3. Set up governance and reporting frameworks
4. Conduct security audits and compliance assessments
5. Establish ongoing account management procedures

---

**AWS Account Setup and Configuration Guide**: Version 1.0.0  
**Created**: 2026-01-28  
**Next Review**: 2026-02-04  
**Implementation Start**: 2026-01-28