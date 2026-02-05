# Compliance Framework for AWS Solutions Architects

**Document ID:** pattern-compliance  
**Index:** [GOV-ARCH-001](../GOV-ARCH-001-Architecture-Documentation-Index.md)  
**Router:** [docs/patterns/compliance.md](../docs/patterns/compliance.md)  
**Related:** [well-architected-pillars.md](well-architected-pillars.md), [architecture-patterns.md](architecture-patterns.md), [CROSS_REFERENCE_INDEX.md](../CROSS_REFERENCE_INDEX.md)

## Purpose

This framework provides comprehensive compliance requirement gathering and mapping to AWS services. It ensures architectures meet regulatory requirements from the start rather than retrofitting compliance later.

### Related Documents
- **[Discovery Process](discovery-questions-enhanced.md)** - Phase 1 covers compliance discovery
- **[Well-Architected Pillars](well-architected-pillars.md)** - Security pillar closely aligns with compliance
- **[Architecture Patterns](architecture-patterns.md)** - Implement compliant patterns
- **[Service Decisions](service-decisions-enhanced.md)** - Select compliant services
- **[Cross-Reference Index](../CROSS_REFERENCE_INDEX.md)** - Navigate by regulation and service

---

## Compliance Discovery Process

### Step 1: Identify Regulatory Requirements

**Ask these questions to identify applicable regulations**:

1. **Industry & Geography**
   ```
   Industry Type:
   - Healthcare (HIPAA, HITECH)
   - Finance (PCI-DSS, SOX, FINRA)
   - Government (FedRAMP, FISMA)
   - International (GDPR, CCPA, PIPEDA)
   - Education (FERPA)
   - Energy (NERC CIP)
   ```

2. **Data Classification**
   ```
   Data Sensitivity Levels:
   - Public: No restrictions
   - Internal: Company use only
   - Confidential: Business sensitive
   - Restricted: Highly sensitive
   - PII/PHI: Personal/health information
   - Card Data: Payment card information
   ```

3. **Data Residency Requirements**
   ```
   Geographic Restrictions:
   - Data must remain within [country/region]
   - Cross-border transfer restrictions
   - Specific data center requirements
   - Sovereignty requirements
   ```

4. **Audit & Reporting**
   ```
   Compliance Needs:
   - Third-party audit requirements
   - Reporting frequency
   - Documentation standards
   - Evidence retention periods
   - Attestation requirements
   ```

### Step 2: Compliance Requirements Mapping

#### HIPAA (Healthcare)

**Requirements**:
- Protected Health Information (PHI) protection
- Access controls and audit trails
- Data encryption at rest and in transit
- Business Associate Agreements (BAAs)
- Incident notification procedures
- Backup and disaster recovery

**AWS Service Mapping**:
```
Encryption:
- KMS: Key management
- EBS: Volume encryption
- S3: Default encryption
- RDS: Encryption at rest and in transit
- Lambda: Environment variable encryption

Access Control:
- IAM: Fine-grained permissions
- Cognito: User authentication
- Directory Service: LDAP/Active Directory integration
- SSO: Single sign-on

Audit & Logging:
- CloudTrail: API audit trails
- CloudWatch: Logging and monitoring
- Config: Configuration tracking
- Security Hub: Centralized security management

Backup & DR:
- Backup: Automated backups
- S3: Cross-region replication
- Route 53: DNS failover
- Global Accelerator: Performance routing

BAA Support:
- AWS executes BAA with customers
- Covered services: [list from AWS documentation]
```

**Detailed Implementation Guide**:

1. **KMS Configuration for HIPAA**:
   ```
   # Create HIPAA-compliant KMS key
   aws kms create-key --description "HIPAA PHI Encryption Key" --tags Key=Compliance,Value=HIPAA
   aws kms create-alias --alias-name alias/hipaa-phi-key --target-key-id <key-id>
   
   # Configure key policy
   cat > key-policy.json <<EOF
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": { "AWS": "arn:aws:iam::<account-id>:root" },
         "Action": "kms:*",
         "Resource": "*"
       },
       {
         "Effect": "Allow",
         "Principal": { "AWS": "arn:aws:iam::<account-id>:role/hipaa-access-role" },
         "Action": [
           "kms:Encrypt",
           "kms:Decrypt",
           "kms:ReEncrypt*",
           "kms:GenerateDataKey*",
           "kms:DescribeKey"
         ],
         "Resource": "*"
       }
     ]
   }
   EOF
   
   aws kms put-key-policy --key-id <key-id> --policy-name default --policy file://key-policy.json
   ```

2. **S3 Bucket Configuration for PHI**:
   ```
   # Create HIPAA-compliant S3 bucket
   aws s3api create-bucket \
     --bucket <bucket-name> \
     --region us-east-1 \
     --tagging TagSet=[{Key=Compliance,Value=HIPAA}]
   
   # Enable default encryption with KMS key
   aws s3api put-bucket-encryption \
     --bucket <bucket-name> \
     --server-side-encryption-configuration '{
       "Rules": [
         {
           "ApplyServerSideEncryptionByDefault": {
             "SSEAlgorithm": "aws:kms",
             "KMSMasterKeyID": "arn:aws:kms:us-east-1:<account-id>:key/<key-id>"
           }
         }
       ]
     }'
   
   # Configure bucket policy for restricted access
   cat > bucket-policy.json <<EOF
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Deny",
         "Principal": "*",
         "Action": "s3:*",
         "Resource": [
           "arn:aws:s3:::<bucket-name>",
           "arn:aws:s3:::<bucket-name>/*"
         ],
         "Condition": {
           "Bool": { "aws:SecureTransport": "false" }
         }
       },
       {
         "Effect": "Allow",
         "Principal": { "AWS": "arn:aws:iam::<account-id>:role/hipaa-access-role" },
         "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
         "Resource": "arn:aws:s3:::<bucket-name>/*"
       }
     ]
   }
   EOF
   
   aws s3api put-bucket-policy --bucket <bucket-name> --policy file://bucket-policy.json
   ```

3. **RDS Configuration for PHI**:
   ```
   # Create HIPAA-compliant RDS instance
   aws rds create-db-instance \
     --db-instance-identifier hipaa-db \
     --allocated-storage 20 \
     --db-instance-class db.t3.medium \
     --engine mysql \
     --master-username admin \
     --master-user-password <password> \
     --kms-key-id <key-id> \
     --storage-encrypted \
     --vpc-security-group-ids <sg-id> \
     --tags Key=Compliance,Value=HIPAA
   
   # Enable automated backups
   aws rds modify-db-instance \
     --db-instance-identifier hipaa-db \
     --backup-retention-period 30 \
     --preferred-backup-window 02:00-03:00
   
   # Enable encryption in transit
   aws rds modify-db-instance \
     --db-instance-identifier hipaa-db \
     --enable-iam-database-authentication
   ```

#### PCI-DSS (Payments)

**Requirements**:
- Cardholder data protection
- Strong access control measures
- Regular security testing
- Secure network design
- Vulnerability management
- Security monitoring
- Documentation requirements

**AWS Service Mapping**:
```
Network Security:
- VPC: Network isolation
- Security Groups: Firewall rules
- NACLs: Network-level filtering
- WAF: Web application firewall
- Shield: DDoS protection

Data Protection:
- KMS: Card data encryption
- S3: Secure storage
- Lambda: No card data in code
- CloudHSM: Hardware security modules

Access Control:
- IAM: Role-based access
- MFA: Multi-factor authentication
- Secrets Manager: Credential management
- Directory Service: User management

Monitoring:
- Inspector: Security assessments
- GuardDuty: Threat detection
- Macie: Data discovery
- Security Hub: Compliance dashboard
```

#### GDPR (Data Privacy)

**Requirements**:
- Lawful processing basis
- Data subject rights
- Data protection by design
- Breach notification (72 hours)
- Data protection officer (DPO)
- Privacy by design and default
- Cross-border transfer controls

**AWS Service Mapping**:
```
Data Discovery:
- Macie: PII detection and classification
- Glue: Data catalog
- Lake Formation: Data governance
- Athena: Data access control

Data Protection:
- KMS: Encryption with customer keys
- RDS: Encryption and data masking
- S3: Object-level locking
- Lambda: Secure processing

Rights Management:
- Data Lifecycle: Automated deletion
- Config: Personal data tracking
- CloudTrail: Access logging
- IAM: Consent management

Cross-Border:
- Direct Connect: Controlled transfer
- S3 Transfer Acceleration: Fast transfers
- Global Infrastructure: Region selection
```

#### FedRAMP (Government)

**Requirements**:
- FIPS 140-2 encryption
- Continuous monitoring
- Incident response
- Security assessment
- Configuration management
- System and communications protection

**AWS Service Mapping**:
```
FIPS Endpoints:
- S3: FIPS-compliant endpoints
- KMS: FIPS 140-2 validated
- DynamoDB: FIPS endpoints
- RDS: FIPS-compliant endpoints

Authorization:
- IAM: Government-specific roles
- STS: Government federation
- Organizations: Account management
- Service Catalog: Approved services

Monitoring:
- CloudWatch GovCloud: Monitoring
- Config GovCloud: Configuration tracking
- CloudTrail GovCloud: Audit trails
- Security Hub GovCloud: Security management
```

### Step 3: Compliance Checklist Framework

#### Discovery Compliance Checklist

**Use this checklist during discovery**:

```
## Compliance Assessment: [Project Name]

### Applicable Regulations
□ HIPAA - Healthcare data
□ PCI-DSS - Payment data
□ GDPR - EU personal data
□ CCPA - California privacy
□ FedRAMP - Government data
□ SOX - Financial reporting
□ FERPA - Education records
□ NERC CIP - Energy sector
□ Other: [specify]

### Data Classification
□ Public data
□ Internal data
□ Confidential data
□ Restricted data
□ PII/Personal data
□ Health information (PHI)
□ Payment card data
□ Financial data

### Geographic Requirements
□ Data must remain in [country/region]
□ Cross-border transfer restricted
□ Specific data centers required
□ Sovereignty requirements

### Technical Requirements

Encryption at Rest:
□ Required for all data
□ Required for sensitive data only
□ Not required

Encryption in Transit:
□ Required for all data
□ Required for sensitive data only
□ Not required

Access Controls:
□ Multi-factor authentication required
□ Role-based access required
□ Attribute-based access required
□ Temporary access only

Audit Requirements:
□ API call logging required
□ Configuration change tracking required
□ Access review required
□ Security incident logging required

### AWS Service Constraints
□ Must use specific regions only
□ Must use GovCloud/FIPS endpoints
□ Must avoid certain services
□ Must use specific encryption keys
□ BAA agreements required
```

### Step 4: Compliance-Aware Architecture Design

#### Design Principles for Compliance

1. **Privacy by Design**
   - Minimize data collection
   - Anonymize where possible
   - Implement data retention policies
   - Enable easy data deletion

2. **Security First**
   - Zero-trust architecture
   - Encryption everywhere
   - Least privilege access
   - Comprehensive monitoring

3. **Audit Readiness**
   - All actions logged
   - Configuration changes tracked
   - Access reviews automated
   - Evidence preservation

4. **Data Governance**
   - Data classification automated
   - Access rights managed
   - Retention policies enforced
   - Cross-border controls in place

#### Compliance-Driven Service Selection

**Use this matrix for service selection**:

```
| Compliance Requirement | AWS Service | Implementation Notes |
|---------------------|---------------|---------------------|
| PHI encryption | KMS + S3 + RDS | Customer-managed keys for PHI |
| PCI data isolation | VPC + Security Groups | Separate VPC for card data |
| GDPR data discovery | Macie + Glue | Automated PII classification |
| FedRAMP monitoring | CloudWatch + Config | Continuous compliance monitoring |
| Audit trails | CloudTrail + Security Hub | Immutable audit logs |
| Access control | IAM + SSO | Just-in-time access provisioning |
```

### Step 5: Ongoing Compliance Management

#### Continuous Compliance Monitoring

**Implement these automated controls**:

1. **Configuration Compliance**
   - AWS Config rules for compliance checks
   - Automated remediation of violations
   - Compliance score tracking
   - Exception management workflow

2. **Access Compliance**
   - IAM access analyzer
   - Permission boundary enforcement
   - Access certification campaigns
   - Unused access removal

3. **Data Compliance**
   - Macie sensitive data discovery
   - Encryption verification
   - Data retention enforcement
   - Cross-border transfer monitoring

4. **Security Compliance**
   - GuardDuty threat detection
   - Inspector security assessments
   - Security Hub compliance checks
   - Vulnerability management

#### Compliance Reporting Framework

**Use this template for compliance reporting**:

```
## Compliance Report: [Time Period]

### Executive Summary
- Compliance Status: [Compliant/Non-compliant/In Progress]
- Critical Issues: [number]
- High Risk: [number]
- Medium Risk: [number]

### Regulatory Requirements
#### HIPAA
- Status: [Compliant/Non-compliant]
- Exceptions: [list]
- Remediation Plan: [timeline]

#### PCI-DSS
- Status: [Compliant/Non-compliant]
- Exceptions: [list]
- Remediation Plan: [timeline]

#### GDPR
- Status: [Compliant/Non-compliant]
- Data Subject Requests: [number processed]
- Data Breaches: [number/incidents]

### Technical Controls Status
- Encryption: [percentage of data encrypted]
- Access Control: [users with appropriate access]
- Monitoring: [percentage of systems monitored]
- Audit: [percentage of actions logged]

### Evidence of Compliance
- Audit Reports: [available/not available]
- Attestations: [current/expired]
- Certifications: [list with expiry dates]
- Third-party Assessments: [completed/pending]

### Improvement Actions
1. [Action 1] - [timeline] - [owner]
2. [Action 2] - [timeline] - [owner]
3. [Action 3] - [timeline] - [owner]
```

---

## Integration with AWS Documentation

**Always verify compliance requirements against current AWS guidance**:

1. **Check compliance programs**:
   ```
   MCP_DOCKER:search_documentation "[standard] AWS compliance program"
   ```

2. **Verify service capabilities**:
   ```
   MCP_DOCKER:search_documentation "[service name] compliance capabilities"
   ```

3. **Check regional requirements**:
   ```
   MCP_DOCKER:search_documentation "[standard] AWS region requirements"
   ```

4. **Review implementation guides**:
   ```
   MCP_DOCKER:search_documentation "[standard] implementation guide AWS"
   ```

This ensures compliance implementations meet current AWS capabilities and regulatory requirements.