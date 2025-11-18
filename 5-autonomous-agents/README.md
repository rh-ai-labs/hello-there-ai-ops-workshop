# Autonomous Agents: Integrating Analysis + Action

**Project:** AI Test Drive – Module 5: Agentes Autônomos  
**Goal:** Build an autonomous agent that can take actions in IT operations to remediate issues automatically

---

## 📋 Overview

This module demonstrates how to build autonomous agents that can analyze IT environments, identify problems, and take corrective actions automatically. Unlike previous modules that focused on analysis and recommendations, this module shows how to integrate AI with action-taking capabilities.

**Target Audience:** IT professionals, business analysts, project managers (not data scientists)  
**Approach:** Educational, step-by-step, with clear explanations of each concept

---

## 🎯 Learning Objectives

By the end of this module, you will understand:

1. **What autonomous agents are** and how they differ from traditional automation
2. **How to build an agent framework** that can reason, plan, and act
3. **How to integrate analysis with action** using LLMs and tools
4. **How agents learn from feedback** to improve over time
5. **Practical applications** in IT operations remediation

---

## 🚀 Quick Start

### Prerequisites

1. **Python Environment**
   ```bash
   # Using uv (recommended)
   cd /Users/gsampaio/redhat/ai/hello-there-ai-ops-workshop
   uv sync
   ```

2. **Ollama (for LLM)**
   ```bash
   # Install Ollama: https://ollama.ai
   # Start server
   ollama serve
   
   # Pull model
   ollama pull llama3.2:3b
   ```

3. **Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

### Running the Notebooks

Execute notebooks in order:
1. `01_introduction_to_agents.ipynb` - Understanding autonomous agents
2. `02_building_simple_agent.ipynb` - Creating an agent with tools
3. `03_agent_decision_making.ipynb` - Decision making and action execution
4. `04_learning_from_feedback.ipynb` - Feedback loops and continuous learning

---

## 📚 Notebook Sequence

### Notebook 01: Introduction to Autonomous Agents ✅

**What it does:**
- Explains what autonomous agents are and how they work
- Compares agents to traditional automation
- Introduces key concepts: perception, reasoning, planning, action
- Shows a simple example of an agent making decisions

**Key Concepts:**
- **Autonomous Agent:** A system that can perceive its environment, reason about it, and take actions
- **Agent Loop:** Observe → Think → Act → Learn
- **Tools:** Actions the agent can take (like API calls, scripts, commands)

**Outputs:**
- Understanding of agent architecture
- Simple agent demonstration

---

### Notebook 02: Building a Simple Agent with Tools ✅

**What it does:**
- Builds a basic agent framework using LangChain
- Defines tools the agent can use (simulated IT operations)
- Shows how an agent selects and uses tools
- Demonstrates agent reasoning process

**Key Concepts:**
- **Tool Definition:** What actions are available to the agent
- **Tool Selection:** How the agent chooses which tool to use
- **Action Execution:** How the agent executes tools and handles results

**Outputs:**
- Working agent framework
- Tool definitions and implementations

---

### Notebook 03: Agent Decision Making and Action Execution ✅

**What it does:**
- Shows how agents analyze problems and create action plans
- Demonstrates multi-step reasoning (breaking down complex problems)
- Implements action execution with safety checks
- Shows how agents handle failures and retries

**Key Concepts:**
- **Planning:** Breaking down problems into steps
- **Reasoning Chain:** Step-by-step thinking process
- **Safety Checks:** Validating actions before execution
- **Error Handling:** What to do when actions fail

**Outputs:**
- Agent with planning capabilities
- Multi-step problem solving demonstration

---

### Notebook 04: Learning from Actions and Feedback Loop ✅

**What it does:**
- Implements feedback collection from actions
- Shows how agents learn from successful and failed actions
- Demonstrates continuous improvement
- Builds a memory system for the agent

**Key Concepts:**
- **Feedback Loop:** Learning from action outcomes
- **Memory:** Storing past experiences
- **Continuous Learning:** Improving over time
- **Success Metrics:** Measuring agent performance

**Outputs:**
- Agent with learning capabilities
- Feedback and memory system

---

## 🔑 Key Concepts

### What is an Autonomous Agent?

An **autonomous agent** is a system that can:
1. **Perceive** its environment (gather information)
2. **Reason** about what it perceives (think and plan)
3. **Act** on its reasoning (take actions)
4. **Learn** from the results (improve over time)

**Key Difference from Automation:**
- **Traditional Automation:** Follows fixed rules (if X then Y)
- **Autonomous Agent:** Uses AI to reason and adapt (if X, analyze context, then decide Y or Z)

### Agent Architecture

```
┌─────────────┐
│  Perception │ ← Gather information about environment
└──────┬──────┘
       │
┌──────▼──────┐
│  Reasoning  │ ← Analyze, plan, decide what to do
└──────┬──────┘
       │
┌──────▼──────┐
│   Action    │ ← Execute tools/actions
└──────┬──────┘
       │
┌──────▼──────┐
│   Learning  │ ← Learn from results, update memory
└──────┬──────┘
       │
       └──────→ Loop back to Perception
```

### Tools and Actions

**Tools** are the actions an agent can take. Examples:
- `check_service_status` - Check if a service is running
- `restart_service` - Restart a service
- `scale_resources` - Increase/decrease resources
- `rollback_deployment` - Revert to previous version

**Tool Selection:**
The agent uses LLM reasoning to decide which tool to use based on the current situation.

### Safety and Control

**Important:** In real IT environments, agents should have:
- **Approval gates** for critical actions
- **Dry-run mode** to test actions without executing
- **Rollback capabilities** to undo changes
- **Audit logging** to track all actions

---

## 📊 Project Structure

```
5-autonomous-agents/
├── data/                    # Datasets and logs
├── notebooks/               # Jupyter notebooks (01-04)
│   ├── 01_introduction_to_agents.ipynb
│   ├── 02_building_simple_agent.ipynb
│   ├── 03_agent_decision_making.ipynb
│   └── 04_learning_from_feedback.ipynb
├── src/                    # Source code modules
│   ├── __init__.py
│   ├── agent.py           # Core agent framework
│   ├── tools.py           # Tool definitions
│   ├── environment.py     # Simulated IT environment
│   └── memory.py          # Agent memory system
└── README.md              # This file
```

---

## 🛠️ Dependencies

**Core Libraries:**
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `matplotlib`, `seaborn` - Visualizations
- `jupyter` - Notebook environment

**AI/ML Libraries:**
- `llama-stack` - Agent framework and unified API
- `ollama` - Local LLM serving
- `requests` - HTTP client for llamastack API calls

**Utilities:**
- `python-dotenv` - Environment variables
- `tqdm` - Progress bars

---

## 🎯 Use Cases

This module demonstrates agents for:

1. **Service Health Monitoring**
   - Detect service failures
   - Automatically restart failed services
   - Scale resources when needed

2. **Incident Remediation**
   - Identify root causes
   - Apply fixes automatically
   - Verify resolution

3. **Resource Management**
   - Monitor resource usage
   - Scale up/down automatically
   - Optimize resource allocation

---

## ⚠️ Important Notes

### Safety First

**This is an educational module.** In production environments:

- ✅ Always implement approval gates for critical actions
- ✅ Use dry-run mode for testing
- ✅ Implement comprehensive logging and auditing
- ✅ Have rollback mechanisms in place
- ✅ Start with read-only operations
- ✅ Gradually enable actions with proper safeguards

### Simulated Environment

The agents in this module work with a **simulated IT environment** for safety and educational purposes. Real implementations would connect to actual IT systems with proper authentication and authorization.

---

## 📈 Current Status

**Completed:**
- ✅ Module structure and documentation
- 🔄 Notebook 01: Introduction to Autonomous Agents (in progress)
- ⏳ Notebook 02: Building Simple Agent
- ⏳ Notebook 03: Agent Decision Making
- ⏳ Notebook 04: Learning from Feedback

---

## 🎯 Next Steps

1. Complete all notebooks
2. Add more sophisticated tools and actions
3. Implement more advanced learning mechanisms
4. Add safety and control features
5. Integrate with real IT systems (with proper safeguards)

---

**Last Updated:** January 2025  
**Project:** AI Test Drive – Module 5: Agentes Autônomos

