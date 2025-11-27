# Llama Stack OpenShift Deployment

This directory contains OpenShift manifests and deployment scripts for deploying Llama Stack on OpenShift using the LlamaStackDistribution Custom Resource.

## Prerequisites

1. **OpenShift 4.19 or newer** installed
2. **GPU support enabled** in OpenShift AI (Node Feature Discovery Operator and NVIDIA GPU Operator)
3. **Cluster administrator privileges** for your OpenShift cluster
4. **Logged in to Red Hat OpenShift AI**
5. **Llama Stack Operator activated** in OpenShift AI
6. **vLLM inference model deployed** with:
   - External route enabled
   - Token authentication enabled
   - `--enable-auto-tool-choice` runtime argument added
7. **OpenShift CLI (oc)** installed and configured

## Quick Start

### Option 1: Using the Deployment Script (Recommended)

1. **Set your configuration** (update these values as needed):

```bash
export NAMESPACE="my-first-model"
export INFERENCE_MODEL="RedHatAI/Meta-Llama-3.1-8B-Instruct-FP8-dynamic"
export VLLM_URL="https://llama-32-3b-instruct-predictor:8443/v1"
export VLLM_TLS_VERIFY="false"  # Use "true" in production
export VLLM_API_TOKEN="<your-token>"
export DEPLOYMENT_TYPE="milvus-inline"  # Options: milvus-inline, faiss-inline, milvus-remote
```

2. **Log in to OpenShift**:

```bash
# In the OpenShift web console, click your username → Copy login command → Display token
# Then paste the command:
oc login --token=<token> --server=<openshift_cluster_url>
```

3. **Run the deployment script**:

```bash
cd openshift
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### Option 2: Manual Deployment

1. **Create the inference model secret**:

```bash
export NAMESPACE="my-first-model"
export INFERENCE_MODEL="RedHatAI/Meta-Llama-3.1-8B-Instruct-FP8-dynamic"
export VLLM_URL="https://llama-32-3b-instruct-predictor:8443/v1"
export VLLM_TLS_VERIFY="false"
export VLLM_API_TOKEN="<your-token>"

oc create secret generic llama-stack-inference-model-secret \
  --from-literal=INFERENCE_MODEL="$INFERENCE_MODEL" \
  --from-literal=VLLM_URL="$VLLM_URL" \
  --from-literal=VLLM_TLS_VERIFY="$VLLM_TLS_VERIFY" \
  --from-literal=VLLM_API_TOKEN="$VLLM_API_TOKEN" \
  --namespace="$NAMESPACE"
```

2. **Deploy LlamaStackDistribution**:

Choose one of the following deployment types:

#### Example A: Inline Milvus (Development/Testing)

```bash
oc apply -f manifests/llamastackdistribution-inline-milvus.yaml
```

#### Example B: Inline FAISS (Experimental/Testing)

```bash
oc apply -f manifests/llamastackdistribution-inline-faiss.yaml
```

#### Example C: Remote Milvus (Production)

First, create the Milvus connection secret:

```bash
export MILVUS_ENDPOINT="tcp://milvus-service:19530"
export MILVUS_TOKEN="<milvus-root-or-user-token>"
export MILVUS_CONSISTENCY_LEVEL="Bounded"

oc create secret generic milvus-secret \
  --from-literal=MILVUS_ENDPOINT="$MILVUS_ENDPOINT" \
  --from-literal=MILVUS_TOKEN="$MILVUS_TOKEN" \
  --from-literal=MILVUS_CONSISTENCY_LEVEL="$MILVUS_CONSISTENCY_LEVEL" \
  --namespace="$NAMESPACE"
```

Then deploy:

```bash
oc apply -f manifests/llamastackdistribution-remote-milvus.yaml
```

## Verification

1. **Check pod status**:

```bash
oc get pods -n my-first-model -l app=llama-stack
```

2. **View pod logs**:

```bash
oc logs -l app=llama-stack -n my-first-model
```

Look for output similar to:
```
INFO     2025-05-15 11:23:52,750 __main__:498 server: Listening on ['::', '0.0.0.0']:8321
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO     2025-05-15 11:23:52,765 __main__:151 server: Starting up
INFO:     Application startup complete.
INFO:     Uvicorn running on http://['::', '0.0.0.0']:8321 (Press CTRL+C to quit)
```

3. **Check service**:

```bash
oc get svc -n my-first-model
```

4. **Create Route for external access** (recommended):

```bash
# Create route with TLS termination
oc apply -f manifests/llamastack-route.yaml

# Or create insecure route (for testing)
oc apply -f manifests/llamastack-route-insecure.yaml

# Get the route URL
oc get route llamastack-route -n my-first-model -o jsonpath='{.spec.host}'
```

The route will be accessible at `https://<route-host>` (OpenShift will auto-generate the hostname).

5. **Or port forward to access locally**:

```bash
oc port-forward -n my-first-model svc/lsd-llama-milvus-inline-service 8321:8321
```

Then access at `http://localhost:8321`

## Testing

### Quick Test Scripts

We provide two test scripts to verify your deployment:

#### Option 1: Bash Test Script

```bash
cd openshift

# Option A: Use Route (if created)
export LLAMA_STACK_URL="https://$(oc get route llamastack-route -n my-first-model -o jsonpath='{.spec.host}')"
./scripts/test-llamastack.sh

# Option B: Use port-forward (in another terminal)
oc port-forward -n my-first-model svc/lsd-llama-milvus-inline-service 8321:8321
# Then in this terminal:
./scripts/test-llamastack.sh
```

The script will:
- Test health endpoint (`/health`)
- List available models (`/v1/models`)
- Test chat completion (`/v1/chat/completions`)
- Test agents endpoint (`/v1/agents`)
- Test ingestion endpoint (`/v1/ingest`)

#### Option 2: Python Test Script

```bash
cd openshift

# Start port-forward first (in another terminal)
oc port-forward -n my-first-model svc/lsd-llama-milvus-inline-service 8321:8321

# Run the Python test script
python3 test-llamastack-python.py

# Or set custom URL
export LLAMA_STACK_URL="http://localhost:8321"
python3 test-llamastack-python.py
```

### Manual Testing with curl

**Option A: Using Route (recommended)**

```bash
# Get route URL
ROUTE_URL=$(oc get route llamastack-route -n my-first-model -o jsonpath='{.spec.host}')

# Test health endpoint
curl https://$ROUTE_URL/health

# List models
curl https://$ROUTE_URL/v1/models | jq

# Test chat completion
curl -X POST https://$ROUTE_URL/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "RedHatAI/Meta-Llama-3.1-8B-Instruct-FP8-dynamic",
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 50
  }' | jq
```

**Option B: Using port-forward**

1. **Start port-forward** (in a separate terminal):

```bash
oc port-forward -n my-first-model svc/lsd-llama-milvus-inline-service 8321:8321
```

2. **Test health endpoint**:

```bash
curl http://localhost:8321/health
```

Expected response: `{"status": "healthy"}` or similar

3. **List available models**:

```bash
curl http://localhost:8321/v1/models | jq
```

4. **Test chat completion**:

```bash
curl -X POST http://localhost:8321/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "RedHatAI/Meta-Llama-3.1-8B-Instruct-FP8-dynamic",
    "messages": [
      {
        "role": "user",
        "content": "Say hello in one sentence"
      }
    ],
    "max_tokens": 50
  }' | jq
```

### Testing from Jupyter Notebook

If you have a Jupyter notebook running in the same namespace or cluster:

```python
from llama_stack_client import LlamaStackClient

# Use the service URL directly (no port-forward needed)
client = LlamaStackClient(base_url='http://lsd-llama-milvus-inline-service.my-first-model.svc.cluster.local:8321')

# Or use localhost if port-forwarding
# client = LlamaStackClient(base_url='http://localhost:8321')

# List models
models = client.models.list()
print(f"Available models: {models.data}")

# Create a chat completion
response = client.chat.completions.create(
    model=models.data[0].id,
    messages=[
        {"role": "user", "content": "Say hello"}
    ],
    max_tokens=50
)

print(response.choices[0].message.content)
```

### Testing from Within the Cluster

If you're running tests from another pod in the cluster:

```python
from llama_stack_client import LlamaStackClient

# Use the internal service URL
client = LlamaStackClient(
    base_url='http://lsd-llama-milvus-inline.my-first-model.svc.cluster.local:8321'
)
```

## Configuration Files

- `llama-stack-inference-model-secret.yaml` - Secret containing vLLM inference model configuration
- `llamastackdistribution-inline-milvus.yaml` - LlamaStackDistribution CR with inline Milvus
- `llamastackdistribution-inline-faiss.yaml` - LlamaStackDistribution CR with inline FAISS
- `llamastackdistribution-remote-milvus.yaml` - LlamaStackDistribution CR with remote Milvus
- `llamastack-route.yaml` - Route for external access with TLS termination
- `llamastack-route-insecure.yaml` - Route allowing insecure access (for testing)
- `deploy.sh` - Automated deployment script
- `test-llamastack.sh` - Bash test script
- `test-llamastack-python.py` - Python test script
- `troubleshoot.sh` - Troubleshooting script

## Important Notes

1. **vLLM URL**: Update the `VLLM_URL` in the secret to match your actual vLLM endpoint. The URL should:
   - End with `/v1`
   - Use the internal service name if vLLM is in the same cluster
   - Use HTTPS with proper TLS verification in production

2. **Model Identifier**: Ensure `INFERENCE_MODEL` matches the model identifier used when deploying vLLM.

3. **API Token**: Replace `VLLM_API_TOKEN` with your actual API token if token authentication is enabled.

4. **Namespace**: All manifests use `my-first-model` namespace by default. Update if using a different namespace.

5. **Disconnected Environments**: If deploying in a disconnected environment, add these environment variables to the LlamaStackDistribution CR:
   ```yaml
   - name: SENTENCE_TRANSFORMERS_HOME
     value: /opt/app-root/src/.cache/huggingface/hub
   - name: HF_HUB_OFFLINE
     value: "1"
   - name: TRANSFORMERS_OFFLINE
     value: "1"
   - name: HF_DATASETS_OFFLINE
     value: "1"
   ```

## Troubleshooting

### Pod not starting

```bash
# Check pod events
oc describe pod -l app=llama-stack -n my-first-model

# Check logs
oc logs -l app=llama-stack -n my-first-model
```

### Cannot connect to vLLM endpoint (Connection Error)

This is the most common issue. The error `VLLMInferenceAdapter.list_provider_model_ids() failed with: Connection error` means Llama Stack cannot reach the vLLM service.

**Diagnosis:**

```bash
# Run diagnostic script
cd openshift
./fix-vllm-connection.sh

# Or find vLLM service
./find-vllm-service.sh
```

**Common fixes:**

1. **Use Fully Qualified Domain Name (FQDN)** if vLLM is in a different namespace:
   ```bash
   # Find vLLM service namespace
   oc get svc --all-namespaces | grep predictor
   
   # Update secret with FQDN
   oc create secret generic llama-stack-inference-model-secret \
     --from-literal=VLLM_URL="https://<service-name>.<namespace>.svc.cluster.local:<port>/v1" \
     --from-literal=VLLM_TLS_VERIFY="false" \
     --from-literal=VLLM_API_TOKEN="<token>" \
     --from-literal=INFERENCE_MODEL="RedHatAI/Meta-Llama-3.1-8B-Instruct-FP8-dynamic" \
     --namespace="my-first-model" \
     --dry-run=client -o yaml | oc apply -f -
   
   # Restart pod to pick up new secret
   oc delete pod -l app=llama-stack -n my-first-model
   ```

2. **Check network policies:**
   ```bash
   oc get networkpolicies -n my-first-model
   oc get networkpolicies -n <vllm-namespace>
   ```

3. **Test connectivity from pod:**
   ```bash
   POD_NAME=$(oc get pods -n my-first-model -l app=llama-stack -o jsonpath='{.items[0].metadata.name}')
   oc exec $POD_NAME -n my-first-model -- curl -k https://<vllm-service-url>/v1/models
   ```

4. **Verify vLLM service exists and is running:**
   ```bash
   oc get svc --all-namespaces | grep vllm
   oc get pods --all-namespaces | grep vllm
   ```

### Secret not found

- Ensure the secret is created in the correct namespace
- Verify secret keys match what's referenced in the CR

## Next Steps

After successful deployment, you can:

1. **Ingest content** into your model using the Llama Stack SDK in a Jupyter notebook
2. **Create agents** using the Llama Stack API
3. **Build RAG workflows** with your vector store

See the main project README for examples and usage.

