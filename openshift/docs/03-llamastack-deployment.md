# LlamaStack Deployment Guide

Complete guide for deploying LlamaStack on OpenShift using LlamaStackDistribution Custom Resource.

## Overview

LlamaStackDistribution is a Custom Resource that manages the complete LlamaStack deployment, including:
- Vector store (Milvus or FAISS)
- API server
- Routes for external access
- Configuration and secrets

---

## Quick Start

### Option 1: Using Deployment Script (Recommended)

```bash
cd openshift/scripts
./deploy-llamastack.sh
```

The script automatically:
- ✅ Detects vLLM configuration
- ✅ Creates necessary secrets
- ✅ Deploys LlamaStackDistribution
- ✅ Creates routes
- ✅ Verifies deployment

### Option 2: Manual Deployment

See detailed steps below.

---

## Prerequisites

- vLLM inference model deployed
- LlamaStack Operator activated
- OpenShift cluster admin access

👉 **[Check Prerequisites](02-prerequisites.md)**

---

## Step-by-Step Deployment

### Step 1: Gather Configuration

Get your vLLM configuration:

```bash
# Get vLLM service URL
VLLM_URL="http://llama-32-3b-instruct-predictor.my-first-model.svc.cluster.local:8080/v1"

# Get model name
INFERENCE_MODEL="llama-32-3b-instruct"

# Get API token (from OpenShift AI dashboard or secret)
VLLM_API_TOKEN="your-token-here"

# Set namespace
NAMESPACE="my-first-model"
```

### Step 2: Create Inference Model Secret

```bash
oc create secret generic llama-stack-inference-model-secret \
  --from-literal=INFERENCE_MODEL="$INFERENCE_MODEL" \
  --from-literal=VLLM_URL="$VLLM_URL" \
  --from-literal=VLLM_TLS_VERIFY="false" \
  --from-literal=VLLM_API_TOKEN="$VLLM_API_TOKEN" \
  --namespace="$NAMESPACE"
```

### Step 3: Deploy LlamaStackDistribution

Choose your deployment type:

#### Option A: Inline Milvus (Recommended for Development)

```bash
oc apply -f manifests/llamastack/llamastackdistribution-inline-milvus.yaml
```

**Best for**: Development, testing, small workloads

#### Option B: Inline FAISS (Experimental)

```bash
oc apply -f manifests/llamastack/llamastackdistribution-inline-faiss.yaml
```

**Best for**: Testing FAISS vector store

#### Option C: Remote Milvus (Production)

1. **Create Milvus connection secret**:
```bash
oc create secret generic milvus-secret \
  --from-literal=MILVUS_ENDPOINT="tcp://milvus-service:19530" \
  --from-literal=MILVUS_USERNAME="root" \
  --from-literal=MILVUS_PASSWORD="password" \
  --namespace="$NAMESPACE"
```

2. **Deploy**:
```bash
oc apply -f manifests/llamastack/llamastackdistribution-remote-milvus.yaml
```

**Best for**: Production, large-scale workloads

### Step 4: Create Route

#### Secure Route (Recommended)

```bash
oc apply -f manifests/llamastack/llamastack-route.yaml
```

#### Insecure Route (Development Only)

```bash
oc apply -f manifests/llamastack/llamastack-route-insecure.yaml
```

### Step 5: Verify Deployment

```bash
# Check LlamaStackDistribution status
oc get llamastackdistribution -n $NAMESPACE

# Check pods
oc get pods -n $NAMESPACE | grep llamastack

# Check route
oc get route llamastack-route -n $NAMESPACE

# Test API
LLAMA_STACK_URL=$(oc get route llamastack-route -n $NAMESPACE -o jsonpath='{.spec.host}')
curl -k https://${LLAMA_STACK_URL}/v1/models
```

---

## Deployment Types Explained

### Inline Milvus
- **Vector store**: Milvus embedded in LlamaStack pod
- **Pros**: Simple, no external dependencies
- **Cons**: Limited scalability, data lost on pod restart
- **Use case**: Development, testing

### Inline FAISS
- **Vector store**: FAISS embedded in LlamaStack pod
- **Pros**: Fast, lightweight
- **Cons**: Experimental, limited features
- **Use case**: Testing FAISS functionality

### Remote Milvus
- **Vector store**: External Milvus cluster
- **Pros**: Scalable, persistent, production-ready
- **Cons**: Requires separate Milvus deployment
- **Use case**: Production workloads

---

## Configuration Options

### Environment Variables

Edit the LlamaStackDistribution manifest to customize:

```yaml
spec:
  env:
    - name: LOG_LEVEL
      value: "INFO"
    - name: MAX_CONCURRENT_REQUESTS
      value: "10"
```

### Resource Limits

```yaml
spec:
  resources:
    requests:
      cpu: "2"
      memory: "4Gi"
    limits:
      cpu: "4"
      memory: "8Gi"
```

### GPU Support

To use GPU nodes:

```yaml
spec:
  nodeSelector:
    node-role.kubernetes.io/gpu: "true"
  resources:
    requests:
      nvidia.com/gpu: 1
```

---

## Troubleshooting

### LlamaStackDistribution Not Ready

```bash
# Check status
oc describe llamastackdistribution -n $NAMESPACE

# Check events
oc get events -n $NAMESPACE --sort-by='.lastTimestamp' | grep llamastack
```

### Pods Not Starting

```bash
# Check pod logs
oc logs -n $NAMESPACE -l app=llamastack --tail=100

# Check pod events
oc describe pod <pod-name> -n $NAMESPACE
```

### Route Not Accessible

```bash
# Check route status
oc get route llamastack-route -n $NAMESPACE -o yaml

# Test from inside cluster
oc run test-pod --image=curlimages/curl --rm -it -- curl -k https://llamastack-route.$NAMESPACE.svc.cluster.local/v1/models
```

---

## Next Steps

Once LlamaStack is deployed:

1. **[Deploy MongoDB & MCP](04-mongodb-mcp-setup.md)**
2. **[Register MCP Server](06-mcp-integration.md)**
3. **[Configure Agents](07-agent-configuration.md)**

---

**Need help?** → [Troubleshooting Guide](troubleshooting.md) | [Quick Reference](quick-reference.md)

