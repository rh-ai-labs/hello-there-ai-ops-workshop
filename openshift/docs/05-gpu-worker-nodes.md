# GPU Worker Nodes Setup

Add GPU worker nodes (g6.4xlarge) to your OpenShift cluster for running LLM inference workloads.

## Overview

g6.4xlarge instances provide:
- **1x NVIDIA T4 GPU** (16GB GPU memory)
- **16 vCPUs**
- **64 GiB RAM**

Perfect for running vLLM inference models and GPU-accelerated workloads.

---

## Quick Start

### Using the Script (Recommended)

```bash
cd openshift/scripts
./create-gpu-workers.sh
```

The script automatically:
- ✅ Detects your cluster configuration
- ✅ Creates 2x g6.4xlarge nodes (1 per availability zone)
- ✅ Labels nodes with `node-role.kubernetes.io/gpu=true`
- ✅ Monitors node creation progress

**Expected time**: 5-10 minutes

---

## Manual Deployment

### Step 1: Get Cluster Information

```bash
# Get cluster name
CLUSTER_NAME=$(oc get machineset -n openshift-machine-api -o jsonpath='{.items[0].metadata.labels.machine\.openshift\.io/cluster-api-cluster}')

# Get region
REGION=$(oc get infrastructure cluster -o jsonpath='{.status.platformStatus.aws.region}')

# Get AMI ID
AMI_ID=$(oc get machineset -n openshift-machine-api -o jsonpath='{.items[0].spec.template.spec.providerSpec.value.ami.id}')
```

### Step 2: Update MachineSet Manifest

Edit `manifests/infrastructure/gpu-worker-machineset.yaml`:
- Replace `ocp-xf56d` with your cluster name
- Update AMI ID if needed
- Update region and availability zones if different

### Step 3: Apply MachineSet

```bash
oc apply -f manifests/infrastructure/gpu-worker-machineset.yaml
```

### Step 4: Monitor Node Creation

```bash
# Watch MachineSets
oc get machineset -n openshift-machine-api -w | grep gpu

# Watch nodes
oc get nodes -l node-role.kubernetes.io/gpu=true -w
```

---

## Verification

### Check MachineSets

```bash
oc get machineset -n openshift-machine-api | grep gpu
```

Expected output:
```
NAME                                    DESIRED   READY   AVAILABLE   AGE
ocp-xf56d-worker-gpu-us-east-2a        1         1       1           5m
ocp-xf56d-worker-gpu-us-east-2b         1         1       1           5m
```

### Check Nodes

```bash
oc get nodes -l node-role.kubernetes.io/gpu=true
```

Expected output:
```
NAME                          STATUS   ROLES   AGE   VERSION
ip-10-0-xxx-xxx.ec2.internal  Ready    worker  5m    v1.30.x
ip-10-0-yyy-yyy.ec2.internal  Ready    worker  5m    v1.30.x
```

### Check GPU Resources

```bash
oc describe node <gpu-node-name> | grep -A 5 "nvidia.com/gpu"
```

Expected:
```
nvidia.com/gpu:  1
```

---

## Using GPU Nodes

### Schedule Workloads on GPU Nodes

Add node selector to your deployments:

```yaml
spec:
  nodeSelector:
    node-role.kubernetes.io/gpu: "true"
  containers:
  - name: my-app
    resources:
      requests:
        nvidia.com/gpu: 1
      limits:
        nvidia.com/gpu: 1
```

### Example: vLLM on GPU Nodes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-inference
spec:
  replicas: 1
  template:
    spec:
      nodeSelector:
        node-role.kubernetes.io/gpu: "true"
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        resources:
          requests:
            nvidia.com/gpu: 1
          limits:
            nvidia.com/gpu: 1
```

---

## Scaling GPU Nodes

### Scale Up

```bash
oc scale machineset ocp-xf56d-worker-gpu-us-east-2a -n openshift-machine-api --replicas=2
```

### Scale Down (Save Costs)

```bash
oc scale machineset ocp-xf56d-worker-gpu-us-east-2a -n openshift-machine-api --replicas=0
oc scale machineset ocp-xf56d-worker-gpu-us-east-2b -n openshift-machine-api --replicas=0
```

---

## Cost Considerations

- **g6.4xlarge pricing**: ~$1.00-1.50/hour per instance
- **2x nodes**: ~$2.00-3.00/hour = ~$1,440-2,160/month (24/7)
- **Recommendation**: Scale down when not in use

### Cost Optimization

1. **Scale down when not in use**:
   ```bash
   ./scripts/create-gpu-workers.sh  # Then scale to 0
   ```

2. **Use cluster autoscaler** (if enabled):
   - Nodes scale down automatically
   - Scale up when workloads request GPU

---

## Troubleshooting

### Nodes Not Coming Up

```bash
# Check Machine status
oc get machines -n openshift-machine-api | grep gpu
oc describe machine <machine-name> -n openshift-machine-api

# Check AWS EC2 instances
aws ec2 describe-instances --filters "Name=instance-type,Values=g6.4xlarge"
```

### GPU Not Detected

```bash
# Check NVIDIA GPU Operator
oc get pods -n nvidia-gpu-operator

# Check Node Feature Discovery
oc get pods -n openshift-nfd

# Verify GPU labels
oc get nodes -l node-role.kubernetes.io/gpu=true --show-labels
```

### Quota Issues

```bash
# Check AWS service quotas
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-34B43A08  # Running On-Demand G instances
```

---

## Cleanup

To remove GPU worker nodes:

```bash
# Delete MachineSets
oc delete machineset ocp-xf56d-worker-gpu-us-east-2a -n openshift-machine-api
oc delete machineset ocp-xf56d-worker-gpu-us-east-2b -n openshift-machine-api

# Wait for nodes to be drained and removed
oc get nodes -l node-role.kubernetes.io/gpu=true -w
```

---

**Need help?** → [Troubleshooting Guide](troubleshooting.md) | [Quick Reference](quick-reference.md)

