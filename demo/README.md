# 🤖 Hedera CLI Agent Demo

A conversational AI agent that performs Hedera Hashgraph operations using natural language! This demo showcases the Hedera Agent Kit integrated with OpenAI GPT-4.

## 🚀 Features

- **Natural Language Interface**: Ask the agent to perform Hedera operations in plain English
- **Account Management**: Create accounts, check balances, transfer HBAR
- **Token Operations**: Create fungible tokens, mint, burn, transfer
- **Consensus Service**: Create topics, submit messages
- **OpenAI Integration**: Uses GPT-4 to understand user intent and execute appropriate tools

## 📋 Prerequisites

1. **OpenAI API Key**: Get one from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Hedera Credentials** (optional for testing): Testnet account ID and private key
3. **Python 3.9+**

## ⚙️ Setup

1. **Install dependencies**:
   ```bash
   cd demo
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   Create a `.env` file in the project root:
   ```bash
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Hedera Configuration (optional for testing)
   HEDERA_NETWORK=testnet
   OPERATOR_ID=0.0.xxxxx
   OPERATOR_KEY=your_private_key_here
   ```

3. **Run the agent**:
   ```bash
   python cli_agent.py
   ```

## 💬 Example Conversations

```
🤖 You: Create a new account with 5 HBAR
🤔 Thinking...
🔧 Executing: create_account with {'initial_balance': 5}
✅ create_account: Account created. ID: 0.0.12345, Public Key: ..., Private Key: ...

🤖 You: Transfer 2 HBAR to account 0.0.67890
🤔 Thinking...
🔧 Executing: transfer_hbar with {'to_account_id': '0.0.67890', 'amount': 2}
✅ transfer_hbar: Transferred 2 HBAR to account 0.0.67890

🤖 You: Check my balance
🤔 Thinking...
🔧 Executing: get_balance with {}
✅ get_balance: Account balance: 8.5 HBAR

🤖 You: Create a token called "MyAwesomeToken" with symbol "MAT"
🤔 Thinking...
🔧 Executing: create_fungible_token with {'name': 'MyAwesomeToken', 'symbol': 'MAT', 'initial_supply': 1000, 'decimals': 2}
✅ create_fungible_token: Fungible token created: MyAwesomeToken (MAT), ID: 0.0.98765
```

## 🎯 Available Operations

The agent can perform these operations through natural language:

### 🏦 Account Management
- Create new accounts
- Check account balances  
- Transfer HBAR between accounts
- Get account information

### 🪙 Token Operations
- Create fungible tokens
- Create NFTs
- Mint and burn tokens
- Transfer tokens
- Manage token associations

### 💬 Consensus Service
- Create consensus topics
- Submit messages to topics
- Query topic information

## 🔧 Technical Details

- **OpenAI Integration**: Uses function calling to map natural language to Hedera operations
- **Async Operations**: All Hedera operations are async for better performance
- **Error Handling**: Graceful error handling with user-friendly messages
- **Environment Safety**: Uses mocks when `hiero-sdk-python` isn't available

## 🛡️ Testing Mode

If you don't have Hedera credentials, the agent runs in **mock mode**:
- All operations return simulated results
- Perfect for testing the conversational interface
- No real transactions are made

## 🎨 Customization

You can extend the agent by:

1. **Adding new tools** to `agent_registry.py`
2. **Updating tool definitions** in `cli_agent.py`
3. **Customizing the system prompt** for different behavior
4. **Adding new conversation patterns**

## 🐛 Troubleshooting

**Missing OpenAI API Key**:
```
❌ Error: OPENAI_API_KEY environment variable is required!
```
→ Add your OpenAI API key to the `.env` file

**Import Errors**:
```
ModuleNotFoundError: No module named 'hedera_agent_kit'
```
→ Run from the demo directory: `cd demo && python cli_agent.py`

**Network Errors**:
→ Check your internet connection and API key validity

---

**Happy chatting with your Hedera agent! 🌟** 