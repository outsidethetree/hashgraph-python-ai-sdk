#!/usr/bin/env python3
"""
Hedera Agent Launcher - One Line Start

Simple launcher script to start the Hedera CLI Agent with proper setup.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the project root directory
    project_root = Path(__file__).parent
    demo_dir = project_root / "demo"
    
    # Check if we're in the right directory
    if not demo_dir.exists():
        print("❌ Error: demo directory not found!")
        print("Please run this script from the project root directory.")
        return 1
    
    # Check for .env file
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️  No .env file found. Creating example...")
        example_env = """# Hedera Agent Configuration
# Copy these values and fill them in:

# Required for CLI agent
OPENAI_API_KEY=your_openai_api_key_here

# Optional for real Hedera operations (leave blank for mock mode)
HEDERA_NETWORK=testnet
OPERATOR_ID=0.0.your_account_id
OPERATOR_KEY=your_private_key_here
"""
        with open(env_file, 'w') as f:
            f.write(example_env)
        
        print(f"✅ Created .env file at {env_file}")
        print("Please edit it with your credentials and run again.")
        return 1
    
    # Change to demo directory and run the agent
    try:
        print("🚀 Starting Hedera CLI Agent...")
        print("=" * 40)
        
        # Run the CLI agent from the demo directory
        result = subprocess.run([
            sys.executable, "cli_agent.py"
        ], cwd=demo_dir)
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error starting agent: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 