# Prerequisites Checklist

Before deploying LlamaStack on OpenShift, ensure you have all prerequisites in place.

## ✅ Required Prerequisites

### 1. OpenShift Cluster
- [ ] **OpenShift 4.19 or newer** installed and running
- [ ] **Cluster administrator privileges** for your user
- [ ] **Access to `openshift-machine-api` namespace** (for GPU nodes)

**Verify:**
```bash
oc whoami
oc get nodes
```

### 2. OpenShift CLI
- [ ] **`oc` CLI installed** and configured
- [ ] **Logged in** to your OpenShift cluster

**Verify:**
```bash
oc version
oc whoami
```

**Install:**
- Download from: https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/

### 3. OpenShift AI Setup
- [ ] **Red Hat OpenShift AI** installed
- [ ] **LlamaStack Operator** activated in OpenShift AI
- [ ] **GPU support enabled** (Node Feature Discovery Operator, NVIDIA GPU Operator)

**Verify:**
```bash
oc get operators -n openshift-operators | grep llama
oc get operators -n openshift-operators | grep nvidia
```

### 4. vLLM Inference Model
- [ ] **vLLM inference model deployed** in OpenShift AI
- [ ] **External route enabled** for the model
- [ ] **Token authentication enabled**
- [ ] **Runtime argument**: `--enable-auto-tool-choice` added

**Verify:**
```bash
# List inference models
oc get inferencemodels -n <your-namespace>

# Check route
oc get route -n <your-namespace> | grep inference
```

### 5. Network Access
- [ ] **Access to OpenShift cluster** (via route or VPN)
- [ ] **DNS resolution** working for cluster routes
- [ ] **Firewall rules** allow access to OpenShift routes

**Verify:**
```bash
# Test cluster access
oc cluster-info
```

### 6. Storage
- [ ] **Storage class available** for persistent volumes
- [ ] **Sufficient storage quota** for MongoDB

**Verify:**
```bash
oc get storageclass
```

---

## 🎯 Optional Prerequisites

### GPU Nodes (for LLM inference)
- [ ] **AWS quota** for g6.4xlarge instances (if adding GPU nodes)
- [ ] **NVIDIA GPU Operator** installed (if using GPU nodes)

**Verify:**
```bash
oc get nodes -l node-role.kubernetes.io/gpu=true
```

### Development Tools
- [ ] **Python 3.11+** installed (for test scripts)
- [ ] **`python-dotenv`** installed (for config)
- [ ] **`llama-stack-client`** installed (for notebooks)

**Verify:**
```bash
python3 --version
pip list | grep llama-stack-client
```

---

## 🔍 Pre-Deployment Checks

Run these commands to verify everything is ready:

```bash
# 1. Check cluster access
oc whoami && echo "✅ Logged in" || echo "❌ Not logged in"

# 2. Check namespace exists or can be created
oc get namespace my-first-model || oc create namespace my-first-model

# 3. Check storage class
oc get storageclass | grep -v "No resources" && echo "✅ Storage available" || echo "❌ No storage class"

# 4. Check LlamaStack Operator
oc get operators -n openshift-operators | grep llama && echo "✅ LlamaStack Operator" || echo "❌ LlamaStack Operator not found"

# 5. Check vLLM inference model (update namespace)
oc get inferencemodels -n my-first-model && echo "✅ vLLM model found" || echo "⚠️  vLLM model not found"
```

---

## 📝 Configuration Values Needed

Before deploying, gather these values:

### From OpenShift AI
- **vLLM Model Name**: e.g., `llama-32-3b-instruct`
- **vLLM Service URL**: e.g., `http://llama-32-3b-instruct-predictor.my-first-model.svc.cluster.local:8080/v1`
- **vLLM API Token**: Your authentication token
- **Namespace**: e.g., `my-first-model`

### From AWS (if adding GPU nodes)
- **Region**: e.g., `us-east-2`
- **Availability Zones**: e.g., `us-east-2a`, `us-east-2b`
- **Instance Quota**: Ensure you have quota for g6.4xlarge instances

---

## 🚀 Ready to Deploy?

Once all prerequisites are met:

👉 **[Go to Getting Started Guide](01-getting-started.md)**

---

## 🆘 Missing Prerequisites?

### LlamaStack Operator Not Found
1. Go to OpenShift AI Dashboard
2. Navigate to Operators → OperatorHub
3. Search for "LlamaStack"
4. Install the operator

### vLLM Model Not Deployed
1. Go to OpenShift AI Dashboard
2. Navigate to Model Serving
3. Deploy a vLLM inference model
4. Enable external route and token authentication

### No Storage Class
1. Contact cluster administrator
2. Request storage class provisioning
3. Or use default storage class if available

---

**All prerequisites met?** → [Getting Started Guide](01-getting-started.md) 🚀

