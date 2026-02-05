# AWS Multi-Account Governance Documentation

## Document Purpose

This document provides comprehensive coverage of AWS multi-account governance strategies, enabling agents to design, implement, and maintain secure, compliant, and operationally efficient AWS environments using AWS Organizations, Service Control Policies, and integrated security services.

---

## Table of Contents

1. [Conceptual Foundations](#1-conceptual-foundations)
2. [AWS Organizations Core Concepts](#2-aws-organizations-core-concepts)
3. [Organizational Unit Design](#3-organizational-unit-design)
4. [Service Control Policies Deep Dive](#4-service-control-policies-deep-dive)
5. [Security Services Integration](#5-security-services-integration)
6. [Governance and Compliance](#6-governance-and-compliance)
7. [Implementation Patterns](#7-implementation-patterns)
8. [Decision Frameworks](#8-decision-frameworks)
9. [Anti-Patterns and Failure Modes](#9-anti-patterns-and-failure-modes)
10. [Operational Excellence](#10-operational-excellence)
11. [Exam Scenarios and Validation](#11-exam-scenarios-and-validation)

---

## 1. Conceptual Foundations

### 1.1 Why Multi-Account Architecture?

Multi-account architecture in AWS addresses several critical organizational challenges that cannot be effectively solved within a single AWS account. Understanding these drivers is essential before making architectural decisions.

**Blast Radius Containment**

When workloads operate within a single account, a security incident, misconfiguration, or accidental resource deletion can affect all resources across the entire environment. Multi-account architecture limits the "blast radius" of such events by creating isolation boundaries. If an attacker compromises an account, they cannot directly access resources in other accounts without explicitly crossing account boundaries, which can be monitored and controlled.

Consider a scenario where a developer accidentally deletes a production database in a single-account environment. The same mistake in a properly segmented multi-account environment would only affect the development account, leaving production completely untouched. This isolation is achieved through AWS Organizations' policy enforcement and explicit cross-account access mechanisms.

**Regulatory Compliance Requirements**

Many compliance frameworks require strict separation of environments and data classifications. PCI DSS mandates that cardholder data environments be isolated from other workloads. HIPAA requires specific controls around healthcare information. SOX compliance often requires separation of production financial systems from development environments. Multi-account architecture provides the structural foundation for meeting these requirements by creating clear boundaries that align with compliance boundaries.

AWS Organizations enables centralized policy enforcement across all accounts, ensuring that compliance requirements are consistently applied. Service Control Policies can enforce restrictions at the organizational level, preventing any account from deviating from required controls regardless of IAM permissions.

**Billing and Cost Allocation**

In a single-account environment, attributing costs to specific teams, projects, or business units requires careful tagging and manual reconciliation. Multi-account architecture aligns AWS costs with organizational structure, enabling direct cost allocation through AWS Organizations' consolidated billing features.

Each account operates as its own billing unit, with AWS Organizations providing a single invoice covering all accounts. Cost allocation tags can be applied at the account level, simplifying chargeback to business units. This structure makes it easier to track, budget, and optimize costs across the organization.

**Security and Access Control**

Multi-account architecture enables defense in depth by creating multiple layers of security controls. Even if one layer is compromised, additional layers provide protection. IAM policies control access within accounts, while Service Control Policies control what actions are possible at all. AWS Config rules can enforce compliance, and CloudTrail provides centralized logging across all accounts.

This layered approach aligns with the AWS Well-Architected Framework's Security Pillar, which recommends using multiple accounts to limit the impact of security events and simplify access control management.

### 1.2 Trade-offs and Considerations

**Complexity vs Security Balance**

Adding accounts increases architectural complexity. Each account requires proper governance, monitoring, and operational procedures. Organizations must invest in automation, Infrastructure as Code, and operational tooling to manage multiple accounts efficiently. The trade-off between security isolation and operational complexity must be carefully evaluated for each use case.

For small teams or simple workloads, the operational overhead of multiple accounts may exceed the security benefits. AWS Organizations helps manage this complexity through centralized policy management, but organizations must still invest in tooling and processes to handle multi-account operations effectively.

**Account Proliferation Management**

Uncontrolled account creation leads to "shadow IT" where teams create accounts outside central governance. Without proper controls, accounts may lack required security controls, accumulate unnecessary costs, and create compliance gaps. Organizations should implement account request processes, automated provisioning, and regular account audits.

The AWS Control Tower Account Factory provides controlled account provisioning with mandatory security and governance controls. Alternatively, custom account provisioning through AWS Organizations APIs can enforce organizational standards while providing flexibility.

**Networking Considerations**

Multi-account architecture introduces networking complexity. Inter-account communication requires VPC peering, Transit Gateway, or other networking constructs. Each approach has different cost, performance, and management implications that must be considered during architecture design.

Shared services architectures, where certain resources exist in central accounts and are accessed by other accounts, can reduce duplication but introduce dependencies and potential single points of failure. The choice between replicated services in each account versus centralized shared services depends on the specific use case and operational requirements.

### 1.3 Decision Framework: Single vs Multi-Account

Organizations should evaluate several factors when deciding between single and multi-account architectures.

**Indicators Favoring Multi-Account:**

- Regulatory compliance requires environment isolation
- Multiple distinct business units with separate budgets
- Development, testing, and production workloads require strict separation
- Different teams need independent administrative access
- Need to limit blast radius of potential security incidents
- Cost allocation requires clear boundaries between workloads

**Indicators Favoring Single Account:**

- Small team with limited operational capacity
- Tight integration between all workloads
- Simple compliance requirements
- Cost optimization through resource sharing is priority
- Limited networking expertise available

**Hybrid Approach:**

Many organizations benefit from a hybrid approach, using a limited number of accounts (perhaps 3-5) to balance isolation with simplicity. A common pattern includes a production account, a development/account, and a shared services account, with AWS Organizations providing centralized governance across all.

---

## 2. AWS Organizations Core Concepts

### 2.1 What is AWS Organizations?

AWS Organizations is an account management service that enables centralized governance and management of multiple AWS accounts. It provides policy-based management for security, backup, AI services opt-out, and tag policies across an organization.

**Key Capabilities:**

- Create accounts programmatically and group them into organizational units
- Apply Service Control Policies (SCPs) to define guardrails
- Enable AWS services across the organization
- Consolidate billing for all member accounts
- Apply tag policies for cost allocation and access control
- Manage resource control policies for S3 access
- Enable delegated administrator for centralized management

**Organization Structure:**

An organization consists of a root account that acts as the parent of all other accounts. Organizational units (OUs) can be created as containers within the root, with accounts placed within OUs. Policies attached to any level in the hierarchy apply to all levels below, though more restrictive policies at lower levels can further constrain permissions.

The management account (formerly master account) is where the organization is created. This account is not subject to the organization's SCPs and has full administrative control over the organization. Member accounts are accounts that have been added to the organization and are subject to SCPs.

**Management Account Best Practices:**

The management account is key to all administrative tasks such as account management, policies, integration with other AWS services, and consolidated billing. Therefore, you should restrict and limit access to the management account only to those admin users who need rights to make changes to the organization.

**Critical Management Account Guidelines:**

1. **Limit Access:** Restrict management account access to only those who need it for organizational changes.

2. **Regular Access Reviews:** Periodically review personnel with access to the root user email, password, MFA, and phone number. Align reviews with business procedures and include monthly or quarterly verification.

3. **Use Only When Required:** Use the management account only for tasks that must be performed only by that account. Store all resources in other AWS accounts in the organization.

4. **Avoid Workloads:** Never deploy workloads to the management account. SCPs do not restrict users or roles in the management account.

5. **Delegate Responsibilities:** Delegate administrative responsibilities outside the management account for decentralization. Use delegated administrators for service management.

### 2.1.1 Root Access Management

AWS recommends enabling root access management to simplify managing root user credentials for member accounts. This feature prevents recovery of root user credentials, improving account security.

**Benefits:**

- Removes need for root user credentials on member accounts
- Newly created member accounts are secure-by-default
- Management account can perform privileged tasks on member accounts

**Common Use Cases:**

- Remove a misconfigured bucket policy that denies all principals from accessing an S3 bucket
- Delete an SQS resource-based policy that denies all principals
- Allow a member account to recover their root user credentials

### 2.1.2 Delegated Administrator Pattern

Delegated administration enables you to designate member accounts to administer specific AWS services or features at the organization level.

**Key Delegated Administrator Types:**

- **GuardDuty Delegated Administrator:** Centralizes threat detection management
- **Security Hub Delegated Administrator:** Aggregates security findings
- **Config Delegated Administrator:** Manages organization-wide compliance
- **IAM Access Analyzer Delegated Administrator:** Analyzes cross-account access

**Implementation:**

```python
def register_delegated_admin(org_client, account_id, service_principal):
    """Register a delegated administrator for an AWS service"""
    response = org_client.register_delegated_administrator(
        AccountId=account_id,
        DelegatedServiceName=service_principal
    )
    return response
```

### 2.2 Enabling AWS Organizations

Organizations can be enabled in two modes: all features or consolidated billing.

**All Features Mode:**

All features mode enables use of Service Control Policies, Resource Control Policies, and Tag Policies. When enabling all features, all member accounts must approve the consolidation. This mode is recommended for organizations that need to enforce governance policies across accounts.

All features mode provides inheritance for policies at all levels, ensuring that organizational policies are applied consistently. The management account can attach policies to the root, OUs, or individual accounts, with policies taking effect based on the hierarchy.

**Consolidated Billing Mode:**

Consolidated billing mode provides only billing consolidation without policy enforcement. This mode is available for organizations that do not need SCPs but want simplified billing across multiple accounts.

### 2.3 Inviting and Managing Member Accounts

**Invitation Process:**

Member accounts can be added to an organization through invitation. The management account sends an invitation to an account, which the account owner must accept to join the organization. Accounts can also be created directly within the organization using the Organizations API.

When an account joins an organization, it agrees to be governed by the organization's policies. The account owner retains control over resources within the account but cannot modify organizational policies or remove the account without going through the proper process.

**Account Removal:**

Accounts can be removed from an organization, returning them to standalone status. When an account is removed, it no longer inherits organizational policies and becomes responsible for its own governance. Billing continues to be consolidated for the billing period in which the removal occurred.

---

## 3. Organizational Unit Design

### 3.1 OU Design Principles

Organizational Units (OUs) provide a way to group accounts for simplified management and policy application. Effective OU design aligns organizational structure with security, operational, and compliance requirements.

**Hierarchical Organization:**

OUs should be organized hierarchically to reflect organizational structure and policy inheritance. A common pattern is to group accounts by environment (production, development, staging), by business unit, or by function (security, infrastructure, workloads). The hierarchy should minimize the number of levels while providing appropriate policy granularity.

**Policy Inheritance:**

Policies attached to an OU apply to all accounts within that OU and any child OUs. More restrictive policies at lower levels can further constrain permissions, but less restrictive policies cannot override more restrictive policies at higher levels. This inheritance model means that policies should become more permissive at lower levels, not more restrictive.

**OU Depth Considerations:**

Deep OU hierarchies provide fine-grained policy control but increase complexity. AWS recommends limiting OU depth to prevent difficult-to-manage structures. A typical organization might use 3-4 levels: root, environment-level OU, business-unit-level OU, and individual accounts.

### 3.2 Recommended OU Structure

AWS documentation recommends several standard OU types that organizations can adapt to their needs.

**Foundation OU:**

Contains the log archive account and audit account that provide foundational governance capabilities. These accounts should be created early and protected with restrictive SCPs.

**Security OU:**

The Security OU contains accounts focused on security operations, logging, and governance. Common accounts include a centralized GuardDuty account for threat detection, a log archive account for centralized CloudTrail and Config data, and an audit account for compliance reporting.

**Infrastructure OU:**

The Infrastructure OU contains accounts that provide shared infrastructure services. This might include a network account managing VPCs and connectivity, a shared services account for common utilities like CI/CD pipelines and directory services, and a bootstrap account for account provisioning infrastructure.

**Workloads OU:**

The Workloads OU contains accounts that run business applications. These are typically organized by business unit, application, or environment. Production workloads, staging environments, and development accounts might each be in separate OUs to enable different policy levels.

**Sandbox OU:**

The Sandbox OU provides isolated environments for experimentation. These accounts typically have the fewest restrictions, allowing developers to explore AWS services freely. However, guardrails should still prevent obviously dangerous actions like launching resources in unexpected regions.

**Policy Staging OU:**

The Policy Staging OU provides a controlled environment for testing new organizational policies before wider deployment. New SCPs or other policies can be attached to accounts in this OU to validate their effects before rolling out to production.

**Suspended OU:**

The Suspended OU contains accounts that are no longer active but need to be retained for compliance or legal reasons. This OU should have policies that prevent any resource operations while preserving data access for compliance purposes.

**Custom OU Types:**

Additional OU types based on organizational needs:

- **Exception OU:** Accounts requiring specific policy exceptions
- **Deployment OU:** CI/CD and deployment pipeline accounts
- **Transitional OU:** Accounts during migration or reorganization

### 3.3 Control Tower Landing Zone Architecture

AWS Control Tower provides a curated landing zone architecture with automated governance. It creates a multi-account environment with best-practice configurations, including mandatory and optional preventive and detective controls.

**Landing Zone Components:**

1. **Management Account:** Root of the organization with organizational management
2. **Log Archive Account:** Dedicated S3 bucket for CloudTrail and Config logs
3. **Audit Account:** Security and compliance monitoring account
4. **Foundational OU:** Contains log archive and audit accounts
5. **Security OU:** Dedicated security service accounts
6. **Custom OUs:** Workload-specific organizational units

**Control Tower Guardrails:**

| Guardrail Type | Description | Enforcement |
|---------------|-------------|-------------|
| Mandatory | Always enabled, cannot be disabled | Preventive |
| Strongly Recommended | Recommended for most environments | Preventive/Detective |
| Elective | Optional based on organizational needs | Detective |

**Landing Zone Evolution:**

Landing zones develop over time. As the number of OUs and accounts increases, extend the deployment to organize workloads effectively. Control Tower continues to maintain corporate policies and security practices across multiple accounts and workloads.

### 3.3 Moving Accounts Between OUs

Accounts can be moved between OUs to reflect organizational changes. When an account is moved, it inherits policies from the new parent OU immediately. This can have significant implications if the new OU has different policies, so account moves should be carefully planned and tested.

Moving production accounts requires particular attention to policy changes. An account that was in a production OU with certain permissions moved to a sandbox OU would suddenly be subject to sandbox restrictions, potentially disrupting production workloads.

---

## 4. Service Control Policies Deep Dive

### 4.1 What are Service Control Policies?

Service Control Policies (SCPs) are a type of policy that can be used to restrict permissions for member accounts in an organization. SCPs define guardrails that limit what actions can be performed, regardless of IAM permissions within individual accounts.

**SCPs are NOT:**

SCPs are not IAM policies. They do not grant permissions; they only restrict them. An SCP cannot allow an action that is not otherwise permitted by IAM policies. SCPs are not applied to the management account, which always has full permissions. SCPs do not affect service-linked roles or service principal permissions.

**SCPs ARE:**

SCPs are organizational policies that can be attached to the root, OUs, or individual accounts. They use the same syntax as IAM policies but serve a different purpose. SCPs can use condition keys to create context-aware restrictions and can reference resources using ARNs or wildcards.

### 4.2 SCP Evaluation Logic

Understanding SCP evaluation is critical for correct policy design. AWS evaluates SCPs as part of the overall policy evaluation chain that includes identity-based policies, resource-based policies, permissions boundaries, and session policies.

**SCP Evaluation Order in Overall Policy Evaluation:**

When AWS receives a request, evaluation proceeds through several stages. First, AWS evaluates identity-based policies attached to the principal making the request. Then resource-based policies on the target resource are evaluated. Permissions boundaries on the principal are checked. Organizations SCPs are evaluated. Finally, any session policies are checked. An explicit deny at any stage results in the request being denied.

**Allow Statement Requirements:**

For a permission to be allowed for a specific account, there must be an explicit Allow statement at every level from the root through each OU in the direct path to the account, including the target account itself. If an Allow statement is missing at any level, the permission is denied.

This is why AWS Organizations automatically attaches the AWS managed SCP named "FullAWSAccess" when you enable SCPs. This policy allows all services and actions. If this policy is removed and not replaced at any level of the organization, all OUs and accounts under that level would be blocked from taking any actions.

**Deny Statement Precedence:**

For a permission to be denied for a specific account, any SCP from the root through each OU in the direct path to the account, including the target account itself, can deny that permission. A Deny statement at any level takes precedence over Allow statements at other levels.

This means that even if an account has an SCP allowing a particular action, if any parent OU or the root has a Deny statement for that action, the action is denied.

### 4.3 SCP Strategy Patterns

**Allow-List Strategy:**

The allow-list strategy starts with a restrictive baseline and explicitly allows only necessary services and actions. This approach provides strong security by default, requiring explicit approval for any new service or capability. The baseline SCP typically denies all actions, with more permissive SCPs attached at lower levels.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowOnlySpecificServices",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": ["us-east-1", "us-west-2"]
        }
      }
    }
  ]
}
```

**Deny-List Strategy:**

The deny-list strategy allows all actions by default but explicitly denies dangerous or restricted actions. This approach is simpler to implement but provides weaker security boundaries. Organizations typically use deny-lists for common restrictions while relying on other controls for broader security.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyDangerousActions",
      "Effect": "Deny",
      "Action": [
        "ec2:DeleteVolume",
        "ec2:TerminateInstances",
        "s3:DeleteBucket"
      ],
      "Resource": "*"
    }
  ]
}
```

**Hybrid Approach:**

Most organizations benefit from a hybrid approach. Production environments might use allow-lists to restrict capabilities, while development environments use deny-lists to prevent obvious dangers while allowing flexibility. The specific approach depends on risk tolerance and operational requirements.

### 4.4 SCP Evaluation Logic - Detailed

**Complete Evaluation Chain:**

When AWS receives a request, evaluation proceeds in this order:

```
Step 1: Identity-Based Policies (IAM policies attached to principal)
        ↓
Step 2: Resource-Based Policies (policies on target resource)
        ↓
Step 3: Permissions Boundaries (policies limiting maximum permissions)
        ↓
Step 4: Organizations SCPs (evaluated across hierarchy)
        ↓
Step 5: Session Policies (policies from assumed roles)
        ↓
Final: Explicit Deny OR Allow
```

**SCP Hierarchy Evaluation:**

```
Root OU (attached SCPs)
    │
    ├── Production OU (attached SCPs)
    │       │
    │       ├── Prod-App-1 (attached SCPs)
    │       └── Prod-App-2 (attached SCPs)
    │
    └── Development OU (attached SCPs)
            │
            └── Dev-Team-A (attached SCPs)

For an action to be ALLOWED:
1. Root must allow (or have FullAWSAccess)
2. Production OU must allow
3. Prod-App-1 must allow

For an action to be DENIED:
- ANY level with Deny statement
```

**Common SCP Evaluation Scenarios:**

```json
// Scenario 1: Account in Production OU trying to use us-east-1 only
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonApprovedRegions",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": ["us-east-1", "us-west-2"]
        }
      }
    }
  ]
}

// Scenario 2: Deny specific actions regardless of IAM permissions
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyDangerousActions",
      "Effect": "Deny",
      "Action": [
        "ec2:DeleteVolume",
        "ec2:TerminateInstances",
        "s3:DeleteBucket",
        "iam:CreateUser"
      ],
      "Resource": "*"
    }
  ]
}

// Scenario 3: Require encryption on S3
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireS3Encryption",
      "Effect": "Deny",
      "Action": "s3:PutObject",
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

### 4.5 SCP Best Practices

**Start with FullAWSAccess:**

When first implementing SCPs, start with the FullAWSAccess policy attached at all levels. Gradually add restrictive SCPs as needed, testing each change before wider deployment. Removing FullAWSAccess without replacement can cause immediate operational disruptions.

**Test in Policy Staging OU:**

Before deploying new SCPs to production, test them in a policy staging OU. This allows identification of unintended consequences before affecting production workloads. Use AWS Organizations' policy simulation features to validate SCP behavior.

**Use Explicit Denies for Guardrails:**

When implementing security guardrails, use explicit Deny statements. This ensures that guardrails cannot be accidentally overridden by permissive policies at lower levels. Deny statements take precedence, providing reliable enforcement.

**Monitor SCP Changes:**

Use CloudTrail to monitor changes to SCPs and their attachments. SCPs are managed resources that can be modified only by authorized principals. Tracking changes helps identify policy drift and potential security issues.

### 4.6 Resource Control Policies (RCPs)

Resource Control Policies (RCPs) restrict permissions at the resource level, even when the account-level permissions allow access. Unlike SCPs which are attached to OUs, RCPs are attached to the organization and control access to specific resource types.

**RCP Use Case:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RestrictS3BucketAccess",
      "Effect": "Deny",
      "Action": [
        "s3:GetBucketPolicy",
        "s3:PutBucketPolicy",
        "s3:DeleteBucketPolicy"
      ],
      "Resource": "arn:aws:s3:::*-security-logs-*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalOrgID": "o-xxxxxxxxxx"
        }
      }
    }
  ]
}
```

### 4.7 Tag Policies

Tag policies enable you to standardize tags across all accounts in your organization. They help enforce tag compliance and generate compliance reports.

**Tag Policy Example:**

```json
{
  "TagPolicy": {
    "Environment": {
      "TagValue": {
        "@@assign": ["Production", "Development", "Staging", "Test"]
      },
      "EnforceFor": {
        "Resources": ["ec2:instance", "s3:bucket"]
      }
    },
    "CostCenter": {
      "TagValue": {
        "@@assign": ["CC-001", "CC-002", "CC-003"]
      },
      "Compliance": {
        "@@report_non_compliant_resources": true
      }
    }
  }
}
```

---

## 5. Security Services Integration

### 5.1 Security Reference Architecture

A comprehensive multi-account security architecture integrates multiple AWS security services to provide defense in depth. Each service plays a specific role in the overall security posture.

**GuardDuty for Threat Detection:**

GuardDuty provides intelligent threat detection by continuously monitoring AWS account activity, VPC flow logs, and DNS queries. In a multi-account environment, GuardDuty can be configured with a delegated administrator to aggregate findings across all accounts. This centralized visibility enables security teams to identify threats that span multiple accounts.

**Security Hub for Centralized Security Posture:**

Security Hub provides a comprehensive view of security alerts and compliance status across all accounts. It aggregates findings from GuardDuty, Config, IAM Access Analyzer, and other sources. Security Hub can enforce security standards through controls that map to compliance frameworks like PCI DSS and AWS Foundational Security Best Practices.

**Config for Resource Compliance:**

AWS Config continuously monitors and records resource configurations, enabling compliance tracking and change management. Config rules can evaluate resources against organizational policies, with remediation actions triggered for non-compliant resources. Multi-account Config aggregates compliance data for centralized reporting.

### 5.2 Multi-Account Security Configuration

**GuardDuty Delegated Administrator:**

The GuardDuty delegated administrator pattern designates one account (typically in the Security OU) to manage GuardDuty across the organization. Member accounts enroll in the organization-wide GuardDuty, with findings automatically sent to the delegated administrator.

```python
def enable_guardduty_delegated_admin(guardduty_client, admin_account_id):
    """Enable GuardDuty delegated administrator for the organization"""
    response = guardduty_client.update_organization_configuration(
        DetectorId=detector_id,
        OrganizationConfiguration={
            'AutoEnable': True,
            'DataSources': {
                'CloudTrail': True,
                'DNSLogs': True,
                'EC2InstanceEvents': True,
                'S3Logs': True,
                'KubernetesAuditLogs': True,
                'KubernetesProtection': True
            }
        }
    )
    return response
```

**Security Hub Organization Configuration:**

Security Hub similarly supports organization-wide configuration through a delegated administrator. The delegated administrator can enable standards across the organization, aggregate findings, and manage security policies.

### 5.3 Centralized Logging Architecture

**CloudTrail Organization Trail:**

An organization trail logs API activity across all accounts in the organization. The trail is created in the management account but logs events from all member accounts. This centralized logging provides a complete audit trail of all organizational activity.

**Log Archive Account:**

A dedicated log archive account should receive logs from all other accounts. This account should have strict access controls, limiting who can view or modify logs. S3 Object Lock can protect logs from deletion or modification, ensuring evidence preservation.

**Multi-Account Logging Architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│                    CloudTrail Organization Trail               │
├─────────────────────────────────────────────────────────────┤
│  Logs from: All accounts in organization                     │
│  Storage: S3 bucket in Log Archive account                   │
│  Encryption: SSE-KMS with dedicated key                      │
│  Access: Strictly controlled via bucket policies              │
│  Integrity: CloudTrail log file validation enabled           │
└─────────────────────────────────────────────────────────────┘
```

### 5.4 Network Architecture for Multi-Account Environments

Multi-account networking requires careful design to enable secure communication while maintaining isolation boundaries.

**Network Connectivity Options:**

| Option | Use Case | Complexity | Cost |
|--------|----------|------------|------|
| VPC Peering | Direct connection between two VPCs | Medium | Per-GB data transfer |
| Transit Gateway | Central hub for multiple VPCs | High | Per- attachment/hour |
| AWS Network Firewall | Centralized traffic inspection | High | Per-GB processed |
| AWS PrivateLink | Private API access to services | Medium | Per-hour + per-GB |

**Shared Services Networking Pattern:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Network Transit Hub                        │
├─────────────────────────────────────────────────────────────┤
│                    Transit Gateway (Central)                   │
├──────────────────┬──────────────────┬──────────────────────────┤
│                  │                  │                          │
│  Production VPC  │  Shared Services │    Development VPC      │
│  (Prod OU)       │  VPC (Infra OU)  │    (Dev OU)             │
│                  │                  │                          │
│  - Private subnets|  - API endpoints │  - Private subnets    │
│  - Tight security|  - DNS resolution │  - Flexible policies  │
│  - Restricted GW  |  - Directory svc │  - Broad access       │
└──────────────────┴──────────────────┴──────────────────────────┘

Network Policies:
- Prod → Shared: Allowed (controlled)
- Dev → Shared: Allowed (controlled)
- Prod ↔ Dev: Blocked by default
```

**Cross-Account DNS Architecture:**

- **Route 53 Resolver:** Centralized DNS resolution across accounts
- **Outbound Endpoints:** Forward queries from VPCs to centralized DNS
- **Inbound Endpoints:** Allow centralized systems to resolve private zones
- **Private Hosted Zones:** Share across accounts with VPCs

### 6.2.1 Tag Policies

Tag policies enable you to standardize tags across all accounts in your organization. They enforce tag rules by preventing non-compliant tag operations.

**Tag Policy Components:**

```json
{
  "TagKey": "Environment",
  "TagValue": {
    "@@assign": ["Production", "Development", "Staging"]
  },
  "Account": {
    "@@max_assign": 5
  }
}
```

**Tag Enforcement Strategies:**

- Prevent non-compliant tag values from being created
- Correct non-compliant tags using automated remediation
- Generate compliance reports across the organization

### 6.2.2 Consolidated Billing

AWS Organizations consolidates billing for all member accounts into a single invoice. This provides volume pricing discounts and simplified cost tracking.

**Billing Benefits:**

- **Combined Usage:** Usage across all accounts contributes to volume discounts
- **Single Invoice:** One bill covering the entire organization
- **Cost Allocation:** Track charges by account, service, or tag
- **Payment Responsibility:** Management account pays all charges

**Cost Management Best Practices:**

- Set up AWS Budgets at organizational and account levels
- Implement cost allocation tags for granular tracking
- Review AWS Cost Explorer reports regularly
- Enable AWS Budgets alerts for proactive management

### 6.2.3 AWS Control Tower Life Cycle Management

Control Tower provides life cycle management for your landing zone, ensuring governance consistency as the organization evolves.

**Key Capabilities:**

- **Account Provisioning:** Standardized account creation with required controls
- **Guardrail Updates:** Automatic updates to preventive and detective controls
- **OU Management:** Structured organization unit hierarchy
- **Compliance Monitoring:** Continuous compliance assessment

---

## 6. Governance and Compliance

### 6.1 AWS Control Tower

AWS Control Tower provides a curated landing zone architecture with automated governance. It creates a multi-account environment with best-practice configurations, including mandatory and optional preventive and detective controls.

**Control Tower Components:**

The landing zone created by Control Tower includes a management account, dedicated log archive account, and the OU structure recommended by AWS. Guardrails are implemented as SCPs (preventive controls) and Config rules (detective controls). Control Tower provides a dashboard showing compliance status across all accounts.

**Customizations with Control Tower:**

Control Tower can be customized through additional SCPs, Config rules, and custom guardrails. Organizations can extend the baseline landing zone with their specific requirements while maintaining the benefits of Control Tower's automated governance.

### 6.2 Compliance Framework Implementation

**PCI DSS Requirements:**

PCI DSS compliance requires specific controls around cardholder data. Organizations can implement these controls through a combination of SCPs enforcing data isolation, Config rules validating compliance requirements, and Security Hub controls checking for PCI DSS requirements.

**SOC 2 Compliance:**

SOC 2 requires controls around security, availability, processing integrity, confidentiality, and privacy. AWS provides services and features that support SOC 2 compliance, including CloudTrail for audit logging, Config for change management, and GuardDuty for threat detection.

### 6.3 Policy Lifecycle Management

**Policy Development Process:**

Organizational policies should follow a formal development process. New policies should be documented with clear rationale, tested in a non-production environment, reviewed by appropriate stakeholders, and approved through appropriate governance channels. Changes to existing policies should follow similar processes.

**Version Control:**

Organizational policies should be stored in version control alongside other infrastructure code. This provides audit trails for policy changes, enables rollback if issues arise, and supports policy-as-code practices.

---

## 7. Implementation Patterns

### 7.1 Account Factory Pattern

**AWS Control Tower Account Factory:**

Control Tower Account Factory provides standardized account provisioning with required governance controls. When a new account is requested through Account Factory, it is automatically placed in the correct OU with required guardrails enabled.

**Custom Account Provisioning:**

Organizations can create custom account provisioning workflows using AWS Organizations APIs. This allows customization of account configurations while enforcing organizational standards.

```python
class AccountFactory:
    def __init__(self, org_client, iam_client):
        self.org_client = org_client
        self.iam_client = iam_client
    
    def create_production_account(self, account_name, email, parent_ou):
        """Create a production account with standard configuration"""
        # Create the account
        create_response = self.org_client.create_account(
            Email=email,
            AccountName=account_name,
            RoleName='OrganizationAccountAccessRole'
        )
        
        # Wait for account creation to complete
        account_id = self._wait_for_account_creation(create_response['CreateAccountStatus']['Id'])
        
        # Move to correct OU
        self.org_client.move_account(
            AccountId=account_id,
            DestinationParentId=parent_ou,
            SourceParentId=self._get_root_id()
        )
        
        # Enable required services
        self._enable_config(account_id)
        self._enable_cloudtrail(account_id)
        self._attach_production_scp(account_id)
        
        return account_id
```

### 7.2 Cross-Account Access Patterns

**Role Assumption for Cross-Account Access:**

The recommended pattern for cross-account access is role assumption. The accessing account assumes a role in the target account, receiving temporary credentials with scoped permissions.

```python
def assume_cross_account_role(sts_client, target_role_arn, session_name):
    """Assume a role in another account"""
    response = sts_client.assume_role(
        RoleArn=target_role_arn,
        RoleSessionName=session_name,
        DurationSeconds=3600
    )
    
    return {
        'access_key': response['Credentials']['AccessKeyId'],
        'secret_key': response['Credentials']['SecretAccessKey'],
        'session_token': response['Credentials']['SessionToken']
    }
```

**Cross-Account Trust Configuration:**

When creating roles for cross-account access, the trust policy must allow the external account to assume the role.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:Externalid": "unique-external-id"
        }
      }
    }
  ]
}
```

### 7.3 Centralized Security Operations

**Security Hub Integration:**

Security Hub provides centralized security posture management across all accounts. Findings from GuardDuty, Config, and other services are aggregated, enabling security teams to view the complete organizational security status.

---

## 8. Decision Frameworks

### 8.1 OU Design Decision Matrix

| Factor | Production OU | Development OU | Sandbox OU |
|--------|--------------|---------------|------------|
| SCP Restriction Level | High (Allow-list) | Medium (Deny-list) | Low (Minimal) |
| Region Restrictions | Approved regions only | Approved regions only | All regions |
| Resource Limits | Defined quotas | Flexible quotas | Unlimited |
| Access Requirements | MFA required | MFA required | MFA preferred |
| Cost Monitoring | Strict budgets | Advisory budgets | Monitoring only |

### 8.2 SCP Complexity Decision Guide

**Simple Restrictions (Production):**

Production environments should have clear, simple restrictions that are easy to understand and validate. Use explicit Deny statements for specific dangerous actions.

**Moderate Restrictions (Staging):**

Staging environments can have slightly more flexibility than production but should maintain similar guardrails. Use Deny statements for actions that should never occur in any environment.

**Minimal Restrictions (Development):**

Development environments should have the minimum restrictions necessary to prevent obvious security issues. Allow developers flexibility to explore and experiment.

### 8.3 Security Services Selection Guide

| Requirement | Recommended Service | Alternative |
|-------------|---------------------|--------------|
| Threat Detection | GuardDuty | Security Hub |
| Configuration Compliance | Config | Security Hub |
| Vulnerability Scanning | Inspector | Security Hub |
| Access Analysis | IAM Access Analyzer | Config |
| Centralized Security | Security Hub | Custom Dashboard |

---

## 9. Anti-Patterns and Failure Modes

### 9.1 Common Anti-Patterns

**Anti-Pattern: Removing FullAWSAccess Without Replacement**

The most dangerous anti-pattern is removing the FullAWSAccess SCP without ensuring equivalent permissions through other SCPs. This immediately blocks all actions for all accounts under that OU, causing operational disruption.

**Anti-Pattern: Inconsistent Policy Application**

Applying different policies to similar accounts creates confusion and potential security gaps. Establish clear guidelines for which policies apply to which OU types.

**Anti-Pattern: Overly Broad Deny Statements**

Deny statements that are too broad can block legitimate operations. Always test deny statements before deployment and use specific actions rather than wildcards.

**Anti-Pattern: Ignoring SCP Evaluation Order**

Failing to understand that SCPs are evaluated alongside other policies can lead to unexpected denials. Always consider the complete evaluation chain when troubleshooting permission issues.

### 9.2 Failure Modes and Recovery

**SCP Lockout Recovery:**

If SCPs accidentally block all access, the management account can detach or modify problematic SCPs. Since SCPs do not apply to the management account, administrators retain full access to fix issues.

**Account Compromise Response:**

If an account is compromised, immediately isolate it by moving it to a suspended OU with restrictive SCPs. Preserve evidence through log exports, then remediate and restore.

### 9.3 Prevention Strategies

**Policy Testing Environment:**

Always test new policies in a non-production environment before deployment. Use the policy simulator to validate expected behavior.

**Change Management:**

Implement formal change management for organizational policies. Require reviews and approvals for policy changes.

**Monitoring and Alerting:**

Monitor policy changes through CloudTrail and set up alerts for unauthorized modifications.

---

## 10. Operational Excellence

### 10.1 Monitoring and Observability

**Centralized Logging:**

All accounts should send logs to a centralized log archive account. CloudTrail logs, GuardDuty findings, and Config compliance data should all be aggregated for organizational visibility.

**Metrics Aggregation:**

CloudWatch metrics from all accounts should be aggregated to a central dashboard. This provides operational visibility across the entire organization.

### 10.2 Incident Response

**Multi-Account Incident Response:**

Security incidents may span multiple accounts. Response procedures should account for cross-account investigation, evidence preservation, and remediation coordination.

**Isolation Procedures:**

When an incident is detected, affected accounts should be isolated by moving them to a restricted OU or applying emergency SCPs.

### 10.3 Cost Management

**Budget Alerts:**

Set up budgets and alerts at the organizational level and for individual accounts. This enables proactive cost management before issues become significant.

**Cost Allocation Tags:**

Implement consistent tagging strategies to enable accurate cost allocation. Use AWS Organizations tag policies to enforce required tags.

---

## 11. Exam Scenarios and Validation

### 11.1 Scenario: Multi-Account Security Architecture

**Scenario:**

A financial services company needs to implement a multi-account architecture to meet regulatory requirements. They have development, testing, and production environments with different security requirements. How should they structure their organization?

**Recommended Approach:**

1. Create a Security OU with dedicated accounts for GuardDuty, log archive, and audit functions
2. Separate production, staging, and development into different OUs
3. Apply restrictive SCPs to production that deny dangerous actions
4. Apply less restrictive SCPs to development that allow experimentation
5. Enable Security Hub with PCI DSS standards for the production OU
6. Implement centralized logging to the log archive account

**Key Considerations:**

- SCPs should deny actions that could compromise data in production
- Development accounts should have flexibility for developers
- Logging must be centralized for compliance evidence
- Security Hub provides compliance visibility

### 11.2 Scenario: SCP Troubleshooting

**Scenario:**

A user with AdministratorAccess IAM policy is unable to create an S3 bucket in a member account. What is the most likely cause?

**Diagnosis:**

The user is likely subject to an SCP that denies S3 bucket creation. Even though the IAM policy allows the action, the SCP denies it. Check SCPs attached to the account, parent OUs, and root.

**Resolution:**

1. Identify restrictive SCPs using the policy simulator
2. Determine if the restriction is intentional
3. If unintentional, modify the SCP to allow S3 bucket creation
4. Test the change before wider deployment

### 11.3 Scenario: Cross-Account Access

**Scenario:**

An application in Account A needs to read data from S3 buckets in Account B. What is the recommended approach?

**Recommended Solution:**

1. Create an IAM role in Account B with S3 read permissions
2. Configure a trust policy allowing Account A to assume the role
3. In Account A, create an IAM policy or role that can assume the role in Account B
4. Use the assumed role's credentials to access S3

**Key Points:**

- Role assumption provides temporary, scoped credentials
- Trust policies control which accounts can assume the role
- Least privilege should be applied to both the trust and permission policies

### 11.4 Scenario: Control Tower Landing Zone Setup

**Scenario:**

A healthcare company needs to implement AWS Control Tower for regulatory compliance (HIPAA). They require:
- Separation of PHI workloads from other workloads
- Mandatory logging and audit trails
- Automated compliance checks
- Guardrails for HIPAA controls

**Recommended Approach:**

1. **Initialize Control Tower Landing Zone:**
   - Use Control Tower Account Factory
   - Enable mandatory guardrails
   - Configure preventive controls for region restrictions

2. **Create OU Structure:**
   ```
   Root
   ├── Security OU
   │   ├── Log Archive Account
   │   └── Audit Account
   ├── Foundational OU
   │   └── Shared Services Account
   ├── PHI Workloads OU
   │   └── Production PHI Accounts
   └── General Workloads OU
       ├── Development
       ├── Staging
       └── Production
   ```

3. **Enable HIPAA Guardrails:**
   - Restrict S3 public access
   - Require encryption at rest
   - Enable CloudTrail logging
   - Enforce VPC security group rules

4. **Implement Compliance Monitoring:**
   - Use Security Hub with HIPAA compliance standard
   - Configure Config rules for HIPAA requirements
   - Set up automated remediation

### 11.5 Scenario: SCP Lockout Recovery

**Scenario:**

An administrator accidentally attached an SCP that denies all actions to the Production OU. All production accounts are now locked out. How do you recover?

**Recovery Steps:**

1. **Access Management Account:**
   - Login to management account (SCPs don't apply)
   - Navigate to AWS Organizations console

2. **Identify Problematic SCP:**
   - Review recent SCP changes using CloudTrail
   - Identify the SCP attached to Production OU

3. **Detach Problematic SCP:**
   ```bash
   aws organizations detach-policy \
     --policy-id p-xxxxxxxxxxxxx \
     --target-id ou-production-xxxxxxxx
   ```

4. **Verify Recovery:**
   - Test access from affected accounts
   - Confirm SCP detachment propagated
   - Document the incident and update change processes

### 11.6 Scenario: Multi-Account Cost Optimization

**Scenario:**

A growing company has 50+ AWS accounts with escalating costs. They need to:
- Understand cost distribution
- Implement cost allocation
- Optimize spending
- Set up budgets

**Recommended Approach:**

1. **Enable Consolidated Billing:**
   - Single payment account
   - Combined usage for volume discounts
   - Detailed billing reports

2. **Implement Tag Policies:**
   ```json
   {
     "TagPolicy": {
       "CostCenter": {
         "TagValue": {
           "@@assign": ["CC-100", "CC-200", "CC-300"]
         },
         "Compliance": {
           "@@report_non_compliant_resources": true
         }
       },
       "Project": {
         "TagValue": {
           "@@assign": ["ProjectA", "ProjectB", "ProjectC"]
         }
       }
     }
   }
   ```

3. **Set Up AWS Budgets:**
   - Organizational budget with member account breakdown
   - Alerts at 50%, 80%, 100% thresholds
   - Forecast-based alerts

4. **Cost Optimization Actions:**
   - Review unattached EBS volumes
   - Identify idle RDS instances
   - Analyze Reserved Instance coverage
   - Implement S3 lifecycle policies

---

## Conclusion

This document provides comprehensive coverage of AWS multi-account governance, from conceptual foundations through operational procedures. Understanding these principles enables effective design, implementation, and management of secure, compliant AWS environments.

Key takeaways:

1. Multi-account architecture provides blast radius containment, compliance alignment, and cost allocation
2. AWS Organizations enables centralized governance through policies
3. Service Control Policies define guardrails but do not grant permissions
4. Organizational Unit design should reflect organizational structure
5. Security services integrate across accounts for comprehensive protection
6. Operational excellence requires monitoring, incident response, and cost management

---

## References

- AWS Organizations SCP Evaluation: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_evaluation.html
- AWS Organizations Best Practices: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices.html
- OU Management Best Practices: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_ous_best-practices.html
- Management Account Best Practices: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices_mgmt-acct.html
- Control Tower Landing Zone: https://docs.aws.amazon.com/controltower/latest/userguide/aws-multi-account-landing-zone.html
- AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/
- Root Access Management: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html
- Consolidated Billing: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing.html
