#!/usr/bin/env python3
"""
Hedera CLI Agent Demo - Production Ready

A conversational agent that can perform Hedera operations using natural language.
Uses OpenAI GPT to understand user requests and execute them via the Hedera Agent Kit.
"""

import asyncio
import json
import os
import sys
from typing import Dict, Any, List
from dotenv import load_dotenv
import openai

# Add parent directory to path to import hedera_agent_kit
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hedera_agent_kit import agent_registry
from hedera_agent_kit.client import client_manager

# Load environment variables
load_dotenv()

class HederaAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.available_tools = self._get_available_tools()
        
    def _get_available_tools(self) -> List[Dict[str, Any]]:
        """Generate OpenAI function definitions from our agent registry"""
        tools = []
        
        # Core tool definitions for OpenAI function calling
        tool_definitions = {
            "create_account": {
                "description": "Create a new Hedera account with optional initial balance",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "initial_balance": {"type": "number", "description": "Initial HBAR balance (default: 0)"},
                        "public_key": {"type": "string", "description": "Public key (optional, will generate if not provided)"}
                    }
                }
            },
            "transfer_hbar": {
                "description": "Transfer HBAR from your account to another account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to_account_id": {"type": "string", "description": "Recipient account ID (format: 0.0.12345)"},
                        "amount": {"type": "number", "description": "Amount in HBAR"},
                        "memo": {"type": "string", "description": "Optional memo for the transfer"}
                    },
                    "required": ["to_account_id", "amount"]
                }
            },
            "get_balance": {
                "description": "Get account balance in HBAR",
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "account_id": {"type": "string", "description": "Account ID (optional, defaults to your account)"}
                    }
                }
            },
            "create_fungible_token": {
                "description": "Create a new fungible token",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Token name"},
                        "symbol": {"type": "string", "description": "Token symbol (e.g., USD, BTC)"},
                        "initial_supply": {"type": "integer", "description": "Initial supply amount"},
                        "decimals": {"type": "integer", "description": "Number of decimal places"}
                    },
                    "required": ["name", "symbol", "initial_supply", "decimals"]
                }
            },
            "create_non_fungible_token": {
                "description": "Create a new NFT collection",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "NFT collection name"},
                        "symbol": {"type": "string", "description": "NFT collection symbol"}
                    },
                    "required": ["name", "symbol"]
                }
            },
            "associate_token": {
                "description": "Associate an account with a token (required before receiving tokens)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string", "description": "Account ID to associate"},
                        "token_id": {"type": "string", "description": "Token ID to associate with"}
                    },
                    "required": ["account_id", "token_id"]
                }
            },
            "dissociate_token": {
                "description": "Dissociate an account from a token",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string", "description": "Account ID to dissociate"},
                        "token_id": {"type": "string", "description": "Token ID to dissociate from"}
                    },
                    "required": ["account_id", "token_id"]
                }
            },
            "delete_token": {
                "description": "Delete a token permanently",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "token_id": {"type": "string", "description": "Token ID to delete"}
                    },
                    "required": ["token_id"]
                }
            },
            "create_topic": {
                "description": "Create a new consensus topic for messaging",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "memo": {"type": "string", "description": "Topic description/memo"}
                    }
                }
            },
            "submit_message": {
                "description": "Submit a message to a consensus topic",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic_id": {"type": "string", "description": "Topic ID to send message to"},
                        "message": {"type": "string", "description": "Message content"}
                    },
                    "required": ["topic_id", "message"]
                }
            },
            "get_topic_info": {
                "description": "Get information about a consensus topic",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic_id": {"type": "string", "description": "Topic ID to query"}
                    },
                    "required": ["topic_id"]
                }
            }
        }
        
        for tool_name, definition in tool_definitions.items():
            tools.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": definition["description"],
                    "parameters": definition["parameters"]
                }
            })
        
        return tools

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a Hedera tool via the agent registry"""
        try:
            result = await agent_registry.call_tool(tool_name, arguments)
            return str(result)
        except Exception as e:
            return f"❌ Error executing {tool_name}: {str(e)}"

    async def process_request(self, user_input: str) -> str:
        """Process user request using OpenAI and execute appropriate tools"""
        try:
            # Create system prompt with current network status
            network_info = f"Connected to {client_manager.network}" if client_manager.is_configured else "Running in mock mode"
            operator_info = f"Operator: {client_manager.operator_id}" if client_manager.operator_id else "No operator configured"
            
            system_prompt = f"""You are a helpful assistant for Hedera Hashgraph operations. 
            You can help users create accounts, transfer HBAR, create tokens, manage consensus topics, and more.
            Use the available functions to fulfill user requests. Be conversational and helpful.
            
            Current Status:
            - Network: {network_info}
            - {operator_info}
            
            Guidelines:
            - Account IDs should be in format 0.0.12345
            - When creating tokens, suggest reasonable defaults if not specified
            - For transfers, remind users they need sufficient balance
            - For token operations, remind about token association requirements
            - Be helpful in explaining what operations are being performed
            - If operations fail, provide helpful debugging tips"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                tools=self.available_tools,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            # If OpenAI wants to call functions
            if message.tool_calls:
                results = []
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    print(f"🔧 Executing: {function_name}")
                    print(f"   Parameters: {arguments}")
                    
                    result = await self.execute_tool(function_name, arguments)
                    results.append(result)
                
                return "\n".join(results)
            
            # If no function calls, just return the response
            return message.content or "I'm not sure how to help with that request."
            
        except Exception as e:
            return f"❌ Error processing request: {str(e)}"

    def print_welcome(self):
        """Print welcome message and current status"""
        print("🌟 Welcome to the Hedera CLI Agent! 🌟")
        print("=" * 60)
        print("I can help you interact with the Hedera network using natural language!")
        
        # Show current configuration status
        print(f"\n⚙️  Configuration Status:")
        print(f"   • Network: {client_manager.network}")
        print(f"   • Operator: {client_manager.operator_id or 'Not configured'}")
        print(f"   • Client: {'✅ Connected' if client_manager.is_configured else '❌ Not configured'}")
        print(f"   • OpenAI: {'✅ Configured' if os.getenv('OPENAI_API_KEY') else '❌ Missing API key'}")
        
        if client_manager.is_configured:
            print(f"   • Mode: 🌐 Live Network")
        else:
            print(f"   • Mode: 🧪 Mock/Testing")
        
        print(f"\n📋 What I can do:")
        print("   • 🏦 Account Management: Create accounts, check balances, transfer HBAR")
        print("   • 🪙 Token Operations: Create tokens, manage associations")
        print("   • 💬 Consensus Service: Create topics, send messages")
        print("   • 🔍 Query Operations: Get account info, token details, topic info")
        
        print(f"\n💡 Example commands:")
        print("   • 'Create a new account with 10 HBAR'")
        print("   • 'Transfer 5 HBAR to account 0.0.12345'")
        print("   • 'Check my balance'")
        print("   • 'Create a token called MyToken with symbol MT'")
        print("   • 'Create a topic for announcements'")
        
        if not client_manager.is_configured:
            print(f"\n⚠️  To use real Hedera operations:")
            print("   1. Set HEDERA_NETWORK=testnet (or mainnet)")
            print("   2. Set OPERATOR_ID=0.0.your_account_id")
            print("   3. Set OPERATOR_KEY=your_private_key")
            print("   4. Restart the agent")
        
        print("=" * 60)
        print("Type 'quit', 'exit', or 'bye' to leave")
        print("Type 'help' for more information\n")

    def print_help(self):
        """Print detailed help information"""
        print("\n📚 Hedera CLI Agent Help")
        print("=" * 40)
        print("🏦 Account Operations:")
        print("   • Create account: 'Create a new account with X HBAR'")
        print("   • Check balance: 'What's my balance?' or 'Check balance of 0.0.12345'")
        print("   • Transfer HBAR: 'Send X HBAR to 0.0.12345'")
        print("\n🪙 Token Operations:")
        print("   • Create token: 'Create a token called TokenName with symbol TKN'")
        print("   • Create NFT: 'Create an NFT collection called MyNFTs'")
        print("   • Associate token: 'Associate my account with token 0.0.12345'")
        print("   • Delete token: 'Delete token 0.0.12345'")
        print("\n💬 Consensus Operations:")
        print("   • Create topic: 'Create a topic for announcements'")
        print("   • Send message: 'Send message \"Hello World\" to topic 0.0.12345'")
        print("   • Topic info: 'Get info about topic 0.0.12345'")
        print("=" * 40 + "\n")

async def main():
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable is required!")
        print("Please add your OpenAI API key to the .env file:")
        print("   OPENAI_API_KEY=your_api_key_here")
        print("\nGet an API key from: https://platform.openai.com/api-keys")
        return
    
    agent = HederaAgent()
    agent.print_welcome()
    
    while True:
        try:
            # Get user input
            user_input = input("🤖 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Thanks for using the Hedera CLI Agent!")
                break
            
            # Check for help command
            if user_input.lower() in ['help', '?']:
                agent.print_help()
                continue
            
            if not user_input:
                continue
            
            # Process the request
            print("🤔 Thinking...")
            response = await agent.process_request(user_input)
            print(f"\n{response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for using the Hedera CLI Agent!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main()) 