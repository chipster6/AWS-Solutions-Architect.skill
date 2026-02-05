# Route 53: Implementation Guide with Health Checks and Failover

**Index:** [GOV-ARCH-001](GOV-ARCH-001-Architecture-Documentation-Index.md) | [CROSS_REFERENCE_INDEX.md](CROSS_REFERENCE_INDEX.md)  
**Related:** [AWS Comprehensive Guide](AWS_Solutions_Architect_Comprehensive_Guide.md) Section 5 (Networking)  
**Related Supplements:** [DRS](drs_implementation_supplement.md) (failover) | [Container Networking](container_networking_supplement.md) (ingress)  
**Domain:** Design for New Solutions (29%)

## Overview

Route 53 routing policies are commonly understood, but SA Pro requires implementation-level knowledge: health check configurations, failover procedures, and operational steps.

### Related Documentation
- **[Architecture Patterns](files/architecture-patterns.md)** - High availability patterns
- **[Well-Architected Pillars](files/well-architected-pillars.md)** - Reliability pillar (failover)
- **[DRS Supplement](drs_implementation_supplement.md)** - Automated failover integration
- **[Cross-Reference Index](CROSS_REFERENCE_INDEX.md)** - Navigate by routing policy and use case

---

## Route 53 Health Checks

### Health Check Types

**1. Endpoint Health Checks**
- Monitor endpoint (IP address or domain name)
- HTTP, HTTPS, or TCP protocols
- Configurable thresholds and intervals

**2. CloudWatch Alarm Health Checks**
- Monitor CloudWatch alarm status
- Useful for complex health logic
- Can monitor RDS, ELB, etc.

**3. Calculated Health Checks**
- Combine multiple health checks with AND/OR logic
- Example: Healthy if (Check1 AND Check2) OR Check3

**4. Routing Control Health Checks (ARC)**
- Used with Application Recovery Controller
- Manual failover control
- Multi-region disaster recovery

### Creating Endpoint Health Checks

**Step-by-Step Implementation:**

**Step 1: Create Basic Health Check**
```bash
aws route53 create-health-check \
  --caller-reference $(date +%s) \
  --health-check-config '{
    "IPAddress": "192.0.2.1",
    "Port": 443,
    "Type": "HTTPS",
    "ResourcePath": "/health",
    "FullyQualifiedDomainName": "api.example.com",
    "RequestInterval": 30,
    "FailureThreshold": 3
  }'
```

**Step 2: Configure CloudWatch Alarm**
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name route53-health-check-failed \
  --alarm-description "Route 53 health check failed" \
  --namespace AWS/Route53 \
  --metric-name HealthCheckStatus \
  --dimensions Name=HealthCheckId,Value=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx \
  --statistic Minimum \
  --period 60 \
  --evaluation-periods 1 \
  --threshold 1 \
  --comparison-operator LessThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:alerts
```

**Configuration Parameters:**

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| RequestInterval | Seconds between checks | 30 (fast) or 10 (standard) |
| FailureThreshold | Consecutive failures to mark unhealthy | 3 |
| ResourcePath | URL path for HTTP/HTTPS | /health |
| Port | TCP port | 80, 443, etc. |

**Fast vs Standard Interval:**
- **Fast (10 seconds):** Lower RTO, higher cost ($1/check/month)
- **Standard (30 seconds):** Higher RTO, lower cost ($0.50/check/month)

### Health Check Advanced Features

**String Matching (HTTP/HTTPS):**
```json
{
  "Type": "HTTPS",
  "ResourcePath": "/health",
  "SearchString": "healthy",
  "FailureThreshold": 3
}
```
- Route 53 looks for "healthy" in response body
- If string not found = unhealthy

**Alarm-Based Health Check:**
```bash
aws route53 create-health-check \
  --caller-reference $(date +%s) \
  --health-check-config '{
    "Type": "CLOUDWATCH_METRIC",
    "AlarmIdentifier": {
      "Region": "us-east-1",
      "Name": "rds-cpu-high"
    }
  }'
```

---

## Failover Routing Implementation

### Active-Passive Failover

**Architecture:**
```
Primary Region: us-east-1
    |
    +-- ALB (Primary)
    +-- Health Check: Healthy
    |
    v
Users -> Route 53 -> Primary ALB

(During Failure)

Primary Region: us-east-1
    |
    +-- ALB (Primary)
    +-- Health Check: UNHEALTHY
    |
    v
Users -> Route 53 -> Secondary ALB (us-west-2)
```

**Implementation Steps:**

**Step 1: Create Health Checks**
```bash
# Primary health check
aws route53 create-health-check \
  --caller-reference primary-$(date +%s) \
  --health-check-config '{
    "IPAddress": "198.51.100.1",
    "Port": 443,
    "Type": "HTTPS",
    "ResourcePath": "/health",
    "FullyQualifiedDomainName": "primary.example.com"
  }'

# Secondary health check (optional but recommended)
aws route53 create-health-check \
  --caller-reference secondary-$(date +%s) \
  --health-check-config '{
    "IPAddress": "203.0.113.1",
    "Port": 443,
    "Type": "HTTPS",
    "ResourcePath": "/health",
    "FullyQualifiedDomainName": "secondary.example.com"
  }'
```

**Step 2: Create Failover Records**
```bash
# Primary record
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "app.example.com",
        "Type": "A",
        "SetIdentifier": "Primary",
        "Failover": "PRIMARY",
        "HealthCheckId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "AliasTarget": {
          "HostedZoneId": "Z35SXDOTRQ7X7K",
          "DNSName": "primary-alb-123456789.us-east-1.elb.amazonaws.com.",
          "EvaluateTargetHealth": true
        }
      }
    }]
  }'

# Secondary record
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "app.example.com",
        "Type": "A",
        "SetIdentifier": "Secondary",
        "Failover": "SECONDARY",
        "HealthCheckId": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy",
        "AliasTarget": {
          "HostedZoneId": "Z18D5FSROUN65G",
          "DNSName": "secondary-alb-987654321.us-west-2.elb.amazonaws.com.",
          "EvaluateTargetHealth": true
        }
      }
    }]
  }'
```

**Step 3: Verify Configuration**
```bash
# Check record sets
aws route53 list-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --query "ResourceRecordSets[?Name=='app.example.com.']"

# Test DNS resolution
dig app.example.com
nslookup app.example.com
```

**Step 4: Test Failover**
```bash
# Simulate primary failure (stop application or block health check)
# Monitor failover time
while true; do
  dig +short app.example.com
  sleep 5
done

# Should switch to secondary IP after ~3 failures (90 seconds with 30s interval)
```

### Multi-Region Failover with CloudFront

**Architecture:**
```
Users
  |
  v
CloudFront (Edge caching + global presence)
  |
  +-- Origin Group:
      |
      +-- Primary: ALB us-east-1 (Health Check)
      +-- Secondary: ALB us-west-2 (Health Check)
```

**Implementation:**

**Step 1: Create Origin Group in CloudFront**
```bash
aws cloudfront create-distribution \
  --origin-groups '{
    "Quantity": 1,
    "Items": [{
      "Id": "origin-group-1",
      "FailoverCriteria": {
        "StatusCodes": {
          "Quantity": 4,
          "Items": [500, 502, 503, 504]
        }
      },
      "Members": {
        "Quantity": 2,
        "Items": [
          {"OriginId": "primary-alb"},
          {"OriginId": "secondary-alb"}
        ]
      }
    }]
  }' \
  --origins '{
    "Quantity": 2,
    "Items": [
      {
        "Id": "primary-alb",
        "DomainName": "primary-alb-123456789.us-east-1.elb.amazonaws.com",
        "CustomOriginConfig": {
          "HTTPPort": 80,
          "HTTPSPort": 443,
          "OriginProtocolPolicy": "https-only"
        }
      },
      {
        "Id": "secondary-alb",
        "DomainName": "secondary-alb-987654321.us-west-2.elb.amazonaws.com",
        "CustomOriginConfig": {
          "HTTPPort": 80,
          "HTTPSPort": 443,
          "OriginProtocolPolicy": "https-only"
        }
      }
    ]
  }'
```

**Step 2: Configure Route 53 for CloudFront**
```bash
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "app.example.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z2FDTNDATAQYW2",
          "DNSName": "d1234.cloudfront.net.",
          "EvaluateTargetHealth": false
        }
      }
    }]
  }'
```

**Benefits:**
- CloudFront handles origin failover (faster than DNS TTL)
- Global edge caching
- No DNS propagation delay

---

## Routing Policy Selection Guide

### Decision Matrix

| Scenario | Recommended Policy | RTO | Use Case |
|----------|-------------------|-----|----------|
| Single endpoint | Simple | N/A | Static websites |
| Load balancing | Weighted | N/A | A/B testing, gradual rollouts |
| Geo-targeting | Geolocation | DNS TTL | Content localization |
| Latency optimization | Latency | DNS TTL | Global applications |
| High availability | Failover | 30-90s | DR scenarios |
| Regional preference | Geoproximity | DNS TTL | Shift traffic between regions |

### Anti-Patterns

**1. Long TTL with Failover:**
```
TTL: 3600 seconds (1 hour)
Problem: Clients cache unhealthy endpoint for 1 hour!

Fix: Use 60 second TTL for failover records
```

**2. No Health Checks with Failover:**
```
Failover routing without health checks
Problem: Route 53 can't detect failures

Fix: Always attach health checks to failover records
```

**3. Single Point of Failure in Health Check:**
```
Health check checks /health endpoint
But /health only checks local server, not database

Fix: Comprehensive health checks (app + dependencies)
```

---

## Testing and Validation

### Pre-Production Checklist

**1. Health Check Validation:**
```bash
# Test endpoint directly
curl -v https://primary.example.com/health

# Verify response time (should be < 2 seconds for Route 53)
time curl https://primary.example.com/health
```

**2. DNS Resolution Test:**
```bash
# Test from different locations
dig @8.8.8.8 app.example.com
dig @1.1.1.1 app.example.com

# Check all record types
dig A app.example.com
dig AAAA app.example.com
```

**3. Failover Simulation:**
```bash
# Block health check endpoint on primary
iptables -A INPUT -p tcp --dport 443 -j DROP

# Monitor DNS resolution
watch -n 5 'dig +short app.example.com'

# Verify traffic shifts to secondary
# (Should see secondary IP after ~90 seconds)
```

**4. Recovery Test:**
```bash
# Restore primary
iptables -D INPUT -p tcp --dport 443 -j DROP

# Verify traffic returns to primary
# (After primary passes 3 consecutive health checks)
```

### Monitoring and Alerting

**CloudWatch Metrics:**
```bash
# Health check status metric
aws cloudwatch get-metric-statistics \
  --namespace AWS/Route53 \
  --metric-name HealthCheckStatus \
  --dimensions Name=HealthCheckId,Value=xxxxxxxx \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 60 \
  --statistics Minimum
```

**Health Check Status Values:**
- **1:** Healthy
- **0:** Unhealthy

**Alarms to Set:**
1. Health check failing for > 5 minutes
2. DNS query volume drop (indicates failover)
3. Latency increase on health checks

---

## Multi-Region Failover Design Pattern

### Architecture Decision Checklist

**Step 1: Determine RTO/RPO Requirements**
```
RTO: How long can we be down?
├── < 1 minute: Active-Active with Route 53 + Global Accelerator
├── 1-5 minutes: Active-Passive with Route 53 failover
├── 5-30 minutes: Warm standby
└── > 30 minutes: Pilot light or Backup & Restore

RPO: How much data can we lose?
├── 0: Synchronous replication (Aurora Global, DynamoDB Global)
├── < 1 minute: Asynchronous with low lag
└── > 1 minute: Backup-based recovery
```

**Step 2: State Replication Strategy**
```
Database:
├── Aurora: Use Aurora Global Database
├── DynamoDB: Use Global Tables
├── RDS: Cross-region read replicas
└── Self-managed: DMS or native replication

Storage:
├── S3: Cross-Region Replication (CRR)
├── EFS: Cross-region replication
└── EBS: Snapshots copied to DR region
```

**Step 3: Client Distribution**
```
Global users:
├── Use latency-based routing
├── Or geolocation routing
└── Consider Global Accelerator for TCP/UDP

Regional users:
├── Use failover routing
└── Route all traffic to one region
```

**Step 4: Testing Plan**
```
Monthly:
├── Failover drill (Route 53 switch)
├── Database replication lag test
└── RTO measurement

Quarterly:
├── Full DR test (complete recovery)
├── Failback procedure
└── Update runbooks
```

---

## Integration with Other Services

### Route 53 + Global Accelerator

**When to Use Global Accelerator Instead:**
- Need static IP addresses
- TCP/UDP applications (not HTTP/HTTPS)
- Need instant failover (no DNS propagation)
- Gaming, VoIP, financial trading

**Architecture:**
```
Users
  |
  v
Global Accelerator (2 static Anycast IPs)
  |
  +-- Endpoint Group: us-east-1 (Health Check)
  +-- Endpoint Group: us-west-2 (Health Check)
```

**Comparison:**
| Feature | Route 53 Failover | Global Accelerator |
|---------|------------------|-------------------|
| Failover Speed | 30-90 seconds | Instant |
| Static IPs | No | Yes |
| Protocols | HTTP/HTTPS | Any (TCP/UDP) |
| Cost | Lower | Higher |
| Use Case | Web apps | Real-time apps |

### Route 53 + Application Recovery Controller (ARC)

**Use Case:** Multi-region active-active with manual failover control

**Benefits:**
- Manual routing control
- Safety rules (prevent accidental failover)
- Routing controls across regions

**Implementation:**
```bash
# Create routing control
aws route53-recovery-control-config create-routing-control \
  --cluster-arn arn:aws:route53-recovery-control::123456789012:cluster/xxx \
  --routing-control-name primary-region

# Create safety rule
aws route53-recovery-control-config create-safety-rule \
  --control-panel-arn arn:aws:route53-recovery-control::123456789012:controlpanel/xxx \
  --assertion-rule '{
    "Name": "prevent-multiple-regions",
    "WaitPeriodMs": 5000,
    "AssertedControls": ["control1", "control2"],
    "RuleConfig": {
      "Type": "ATLEAST",
      "Threshold": 1
    }
  }'
```

---

## Troubleshooting Common Issues

### Issue 1: Failover Not Occurring

**Symptoms:** Primary is down but traffic still routed there

**Checklist:**
1. ✅ Health check is attached to record
2. ✅ Health check is actually failing (check CloudWatch)
3. ✅ Record has EvaluateTargetHealth = true (for ALB/CloudFront)
4. ✅ TTL is low enough (60 seconds recommended)
5. ✅ Client DNS cache is cleared

**Debug Commands:**
```bash
# Check health check status
aws route53 get-health-check-status \
  --health-check-id xxxxxxxx

# Check record configuration
aws route53 list-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --query "ResourceRecordSets[?Name=='app.example.com.']"
```

### Issue 2: Intermittent Failover

**Symptoms:** Constantly switching between primary and secondary

**Causes:**
- Health check threshold too low
- Endpoint is flaky (intermittent 500 errors)
- Network instability

**Fix:**
```bash
# Increase failure threshold
aws route53 update-health-check \
  --health-check-id xxxxxxxx \
  --failure-threshold 5  # Was 3
```

### Issue 3: Failback Not Working

**Symptoms:** Traffic doesn't return to primary after recovery

**Checklist:**
1. ✅ Primary health check shows healthy for > 3 consecutive checks
2. ✅ Primary record is PRIMARY (not SECONDARY)
3. ✅ No client-side caching issues

**Note:** Route 53 doesn't automatically failback on DNS level - it's preference-based, not sticky.

---

*This section addresses the critical implementation gap in Route 53 failover for SA Pro certification.*
