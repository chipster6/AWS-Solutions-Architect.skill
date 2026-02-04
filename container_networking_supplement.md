# AWS Solutions Architect: Container Networking Deep Dive

## Overview

Container networking extends beyond traditional VPC networking. ECS and EKS have specific networking patterns that SA Pro architects must master.

---

## Amazon ECS Networking

### Network Modes

ECS supports multiple network modes, each with different use cases and implications:

#### **awsvpc Mode (Recommended)**

**What It Is:**
Each task gets its own Elastic Network Interface (ENI) with a private IP address from the VPC.

**Architecture:**
```
VPC Subnet
    |
    +-- ENI 1 (Task A) - 10.0.1.10
    |       +-- Container 1
    |       +-- Container 2 (same task)
    |
    +-- ENI 2 (Task B) - 10.0.1.11
    |       +-- Container 1
    |
    +-- ENI 3 (Task C) - 10.0.1.12
```

**Key Characteristics:**
- **Security:** Each task can have its own security group
- **Monitoring:** VPC Flow Logs see each task individually
- **Connectivity:** Tasks communicate over the VPC network
- **Limitation:** ENI quota per instance type (e.g., t3.large = 3 ENIs = 3 tasks)

**Implementation:**
```json
{
  "family": "web-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["EC2"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "web",
      "image": "nginx:latest",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

**ENI Quota Considerations:**
| Instance Type | Max ENIs | Max Tasks (awsvpc) |
|---------------|----------|-------------------|
| t3.micro | 2 | 2 |
| t3.small | 3 | 3 |
| t3.medium | 3 | 3 |
| t3.large | 3 | 3 |
| m5.large | 3 | 3 |
| m5.xlarge | 4 | 4 |

**When to Use awsvpc:**
- ✅ Microservices requiring fine-grained security
- ✅ Compliance requirements (audit each task)
- ✅ Service-to-service communication within VPC
- ❌ Not for: High-density workloads (limited by ENI quota)

#### **bridge Mode (Default for Linux)**

**What It Is:**
Uses Docker's built-in bridge network. All containers on the same host share the host's ENI.

**Architecture:**
```
EC2 Instance (ENI: 10.0.1.10)
    |
    +-- Docker Bridge Network
        |
        +-- Task A Container 1 (172.17.0.2)
        +-- Task A Container 2 (172.17.0.3)
        +-- Task B Container 1 (172.17.0.4)
```

**Key Characteristics:**
- **Port Mapping:** Requires hostPort:containerPort mapping
- **Density:** Can run many more tasks (limited by CPU/memory, not ENIs)
- **Security:** All tasks share host security group
- **Connectivity:** Tasks communicate via host's network

**Port Mapping Conflict:**
```
# BAD: Two tasks with same hostPort
Task 1: hostPort: 80, containerPort: 80
Task 2: hostPort: 80, containerPort: 80  # CONFLICT!

# GOOD: Dynamic hostPort
Task 1: hostPort: 0 (random), containerPort: 80
Task 2: hostPort: 0 (random), containerPort: 80
```

**When to Use bridge:**
- ✅ High-density workloads
- ✅ Legacy applications
- ✅ When ENI quota is a concern
- ❌ Not for: Fine-grained security requirements

#### **host Mode**

**What It Is:**
Container uses the host's network directly (no network isolation).

**Characteristics:**
- No port mapping needed
- Container port = Host port
- Limited to one task per port per host

**When to Use:**
- ✅ Maximum network performance
- ✅ Specific networking requirements
- ❌ Not for: Multi-task scenarios (port conflicts)

### ECS Service Discovery

**Problem:**
```
Service A needs to call Service B
With awsvpc mode, each task has a different IP
How does Service A find Service B tasks?
```

**Solution: AWS Cloud Map**

**Architecture:**
```
ECS Service B (3 tasks)
    |
    v
Cloud Map Service Registry ("service-b.namespace")
    |-- 10.0.1.10 (Task 1)
    |-- 10.0.1.11 (Task 2)
    |-- 10.0.1.12 (Task 3)
    |
    v
ECS Service A (calls "service-b.namespace")
```

**Implementation:**
```yaml
Service:
  Type: AWS::ECS::Service
  Properties:
    ServiceName: service-b
    ServiceRegistries:
      - RegistryArn: !GetAtt CloudMapService.Arn
    # ... other properties

CloudMapService:
  Type: AWS::ServiceDiscovery::Service
  Properties:
    Name: service-b
    NamespaceId: !Ref CloudMapNamespace
    DnsConfig:
      RoutingPolicy: MULTIVALUE
      DnsRecords:
        - Type: A
          TTL: 60
```

**DNS Resolution:**
- **MULTIVALUE:** Returns all IPs (client-side load balancing)
- **WEIGHTED:** Route 53 weighted routing

### ECS Private Connectivity Patterns

**Pattern 1: Internal-Only Services**
```
Internet
    |
    v
ALB (Public Subnet) - Only entry point
    |
    v
ECS Tasks (Private Subnet) - No direct internet
    |
    +-- Service A (Internal ALB)
        |
        +-- Service B (awsvpc mode)
        +-- Service C (awsvpc mode)
```

**Pattern 2: VPC Endpoints for Dependencies**
```
ECS Tasks (Private Subnet)
    |
    +-- VPC Endpoint (S3) ----> S3
    +-- VPC Endpoint (DynamoDB) -> DynamoDB
    +-- VPC Endpoint (ECR) ---> ECR (for images)
    +-- NAT Gateway ----------> Internet (if needed)
```

**Security Best Practices:**
1. **Security Groups:**
   - ALB: Allow 80/443 from internet
   - ECS Tasks: Allow traffic only from ALB security group
   - Database: Allow traffic only from ECS tasks security group

2. **Network ACLs:**
   - Keep ECS subnet NACLs open (security groups handle it)
   - Use NACLs for broad restrictions (e.g., block specific IP ranges)

---

## Amazon EKS Networking

### VPC CNI Plugin

**What It Is:**
The Amazon VPC CNI plugin assigns real VPC IP addresses to each Pod.

**Architecture:**
```
VPC (10.0.0.0/16)
    |
    +-- Node 1 (m5.large)
    |       |
    |       +-- ENI 1 (primary) - 10.0.1.10
    |       |       +-- Pod 1 (10.0.1.11)
    |       |       +-- Pod 2 (10.0.1.12)
    |       |       +-- Pod 3 (10.0.1.13)
    |       |
    |       +-- ENI 2 (secondary) - 10.0.1.20
    |               +-- Pod 4 (10.0.1.21)
    |               +-- Pod 5 (10.0.1.22)
    |               +-- Pod 6 (10.0.1.23)
    |
    +-- Node 2
            +-- ENI 1 (primary)
                    +-- Pod 7
                    +-- Pod 8
```

**IP Allocation:**
- Each ENI has a primary IP + multiple secondary IPs
- Each Pod gets one secondary IP
- Instance type determines max Pods (based on ENI limits)

**Max Pods Formula:**
```
Max Pods = (Number of ENIs × IPs per ENI) - 1 (for primary IP)

Example: m5.large
- ENIs: 3
- IPs per ENI: 10
- Max Pods = (3 × 10) - 1 = 29
```

**Common Max Pods:**
| Instance Type | ENIs | IPs/ENI | Max Pods |
|---------------|------|---------|----------|
| t3.medium | 3 | 6 | 17 |
| m5.large | 3 | 10 | 29 |
| m5.xlarge | 4 | 15 | 58 |
| m5.2xlarge | 4 | 15 | 58 |

### IP Exhaustion Problem

**Problem:**
```
VPC CIDR: 10.0.0.0/20 (4096 IPs)
    |
    +-- Subnet A: 10.0.0.0/22 (1024 IPs)
    |       +-- Node 1: 50 Pods
    |       +-- Node 2: 50 Pods
    |       +-- Node 3: 50 Pods
    |       ...
    |       # After 20 nodes: IP exhaustion!
```

**Solutions:**

1. **Prefix Delegation (Recommended for high-density):**
   - Assigns /28 prefixes instead of individual IPs
   - Increases Pod density
   - Available in VPC CNI v1.9.0+

2. **Custom Networking:**
   - Use secondary CIDR blocks for Pods
   - Separate network for Pods from nodes

3. **ENIConfig:**
   ```yaml
   apiVersion: crd.k8s.amazonaws.com/v1alpha1
   kind: ENIConfig
   metadata:
     name: us-east-1a
   spec:
     securityGroups:
       - sg-xxxxxxxx
     subnet: subnet-xxxxxxxx
   ```

### EKS Ingress Patterns

**Pattern 1: AWS Load Balancer Controller (ALB)**

**Architecture:**
```
Internet
    |
    v
ALB (Application Load Balancer)
    |-- Path: /api/* -> Service A
    |-- Path: /web/* -> Service B
    |
    v
Target Group (IP mode)
    |-- Pod 1 (10.0.1.11)
    |-- Pod 2 (10.0.1.12)
```

**Ingress Resource:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
spec:
  ingressClassName: alb
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

**Target Types:**
- **instance:** Targets NodePort on EC2 instances (works with any CNI)
- **ip:** Targets Pod IPs directly (requires VPC CNI, more efficient)

**Pattern 2: Network Load Balancer (NLB)**

**Use Case:** TCP/UDP traffic, static IPs, preserve client IP

**Service:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: tcp-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
spec:
  type: LoadBalancer
  selector:
    app: tcp-app
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
```

### Internal-Only Clusters

**Architecture:**
```
Private Subnets Only (no public subnets)
    |
    +-- EKS Control Plane (AWS managed, public endpoint disabled)
    +-- Worker Nodes (no public IPs)
    +-- Internal ALB/NLB
```

**Access Patterns:**
1. **Bastion Host:** Jump box in public subnet
2. **VPN/Direct Connect:** Access from corporate network
3. **AWS Systems Manager Session Manager:** Secure shell without bastion

### EKS Security Boundaries

**Network Policies (CNI/Calico):**

**Default:** All Pods can communicate with all other Pods

**With Network Policies:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: frontend
      ports:
        - protocol: TCP
          port: 8080
```

**This Policy:**
- Allows traffic to "api" Pods only from "frontend" namespace
- Denies all other traffic (including from same namespace)

---

## Container Networking Decision Framework

### ECS vs EKS vs Lambda: Networking Comparison

| Aspect | ECS (awsvpc) | ECS (bridge) | EKS | Lambda |
|--------|-------------|--------------|-----|--------|
| IP per Task/Pod | ✅ Yes | ❌ No | ✅ Yes | N/A |
| Security Group per Task | ✅ Yes | ❌ No | ❌ No (Node level) | N/A |
| Service Discovery | Cloud Map | Cloud Map | DNS/Kubernetes | Event-driven |
| Load Balancing | ALB/NLB | ALB/NLB | ALB/NLB/Ingress | API Gateway |
| Network Isolation | Task-level | Host-level | Pod-level | Function-level |
| ENI Limit Impact | Yes | No | Yes | N/A |

### Decision Tree

```
Need Kubernetes ecosystem?
├── YES -> Use EKS
│   ├── Need fine-grained network policies?
│   │   ├── YES -> Use Calico CNI
│   │   └── NO -> VPC CNI is fine
│   └── Need custom ingress controller?
│       ├── YES -> Deploy NGINX/Traefik
│       └── NO -> Use AWS Load Balancer Controller
└── NO -> Use ECS
    ├── Need task-level security groups?
    │   ├── YES -> awsvpc mode
    │   └── NO -> bridge mode (higher density)
    └── Need service discovery?
        ├── YES -> Enable Cloud Map
        └── NO -> Use ALB/NLB directly
```

---

## Gateway Load Balancer + Inspection VPC Pattern

**Use Case:** Centralized network inspection (firewall, IDS/IPS)

**Architecture:**
```
Application VPC A              Application VPC B
      |                              |
      v                              v
  TGW Attachment              TGW Attachment
      |                              |
      +--------------+---------------+
                     |
                 Transit Gateway
                     |
                     +---> Inspection VPC
                     |       |
                     |       v
                     |   GWLB (Gateway Load Balancer)
                     |       |
                     |       +---> Firewall Appliance 1
                     |       +---> Firewall Appliance 2
                     |       +---> Firewall Appliance 3
                     |           (Third-party virtual appliances)
                     |
                     +---> Internet (if needed)
```

**Traffic Flow:**
1. Traffic from VPC A to VPC B goes to TGW
2. TGW sends traffic to Inspection VPC via GWLB endpoint
3. GWLB distributes traffic to firewall appliances
4. After inspection, traffic returns to GWLB
5. GWLB sends traffic back to TGW
6. TGW routes to destination (VPC B)

**Benefits:**
- Centralized inspection for all inter-VPC traffic
- Scalable (add more appliances behind GWLB)
- Transparent to application VPCs

---

## Operational Considerations

### Monitoring Container Networking

**ECS:**
- VPC Flow Logs (at ENI level for awsvpc mode)
- CloudWatch Logs (container logs)
- Container Insights (metrics)

**EKS:**
- VPC Flow Logs (at Pod IP level)
- CloudWatch Container Insights
- Prometheus + Grafana

### Troubleshooting

**ECS awsvpc Issues:**
```bash
# Check ENI attachment
aws ec2 describe-network-interfaces \
  --filters Name=description,Values="*ecs*"

# Verify security group rules
aws ec2 describe-security-groups \
  --group-ids sg-xxxxxxxx

# Check task ENI in logs
aws logs filter-log-events \
  --log-group-name /ecs/my-task \
  --filter-pattern "ENI"
```

**EKS Pod Networking Issues:**
```bash
# Check VPC CNI logs
kubectl logs -n kube-system -l k8s-app=aws-node

# Verify IP allocation
kubectl get eniconfig

# Check Pod IP assignment
kubectl get pod -o wide
```

---

*This section addresses the critical gap in container networking for SA Pro certification.*
