# CI/CD Implementation: CodePipeline, CodeBuild, CodeDeploy

**Index:** [GOV-ARCH-001](GOV-ARCH-001-Architecture-Documentation-Index.md) | [CROSS_REFERENCE_INDEX.md](CROSS_REFERENCE_INDEX.md)  
**Related:** [AWS Comprehensive Guide](AWS_Solutions_Architect_Comprehensive_Guide.md) Section 9 (Serverless)  
**Related Supplements:** [Route 53](route53_implementation_supplement.md) (Blue/Green) | [Security](security_services_supplement.md) (pipeline security)  
**Domain:** Design for New Solutions (29%)

## Overview

CI/CD (Continuous Integration/Continuous Delivery) is critical for SA Pro Domain 2 (29% weight). This section covers implementation-level patterns, not just concepts.

### Related Documentation
- **[Architecture Patterns](files/architecture-patterns.md)** - Deployment patterns (Blue/Green, Canary)
- **[Service Decisions](files/service-decisions-enhanced.md)** - CI/CD service selection
- **[Well-Architected Pillars](files/well-architected-pillars.md)** - Operational Excellence pillar
- **[Route 53 Supplement](route53_implementation_supplement.md)** - DNS routing for deployments
- **[Cross-Reference Index](CROSS_REFERENCE_INDEX.md)** - Navigate by deployment strategy

---

## AWS CI/CD Service Architecture

### Service Relationships

```
Source (GitHub, CodeCommit, S3)
    |
    v
CodePipeline (Orchestration)
    |
    +-- Stage 1: Source
    |       |
    |       v
    |   CodeCommit/GitHub
    |
    +-- Stage 2: Build
    |       |
    |       v
    |   CodeBuild / Jenkins
    |
    +-- Stage 3: Deploy
            |
            v
        CodeDeploy (EC2/ECS/Lambda)
        OR
        CloudFormation / SAM
```

---

## CodePipeline Implementation

### Basic Pipeline Structure

**Architecture:**
```yaml
Pipeline:
  Source Stage:
    - CodeCommit Repository
    - Webhook trigger on push
  
  Build Stage:
    - CodeBuild Project
    - Build artifacts
    - Run tests
  
  Deploy Stage:
    - CodeDeploy Application
    - Deploy to ECS/EC2/Lambda
```

**Implementation:**
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: CI/CD Pipeline for Web Application

Resources:
  # CodeCommit Repository
  CodeRepository:
    Type: AWS::CodeCommit::Repository
    Properties:
      RepositoryName: web-app
      RepositoryDescription: Web application source code

  # CodeBuild Project
  BuildProject:
    Type: AWS::CodeBuild::Project
    Properties:
      Name: web-app-build
      ServiceRole: !GetAtt CodeBuildRole.Arn
      Artifacts:
        Type: CODEPIPELINE
      Environment:
        Type: LINUX_CONTAINER
        ComputeType: BUILD_GENERAL1_SMALL
        Image: aws/codebuild/amazonlinux2-x86_64-standard:4.0
        PrivilegedMode: true
        EnvironmentVariables:
          - Name: AWS_DEFAULT_REGION
            Value: !Ref AWS::Region
          - Name: ECR_REPOSITORY_URI
            Value: !Sub '${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/web-app'
      Source:
        Type: CODEPIPELINE
        BuildSpec: |
          version: 0.2
          phases:
            pre_build:
              commands:
                - echo Logging in to Amazon ECR...
                - aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REPOSITORY_URI
            build:
              commands:
                - echo Build started on `date`
                - echo Building the Docker image...
                - docker build -t web-app:latest .
                - docker tag web-app:latest $ECR_REPOSITORY_URI:latest
                - docker tag web-app:latest $ECR_REPOSITORY_URI:$CODEBUILD_BUILD_NUMBER
            post_build:
              commands:
                - echo Build completed on `date`
                - echo Pushing the Docker image...
                - docker push $ECR_REPOSITORY_URI:latest
                - docker push $ECR_REPOSITORY_URI:$CODEBUILD_BUILD_NUMBER
                - printf '{"ImageUri":"%s"}' $ECR_REPOSITORY_URI:latest > imageDetail.json
          artifacts:
            files:
              - imageDetail.json
              - taskdef.json
              - appspec.yaml

  # CodePipeline
  Pipeline:
    Type: AWS::CodePipeline::Pipeline
    Properties:
      Name: web-app-pipeline
      RoleArn: !GetAtt PipelineRole.Arn
      ArtifactStore:
        Type: S3
        Location: !Ref ArtifactBucket
      Stages:
        - Name: Source
          Actions:
            - Name: SourceAction
              ActionTypeId:
                Category: Source
                Owner: AWS
                Provider: CodeCommit
                Version: 1
              Configuration:
                RepositoryName: !GetAtt CodeRepository.Name
                BranchName: main
              OutputArtifacts:
                - Name: SourceCode
        
        - Name: Build
          Actions:
            - Name: BuildAction
              ActionTypeId:
                Category: Build
                Owner: AWS
                Provider: CodeBuild
                Version: 1
              Configuration:
                ProjectName: !Ref BuildProject
              InputArtifacts:
                - Name: SourceCode
              OutputArtifacts:
                - Name: BuildArtifact
        
        - Name: Deploy
          Actions:
            - Name: DeployAction
              ActionTypeId:
                Category: Deploy
                Owner: AWS
                Provider: ECS
                Version: 1
              Configuration:
                ClusterName: !Ref ECSCluster
                ServiceName: !Ref ECSService
                FileName: imageDetail.json
              InputArtifacts:
                - Name: BuildArtifact
```

### Multi-Account Pipeline

**Architecture:**
```
Development Account
    |
    +-- CodeCommit (Source)
    +-- CodeBuild (Unit Tests)
    +-- CodeDeploy (Dev Environment)
    |
    v
Staging Account (Cross-Account Role)
    |
    +-- CodeDeploy (Staging Environment)
    +-- Manual Approval
    |
    v
Production Account (Cross-Account Role)
    |
    +-- CodeDeploy (Production)
    +-- CloudWatch Alarms (Rollback trigger)
```

**Implementation - Cross-Account Role:**
```yaml
# In Staging/Production Account
CrossAccountRole:
  Type: AWS::IAM::Role
  Properties:
    RoleName: CodePipeline-CrossAccount-Role
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            AWS: arn:aws:iam::DEV-ACCOUNT-ID:root
          Action: sts:AssumeRole
    Policies:
      - PolicyName: CodeDeployAccess
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - codedeploy:*
                - ecs:*
                - s3:GetObject
              Resource: '*'
```

**Pipeline Configuration:**
```yaml
- Name: DeployToStaging
  Actions:
    - Name: DeployToStaging
      ActionTypeId:
        Category: Deploy
        Owner: AWS
        Provider: CodeDeploy
        Version: 1
      Configuration:
        ApplicationName: web-app
        DeploymentGroupName: staging-group
        RoleArn: arn:aws:iam::STAGING-ACCOUNT:role/CodePipeline-CrossAccount-Role
      InputArtifacts:
        - Name: BuildArtifact
```

---

## CodeDeploy Deployment Strategies

### 1. Blue/Green Deployment

**What It Is:**
- Maintain two identical environments (Blue = current, Green = new)
- Switch traffic from Blue to Green after validation
- Instant rollback by switching back

**Architecture:**
```
Current State (Blue):
    ALB
      |
      +-- Target Group: Blue (v1.0)
              |
              +-- EC2/ECS Instances (v1.0)

Deployment:
1. Create Green environment with v2.0
2. Test Green environment
3. Switch ALB to Green Target Group
4. Monitor
5. Terminate Blue (or keep for rollback)
```

**Implementation for ECS:**
```yaml
# appspec.yaml
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: <TASK_DEFINITION>
        LoadBalancerInfo:
          ContainerName: web-app
          ContainerPort: 80
        PlatformVersion: LATEST

# CodeDeploy Application
BlueGreenDeployment:
  Type: AWS::CodeDeploy::DeploymentGroup
  Properties:
    ApplicationName: web-app
    ServiceRoleArn: !GetAtt CodeDeployRole.Arn
    DeploymentConfigName: CodeDeployDefault.ECSAllAtOnce
    DeploymentStyle:
      DeploymentType: BLUE_GREEN
      DeploymentOption: WITH_TRAFFIC_CONTROL
    BlueGreenDeploymentConfiguration:
      TerminateBlueInstancesOnDeploymentSuccess:
        Action: TERMINATE
        TerminationWaitTimeInMinutes: 30
      DeploymentReadyOption:
        ActionOnTimeout: CONTINUE_DEPLOYMENT
        WaitTimeInMinutes: 0
    ECSAttributes:
      ClusterName: !Ref ECSCluster
      ServiceName: !Ref ECSService
    LoadBalancerInfo:
      TargetGroupPairInfoList:
        - TargetGroups:
            - Name: !Ref BlueTargetGroup
            - Name: !Ref GreenTargetGroup
          ProdTrafficRoute:
            ListenerArns:
              - !Ref ALBListener
```

**Traffic Shifting:**
```yaml
# AllAtOnce: 100% traffic immediately
DeploymentConfigName: CodeDeployDefault.ECSAllAtOnce

# Canary: 10% for 5 minutes, then 100%
DeploymentConfigName: CodeDeployDefault.ECSCanary10percent5Minutes

# Linear: 10% every minute until 100%
DeploymentConfigName: CodeDeployDefault.ECSLinear10PercentEvery1Minutes
```

### 2. Canary Deployment

**What It Is:**
- Deploy new version to small subset of users
- Monitor for errors
- Gradually increase traffic if healthy
- Automatic rollback if errors detected

**Architecture:**
```
ALB
  |
  +-- 90% Traffic -> Target Group A (v1.0)
  +-- 10% Traffic -> Target Group B (v2.0) [Canary]

After Validation:
ALB
  |
  +-- 100% Traffic -> Target Group B (v2.0)
```

**Implementation with Auto Rollback:**
```yaml
CanaryDeployment:
  Type: AWS::CodeDeploy::DeploymentGroup
  Properties:
    ApplicationName: web-app
    DeploymentConfigName: CodeDeployDefault.ECSCanary10percent5Minutes
    AutoRollbackConfiguration:
      Enabled: true
      Events:
        - DEPLOYMENT_FAILURE
        - ALARM
    AlarmConfiguration:
      Enabled: true
      Alarms:
        - Name: HighErrorRate
        - Name: HighLatency
      IgnorePollAlarmFailure: false
```

**CloudWatch Alarms for Rollback:**
```yaml
HighErrorRateAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: HighErrorRate
    MetricName: HTTPCode_Target_5XX_Count
    Namespace: AWS/ApplicationELB
    Statistic: Sum
    Period: 60
    EvaluationPeriods: 2
    Threshold: 10
    ComparisonOperator: GreaterThanThreshold
    Dimensions:
      - Name: LoadBalancer
        Value: !GetAtt ALB.LoadBalancerFullName
```

### 3. Rolling Deployment

**What It Is:**
- Gradually replace old instances with new ones
- Maintains capacity during deployment
- Built-in rollback capability

**Architecture:**
```
Initial: 4 instances (v1.0)
Step 1: Replace 1 instance -> 3 v1.0 + 1 v2.0
Step 2: Replace 1 instance -> 2 v1.0 + 2 v2.0
Step 3: Replace 1 instance -> 1 v1.0 + 3 v2.0
Step 4: Replace 1 instance -> 4 v2.0
```

**Implementation for EC2:**
```yaml
RollingDeployment:
  Type: AWS::CodeDeploy::DeploymentGroup
  Properties:
    ApplicationName: web-app
    DeploymentConfigName: CodeDeployDefault.OneAtATime
    # Or: CodeDeployDefault.HalfAtATime
    # Or: Custom configuration
    AutoScalingGroups:
      - !Ref AutoScalingGroup
    DeploymentStyle:
      DeploymentType: IN_PLACE
```

**Custom Deployment Config:**
```bash
aws deploy create-deployment-config \
  --deployment-config-name ThreeAtATime \
  --minimum-healthy-hosts type=HOST_COUNT,value=1
```

### 4. All-at-Once (In-Place)

**What It Is:**
- Deploy to all instances simultaneously
- Fastest deployment
- Highest risk (no gradual rollout)
- Brief downtime during switch

**Use Case:** Development environments, non-critical updates

**Implementation:**
```yaml
AllAtOnceDeployment:
  Type: AWS::CodeDeploy::DeploymentGroup
  Properties:
    ApplicationName: web-app
    DeploymentConfigName: CodeDeployDefault.AllAtOnce
```

---

## Deployment Strategy Selection Framework

### Decision Matrix

| Factor | Blue/Green | Canary | Rolling | All-at-Once |
|--------|-----------|--------|---------|-------------|
| **Zero Downtime** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ Brief |
| **Rollback Speed** | Instant | Gradual | Per-instance | Re-deploy |
| **Resource Cost** | 2x capacity | 10% extra | No extra | No extra |
| **Risk Level** | Low | Low | Medium | High |
| **Testing Window** | Full (Green) | Limited (10%) | Limited | None |
| **Complexity** | High | Medium | Low | Low |

### Selection Decision Tree

```
Can we afford 2x capacity during deployment?
├── YES -> Blue/Green (safest, instant rollback)
│   └── Need gradual rollout?
│       ├── YES -> Blue/Green with canary (10% to Green first)
│       └── NO -> Standard Blue/Green
└── NO -> In-place deployment
    ├── Need zero downtime?
    │   ├── YES -> Canary (10% traffic, monitor, scale)
    │   └── NO -> Rolling or All-at-Once
    └── Risk tolerance?
        ├── High risk acceptable -> All-at-Once (dev/test)
        └── Low risk required -> Rolling (controlled batches)
```

### SA Pro Exam Scenarios

**Scenario 1: E-commerce Production**
- Requirements: Zero downtime, instant rollback, high confidence
- **Answer:** Blue/Green with automated testing

**Scenario 2: Microservices with API Gateway**
- Requirements: Test new version with small user subset
- **Answer:** Canary deployment with CloudWatch alarms

**Scenario 3: Batch Processing Workers**
- Requirements: No downtime, cost-sensitive
- **Answer:** Rolling deployment with 25% at a time

**Scenario 4: Development Environment**
- Requirements: Fastest deployment, downtime OK
- **Answer:** All-at-Once

---

## Artifact Promotion Strategy

### Multi-Account Pipeline

**Flow:**
```
Build (Dev Account)
    |
    v
Store Artifact in S3 (with KMS encryption)
    |
    +-- Dev Deployment (auto)
    +-- Staging Deployment (after dev success)
    +-- Production Deployment (manual approval)
```

**Implementation:**
```yaml
# Artifact bucket with cross-account access
ArtifactBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketName: cicd-artifacts-cross-account
    BucketEncryption:
      ServerSideEncryptionConfiguration:
        - ServerSideEncryptionByDefault:
            SSEAlgorithm: aws:kms
            KMSMasterKeyID: !Ref ArtifactKey
    PolicyDocument:
      Statement:
        - Effect: Allow
          Principal:
            AWS: 
              - arn:aws:iam::STAGING-ACCOUNT:root
              - arn:aws:iam::PROD-ACCOUNT:root
          Action:
            - s3:GetObject
            - s3:GetObjectVersion
          Resource: !Sub '${ArtifactBucket.Arn}/*'
```

**Pipeline Stages:**
```yaml
Stages:
  - Name: Source
    # ... source action
  
  - Name: Build
    # ... build action
  
  - Name: DeployToDev
    Actions:
      - Name: Deploy
        # Deploy to dev ECS/EC2
  
  - Name: DeployToStaging
    Actions:
      - Name: Approve
        ActionTypeId:
          Category: Approval
          Owner: AWS
          Provider: Manual
          Version: 1
        Configuration:
          CustomData: "Approve deployment to staging"
          ExternalEntityLink: "https://dev.example.com"
      
      - Name: Deploy
        # Deploy to staging (cross-account)
  
  - Name: DeployToProd
    Actions:
      - Name: Approve
        ActionTypeId:
          Category: Approval
          Owner: AWS
          Provider: Manual
          Version: 1
        Configuration:
          CustomData: "Approve deployment to production"
      
      - Name: Deploy
        # Deploy to production (cross-account)
```

---

## Rollback Mechanisms

### Automatic Rollback Triggers

**1. CloudWatch Alarm Trigger:**
```yaml
AutoRollbackConfiguration:
  Enabled: true
  Events:
    - DEPLOYMENT_FAILURE
    - ALARM
AlarmConfiguration:
  Enabled: true
  Alarms:
    - Name: HighErrorRate
    - Name: HighLatency
    - Name: LowSuccessRate
```

**2. Automatic Rollback on Failure:**
```yaml
DeploymentGroup:
  Type: AWS::CodeDeploy::DeploymentGroup
  Properties:
    AutoRollbackConfiguration:
      Enabled: true
      Events:
        - DEPLOYMENT_FAILURE  # Rollback on deployment error
```

**3. Manual Rollback:**
```bash
# Roll back to previous revision
aws deploy create-deployment \
  --application-name web-app \
  --deployment-group-name production \
  --revision '{"revisionType":"S3","s3Location":{"bucket":"artifacts","key":"app-v1.0.zip","bundleType":"zip"}}' \
  --deployment-config-name CodeDeployDefault.AllAtOnce
```

### Rollback Strategy Comparison

| Strategy | Rollback Method | Time to Rollback | Data Loss |
|----------|----------------|------------------|-----------|
| Blue/Green | Switch target group | Instant | None |
| Canary | Reduce canary to 0% | 1-2 minutes | Minimal (canary traffic only) |
| Rolling | Replace back to old version | 5-15 minutes | Depends on batch size |
| All-at-Once | Re-deploy old version | 5-15 minutes | Transactions in flight |

---

## Infrastructure as Code in CI/CD

### CloudFormation in Pipeline

**Pipeline Stage:**
```yaml
- Name: UpdateInfrastructure
  Actions:
    - Name: CreateChangeSet
      ActionTypeId:
        Category: Deploy
        Owner: AWS
        Provider: CloudFormation
        Version: 1
      Configuration:
        ActionMode: CHANGE_SET_REPLACE
        StackName: web-app-stack
        ChangeSetName: pipeline-changeset
        TemplatePath: SourceCode::infrastructure/template.yaml
        RoleArn: !GetAtt CloudFormationRole.Arn
        Capabilities: CAPABILITY_IAM
    
    - Name: ExecuteChangeSet
      ActionTypeId:
        Category: Deploy
        Owner: AWS
        Provider: CloudFormation
        Version: 1
      Configuration:
        ActionMode: CHANGE_SET_EXECUTE
        StackName: web-app-stack
        ChangeSetName: pipeline-changeset
```

### Change Set Approval

**Best Practice:**
```
1. Create Change Set (shows what will change)
2. Manual Approval (review changes)
3. Execute Change Set (apply changes)
```

---

## Security in CI/CD

### Least Privilege Roles

**CodeBuild Service Role:**
```yaml
CodeBuildRole:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: codebuild.amazonaws.com
          Action: sts:AssumeRole
    Policies:
      - PolicyName: BuildPermissions
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            # Minimal permissions for build
            - Effect: Allow
              Action:
                - logs:CreateLogGroup
                - logs:CreateLogStream
                - logs:PutLogEvents
              Resource: 
                - !Sub 'arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/codebuild/*'
            
            - Effect: Allow
              Action:
                - s3:GetObject
                - s3:PutObject
              Resource: 
                - !Sub '${ArtifactBucket.Arn}/*'
            
            - Effect: Allow
              Action:
                - ecr:GetAuthorizationToken
                - ecr:BatchCheckLayerAvailability
                - ecr:GetDownloadUrlForLayer
                - ecr:BatchGetImage
                - ecr:PutImage
                - ecr:InitiateLayerUpload
                - ecr:UploadLayerPart
                - ecr:CompleteLayerUpload
              Resource: '*'
```

### Artifact Encryption

```yaml
ArtifactBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketEncryption:
      ServerSideEncryptionConfiguration:
        - ServerSideEncryptionByDefault:
            SSEAlgorithm: aws:kms
            KMSMasterKeyID: !Ref ArtifactKey
```

### Secrets Management

**Don't commit secrets to source control!**

**Use Systems Manager Parameter Store:**
```yaml
# In CodeBuild buildspec
version: 0.2
phases:
  pre_build:
    commands:
      - echo Getting secrets...
      - DATABASE_PASSWORD=$(aws ssm get-parameter --name /prod/database/password --with-decryption --query Parameter.Value --output text)
  build:
    commands:
      - echo Building with secrets...
      - docker build --build-arg DB_PASSWORD=$DATABASE_PASSWORD -t web-app .
```

---

## Monitoring CI/CD

### CloudWatch Metrics

**Key Metrics:**
- **Pipeline Executions:** Success/failure rate
- **Build Duration:** Time to build
- **Deployment Duration:** Time to deploy
- **Failed Deployments:** Rollback frequency

**Dashboard:**
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/CodePipeline", "PipelineExecutionSuccess", "PipelineName", "web-app-pipeline"],
          [".", "PipelineExecutionFailure", ".", "."]
        ],
        "period": 3600,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "Pipeline Executions"
      }
    }
  ]
}
```

### Pipeline Notifications

```yaml
PipelineSNSTopic:
  Type: AWS::SNS::Topic
  Properties:
    Subscription:
      - Protocol: email
        Endpoint: team@example.com

events:
  - RuleName: PipelineFailed
    EventPattern:
      source:
        - aws.codepipeline
      detail-type:
        - CodePipeline Pipeline Execution State Change
      detail:
        state:
          - FAILED
    Targets:
      - Arn: !Ref PipelineSNSTopic
        Id: PipelineFailedNotification
```

---

## Best Practices for SA Pro

### 1. Immutable Infrastructure

**Principle:** Don't modify existing resources; replace them

**Implementation:**
- Use Blue/Green deployments
- Treat infrastructure as cattle, not pets
- Version control everything

### 2. Shift Left Testing

**Implementation:**
```yaml
# In buildspec
phases:
  pre_build:
    commands:
      - echo Running security scan...
      - docker run --rm -v $(pwd):/app securecodewarrior/sast-scan
      
      - echo Running unit tests...
      - npm test
      
  build:
    commands:
      - echo Building...
      - docker build -t web-app .
      
  post_build:
    commands:
      - echo Running integration tests...
      - npm run test:integration
```

### 3. Automated Security Scanning

**Tools to Integrate:**
- Amazon ECR image scanning
- AWS Security Hub
- Third-party tools (SonarQube, Checkmarx)

### 4. Deployment Windows

**Use Events in CodeDeploy:**
```bash
aws deploy create-deployment-group \
  --application-name web-app \
  --deployment-group-name production \
  --deployment-config-name CodeDeployDefault.OneAtATime \
  --auto-scaling-groups my-asg \
  --trigger-configurations "triggerName=DeploymentWindow,triggerEvents=DeploymentSuccess,DeploymentFailure,triggerTargetArn=arn:aws:sns:us-east-1:123456789012:alerts"
```

---

*This section addresses the critical gap in CI/CD implementation for SA Pro Domain 2 (29% weight).*
