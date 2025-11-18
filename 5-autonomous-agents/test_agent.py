#!/usr/bin/env python3
"""
Test script for AutonomousAgent with LlamaStack SDK

This script tests the agent creation and execution step by step.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from environment import SimulatedEnvironment
from tools import ToolRegistry
from agent import AutonomousAgent
from memory import AgentMemory

def main():
    print("=" * 60)
    print("Testing AutonomousAgent with LlamaStack SDK")
    print("=" * 60)
    
    # Configuration
    llamastack_url = os.getenv("LLAMA_STACK_URL", "http://localhost:8321")
    print(f"\n📡 LlamaStack URL: {llamastack_url}")
    
    # Step 1: Create environment
    print("\n" + "=" * 60)
    print("Step 1: Creating SimulatedEnvironment")
    print("=" * 60)
    try:
        env = SimulatedEnvironment()
        print("✅ Environment created")
        print(f"   Services: {list(env.services.keys())}")
    except Exception as e:
        print(f"❌ Error creating environment: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 2: Create tool registry
    print("\n" + "=" * 60)
    print("Step 2: Creating ToolRegistry")
    print("=" * 60)
    try:
        tool_registry = ToolRegistry(env)
        tools = tool_registry.list_tools()
        print(f"✅ Tool registry created")
        print(f"   Tools available: {len(tools)}")
        for tool in tools:
            print(f"     - {tool['name']}: {tool['description'][:50]}...")
    except Exception as e:
        print(f"❌ Error creating tool registry: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Check tool format
    print("\n" + "=" * 60)
    print("Step 3: Checking tool format for LlamaStack")
    print("=" * 60)
    try:
        llamastack_tools = tool_registry.get_tools_for_llamastack()
        print(f"✅ Tools formatted for LlamaStack")
        print(f"   Number of tools: {len(llamastack_tools)}")
        if llamastack_tools:
            print(f"\n   First tool structure:")
            import json
            print(json.dumps(llamastack_tools[0], indent=2))
    except Exception as e:
        print(f"❌ Error formatting tools: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Create memory
    print("\n" + "=" * 60)
    print("Step 4: Creating AgentMemory")
    print("=" * 60)
    try:
        memory = AgentMemory()
        print("✅ Memory created")
    except Exception as e:
        print(f"❌ Error creating memory: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 5: Create agent
    print("\n" + "=" * 60)
    print("Step 5: Creating AutonomousAgent")
    print("=" * 60)
    try:
        agent = AutonomousAgent(
            tool_registry=tool_registry,
            memory=memory,
            llamastack_url=llamastack_url,
            verbose=True
        )
        print(f"\n✅ Agent created successfully!")
        print(f"   Agent ID: {agent.agent_id}")
        print(f"   LlamaStack URL: {agent.llamastack_url}")
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 6: Test simple task
    print("\n" + "=" * 60)
    print("Step 6: Testing simple task execution")
    print("=" * 60)
    try:
        task = "Check the status of all services"
        print(f"\n📋 Task: {task}")
        print("\n🔄 Executing task...")
        
        result = agent.run(task)
        
        print("\n" + "=" * 60)
        print("📊 Agent Result:")
        print("=" * 60)
        if result.get("success"):
            print("✅ Task completed successfully!")
            print(f"\nResult:\n{result.get('result', 'No result')}")
            if result.get("session_id"):
                print(f"\nSession ID: {result['session_id']}")
            if result.get("turn_id"):
                print(f"Turn ID: {result['turn_id']}")
            if result.get("tool_calls"):
                print(f"\nTool calls made: {len(result['tool_calls'])}")
        else:
            print("❌ Task failed!")
            print(f"Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error executing task: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()

