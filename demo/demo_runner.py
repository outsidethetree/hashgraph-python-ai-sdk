#!/usr/bin/env python3
"""
Quick demo runner to show the CLI agent interface
"""

import os
import sys

def show_demo_interface():
    print("🌟 Welcome to the Hedera CLI Agent! 🌟")
    print("=" * 50)
    print("I can help you with Hedera operations using natural language!")
    print("\n📋 What I can do:")
    print("• Create accounts and check balances")
    print("• Transfer HBAR between accounts") 
    print("• Create and manage tokens")
    print("• Create topics and send messages")
    print("• And much more!")
    print("\n💡 Example commands:")
    print("• 'Create a new account with 10 HBAR'")
    print("• 'Transfer 5 HBAR to account 0.0.12345'")
    print("• 'Check my balance'")
    print("• 'Create a token called MyToken with symbol MT'")
    print("\n⚙️ Environment:")
    print(f"• Network: {os.getenv('HEDERA_NETWORK', 'not set')}")
    print(f"• Operator: {os.getenv('OPERATOR_ID', 'not set')}")
    print(f"• OpenAI Key: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}")
    print("=" * 50)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("\n💡 To use the full CLI agent:")
        print("1. Get an OpenAI API key from https://platform.openai.com/api-keys")
        print("2. Add OPENAI_API_KEY=your_key_here to your .env file")
        print("3. Run: python3 cli_agent.py")
        print("\n🧪 For testing, the agent works with mock data!")
    else:
        print("\n🚀 Ready to use! Run: python3 cli_agent.py")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    show_demo_interface() 