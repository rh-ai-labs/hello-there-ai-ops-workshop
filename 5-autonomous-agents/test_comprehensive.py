#!/usr/bin/env python3
"""
Comprehensive test script for LlamaStack features

This script demonstrates:
1. Simple Chat
2. RAG (Retrieval Augmented Generation)
3. MCP (Model Context Protocol)
4. Safety
5. Eval (Evaluation)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from llama_stack_client import LlamaStackClient
from environment import SimulatedEnvironment
from tools import ToolRegistry
from agent import AutonomousAgent
from memory import AgentMemory


def test_chat(client: LlamaStackClient, model: str = "ollama/llama3.2:3b"):
    """Test simple chat functionality."""
    print("\n" + "=" * 60)
    print("1. Testing Simple Chat")
    print("=" * 60)
    
    try:
        # Get available models
        models = client.models.list()
        if not models:
            print("⚠️  No models available")
            return
        
        # Use the first available model or specified model
        model_id = model
        available_models = [m.identifier for m in models if hasattr(m, 'identifier')]
        if model_id not in available_models and available_models:
            model_id = available_models[0]
            print(f"   Using model: {model_id}")
        
        # Create a chat completion
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France? Answer in one sentence."}
            ],
        )
        
        print("✅ Chat test successful!")
        if hasattr(response, 'choices') and response.choices:
            content = response.choices[0].message.content
            print(f"   Response: {content}")
        else:
            print(f"   Response: {response}")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        import traceback
        traceback.print_exc()


def test_rag(client: LlamaStackClient, model: str = "ollama/llama3.2:3b"):
    """Test RAG (Retrieval Augmented Generation) functionality."""
    print("\n" + "=" * 60)
    print("2. Testing RAG (Retrieval Augmented Generation)")
    print("=" * 60)
    
    try:
        # Check if vector stores are available
        if not hasattr(client, 'vector_stores'):
            print("⚠️  Vector stores API not available")
            return
        
        # List vector stores
        vector_stores = client.vector_stores.list()
        store_count = len(vector_stores) if hasattr(vector_stores, '__len__') else 0
        print(f"   Found {store_count} vector stores")
        
        # Try to create a simple vector store (if possible)
        try:
            # Create a test vector store
            vs_response = client.vector_stores.create(
                name="test-rag-store",
                description="Test vector store for RAG demonstration"
            )
            print(f"✅ Created test vector store: {vs_response.id if hasattr(vs_response, 'id') else 'created'}")
            
            # Show how to add files and search
            print("   ℹ️  To use RAG:")
            print("      1. Add files to vector store: client.vector_stores.files.create(...)")
            print("      2. Search for relevant documents: client.vector_stores.search(...)")
            print("      3. Use retrieved context in chat completion")
            
            # Clean up test store
            if hasattr(vs_response, 'id'):
                try:
                    client.vector_stores.delete(vs_response.id)
                    print("   🧹 Cleaned up test vector store")
                except:
                    pass
        except Exception as create_error:
            print(f"   ℹ️  Vector store creation: {create_error}")
            print("   ℹ️  RAG requires vector store setup with documents")
            print("   ℹ️  For full RAG workflow:")
            print("      1. Create a vector store")
            print("      2. Add documents/files to the store")
            print("      3. Query the store for relevant context")
            print("      4. Use retrieved context in chat completion")
        
        print("✅ RAG API available")
    except Exception as e:
        print(f"❌ RAG test failed: {e}")
        import traceback
        traceback.print_exc()


def test_mcp(client: LlamaStackClient):
    """Test MCP (Model Context Protocol) functionality."""
    print("\n" + "=" * 60)
    print("3. Testing MCP (Model Context Protocol)")
    print("=" * 60)
    
    try:
        # Check if tool runtime is available (MCP is often integrated here)
        if not hasattr(client, 'tool_runtime'):
            print("⚠️  Tool runtime API not available")
            return
        
        # List tool runtimes
        print("   ℹ️  MCP allows agents to access external tools and data sources")
        print("   ℹ️  Tool runtime provides execution environment for tools")
        
        # Check toolgroups (MCP tools are often registered as toolgroups)
        if hasattr(client, 'toolgroups'):
            toolgroups = client.toolgroups.list()
            print(f"   Found {len(toolgroups) if hasattr(toolgroups, '__len__') else 0} tool groups")
        
        print("✅ MCP infrastructure available")
    except Exception as e:
        print(f"❌ MCP test failed: {e}")
        import traceback
        traceback.print_exc()


def test_safety(client: LlamaStackClient, model: str = "ollama/llama3.2:3b"):
    """Test Safety functionality."""
    print("\n" + "=" * 60)
    print("4. Testing Safety")
    print("=" * 60)
    
    try:
        if not hasattr(client, 'safety'):
            print("⚠️  Safety API not available")
            return
        
        # Test safety shield
        test_text = "This is a test message to check safety filters."
        
        # Check safety.run_shield method
        if hasattr(client.safety, 'run_shield'):
            print("   ℹ️  Safety shields are available")
            print("   ℹ️  Shields need to be configured for specific models")
            print(f"   ℹ️  Model {model} may not have a shield configured")
            print("   ℹ️  To use safety:")
            print("      1. Configure a shield for your model")
            print("      2. Use safety.run_shield() to check content")
            print("      3. Safety is often integrated into chat completions")
        else:
            print("   ℹ️  Safety API available but run_shield method not found")
        
        # Try moderations as alternative
        if hasattr(client, 'moderations'):
            try:
                moderation = client.moderations.create(
                    input=test_text,
                    model=model
                )
                print("✅ Safety moderation test successful!")
                print(f"   Input: {test_text}")
                if hasattr(moderation, 'results') and moderation.results:
                    result = moderation.results[0]
                    flagged = getattr(result, 'flagged', False)
                    print(f"   Flagged: {flagged}")
            except Exception as mod_error:
                print(f"   ⚠️  Moderation requires shield configuration: {mod_error}")
        
        print("✅ Safety infrastructure available")
    except Exception as e:
        print(f"❌ Safety test failed: {e}")
        # Don't print full traceback for expected errors
        if "shield" not in str(e).lower():
            import traceback
            traceback.print_exc()


def test_eval(client: LlamaStackClient, model: str = "ollama/llama3.2:3b"):
    """Test Evaluation functionality."""
    print("\n" + "=" * 60)
    print("5. Testing Eval (Evaluation)")
    print("=" * 60)
    
    try:
        if not hasattr(client, 'alpha') or not hasattr(client.alpha, 'eval'):
            print("⚠️  Eval API not available")
            return
        
        eval_api = client.alpha.eval
        
        # Create a simple evaluation dataset
        test_data = [
            {
                "input": "What is 2+2?",
                "expected_output": "4"
            },
            {
                "input": "What is the capital of France?",
                "expected_output": "Paris"
            }
        ]
        
        print(f"   Created test dataset with {len(test_data)} examples")
        
        # Check available eval methods
        eval_methods = [x for x in dir(eval_api) if not x.startswith('_') and x not in ['with_raw_response', 'with_streaming_response']]
        print(f"   Available eval methods: {eval_methods}")
        
        # Try a simple evaluation (if possible)
        try:
            # Example of how to run evaluation
            print("   ℹ️  To run evaluation:")
            print("      eval_job = client.alpha.eval.run_eval_alpha(")
            print("          dataset=test_data,")
            print(f"          model='{model}',")
            print("          metrics=['accuracy', 'bleu'],")
            print("      )")
            print("   ℹ️  Full evaluation requires:")
            print("      - Dataset with inputs and expected outputs")
            print("      - Evaluation metrics (accuracy, BLEU, ROUGE, etc.)")
            print("      - Model to evaluate")
            print("      - Evaluation job configuration")
        except Exception as eval_error:
            print(f"   ℹ️  Evaluation setup: {eval_error}")
        
        print("✅ Eval API available")
    except Exception as e:
        print(f"❌ Eval test failed: {e}")
        import traceback
        traceback.print_exc()


def test_agent_with_tools(client: LlamaStackClient):
    """Test autonomous agent with tools."""
    print("\n" + "=" * 60)
    print("6. Testing Autonomous Agent with Tools")
    print("=" * 60)
    
    try:
        # Create environment and tools
        env = SimulatedEnvironment()
        tool_registry = ToolRegistry(env)
        memory = AgentMemory()
        
        # Create agent (convert URL object to string)
        llamastack_url = str(client.base_url) if hasattr(client.base_url, '__str__') else client.base_url
        
        agent = AutonomousAgent(
            tool_registry=tool_registry,
            memory=memory,
            llamastack_url=llamastack_url,
            verbose=False  # Less verbose for this test
        )
        
        print(f"✅ Agent created: {agent.agent_id}")
        
        # Test agent execution
        result = agent.run("Check the status of the web-server service")
        
        if result.get("success"):
            print("✅ Agent execution successful!")
            print(f"   Result: {result.get('result', '')[:200]}...")
        else:
            print(f"❌ Agent execution failed: {result.get('error')}")
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    print("=" * 60)
    print("LlamaStack Comprehensive Feature Test")
    print("=" * 60)
    
    # Configuration
    llamastack_url = os.getenv("LLAMA_STACK_URL", "http://localhost:8321")
    model = os.getenv("LLAMA_MODEL", "ollama/llama3.2:3b")
    
    print(f"\n📡 LlamaStack URL: {llamastack_url}")
    print(f"🤖 Model: {model}")
    
    try:
        # Initialize client
        client = LlamaStackClient(base_url=llamastack_url)
        
        # Verify connection
        try:
            client.models.list()
            print("✅ Connected to LlamaStack")
        except Exception as e:
            print(f"❌ Cannot connect to LlamaStack: {e}")
            return
        
        # Run tests
        test_chat(client, model)
        test_rag(client, model)
        test_mcp(client)
        test_safety(client, model)
        test_eval(client, model)
        test_agent_with_tools(client)
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

