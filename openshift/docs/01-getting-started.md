# Getting Started with LlamaStack on OpenShift

Welcome! This guide will walk you through deploying LlamaStack and related services on OpenShift step by step.

## 🎯 What You'll Deploy

By the end of this guide, you'll have:
- ✅ LlamaStack running on OpenShift
- ✅ MongoDB database with sample data
- ✅ MongoDB MCP server for agent integration
- ✅ Everything connected and ready to use

---

## ⏱️ Time Estimate

- **Total time**: 30-45 minutes
- **Prerequisites check**: 5 minutes
- **Deployment**: 20-30 minutes
- **Verification**: 5-10 minutes

---

## 📋 Step 1: Check Prerequisites

Before starting, make sure you have everything you need:

👉 **[Go to Prerequisites Checklist](02-prerequisites.md)**

**Quick checklist:**
- [ ] OpenShift cluster access
- [ ] `oc` CLI installed and logged in
- [ ] Cluster admin privileges
- [ ] vLLM inference model deployed
- [ ] LlamaStack Operator activated

---

## 🚀 Step 2: Deploy LlamaStack

### Quick Deploy (Recommended)

```bash
cd openshift/scripts
./deploy-llamastack.sh
```

This script will:
1. ✅ Create necessary secrets
2. ✅ Deploy LlamaStackDistribution
3. ✅ Create routes for external access
4. ✅ Verify deployment

### What Happens

The script detects your vLLM configuration and creates:
- **LlamaStackDistribution** - Main LlamaStack deployment
- **Route** - External access URL
- **Secrets** - Configuration and credentials

**Expected time**: 5-10 minutes

---

## 🗄️ Step 3: Deploy MongoDB & MCP Server

### Quick Deploy

```bash
cd openshift/scripts
./deploy-mongodb-mcp.sh
```

This script will:
1. ✅ Deploy MongoDB database
2. ✅ Deploy MongoDB MCP server
3. ✅ Initialize database with sample data
4. ✅ Create routes for access

**Expected time**: 5-10 minutes

---

## 🔗 Step 4: Register MCP Server

Connect MongoDB MCP server to LlamaStack:

```bash
cd openshift/scripts
./register-mongodb-mcp.sh
```

This registers the MongoDB MCP server as a toolgroup that agents can use.

**Expected time**: 1-2 minutes

---

## ✅ Step 5: Verify Everything Works

### Test LlamaStack

```bash
# Get LlamaStack URL
LLAMA_STACK_URL=$(oc get route llamastack-route -n my-first-model -o jsonpath='{.spec.host}')

# Test connection
curl -k https://${LLAMA_STACK_URL}/v1/models
```

### Test MongoDB MCP

```bash
# Test MongoDB MCP agent
python openshift/scripts/test-mongodb-agent-simple.py
```

---

## 🎉 Success!

If everything worked, you should see:
- ✅ LlamaStack responding to API calls
- ✅ MongoDB MCP server registered
- ✅ Agents can use MongoDB tools

---

## 📚 Next Steps

Now that everything is deployed:

1. **Learn about MCP**: [MCP Integration Guide](06-mcp-integration.md)
2. **Configure agents**: [Agent Configuration Guide](07-agent-configuration.md)
3. **Add GPU nodes**: [GPU Worker Nodes Guide](05-gpu-worker-nodes.md) (optional)

---

## 🆘 Having Issues?

👉 **[Check Troubleshooting Guide](troubleshooting.md)**

Common issues:
- LlamaStack not accessible → Check routes and services
- MCP registration fails → Verify MCP server is running
- Connection errors → Check network policies and firewalls

---

## 📖 Detailed Guides

For more information, see:
- **[LlamaStack Deployment](03-llamastack-deployment.md)** - Detailed LlamaStack setup
- **[MongoDB & MCP Setup](04-mongodb-mcp-setup.md)** - Detailed MongoDB setup
- **[Quick Reference](quick-reference.md)** - Common commands

---

**Ready to continue?** → [Prerequisites Checklist](02-prerequisites.md) → [LlamaStack Deployment](03-llamastack-deployment.md)

