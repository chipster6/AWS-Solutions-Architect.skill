# Multi-Account Governance Reference

**Document ID:** ref-multi-account-governance  
**Purpose:** SA Pro-level reference for AWS Organizations, Control Tower, and governance

---

## AWS Organizations

### Organizational Structure

#### Recommended OU Design
```
└── Root
    ├── Security
    │   ├── SecurityTooling
    │   ├── LogArchive
    │   └── Guardrails
    │
    ├── Infrastructure
    │   ├── Network
    │   └── SharedServices
    │
    ├── Workloads
    │   ├── Production
    │   ├── Staging
    │   └── Development
    │
    └── Sandbox
        ├── IndividualSandbox
        └── TeamSandbox
```

#### OU Design Principles
| OU Name | Purpose | SCP Attached | Account Types |
|---------|---------|--------------|---------------|
| Security | Security tooling, logging | Restrictive | Security, Audit, Log Archive |
| Infrastructure | Network, shared services | Moderate | Network, Shared Services |
| Production | Production workloads | Minimal | Production workloads |
| Staging | Staging environments | Moderate | Staging, Pre-prod |
| Development | Development workloads | Moderate | Dev, Feature testing |
| Sandbox | Experimentation | Lenient | Sandboxes, Proof of Concept |

### Service Control Policies (SCPs)

#### SCP Evaluation Logic
```
1. Does account belong to OU?
2. Is SCP attached at OU or parent?
3. Are there deny statements?
4. Are there allow statements?
5. Does IAM permission check pass?
6. Final decision: Allow/Deny
```

#### SCP Examples

##### Guardrail: Prevent Disabling CloudTrail
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PreventCloudTrailDisable",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:StopLogging",
        "cloudtrail:DeleteTrail"
      ],
      "Resource": "*"
    }
  ]
}
```

##### Guardrail: Restrict Regions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSpecificRegions",
      "Effect": "Deny",
      "NotAction": [
        "a4b:*",
        "acm:*",
        "aws-marketplace:*",
        "iam:*",
        "sts:*",
        "support:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "us-east-1",
            "us-west-2",
            "eu-west-1"
          ]
        }
      }
    }
  ]
}
```

##### Guardrail: Require Encryption
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireEncryption",
      "Effect": "Deny",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "AES256"
        }
      }
    }
  ]
}
```

### CloudFormation StackSets

#### Organizational Deployment
```yaml
# StackSet Configuration for Multi-Account Deployment
stackset:
  name: "CommonSecurityResources"
  
  permission_model: "SERVICE_MANAGED"
  
  auto_deployment:
    enabled: true
    type: "UPDATE`
    prune: false
  
  targets:
    organizational_unit_ids:
      - "ou-security-12345"
      - "ou-prod-67890"
  
  operation_preferences:
    region_order:
      - "us-east-1"
      - "us-west-2"
    failure_tolerance_count: 2
    max_concurrent_count: 5
```

## Control Tower

### Landing Zone Architecture

#### Control Tower Components
```
┌─────────────────────────────────────────────────────────┐
│                   Control Tower                          │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐│
│  │              Shared Accounts                          ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────────────────────┐││
│  │  │  Log   │ │ Security│ │    Infrastructure      │││
│  │  │ Archive│ │  Tooling │ │      (Network)         │││
│  │  └─────────┘ └─────────┘ └─────────────────────────┘││
│  └─────────────────────────────────────────────────────┘│
│                                                          │
│  ┌─────────────────────────────────────────────────────┐│
│  │              Member Accounts                         ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────────────────────┐││
│  │  │  Prod   │ │ Staging │ │       Dev              │││
│  │  │ Account │ │ Account │ │      Account           │││
│  │  └─────────┘ └─────────┘ └─────────────────────────┘││
│  └─────────────────────────────────────────────────────┘│
│                                                          │
│  ┌─────────────────────────────────────────────────────┐│
│  │              Guardrails                              ││
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │││
│  │  │  Preventive │ │ Detective   │ │  Mandatory   │ │││
│  │  └─────────────┘ └─────────────┘ └─────────────┘ │││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

### Guardrails

#### Preventive Guardrails (SCPs)
| Guardrail | Category | Severity | Description |
|-----------|----------|----------|-------------|
| Prevent deletion of CloudTrail | Security | High | Prevents disabling or deleting CloudTrail |
| Prevent public S3 access | Security | High | Blocks public access to S3 buckets |
| Enable security best practices | Security | Medium | Enforces encryption, version control |
| Restrict regions | Compliance | High | Limits deployment to approved regions |

#### Detective Guardrails (Config Rules)
| Guardrail | Category | Severity | Description |
|-----------|----------|----------|-------------|
| EBS encryption enabled | Security | High | Checks EBS volumes are encrypted |
| S3 versioning enabled | Security | Medium | Verifies S3 versioning is enabled |
| RDS backup enabled | Reliability | High | Ensures RDS has automated backups |
| ELB security groups | Security | Medium | Validates ALB security group rules |

### Account Factory

#### Account Provisioning
```yaml
# Account Factory Configuration
account_factory:
  account:
    account_name: "prod-workload-001"
    email: "admin+prod-workload@company.com"
    
    managedOrganizationalUnit:
      name: "Production"
      path: "/Workloads/Production"
    
    # SSO configuration
    sso:
      enabled: true
      group_assignments:
        - group: "Administrators"
          permission_set: "AdministratorAccess"
        - group: "Developers"
          permission_set: "DeveloperAccess"
    
    # Network configuration
    network:
      vpc_cidr: "10.0.0.0/16"
      enable_nat_gateway: true
      enable_vpn: false
```

## Centralized Logging & Security

### AWS CloudTrail

#### Organization Trail Configuration
```yaml
cloudtrail:
  name: "org-all-events-trail"
  
  is_organization_trail: true
  
  # Event selectors
  event_selectors:
    - read_write_type: "All"
      include_management_events: true
      data_resources:
        - type: "AWS::S3::Object"
          values:
            - "arn:aws:s3:::company-logs-*/"
  
  # Integration with CloudWatch
  cloud_watch_logs:
    log_group: "/org/trail/all-events"
    role_arn: "arn:aws:iam::123456789012:role/CloudTrail-Logs"
  
  # S3 bucket
  s3_bucket_name: "company-cloudtrail-logs"
  s3_key_prefix: "org-trail/"
```

### AWS Config

#### Organization Config Rules
```yaml
aws_config:
  rules:
    - name: "required-tags"
      identifier: "REQUIRED_TAGS"
      scope:
        compliance_resource_types:
          - "AWS::EC2::Instance"
          - "AWS::RDS::DBInstance"
      input_parameters:
        "tag1Key": "Environment"
        "tag2Key": "Owner"
    
    - name: "encrypted-volumes"
      identifier: "ENCRYPTED_VOLUMES"
      scope:
        compliance_resource_types:
          - "AWS::EC2::Volume"
```

### Security Hub

#### Organization Aggregation
```yaml
security_hub:
  organization:
    enable: true
    
    auto_enable_standards:
      - "aws-foundational-security-best-practices"
      - "pci-dss-v3.2.1"
      - "cis-aws-foundations-benchmark"
    
    organization_configuration:
      auto_enable: true
      member_account_limit: 100
```

## Account Isolation Strategies

### Workload Isolation Models

#### Model 1: Single Account per Environment
```
┌─────────────────────────────────────────────────┐
│  AWS Organization                               │
│                                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │   Prod   │  │  Staging  │  │    Dev   │   │
│  │ Account  │  │  Account  │  │  Account │   │
│  └───────────┘  └───────────┘  └───────────┘   │
│                                                  │
│  Cross-account access via IAM roles             │
└─────────────────────────────────────────────────┘
```

#### Model 2: Account per Workload
```
┌─────────────────────────────────────────────────┐
│  AWS Organization                               │
│                                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │Workload A│  │Workload B│  │Workload C│   │
│  │  (All    │  │  (All     │  │  (All     │   │
│  │  envs)   │  │   envs)   │  │   envs)   │   │
│  └───────────┘  └───────────┘  └───────────┘   │
│                                                  │
│  Each workload has Prod, Staging, Dev accounts   │
└─────────────────────────────────────────────────┘
```

### Network Isolation

#### VPC Architecture Pattern
```yaml
vpc:
  cidr_block: "10.0.0.0/16"
  
  # Subnet allocation
  subnets:
    - name: "public"
      cidr: "10.0.1.0/24"
      route_table: "rtb-public"
      
    - name: "private-app"
      cidr: "10.0.2.0/24"
      route_table: "rtb-private-app"
      
    - name: "private-data"
      cidr: "10.0.3.0/24"
      route_table: "rtb-private-data"
      
    - name: "management"
      cidr: "10.0.4.0/24"
      route_table: "rtb-management"

  # Security groups
  security_groups:
    - name: "sg-app"
      rules:
        - type: "ingress"
          from_port: 443
          to_port: 443
          cidr: "10.0.0.0/16"
```

## Governance Automation

### CloudWatch Events Rules
```yaml
cloudwatch:
  events:
    - name: "detect-config-changes"
      description: "Detect Config configuration changes"
      
      event_pattern: |
        {
          "source": ["aws.config"],
          "detail-type": ["Config Configuration Compliance Change"],
          "detail": {
            "change-type": ["UPDATE"]
          }
        }
      
      targets:
        - arn: "arn:aws:lambda:us-east-1:123456789012:function:ConfigChangeHandler"
```

### Service Catalog Governance
```yaml
service_catalog:
  portfolios:
    - name: "ApprovedArchitectures"
      description: "Approved architecture patterns"
      
      products:
        - name: "WebAppStandard"
          owner: "platform-team@company.com"
          
          provisioning_artifacts:
            - name: "v1.0"
              template_url: "s3://templates/webapp-standard-v1.yaml"
              constraints:
                - type: "LAUNCH"
                  role_arn: "arn:aws:iam::123456789012:role/ServiceCatalogLaunchRole"
```
