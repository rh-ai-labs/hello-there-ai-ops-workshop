# Environment Setup Guide

This guide will help you set up your environment for the AI Ops Workshop, including deploying LlamaStack, MongoDB, and configuring all necessary services on OpenShift.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Before starting, ensure you have:

- [ ] **OpenShift Cluster Access**
  - OpenShift 4.19 or newer
  - Cluster administrator privileges
  - Access to `openshift-machine-api` namespace (for GPU nodes)

- [ ] **OpenShift CLI (`oc`)**
  - Installed and configured
  - Logged in to your cluster
  
  ```bash
  oc version
  oc whoami
  ```

- [ ] **OpenShift AI Setup**
  - Red Hat OpenShift AI installed
  - LlamaStack Operator activated
  - GPU support enabled (if using GPU nodes)

- [ ] **vLLM Inference Model**
  - vLLM inference model deployed in OpenShift AI
  - External route enabled (or service accessible)
  - Token authentication configured

- [ ] **Network Access**
  - Access to OpenShift cluster routes
  - DNS resolution working for cluster routes

**Verify prerequisites:**
```bash
# Check OpenShift access
oc whoami
oc get nodes

# Check operators
oc get operators -n openshift-operators | grep llama
oc get operators -n openshift-operators | grep nvidia

# Check inference models
oc get inferencemodels -n my-first-model
```

---

## 🚀 Quick Start

If you want to deploy everything quickly:

```bash
# 1. Deploy LlamaStack
./scripts/deploy-llamastack.sh

# 2. Deploy MongoDB & MCP Server
./scripts/deploy-mongodb-mcp.sh

# 3. Register MCP Server with LlamaStack
./scripts/register-mongodb-mcp.sh

# 4. Configure environment
./scripts/setup-env.sh
```

**Expected time:** 20-30 minutes

---

## 📝 Step-by-Step Setup

### Step 1: Deploy LlamaStack

LlamaStack provides RAG (Retrieval-Augmented Generation) capabilities for Modules 2 and 4.

**Using the deployment script:**
```bash
./scripts/deploy-llamastack.sh
```

**What it does:**
- Creates necessary secrets for LlamaStack
- Deploys LlamaStackDistribution (with Milvus inline vector store)
- Creates routes for external access
- Verifies deployment is ready

**Configuration:**
The script uses these defaults (can be overridden with environment variables):
- `NAMESPACE`: `my-first-model`
- `DEPLOYMENT_TYPE`: `milvus-inline`
- Auto-detects vLLM URL and model

**Customize:**
```bash
export NAMESPACE="your-namespace"
export DEPLOYMENT_TYPE="milvus-remote"  # or "faiss-inline"
./scripts/deploy-llamastack.sh
```

**Expected time:** 5-10 minutes

**Verify:**
```bash
oc get pods -n my-first-model | grep llama
oc get route llamastack-route -n my-first-model
```

---

### Step 2: Deploy MongoDB & MCP Server

MongoDB stores IT operations data, and the MCP server provides agent access to MongoDB (needed for Module 4 - AI Agents).

**Using the deployment script:**
```bash
./scripts/deploy-mongodb-mcp.sh
```

**What it does:**
- Creates MongoDB secret with credentials
- Deploys MongoDB database with initialization
- Deploys MongoDB MCP server
- Creates routes for external access
- Initializes database with sample data

**Configuration:**
- `NAMESPACE`: `my-first-model` (default)
- MongoDB credentials: `admin` / `password123` (default)
- Database: `mcp_demo`

**Customize:**
```bash
export NAMESPACE="your-namespace"
export MONGO_USERNAME="your-user"
export MONGO_PASSWORD="your-password"
./scripts/deploy-mongodb-mcp.sh
```

**Expected time:** 5-10 minutes

**Verify:**
```bash
oc get pods -n my-first-model | grep mongodb
oc get route mongodb-mcp-server -n my-first-model
```

---

### Step 3: Register MCP Server with LlamaStack

This connects the MongoDB MCP server to LlamaStack so agents can use MongoDB tools.

**Using the registration script:**
```bash
./scripts/register-mongodb-mcp.sh
```

**What it does:**
- Detects LlamaStack route URL
- Detects MongoDB MCP server route URL
- Registers MCP server as a toolgroup in LlamaStack
- Verifies registration

**Configuration:**
The script auto-detects routes, but you can override:
```bash
export NAMESPACE="your-namespace"
export LLAMASTACK_ROUTE="your-llamastack-route-url"
export MCP_SERVER_ROUTE="your-mcp-server-route-url"
./scripts/register-mongodb-mcp.sh
```

**Expected time:** 1-2 minutes

**Verify:**
```bash
# Check toolgroups in LlamaStack
oc exec -it deployment/lsd-llama-milvus-inline -n my-first-model -- \
  curl -k http://localhost:8321/v1/toolgroups
```

---

### Step 4: Configure Environment

Generate the `.env` file with all necessary configuration for notebooks.

**Run the setup script:**
```bash
./scripts/setup-env.sh
```

**What it does:**
- Detects if running inside or outside OpenShift cluster
- Auto-discovers LlamaStack route URL
- Auto-discovers MongoDB MCP route URL
- Auto-discovers vLLM service/route URL
- Generates `.env` file with all configuration

**Configuration detected:**
- ✅ **LlamaStack URL** - Route or service URL
- ✅ **MongoDB MCP URL** - Route or service URL (optional, Module 4)
- ✅ **vLLM API Base** - Route or service URL (REQUIRED, Module 3)
- ✅ **Model identifiers** - Default models configured

**Expected time:** < 1 minute

**Verify:**
```bash
cat .env
```

**Example output:**
```
LLAMA_STACK_URL=https://llamastack-route-my-first-model.apps.ocp.example.com
MCP_MONGODB_URL=https://mongodb-mcp-server-my-first-model.apps.ocp.example.com
VLLM_API_BASE=https://vllm-predictor-route-my-first-model.apps.ocp.example.com/v1
LLAMA_MODEL=vllm-inference/llama-32-3b-instruct
OPENAI_MODEL=RedHatAI/Meta-Llama-3.1-8B-Instruct-FP8-dynamic
NAMESPACE=my-first-model
```

---

### Step 5: (Optional) Add GPU Worker Nodes

If you need GPU nodes for LLM inference:

```bash
./scripts/create-gpu-workers.sh
```

**What it does:**
- Creates GPU worker node MachineSet
- Configures NVIDIA GPU support
- Waits for nodes to be ready

**Configuration:**
- `NAMESPACE`: `my-first-model` (default)
- Instance type: `g6.4xlarge` (AWS) or configurable

**Expected time:** 10-15 minutes

**Verify:**
```bash
oc get nodes -l node-role.kubernetes.io/worker
```

---

## ⚙️ Configuration

### Environment Variables

All scripts support environment variables for customization:

**Common variables:**
- `NAMESPACE` - OpenShift namespace (default: `my-first-model`)
- `LLAMA_STACK_URL` - LlamaStack URL (auto-detected)
- `MCP_MONGODB_URL` - MongoDB MCP URL (auto-detected)
- `VLLM_API_BASE` - vLLM API base URL (auto-detected)

**LlamaStack deployment:**
- `DEPLOYMENT_TYPE` - `milvus-inline`, `milvus-remote`, or `faiss-inline`
- `VLLM_TLS_VERIFY` - TLS verification (default: `false`)
- `VLLM_API_TOKEN` - API token (default: `fake`)

**MongoDB deployment:**
- `MONGO_USERNAME` - MongoDB username (default: `admin`)
- `MONGO_PASSWORD` - MongoDB password (default: `password123`)
- `MONGO_DATABASE` - Database name (default: `mcp_demo`)

### Manual Configuration

If auto-detection fails, you can manually configure:

**1. Edit `.env` file:**
```bash
nano .env
```

**2. Set environment variables:**
```bash
export LLAMA_STACK_URL='https://your-llamastack-route'
export VLLM_API_BASE='https://your-vllm-route/v1'
./scripts/setup-env.sh
```

---

## ✅ Verification

### Check All Services

```bash
# Check pods
oc get pods -n my-first-model

# Check routes
oc get routes -n my-first-model

# Check services
oc get svc -n my-first-model
```

**Expected services:**
- ✅ `lsd-llama-milvus-inline-*` - LlamaStack pod
- ✅ `mongodb-*` - MongoDB pod
- ✅ `mongodb-mcp-server-*` - MCP server pod
- ✅ `llama-32-3b-instruct-predictor-*` - vLLM predictor pod

**Expected routes:**
- ✅ `llamastack-route` - LlamaStack external access
- ✅ `mongodb-mcp-server` - MongoDB MCP external access
- ⚠️ `vllm-predictor-route` - vLLM route (may not exist, service URL used instead)

### Test LlamaStack

```bash
# Get route URL
LLAMA_URL=$(oc get route llamastack-route -n my-first-model -o jsonpath='{.spec.host}')

# Test health endpoint
curl -k "https://${LLAMA_URL}/health"
```

### Test MongoDB MCP

```bash
# Get route URL
MCP_URL=$(oc get route mongodb-mcp-server -n my-first-model -o jsonpath='{.spec.host}')

# Test MCP endpoint
curl -k "https://${MCP_URL}/health"
```

### Test vLLM

```bash
# If route exists
VLLM_URL=$(oc get route vllm-predictor-route -n my-first-model -o jsonpath='{.spec.host}')
curl -k "https://${VLLM_URL}/v1/models"

# Or use service URL (inside cluster)
oc exec -it deployment/llama-32-3b-instruct-predictor -n my-first-model -- \
  curl http://localhost:80/v1/models
```

---

## 🔧 Troubleshooting

### LlamaStack Not Starting

**Symptoms:**
- Pods in `CrashLoopBackOff` or `Pending` state
- Routes not accessible

**Solutions:**
1. Check pod logs:
   ```bash
   oc logs -l app=lsd-llama-milvus-inline -n my-first-model --tail=100
   ```

2. Check resource quotas:
   ```bash
   oc describe quota -n my-first-model
   ```

3. Verify vLLM is accessible:
   ```bash
   oc get inferencemodels -n my-first-model
   ```

4. Check secrets:
   ```bash
   oc get secrets -n my-first-model | grep llama
   ```

### MongoDB Not Initializing

**Symptoms:**
- MongoDB pod running but database empty
- MCP server can't connect

**Solutions:**
1. Check MongoDB logs:
   ```bash
   oc logs deployment/mongodb -n my-first-model --tail=100
   ```

2. Check init script:
   ```bash
   oc get configmap mongodb-init -n my-first-model -o yaml
   ```

3. Manually initialize:
   ```bash
   oc exec -it deployment/mongodb -n my-first-model -- mongosh -u admin -p password123 --authenticationDatabase admin
   ```

### vLLM Route Not Found

**Symptoms:**
- Script shows "Could not detect vLLM route"
- Using service URL instead

**Solutions:**
1. **Create a route** (recommended for external access):
   ```bash
   oc create route edge vllm-predictor-route \
     --service=llama-32-3b-instruct-predictor \
     --port=80 \
     -n my-first-model
   ```

2. **Use port-forwarding** (for local development):
   ```bash
   oc port-forward svc/llama-32-3b-instruct-predictor 8080:80 -n my-first-model
   # Then use: http://localhost:8080/v1
   ```

3. **Use service URL** (inside cluster):
   - Service URL is automatically used if no route exists
   - Works inside cluster or with VPN/port-forwarding

### MCP Server Not Registering

**Symptoms:**
- Registration script fails
- Agents can't use MongoDB tools

**Solutions:**
1. Verify MCP server is running:
   ```bash
   oc get pods -n my-first-model | grep mongodb-mcp-server
   oc logs deployment/mongodb-mcp-server -n my-first-model --tail=50
   ```

2. Check routes:
   ```bash
   oc get route mongodb-mcp-server -n my-first-model
   oc get route llamastack-route -n my-first-model
   ```

3. Manually register:
   ```bash
   # Get URLs
   LLAMA_URL=$(oc get route llamastack-route -n my-first-model -o jsonpath='{.spec.host}')
   MCP_URL=$(oc get route mongodb-mcp-server -n my-first-model -o jsonpath='{.spec.host}')
   
   # Register
   curl -k -X POST "https://${LLAMA_URL}/v1/toolgroups" \
     -H "Content-Type: application/json" \
     -d "{
       \"id\": \"mcp::mongodb\",
       \"name\": \"MongoDB MCP\",
       \"transport\": \"http\",
       \"url\": \"https://${MCP_URL}/mcp\"
     }"
   ```

### Configuration Not Detected

**Symptoms:**
- `.env` file has empty values
- Scripts can't find routes/services

**Solutions:**
1. Verify `oc` CLI is working:
   ```bash
   oc whoami
   oc get routes -n my-first-model
   ```

2. Check namespace:
   ```bash
   oc project
   export NAMESPACE="my-first-model"
   ./scripts/setup-env.sh
   ```

3. Manually set values:
   ```bash
   # Edit .env file
   nano .env
   
   # Or set environment variables
   export LLAMA_STACK_URL='https://your-route'
   export VLLM_API_BASE='https://your-vllm-route/v1'
   ```

---

## 📚 Script Reference

### `setup-env.sh`
Generates `.env` file with auto-detected configuration.

**Usage:**
```bash
./scripts/setup-env.sh
```

**What it detects:**
- LlamaStack route/service URL
- MongoDB MCP route/service URL
- vLLM route/service URL
- Model identifiers

### `deploy-llamastack.sh`
Deploys LlamaStack on OpenShift.

**Usage:**
```bash
./scripts/deploy-llamastack.sh
```

**Options:**
- `NAMESPACE` - Target namespace
- `DEPLOYMENT_TYPE` - `milvus-inline`, `milvus-remote`, or `faiss-inline`
- `AUTO_DETECT_VLLM` - Auto-detect vLLM configuration

### `deploy-mongodb-mcp.sh`
Deploys MongoDB and MongoDB MCP server.

**Usage:**
```bash
./scripts/deploy-mongodb-mcp.sh
```

**Options:**
- `NAMESPACE` - Target namespace
- `MONGO_USERNAME` - MongoDB username
- `MONGO_PASSWORD` - MongoDB password

### `register-mongodb-mcp.sh`
Registers MongoDB MCP server with LlamaStack.

**Usage:**
```bash
./scripts/register-mongodb-mcp.sh
```

**Options:**
- `NAMESPACE` - Target namespace
- `LLAMASTACK_ROUTE` - LlamaStack route URL
- `MCP_SERVER_ROUTE` - MCP server route URL
- `TOOLGROUP_ID` - Toolgroup ID (default: `mcp::mongodb`)

### `create-gpu-workers.sh`
Creates GPU worker nodes for LLM inference.

**Usage:**
```bash
./scripts/create-gpu-workers.sh
```

**Options:**
- `NAMESPACE` - Target namespace
- `INSTANCE_TYPE` - AWS instance type (default: `g6.4xlarge`)

---

## 🎯 Next Steps

After completing setup:

1. **Verify configuration:**
   ```bash
   ./scripts/setup-env.sh
   cat .env
   ```

2. **Start with Module 1:**
   - Navigate to `1-ai-fundamentals/`
   - Follow the module README

3. **Module-specific requirements:**
   - **Module 2 (RAG)**: Requires LlamaStack ✅
   - **Module 3 (Evaluation)**: Requires vLLM ✅
   - **Module 4 (Agents)**: Requires LlamaStack + MongoDB MCP ✅
   - **Module 5 (Fine-tuning)**: No OpenShift services needed

---

## 📖 Additional Resources

- **[Main README](../README.md)** - Workshop overview
- **[Configuration Guide](../CONFIGURATION.md)** - Detailed configuration documentation
- **[OpenShift Deployment Docs](../openshift/README.md)** - Advanced deployment guides

---

## 💡 Tips

1. **Always run `setup-env.sh` after deployments** to update `.env` file
2. **Check routes** if external access doesn't work: `oc get routes -n my-first-model`
3. **Use service URLs** if running inside cluster (auto-detected)
4. **Create vLLM route** for external access (script provides instructions)
5. **Check logs** if services aren't working: `oc logs deployment/<name> -n my-first-model`

---

**Last Updated:** December 2024

