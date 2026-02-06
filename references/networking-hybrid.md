# Networking & Hybrid Cloud Reference

**Document ID:** ref-networking-hybrid  
**Purpose:** SA Pro-level reference for advanced AWS networking scenarios

---

## Transit Gateway (TGW) Patterns

### Hub-and-Spoke Architecture

#### Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                      Transit Gateway                         │
│                                                           │
│    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐│
│    │   Spoke 1   │     │   Spoke 2   │     │   Spoke 3   ││
│    │   VPC-A     │     │   VPC-B     │     │   VPC-C     ││
│    └──────┬──────┘     └──────┬──────┘     └──────┬──────┘│
│           │                   │                   │        │
│           └───────────────────┼───────────────────┘        │
│                               │                            │
│                       ┌───────┴───────┐                   │
│                       │   Shared      │                   │
│                       │   Services    │                   │
│                       │   VPC         │                   │
│                       └───────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

#### TGW Configuration Best Practices

| Aspect | Recommendation | Rationale |
|--------|----------------|-----------|
| Route Tables | Use separate route tables per attachment | Security isolation |
| Attachments | Limit VPCs per TGW to < 50 | Operational complexity |
| Capacity | Monitor attachment limits | Scale planning |
| Monitoring | Use TGW Network Manager | Centralized visibility |

#### Route Table Strategies
```yaml
# Hub VPC Route Table (Shared Services)
hub_route_table:
  routes:
    - destination: 10.0.0.0/16      # Spoke 1
      attachment: attach-spoke-1
    - destination: 10.1.0.0/16      # Spoke 2
      attachment: attach-spoke-2
    - destination: 10.2.0.0/16      # Spoke 3
      attachment: attach-spoke-3

# Spoke VPC Route Table
spoke_route_table:
  routes:
    - destination: 10.0.0.0/8       # All TGW
      attachment: attach-tgw
```

### TGW Segmentation

#### Security Domain Isolation
| Domain | CIDR Blocks | Route Table | Use Case |
|--------|--------------|-------------|----------|
| Production | 10.0.0.0/16 | prod-rt | Production workloads |
| Staging | 10.1.0.0/16 | stage-rt | Pre-production testing |
| Development | 10.2.0.0/16 | dev-rt | Development environments |
| Shared Services | 10.10.0.0/16 | shared-rt | Common services |

#### TGW Attachments with Security Groups
```yaml
# TGW Connect Peering for cross-account
tgw_connect:
  peer_account_id: "123456789012"
  peer_tgw_id: "tgw-0123456789abcdef0"
  allowed_prefixes:
    - 10.0.0.0/16
```

### Multi-Region TGW

#### Cross-Region Architecture
```
┌──────────────────┐         ┌──────────────────┐
│   us-east-1     │         │   us-west-2      │
│   TGW-1         │◄───────►│   TGW-2         │
│   (Primary)     │ TGW PE  │   (Secondary)   │
└──────────────────┘         └──────────────────┘
         │                           │
         │ VPC                       │ VPC
    ┌────┴────┐                 ┌────┴────┐
    │ Prod VPC │                 │ DR VPC  │
    └──────────┘                 └─────────┘
```

## Direct Connect (DX) Patterns

### DX + VPN Failover

#### Architecture
```
┌─────────────────────────────────────────────────┐
│              On-Premises Data Center            │
│                                                 │
│  ┌─────────┐      ┌─────────┐                  │
│  │ Router 1 │──────│ Router 2 │                  │
│  └────┬────┘      └────┬────┘                  │
│       │                 │                       │
│       │  DX Connection  │  VPN Backup          │
│       │  (Primary)      │  (Failover)          │
│       └────────┬────────┘                       │
│                │                                │
└────────────────┼────────────────────────────────┘
                 │
            AWS Direct Connect
                 │
                 ▼
        ┌────────────────┐
        │   DX Gateway   │
        └───────┬────────┘
                │
        ┌───────┴───────┐
        │               │
   ┌────▼────┐     ┌────▼────┐
   │  VPC 1  │     │  VPC 2  │
   └─────────┘     └─────────┘
```

#### BGP Configuration
```yaml
# DX Virtual Interface BGP Configuration
virtual_interface:
  asn: 65001
  bgp_peering: "169.254.100.1/30"
  bgp_peer: "169.254.100.2"
  md5_secret: "${DX_BGP_SECRET}"
  
  # Failover configuration
  bgp_status:
    - interface: "dx-ifa-123"
      state: "UP"
      priority: 100
    - interface: "vgw-tunnel-456"
      state: "STANDBY"
      priority: 200
```

### DX Connection Types

| Type | Bandwidth | Use Case | Pricing |
|------|-----------|----------|---------|
| Dedicated | 1 Gbps, 10 Gbps | Enterprise workloads | Port hourly + outbound |
| Hosted | 50 Mbps - 10 Gbps | SMB, variable workloads | Port hourly + transfer |
| Hosted Connection | 1 Gbps - 10 Gbps | Service providers | Per Gbps rate |

### DX Resiliency Patterns

#### Single Connection with VPN Backup
```
Single DX (Primary)
     │
     ├── DX Connection ──► Primary path
     │
     └── VPN Tunnel ──► Fallback path (active standby)
```

#### Dual Location Resiliency
```
Location A           Location B
    │                   │
    ├── DX-1 ──────────┤
    │      (Primary)    │
    │                  │
    └── DX-2 ──────────┘
         (Secondary)
```

## Route 53 Resolver Hybrid DNS

### Inbound Resolver

#### Architecture
```
┌────────────────────────────────────────────────┐
│              On-Premises DNS                   │
│                                                │
│  ┌─────────────────┐                           │
│  │ DNS Resolver    │──────► Route 53 Resolver │
│  │                 │      Inbound Endpoint    │
│  └─────────────────┘              │            │
│                                  │ VPC        │
│                                  ▼            │
│                           ┌─────────────┐    │
│                           │   Private   │◄───┘
│                           │   Zones     │
│                           └─────────────┘
```

#### Inbound Endpoint Configuration
```yaml
route53_resolver_inbound:
  endpoint:
    name: "hybrid-dns-inbound"
    direction: "INBOUND"
    
  ip_addresses:
    - subnet_id: "subnet-12345"
      ip: "10.0.0.100"
    - subnet_id: "subnet-67890"
      ip: "10.0.1.100"
  
  security_group: "sg-resolver-inbound"
```

### Outbound Resolver

#### Architecture
```
┌────────────────────────────────────────────────┐
│              VPC DNS                          │
│                                                │
│  ┌─────────────────┐                           │
│  │   Application   │──────► Route 53 Resolver │
│  │   Servers      │      Outbound Endpoint   │
│  └─────────────────┘              │            │
│                                  │            │
│                                  ▼            │
│                           ┌─────────────┐    │
│                           │ Forward to   │───►
│                           │ On-Premises │   On-Premises
│                           │ DNS         │     DNS
│                           └─────────────┘
```

#### Outbound Endpoint Configuration
```yaml
route53_resolver_outbound:
  endpoint:
    name: "hybrid-dns-outbound"
    direction: "OUTBOUND"
  
  ip_addresses:
    - subnet_id: "subnet-dns"
      ip: "10.0.100.10"
  
  # Forwarding rules
  resolver_rules:
    - domain: "corp.company.com"
      target_ips:
        - "172.16.0.53"
        - "172.16.0.54"
```

### Hybrid DNS Architecture

#### Split-Brain DNS Considerations
| Scenario | Resolution Strategy | Configuration |
|----------|---------------------|---------------|
| Same domain in both environments | Conditional forwarding | Use resolver rules |
| Different subdomains | Direct delegation | NS records in Route 53 |
| Internal-only domains | Private hosted zones | Associate with VPCs |

## PrivateLink/Endpoint Services

### VPC Endpoints

#### Gateway Endpoints (S3, DynamoDB)
```yaml
# S3 Gateway Endpoint
s3_endpoint:
  service: "com.amazonaws.${REGION}.s3"
  type: "Gateway"
  
  route_table_associations:
    - "rtb-public"
    - "rtb-private-app"
  
  # Endpoint policy
  policy: |
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowSpecificBuckets",
          "Effect": "Allow",
          "Principal": "*",
          "Action": "s3:*",
          "Resource": [
            "arn:aws:s3:::company-data-*"
          ]
        }
      ]
    }
```

#### Interface Endpoints (AWS Services + SaaS)
```yaml
# Bedrock Interface Endpoint
bedrock_endpoint:
  service: "bedrock-runtime"
  type: "Interface"
  
  subnets:
    - "subnet-app-1"
    - "subnet-app-2"
  
  security_groups:
    - "sg-bedrock-access"
  
  private_dns:
    enabled: true
    dns_name: "bedrock-runtime.${REGION}.amazonaws.com"
```

### PrivateLink Architecture

#### Service Provider Model
```
┌─────────────────────────────────────────────────────┐
│                    Service Provider                  │
│                                                      │
│  ┌─────────────────┐    ┌─────────────────────────┐  │
│  │ Network Load   │───►│  Endpoint Service       │  │
│  │ Balancer       │    │  (PrivateLink)          │  │
│  └─────────────────┘    └───────────┬─────────────┘  │
└──────────────────────────────────────┼────────────────┘
                                       │
                                VPC Endpoint
                                       │
                                       ▼
┌─────────────────────────────────────────────────────┐
│                    Service Consumer                  │
│                                                      │
│  ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   Application   │───►│  VPC Endpoint           │  │
│  │   Servers      │    │  (Interface)            │  │
│  └─────────────────┘    └─────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

#### PrivateLink Configuration
```yaml
# Provider-side: Create Endpoint Service
endpoint_service:
  name: "company-ai-service"
  
  load_balancers:
    - "arn:aws:elasticloadbalancing:${REGION}:${ACCOUNT}:loadbalancer/net/ai-lb/xxx"
  
  # Acceptance required?
  acceptance_required: true
  
  # Allowed principals (consumer accounts)
  allowed_principals:
    - "arn:aws:iam::123456789012:root"

# Consumer-side: Create VPC Endpoint
vpc_endpoint:
  service_name: "com.amazonaws.${REGION}.company-ai-service"
  
  vpc: "vpc-app"
  
  subnet_ids:
    - "subnet-app-1"
    - "subnet-app-2"
  
  security_group_ids:
    - "sg-app-endpoint"
```

### Security Considerations

#### Endpoint Access Control
```yaml
# VPC Endpoint Policy Example
endpoint_policy:
  version: "2012-10-17"
  statement:
    - sid: "RestrictS3Access"
      effect: "Allow"
      principal: "*"
      action:
        - "s3:GetObject"
        - "s3:PutObject"
      resource:
        - "arn:aws:s3:::secure-bucket/*"
      condition:
        - string_equals:
            "aws:PrincipalOrgID": "o-1234567890"
```

## Network Security Patterns

### Firewall Manager Integration
```yaml
firewall_manager:
  policy:
    name: "network-security-policy"
    type: "NetworkShieldAdvanced"
    
    # Firewall policy configuration
    firewall_policy:
      network_shield_protection:
        - enable_ddos_protection: true
          automatic_routing: true
```

### VPC Flow Logs Analysis
```yaml
flow_logs:
  destination: "cloud-watch-logs"
  log_format: |
    ${version} ${account-id} ${interface-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status}
  
  # Traffic analysis
  analyze_with_inspector: true
```
