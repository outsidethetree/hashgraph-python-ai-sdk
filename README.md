# 🤖 Hashgraph Python AI Agent Kit

A **production-ready AI agent toolkit** for the Hedera Hashgraph network. This project provides a comprehensive Python SDK that wraps the `hiero-sdk-python` library, making it simple for AI agents to understand and execute Hedera transactions through natural language.

## 🌟 Features

- **🗣️ Natural Language Interface**: Talk to Hedera using plain English
- **🤖 AI-Powered**: Integrated with OpenAI GPT-4 for intelligent command processing
- **🔧 Production Ready**: Full async support, type safety, and comprehensive error handling
- **🧪 Development Friendly**: Mock mode for testing without real network dependency
- **📦 LangChain Compatible**: Drop-in integration with LangChain workflows
- **🌐 Network Agnostic**: Works with testnet, previewnet, and mainnet

## 🚀 Quick Start

### **One-Line Demo**
```bash
python3 start_agent.py
```

This will:
1. Create a `.env` template if none exists
2. Guide you through configuration
3. Start the conversational AI agent

### **Core Operations Supported**

#### 🏦 Account Management (9 tools)
- Create accounts with initial balance
- Transfer HBAR between accounts
- Check account balances and info
- Manage HBAR allowances

#### 🪙 Token Operations (22 tools)
- Create fungible tokens and NFTs
- Mint, burn, and transfer tokens
- Associate/dissociate accounts with tokens
- Manage token freezing, KYC, and pause states
- Token airdrops and batch operations

#### 💬 Consensus Service (6 tools)
- Create and manage consensus topics
- Submit messages to topics
- Query topic information and message history

## 📋 Prerequisites

- **Python 3.9+**
- **OpenAI API Key** (for natural language processing)
- **Hedera Account** (optional, for live operations)

## ⚙️ Installation & Setup

### 1. Clone and Install
```bash
git clone <repository-url>
cd hashgraph-python-ai-sdk
pip install -r demo/requirements.txt
```

### 2. Configure Environment
Create a `.env` file:
```env
# Required for AI agent
OPENAI_API_KEY=your_openai_api_key_here

# Optional for live Hedera operations
HEDERA_NETWORK=testnet
OPERATOR_ID=0.0.your_account_id
OPERATOR_KEY=your_private_key_here
```

### 3. Start the Agent
```bash
python3 start_agent.py
```

## 💬 Example Conversations

```
🤖 You: Create a new account with 10 HBAR
🔧 Executing: create_account
   Parameters: {'initial_balance': 10}
✅ Account created. ID: 0.0.123456, Private Key: ..., Public Key: ...

🤖 You: Transfer 5 HBAR to account 0.0.67890
🔧 Executing: transfer_hbar
   Parameters: {'to_account_id': '0.0.67890', 'amount': 5}
✅ Transferred 5 HBAR to 0.0.67890. Transaction: 0.0.123@1234567890.123456789

🤖 You: Create a token called "MyToken" with symbol "MT"
🔧 Executing: create_fungible_token
   Parameters: {'name': 'MyToken', 'symbol': 'MT', 'initial_supply': 1000, 'decimals': 2}
✅ Fungible token created: MyToken (MT), ID: 0.0.234567

🤖 You: Create a topic for announcements
🔧 Executing: create_topic
   Parameters: {'memo': 'announcements'}
✅ Topic created: 0.0.345678 with memo 'announcements'
```

## 🏗️ Project Structure

```
hashgraph-python-ai-sdk/
├── start_agent.py          # 🚀 One-line launcher
├── run_tests.py           # 🧪 Test runner
├── src/hedera_agent_kit/  # 📦 Main SDK
│   ├── client.py          # 🌐 Network client management
│   ├── accounts.py        # 🏦 Account operations
│   ├── tokens.py          # 🪙 Token operations
│   ├── consensus.py       # 💬 Consensus operations
│   └── agent_registry.py  # 🔧 LangChain-compatible registry
├── demo/                  # 🎯 Demo applications
│   ├── cli_agent.py      # 🤖 Main conversational agent
│   ├── quick_demo.py     # ⚡ Simple demo script
│   └── example_session.py # 📝 Programmatic usage
└── tests/                # ✅ Comprehensive test suite
    ├── test_accounts.py
    ├── test_tokens.py
    ├── test_consensus.py
    └── test_agent_registry.py
```

## 🔧 Technical Architecture

### **Agent Registry**
The heart of the system - maps natural language to Hedera operations:
```python
from hedera_agent_kit import agent_registry

# Execute any operation programmatically
result = await agent_registry.call_tool("create_account", {
    "initial_balance": 10
})
```

### **Client Manager**
Handles network connections and configuration:
```python
from hedera_agent_kit.client import client_manager

# Check network status
print(f"Connected to: {client_manager.network}")
print(f"Operator: {client_manager.operator_id}")
```

### **Type-Safe Operations**
All operations use strongly-typed dataclasses:
```python
@dataclass
class CreateAccountInput:
    initial_balance: float = 0
    public_key: Optional[str] = None
```

## 🌐 Operating Modes

### **🧪 Mock Mode** (Default)
- No credentials required
- Perfect for development and testing
- All operations return simulated results
- No real transactions or network calls

### **🌐 Live Network Mode**
- Requires operator credentials
- Real transactions on Hedera network
- Supports testnet, previewnet, and mainnet
- Full SDK functionality

## 📊 Development

### **Run Tests**
```bash
python3 run_tests.py
```

### **Type Checking**
```bash
mypy src/ --strict
```

### **Programmatic Usage**
```python
import asyncio
from hedera_agent_kit import agent_registry

async def example():
    # Create account
    account = await agent_registry.call_tool("create_account", {
        "initial_balance": 5.0
    })
    
    # Check balance
    balance = await agent_registry.call_tool("get_balance", {})
    
    # Create token
    token = await agent_registry.call_tool("create_fungible_token", {
        "name": "MyToken",
        "symbol": "MT",
        "initial_supply": 1000000,
        "decimals": 2
    })

asyncio.run(example())
```

## 🎯 Advanced Usage

### **Custom Tool Integration**
```python
# Add custom tools to the registry
from hedera_agent_kit.agent_registry import _tools

def my_custom_operation(input_data):
    # Your custom logic here
    return "Custom operation completed"

_tools["my_operation"] = (MyInputSchema, my_custom_operation)
```

### **LangChain Integration**
```python
from langchain.tools import Tool
from hedera_agent_kit import agent_registry

# Convert to LangChain tool
hedera_tool = Tool(
    name="hedera_operations",
    description="Execute Hedera blockchain operations",
    func=lambda query: asyncio.run(agent_registry.call_tool(query))
)
```

## 🔐 Security

- **Private Key Management**: Keys are handled securely via environment variables
- **Network Isolation**: Clear separation between mock and live modes
- **Type Safety**: Comprehensive input validation and error handling
- **Async Safety**: All operations are properly async with timeout handling

## 🧪 Testing

The project includes a comprehensive test suite with:
- **26 unit tests** covering all operations
- **Mock-based testing** (no network dependency)
- **Type safety verification**
- **Error handling validation**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `python3 run_tests.py`
5. Submit a pull request

## 📚 Documentation

- **API Reference**: See docstrings in source code
- **Examples**: Check the `demo/` directory
- **Type Definitions**: All schemas defined in module files

## 📄 License

Apache 2.0 License - see LICENSE file for details.

## 🙋 Support

- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions
- **Examples**: See `demo/` directory for usage examples

---

**Ready to start building with Hedera? Run `python3 start_agent.py` and start chatting with your blockchain! 🚀** 