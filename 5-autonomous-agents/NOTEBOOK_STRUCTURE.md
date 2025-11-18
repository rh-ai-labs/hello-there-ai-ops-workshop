# Notebook Structure for Module 5: Autonomous Agents

## 📚 Proposed Notebook Sequence

### ✅ Notebook 01: Introduction to Autonomous Agents
**Status:** Exists  
**Focus:** Concepts and theory

**Content:**
- What are autonomous agents?
- Agent vs traditional automation
- The agent loop (Observe → Think → Act → Learn)
- Simple examples and demonstrations

---

### ✅ Notebook 02: Building a Simple Agent with Tools
**Status:** ✅ Complete - Updated to use Python SDK  
**Focus:** Basic agent implementation with custom tools

**Content:**
- Setting up LlamaStack connection
- Creating a custom Wikipedia search tool (no API key required)
- Creating an agent with custom tools
- Testing agent execution with AgentEventLogger
- Understanding tool calls and responses
- Creating custom client-side tools (IT operations example)

**Completed Updates:**
- ✅ Refactored to use Python SDK (Agent class from llama-stack-client)
- ✅ Replaced DuckDuckGo with Wikipedia search (more reliable, no API key)
- ✅ Simplified setup cell (removed installation logic, assumes requirements.txt)
- ✅ Fixed inspection code (removed get_session calls)
- ✅ Improved Wikipedia search function (uses search API first)
- ✅ Added custom IT tools example (check_service_status, restart_service)
- ✅ All custom tools working correctly with Agent class

---

### ✅ Notebook 03: LlamaStack Core Features
**Status:** ✅ Exists  
**Focus:** Chat, RAG, MCP, Safety, Eval basics

**Content:**
1. **Simple Chat**
   - Basic chat completions
   - System and user messages
   - Streaming responses

2. **RAG (Retrieval Augmented Generation)**
   - Creating vector stores
   - Adding documents
   - Searching for context
   - Using retrieved context in chat

3. **MCP (Model Context Protocol)**
   - Understanding tool runtime
   - Tool groups and tool execution
   - Integrating external tools

4. **Safety**
   - Safety shields
   - Content moderation
   - Safety in chat completions

5. **Eval (Evaluation)**
   - Creating evaluation datasets
   - Running evaluations
   - Understanding metrics

**Learning Path:** Each feature demonstrated independently, then shown how they integrate

---

### 📝 Notebook 04: Advanced Agent Capabilities
**Status:** To be created  
**Focus:** Combining features in agents

**Content:**
- Agents with RAG (knowledge-augmented agents)
- Agents with Safety (safe action-taking)
- Agents with MCP tools (external integrations)
- Evaluating agent performance
- Multi-step problem solving

---

### 📝 Notebook 05: Agent Decision Making and Action Execution
**Status:** Mentioned in README, to be created  
**Focus:** Complex decision-making

**Content:**
- Multi-step reasoning
- Tool selection strategies
- Handling failures and retries
- Action verification
- Complex remediation scenarios

---

### 📝 Notebook 06: Learning from Actions and Feedback Loop
**Status:** Mentioned in README, to be created  
**Focus:** Continuous improvement

**Content:**
- Agent memory and learning
- Feedback collection
- Performance tracking
- Adaptive behavior
- Case studies of learning agents

---

## 🎯 Recommended Structure

### Option A: Feature-Focused (Recommended)
**Progression:** Features → Integration → Advanced

1. **01_introduction_to_agents.ipynb** ✅ (Concepts)
2. **02_building_simple_agent.ipynb** ✅ (Basic agent)
3. **03_llamastack_features.ipynb** 📝 (Chat, RAG, MCP, Safety, Eval)
4. **04_advanced_agents.ipynb** 📝 (Combining features)
5. **05_agent_decision_making.ipynb** 📝 (Complex scenarios)
6. **06_learning_and_feedback.ipynb** 📝 (Continuous improvement)

### Option B: Progressive Integration
**Progression:** Simple → Complex features

1. **01_introduction_to_agents.ipynb** ✅
2. **02_building_simple_agent.ipynb** ✅
3. **03_chat_and_basic_features.ipynb** 📝 (Chat, Safety)
4. **04_rag_and_knowledge.ipynb** 📝 (RAG integration)
5. **05_mcp_and_external_tools.ipynb** 📝 (MCP integration)
6. **06_evaluation_and_improvement.ipynb** 📝 (Eval, Learning)

---

## 💡 Recommendation: Option A

**Why Option A?**
- Clear separation of concerns
- Each notebook has a focused learning objective
- Easier to reference specific features
- Better for modular learning

**Notebook 03 Structure:**
```
# Notebook 03: LlamaStack Core Features

## Part 1: Simple Chat
- Basic chat completions
- Message types and roles
- Streaming responses
- Practical examples

## Part 2: RAG (Retrieval Augmented Generation)
- What is RAG?
- Creating vector stores
- Adding documents
- Searching and retrieval
- Using context in chat

## Part 3: MCP (Model Context Protocol)
- What is MCP?
- Tool runtime
- Tool groups
- External tool integration

## Part 4: Safety
- Safety shields
- Content moderation
- Safety in production

## Part 5: Evaluation
- Evaluation datasets
- Running evaluations
- Understanding metrics
- Best practices

## Summary
- How all features work together
- When to use each feature
- Next steps
```

---

## 📋 Implementation Plan

1. **✅ Update Notebook 02** - Refactor to use Python SDK - **COMPLETED**
   - Uses Agent class from llama-stack-client
   - Custom Wikipedia search tool
   - Custom IT operations tools example
   - All working correctly
2. **✅ Create Notebook 03** - LlamaStack features - **COMPLETED**
3. **📝 Create Notebook 04** - Advanced agent capabilities - **TODO**
4. **📝 Create Notebook 05** - Decision making (if needed) - **TODO**
5. **📝 Create Notebook 06** - Learning and feedback (if needed) - **TODO**

## 🎯 Recent Changes (Latest Session)

### Notebook 02 Updates:
- **Replaced DuckDuckGo with Wikipedia**: More reliable, no API key, works better with small models
- **Simplified setup**: Removed complex installation logic, assumes requirements.txt is used
- **Fixed errors**: Removed get_session() calls, cleaned up exception handling
- **Improved tool function**: Wikipedia search now uses search API first for better results
- **Verified functionality**: All custom tools (Wikipedia, calculator, time, IT ops) working correctly

### Key Learnings:
- Custom tools work well with Agent class when properly formatted (RST-style docstrings)
- Small models (llama3.2:3b) can use tools effectively with clear instructions
- Wikipedia API is more reliable than DuckDuckGo for educational purposes
- AgentEventLogger provides good visual feedback for tool usage

---

## 🎓 Educational Principles

Each notebook should:
- Start with clear learning objectives
- Explain concepts before code
- Provide working examples
- Include exercises or challenges
- End with a summary and next steps
- Use the simulated environment for safety

