# Architecture Overview

System architecture and component relationships for LlamaStack on OpenShift.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenShift Cluster                        │
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                   │
│  │  LlamaStack  │◄─────│  vLLM Model │                   │
│  │  Distribution│      │  (Inference) │                   │
│  └──────┬───────┘      └──────────────┘                   │
│         │                                                    │
│         │ MCP Protocol                                        │
│         │                                                    │
│  ┌──────▼──────────┐                                         │
│  │  MongoDB MCP    │      ┌──────────────┐                 │
│  │  Server         │◄─────│  MongoDB     │                 │
│  └─────────────────┘      └──────────────┘                 │
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                   │
│  │  GPU Worker  │      │  GPU Worker  │                   │
│  │  Node (g6.4x)│      │  Node (g6.4x)│                   │
│  └──────────────┘      └──────────────┘                   │
└─────────────────────────────────────────────────────────────┘
         │                              │
         │ Routes                       │ Routes
         ▼                              ▼
┌──────────────┐              ┌──────────────┐
│  External    │              │  External    │
│  Access      │              │  Access      │
└──────────────┘              └──────────────┘
```

---

## Components

### LlamaStack Distribution

**Purpose**: Main LlamaStack deployment

**Components**:
- API server (port 8321)
- Vector store (Milvus or FAISS)
- Route for external access

**Deployment**: `LlamaStackDistribution` Custom Resource

**Access**:
- Inside cluster: `http://llamastack-service.namespace.svc.cluster.local:8321`
- Outside cluster: `https://llamastack-route.namespace.apps.cluster.com`

---

### vLLM Inference Model

**Purpose**: LLM inference engine

**Components**:
- vLLM server (port 8080)
- Model weights
- API endpoint

**Deployment**: OpenShift AI InferenceModel

**Access**:
- Service: `http://model-predictor.namespace.svc.cluster.local:8080/v1`
- Route: `https://model-route.namespace.apps.cluster.com`

---

### MongoDB

**Purpose**: Data storage for agents

**Components**:
- MongoDB database (port 27017)
- Persistent storage
- Sample data initialization

**Deployment**: Kubernetes Deployment

**Access**:
- Service: `mongodb.namespace.svc.cluster.local:27017`

---

### MongoDB MCP Server

**Purpose**: MCP interface for MongoDB

**Components**:
- MCP server (port 3000)
- MCP protocol endpoint (`/mcp`)
- MongoDB connection

**Deployment**: Kubernetes Deployment

**Access**:
- Inside cluster: `http://mongodb-mcp-server.namespace.svc.cluster.local:3000`
- Outside cluster: Route (if created)

**Protocol**: streamable-http (endpoint: `/mcp`)

---

### GPU Worker Nodes

**Purpose**: GPU-accelerated compute for inference

**Components**:
- g6.4xlarge instances
- NVIDIA T4 GPUs
- GPU operator integration

**Deployment**: MachineSet

**Labels**: `node-role.kubernetes.io/gpu=true`

---

## Data Flow

### Agent Query Flow

```
User Query
    ↓
Agent (LlamaStack)
    ↓
Agent decides to use MongoDB tool
    ↓
LlamaStack forwards to MCP server
    ↓
MCP Server queries MongoDB
    ↓
MongoDB returns data
    ↓
MCP Server returns to LlamaStack
    ↓
Agent generates response with real data
    ↓
User receives response
```

### Tool Execution Flow

```
1. Agent receives query: "What collections are in mcp_demo?"
   ↓
2. Agent reasons: "I need to query MongoDB"
   ↓
3. Agent calls tool: list-collections(database="mcp_demo")
   ↓
4. LlamaStack forwards to MCP server via MCP protocol
   ↓
5. MCP server executes: MongoDB query
   ↓
6. MongoDB returns: ["incidents", "services", "alerts"]
   ↓
7. MCP server returns result to LlamaStack
   ↓
8. Agent uses result in response: "The mcp_demo database contains 3 collections..."
```

---

## Network Architecture

### Inside Cluster Communication

```
LlamaStack Pod
    ↓ (service DNS)
MongoDB MCP Server Service
    ↓ (service DNS)
MongoDB Service
```

**URLs**:
- `http://service-name.namespace.svc.cluster.local:port`

### External Access

```
External Client
    ↓ (HTTPS)
OpenShift Route
    ↓ (HTTP)
Service
    ↓ (HTTP)
Pod
```

**URLs**:
- `https://route-name.namespace.apps.cluster.com`

---

## Storage Architecture

### MongoDB Persistent Storage

```
MongoDB Pod
    ↓
PersistentVolumeClaim
    ↓
StorageClass
    ↓
PersistentVolume (EBS)
```

**Storage**: 20Gi persistent volume (configurable)

---

## Security Architecture

### Authentication

- **vLLM**: Token-based authentication
- **MongoDB**: Username/password authentication
- **OpenShift Routes**: TLS termination

### Network Policies

- Pod-to-pod communication within namespace
- Service-to-service communication
- External access via routes only

---

## Scalability

### Horizontal Scaling

- **LlamaStack**: Scale pods via replicas
- **MongoDB**: Single instance (can be scaled with StatefulSet)
- **GPU Nodes**: Add more MachineSets

### Vertical Scaling

- **Resource limits**: CPU, memory, GPU
- **Node resources**: Add larger instance types

---

## Monitoring

### Key Metrics

- **LlamaStack**: API request rate, response time
- **MongoDB**: Connection count, query performance
- **GPU Nodes**: GPU utilization, memory usage
- **MCP Server**: Tool execution rate, errors

### Logs

- **LlamaStack**: `oc logs -l app=llamastack`
- **MongoDB**: `oc logs deployment/mongodb`
- **MCP Server**: `oc logs deployment/mongodb-mcp-server`

---

## Component Dependencies

```
vLLM Model (required)
    ↓
LlamaStack Distribution (depends on vLLM)
    ↓
MongoDB (optional, for MCP)
    ↓
MongoDB MCP Server (depends on MongoDB)
    ↓
Agent Configuration (depends on LlamaStack + MCP)
```

---

## Deployment Order

1. **vLLM Inference Model** (via OpenShift AI)
2. **LlamaStack Distribution** (depends on vLLM)
3. **MongoDB** (optional)
4. **MongoDB MCP Server** (depends on MongoDB)
5. **MCP Registration** (depends on MCP server)
6. **Agent Creation** (depends on LlamaStack + MCP)

---

**Want to learn more?** → [Getting Started Guide](01-getting-started.md) | [Deployment Guides](03-llamastack-deployment.md)

