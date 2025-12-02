# OpenShift Deployment Guide

Welcome! This guide helps you deploy LlamaStack and related services on OpenShift.

## 🚀 Quick Start

**New to this?** Start here → [Getting Started Guide](docs/01-getting-started.md)

**Just need a quick reference?** → [Quick Reference](docs/quick-reference.md)

**Having issues?** → [Troubleshooting Guide](docs/troubleshooting.md)

---

## 📚 Documentation Index

### Getting Started
- **[01. Getting Started](docs/01-getting-started.md)** - Complete setup from scratch
- **[02. Prerequisites Checklist](docs/02-prerequisites.md)** - What you need before starting

### Deployment Guides
- **[03. LlamaStack Deployment](docs/03-llamastack-deployment.md)** - Deploy LlamaStack on OpenShift
- **[04. MongoDB & MCP Setup](docs/04-mongodb-mcp-setup.md)** - Deploy MongoDB and MCP server
- **[05. GPU Worker Nodes](docs/05-gpu-worker-nodes.md)** - Add GPU nodes for inference

### Integration Guides
- **[06. MCP Integration](docs/06-mcp-integration.md)** - Complete MCP implementation guide
- **[07. Agent Configuration](docs/07-agent-configuration.md)** - Configure agents with tools

### Reference
- **[Quick Reference](docs/quick-reference.md)** - Common commands and configurations
- **[Troubleshooting](docs/troubleshooting.md)** - Solutions to common issues
- **[Architecture Overview](docs/architecture.md)** - System architecture and components

---

## 🎯 Common Tasks

### Deploy Everything
```bash
# From project root
# 1. Deploy LlamaStack
./scripts/deploy-llamastack.sh

# 2. Deploy MongoDB & MCP
./scripts/deploy-mongodb-mcp.sh

# 3. Register MCP with LlamaStack
./scripts/register-mongodb-mcp.sh
```

### Add GPU Nodes
```bash
./scripts/create-gpu-workers.sh
```

### Test Deployment
```bash
# Test LlamaStack
./scripts/test-llamastack.sh

# Test MongoDB MCP agent
python openshift/scripts/test-mongodb-agent.py
```

---

## 📁 Directory Structure

```
openshift/
├── README.md                    # This file - start here!
├── docs/                        # 📚 All documentation
│   ├── 01-getting-started.md   # First-time setup guide
│   ├── 02-prerequisites.md     # Prerequisites checklist
│   ├── 03-llamastack-deployment.md
│   ├── 04-mongodb-mcp-setup.md
│   ├── 05-gpu-worker-nodes.md
│   ├── 06-mcp-integration.md
│   ├── 07-agent-configuration.md
│   ├── quick-reference.md      # Quick reference card
│   ├── troubleshooting.md      # Common issues & solutions
│   └── architecture.md         # System architecture
├── manifests/                   # Kubernetes/OpenShift manifests
│   ├── llamastack/            # LlamaStack deployments
│   ├── mongodb/               # MongoDB & MCP server
│   ├── infrastructure/        # GPU nodes, etc.
│   └── secrets/               # Secret templates
└── scripts/                     # Deployment scripts
    ├── deploy-llamastack.sh
    ├── deploy-mongodb-mcp.sh
    ├── register-mongodb-mcp.sh
    └── create-gpu-workers.sh
```

---

## 🆘 Need Help?

1. **Check the [Troubleshooting Guide](docs/troubleshooting.md)**
2. **Review the [Quick Reference](docs/quick-reference.md)**
3. **Read the detailed guides** in the `docs/` folder

---

## ✅ What's Next?

1. ✅ **Read** [Getting Started Guide](docs/01-getting-started.md)
2. ✅ **Deploy** LlamaStack and MongoDB
3. ✅ **Configure** agents with MCP tools
4. ✅ **Start building** your AI agents!

---

**Ready to begin?** → [Getting Started Guide](docs/01-getting-started.md) 🚀
