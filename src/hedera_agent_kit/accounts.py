"""
Hedera Account Operations

Comprehensive account management operations using the Hedera SDK.
"""

from dataclasses import dataclass
from typing import Optional
import asyncio

from .client import client_manager, SDK_AVAILABLE

if SDK_AVAILABLE:
    from hiero_sdk_python import (
        AccountCreateTransaction, AccountId, PrivateKey, PublicKey,
        TransferTransaction, Hbar, CryptoGetAccountBalanceQuery
    )

@dataclass
class CreateAccountInput:
    initial_balance: float = 0
    public_key: Optional[str] = None

@dataclass
class UpdateAccountInput:
    account_id: str
    new_public_key: str

@dataclass
class DeleteAccountInput:
    account_id: str
    transfer_account_id: str

@dataclass
class TransferHbarInput:
    to_account_id: str
    amount: float
    memo: Optional[str] = None

@dataclass
class GetBalanceInput:
    account_id: Optional[str] = None

@dataclass
class GetAccountInfoInput:
    account_id: str

@dataclass
class ApproveHbarAllowanceInput:
    spender_account_id: str
    amount: float

@dataclass
class ApproveTokenAllowanceInput:
    token_id: str
    spender_account_id: str
    amount: int

@dataclass
class SignScheduleInput:
    schedule_id: str

async def create_account(input: CreateAccountInput) -> str:
    """Create a new Hedera account"""
    
    if not client_manager.is_configured:
        return f"🧪 Mock: Account created with {input.initial_balance} HBAR. ID: 0.0.123456"
    
    if not SDK_AVAILABLE:
        # Mock response for development
        return f"🧪 Mock: Account created with {input.initial_balance} HBAR. ID: 0.0.123456"
    
    try:
        client = client_manager.client
        
        # Generate new key pair if not provided
        if input.public_key is None:
            private_key = PrivateKey.generate()
            public_key = private_key.public_key()
        else:
            public_key = PublicKey.from_string(input.public_key)
            private_key = None
        
        # Create account transaction
        transaction = AccountCreateTransaction()\
            .set_key(public_key)\
            .set_initial_balance(Hbar(input.initial_balance))
        
        # Set operator and node account IDs for proper signing
        transaction.operator_account_id = AccountId.from_string(client_manager.operator_id)
        node_ids = client.get_node_account_ids()
        if node_ids:
            transaction.node_account_id = node_ids[0]
        
        # Execute transaction - this returns a receipt directly
        receipt = transaction.execute(client)
        
        account_id = receipt.accountId
        
        result = f"✅ Account created. ID: {account_id}"
        if private_key:
            result += f", Private Key: {private_key}, Public Key: {public_key}"
        
        return result
        
    except Exception as e:
        error_msg = str(e)
        if "INVALID_SIGNATURE" in error_msg or "7" in error_msg:
            return f"❌ Invalid signature error - this usually means:\n" \
                   f"   • The OPERATOR_KEY doesn't match the OPERATOR_ID account\n" \
                   f"   • Double-check your .env file credentials\n" \
                   f"   • Ensure you're using the correct private key for account {client_manager.operator_id}\n" \
                   f"   • Try regenerating credentials from Hedera Portal/Faucet"
        return f"❌ Error creating account: {error_msg}"

async def transfer_hbar(input: TransferHbarInput) -> str:
    """Transfer HBAR between accounts"""
    
    if not client_manager.is_configured:
        return f"🧪 Mock: Transferred {input.amount} HBAR to {input.to_account_id}"
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Transferred {input.amount} HBAR to {input.to_account_id}"
    
    try:
        client = client_manager.client
        operator_id = AccountId.from_string(client_manager.operator_id)
        to_account_id = AccountId.from_string(input.to_account_id)
        
        # Create transfer transaction
        transaction = TransferTransaction()\
            .add_hbar_transfer(operator_id, Hbar(-input.amount))\
            .add_hbar_transfer(to_account_id, Hbar(input.amount))
        
        if input.memo:
            transaction.set_transaction_memo(input.memo)
        
        # Set operator and node account IDs for proper signing
        transaction.operator_account_id = operator_id
        node_ids = client.get_node_account_ids()
        if node_ids:
            transaction.node_account_id = node_ids[0]
        
        # Execute transaction - this returns a receipt directly
        receipt = transaction.execute(client)
        
        # Note: for transfers, we might want to get transaction ID differently
        transaction_id = getattr(receipt, 'transaction_id', 'completed')
        return f"✅ Transferred {input.amount} HBAR to {input.to_account_id}. Transaction: {transaction_id}"
        
    except Exception as e:
        return f"❌ Error transferring HBAR: {str(e)}"

async def get_balance(input: GetBalanceInput) -> str:
    """Get account balance"""
    
    if not client_manager.is_configured:
        account_id = input.account_id or "0.0.123456"
        return f"🧪 Mock: Account {account_id} balance: 10.5 HBAR"
    
    account_id = input.account_id or client_manager.operator_id
    if not account_id:
        return "❌ Error: No account ID provided and no operator account configured."
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Account {account_id} balance: 10.5 HBAR"
    
    try:
        client = client_manager.client
        account_id_obj = AccountId.from_string(account_id)
        
        # Create balance query
        query = CryptoGetAccountBalanceQuery()\
            .set_account_id(account_id_obj)
        
        # Execute query
        balance = query.execute(client)
        
        # Convert balance to readable format
        try:
            # Use the correct attribute for HBAR balance
            if hasattr(balance, 'hbars'):
                hbar_amount = balance.hbars
            elif hasattr(balance, 'hbar'):
                hbar_amount = balance.hbar
            elif hasattr(balance, 'to_hbars'):
                hbar_amount = balance.to_hbars()
            elif hasattr(balance, 'balance'):
                hbar_amount = balance.balance
            else:
                hbar_amount = str(balance)
            
            return f"✅ Account {account_id} balance: {hbar_amount} HBAR"
        except Exception as e:
            return f"✅ Account {account_id} balance query completed (format: {type(balance).__name__})"
        
    except Exception as e:
        return f"❌ Error getting balance: {str(e)}"

async def get_account_info(input: GetAccountInfoInput) -> str:
    """Get detailed account information"""
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Account {input.account_id} - Balance: 10.5 HBAR, Key: mock_public_key"
    
    # For now, return balance as account info
    balance_result = await get_balance(GetBalanceInput(account_id=input.account_id))
    return balance_result.replace("balance:", "info - Balance:")

# Placeholder implementations for other operations
async def update_account(input: UpdateAccountInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Account {input.account_id} updated with new key"
    return f"❌ Account update not yet implemented in SDK wrapper"

async def delete_account(input: DeleteAccountInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Account {input.account_id} deleted, funds transferred to {input.transfer_account_id}"
    return f"❌ Account deletion not yet implemented in SDK wrapper"

async def approve_hbar_allowance(input: ApproveHbarAllowanceInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Approved {input.amount} HBAR allowance for {input.spender_account_id}"
    return f"❌ HBAR allowance not yet implemented in SDK wrapper"

async def approve_token_allowance(input: ApproveTokenAllowanceInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Approved {input.amount} token allowance for {input.spender_account_id}"
    return f"❌ Token allowance not yet implemented in SDK wrapper"

async def sign_schedule(input: SignScheduleInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Signed scheduled transaction {input.schedule_id}"
    return f"❌ Schedule signing not yet implemented in SDK wrapper" 