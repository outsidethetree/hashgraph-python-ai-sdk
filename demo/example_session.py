#!/usr/bin/env python3
"""
Example: Using the Hedera Agent Programmatically

This shows how to integrate the Hedera Agent Kit into your own applications.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hedera_agent_kit import agent_registry

async def example_session():
    """Example of using the agent kit directly"""
    
    print("🌟 Hedera Agent Kit - Programmatic Example")
    print("=" * 50)
    
    try:
        # Example 1: Create an account
        print("📋 Creating a new account...")
        result = await agent_registry.call_tool("create_account", {
            "initial_balance": 10
        })
        print(f"✅ Result: {result}\n")
        
        # Example 2: Check balance
        print("💰 Checking balance...")
        result = await agent_registry.call_tool("get_balance", {})
        print(f"✅ Result: {result}\n")
        
        # Example 3: Create a token
        print("🪙 Creating a fungible token...")
        result = await agent_registry.call_tool("create_fungible_token", {
            "name": "ExampleToken",
            "symbol": "EXT", 
            "initial_supply": 1000000,
            "decimals": 2
        })
        print(f"✅ Result: {result}\n")
        
        # Example 4: Create a consensus topic
        print("💬 Creating a consensus topic...")
        result = await agent_registry.call_tool("create_topic", {
            "memo": "Example topic for demo"
        })
        print(f"✅ Result: {result}\n")
        
        # Example 5: Get available tools
        print("🔧 Available tools:")
        for tool_name in agent_registry._tools.keys():
            schema = agent_registry.get_schema(tool_name)
            print(f"  • {tool_name}: {schema.__name__}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    load_dotenv()
    await example_session()

if __name__ == "__main__":
    asyncio.run(main()) 