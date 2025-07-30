#!/usr/bin/env python3
"""
Quick Hedera Agent Demo

Demonstrates the agent kit capabilities without requiring real credentials.
Shows both mock mode and the potential for real operations.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hedera_agent_kit import agent_registry
from hedera_agent_kit.client import client_manager

async def run_demo():
    print("🌟 Hedera Agent Kit - Quick Demo")
    print("=" * 50)
    
    # Show current configuration
    print(f"📊 Current Configuration:")
    print(f"   • Network: {client_manager.network}")
    print(f"   • SDK Available: {'✅ Yes' if hasattr(agent_registry, 'SDK_AVAILABLE') else '❓ Unknown'}")
    print(f"   • Client Configured: {'✅ Yes' if client_manager.is_configured else '❌ No'}")
    print(f"   • Mode: {'🌐 Live Network' if client_manager.is_configured else '🧪 Mock/Testing'}")
    
    print(f"\n🚀 Testing Core Operations:")
    
    # Test 1: Create Account
    print(f"\n1️⃣ Creating a new account...")
    try:
        result = await agent_registry.call_tool("create_account", {
            "initial_balance": 5.0
        })
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Check Balance
    print(f"\n2️⃣ Checking account balance...")
    try:
        result = await agent_registry.call_tool("get_balance", {})
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Create Token
    print(f"\n3️⃣ Creating a fungible token...")
    try:
        result = await agent_registry.call_tool("create_fungible_token", {
            "name": "Demo Token",
            "symbol": "DEMO",
            "initial_supply": 1000000,
            "decimals": 2
        })
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Create Topic
    print(f"\n4️⃣ Creating a consensus topic...")
    try:
        result = await agent_registry.call_tool("create_topic", {
            "memo": "Demo topic for testing"
        })
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n✅ Demo Complete!")
    print(f"\n💡 Next Steps:")
    if not client_manager.is_configured:
        print("   • Add real Hedera credentials to .env file to use live network")
        print("   • Set OPERATOR_ID and OPERATOR_KEY for your testnet account")
    print("   • Run the full CLI agent: python3 ../start_agent.py")
    print("   • Try natural language commands with OpenAI integration")

def main():
    load_dotenv()
    
    print("Loading Hedera Agent Kit...")
    asyncio.run(run_demo())

if __name__ == "__main__":
    main() 