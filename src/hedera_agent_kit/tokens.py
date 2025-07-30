"""
Hedera Token Operations

Comprehensive token management operations using the Hedera SDK.
"""

from dataclasses import dataclass
from typing import List, Optional
import asyncio

from .client import client_manager, SDK_AVAILABLE

if SDK_AVAILABLE:
    from hiero_sdk_python import (
        TokenCreateTransaction, TokenDeleteTransaction, TokenMintTransaction,
        TokenAssociateTransaction, TokenDissociateTransaction, TokenFreezeTransaction,
        TokenId, AccountId, Hbar, PublicKey, PrivateKey
    )

@dataclass
class CreateFungibleTokenInput:
    name: str
    symbol: str
    initial_supply: int
    decimals: int
    treasury_account_id: Optional[str] = None

@dataclass
class CreateNonFungibleTokenInput:
    name: str
    symbol: str
    treasury_account_id: Optional[str] = None

@dataclass
class UpdateTokenInput:
    token_id: str
    name: Optional[str] = None
    symbol: Optional[str] = None

@dataclass
class DeleteTokenInput:
    token_id: str

@dataclass
class MintTokenInput:
    token_id: str
    amount: int

@dataclass
class MintNftInput:
    token_id: str
    metadata: List[bytes]

@dataclass
class BurnTokenInput:
    token_id: str
    amount: int

@dataclass
class BurnNftInput:
    token_id: str
    serial_numbers: List[int]

@dataclass
class TransferTokenInput:
    token_id: str
    to_account_id: str
    amount: float

@dataclass
class TransferNftInput:
    token_id: str
    to_account_id: str
    serial_number: int

@dataclass
class AssociateTokenInput:
    account_id: str
    token_id: str

@dataclass
class DissociateTokenInput:
    account_id: str
    token_id: str

@dataclass
class FreezeTokenAccountInput:
    token_id: str
    account_id: str

@dataclass
class UnfreezeTokenAccountInput:
    token_id: str
    account_id: str

@dataclass
class GrantKycInput:
    token_id: str
    account_id: str

@dataclass
class RevokeKycInput:
    token_id: str
    account_id: str

@dataclass
class PauseTokenInput:
    token_id: str

@dataclass
class UnpauseTokenInput:
    token_id: str

@dataclass
class WipeTokenAccountInput:
    token_id: str
    account_id: str
    amount: float

@dataclass
class WipeTokenAccountNftInput:
    token_id: str
    account_id: str
    serial_numbers: List[int]

@dataclass
class TokenAirdropInput:
    token_id: str
    recipients: List[tuple]  # list of (account_id, amount) pairs

@dataclass
class GetTokenInfoInput:
    token_id: str

async def create_fungible_token(input: CreateFungibleTokenInput) -> str:
    """Create a new fungible token"""
    
    if not client_manager.is_configured:
        return f"🧪 Mock: Fungible token created - {input.name} ({input.symbol}), ID: 0.0.789012"
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Fungible token created - {input.name} ({input.symbol}), ID: 0.0.789012"
    
    try:
        client = client_manager.client
        operator_id = AccountId.from_string(client_manager.operator_id)
        
        # Use treasury account if provided, otherwise use operator
        treasury_id = AccountId.from_string(input.treasury_account_id) if input.treasury_account_id else operator_id
        
        # Create token transaction
        transaction = TokenCreateTransaction()\
            .set_token_name(input.name)\
            .set_token_symbol(input.symbol)\
            .set_decimals(input.decimals)\
            .set_initial_supply(input.initial_supply)\
            .set_treasury_account_id(treasury_id)
        
        # Set operator and node account IDs for proper signing
        transaction.operator_account_id = operator_id
        node_ids = client.get_node_account_ids()
        if node_ids:
            transaction.node_account_id = node_ids[0]
        
        # Execute transaction
        receipt = transaction.execute(client)
        
        
        token_id = receipt.tokenId
        
        return f"✅ Fungible token created: {input.name} ({input.symbol}), ID: {token_id}, Initial supply: {input.initial_supply}"
        
    except Exception as e:
        return f"❌ Error creating fungible token: {str(e)}"

async def create_non_fungible_token(input: CreateNonFungibleTokenInput) -> str:
    """Create a new NFT"""
    
    if not client_manager.is_configured:
        return "❌ Error: Hedera client not configured. Please set OPERATOR_ID and OPERATOR_KEY."
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: NFT created - {input.name} ({input.symbol}), ID: 0.0.789013"
    
    try:
        client = client_manager.client
        operator_id = AccountId.from_string(client_manager.operator_id)
        
        # Use treasury account if provided, otherwise use operator
        treasury_id = AccountId.from_string(input.treasury_account_id) if input.treasury_account_id else operator_id
        
        # Create NFT transaction
        transaction = TokenCreateTransaction()\
            .set_token_name(input.name)\
            .set_token_symbol(input.symbol)\
            .set_treasury_account_id(treasury_id)
        # Note: NFT configuration may require additional setup
        
        # Set operator and node account IDs for proper signing
        transaction.operator_account_id = operator_id
        node_ids = client.get_node_account_ids()
        if node_ids:
            transaction.node_account_id = node_ids[0]
        
        # Execute transaction
        receipt = transaction.execute(client)
        
        
        token_id = receipt.tokenId
        
        return f"✅ NFT created: {input.name} ({input.symbol}), ID: {token_id}"
        
    except Exception as e:
        return f"❌ Error creating NFT: {str(e)}"

async def associate_token(input: AssociateTokenInput) -> str:
    """Associate an account with a token"""
    
    if not client_manager.is_configured:
        return "❌ Error: Hedera client not configured. Please set OPERATOR_ID and OPERATOR_KEY."
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Associated account {input.account_id} with token {input.token_id}"
    
    try:
        client = client_manager.client
        account_id = AccountId.from_string(input.account_id)
        token_id = TokenId.from_string(input.token_id)
        
        # Create association transaction
        transaction = TokenAssociateTransaction()\
            .set_account_id(account_id)\
            .add_token_id(token_id)
        
        # Set operator and node account IDs for proper signing
        operator_id = AccountId.from_string(client_manager.operator_id)
        transaction.operator_account_id = operator_id
        node_ids = client.get_node_account_ids()
        if node_ids:
            transaction.node_account_id = node_ids[0]
        
        # Execute transaction
        receipt = transaction.execute(client)
        
        
        return f"✅ Associated account {input.account_id} with token {input.token_id}"
        
    except Exception as e:
        return f"❌ Error associating token: {str(e)}"

async def dissociate_token(input: DissociateTokenInput) -> str:
    """Dissociate an account from a token"""
    
    if not client_manager.is_configured:
        return "❌ Error: Hedera client not configured. Please set OPERATOR_ID and OPERATOR_KEY."
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Dissociated account {input.account_id} from token {input.token_id}"
    
    try:
        client = client_manager.client
        account_id = AccountId.from_string(input.account_id)
        token_id = TokenId.from_string(input.token_id)
        
        # Create dissociation transaction
        transaction = TokenDissociateTransaction()\
            .set_account_id(account_id)\
            .add_token_id(token_id)
        
        # Set operator and node account IDs for proper signing
        transaction.operator_account_id = AccountId.from_string(client_manager.operator_id)
        node_ids = client.get_node_account_ids()
        if node_ids:
            transaction.node_account_id = node_ids[0]
        
        # Execute transaction
        receipt = transaction.execute(client)
        
        
        return f"✅ Dissociated account {input.account_id} from token {input.token_id}"
        
    except Exception as e:
        return f"❌ Error dissociating token: {str(e)}"

async def delete_token(input: DeleteTokenInput) -> str:
    """Delete a token"""
    
    if not client_manager.is_configured:
        return "❌ Error: Hedera client not configured. Please set OPERATOR_ID and OPERATOR_KEY."
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Token {input.token_id} deleted"
    
    try:
        client = client_manager.client
        token_id = TokenId.from_string(input.token_id)
        
        # Create delete transaction
        transaction = TokenDeleteTransaction()\
            .set_token_id(token_id)
        
        # Set operator and node account IDs for proper signing
        transaction.operator_account_id = AccountId.from_string(client_manager.operator_id)
        node_ids = client.get_node_account_ids()
        if node_ids:
            transaction.node_account_id = node_ids[0]
        
        # Execute transaction
        receipt = transaction.execute(client)
        
        
        return f"✅ Token {input.token_id} deleted"
        
    except Exception as e:
        return f"❌ Error deleting token: {str(e)}"

# Placeholder implementations for operations not yet implemented
async def update_token(input: UpdateTokenInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Token {input.token_id} updated"
    return f"❌ Token update not yet implemented in SDK wrapper"

async def mint_token(input: MintTokenInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Minted {input.amount} units to token {input.token_id}"
    return f"❌ Token minting not yet implemented in SDK wrapper"

async def mint_nft(input: MintNftInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Minted {len(input.metadata)} NFT(s) for token {input.token_id}"
    return f"❌ NFT minting not yet implemented in SDK wrapper"

async def burn_token(input: BurnTokenInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Burned {input.amount} units from token {input.token_id}"
    return f"❌ Token burning not yet implemented in SDK wrapper"

async def burn_nft(input: BurnNftInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Burned {len(input.serial_numbers)} NFT(s) of token {input.token_id}"
    return f"❌ NFT burning not yet implemented in SDK wrapper"

async def transfer_token(input: TransferTokenInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Transferred {input.amount} of token {input.token_id} to {input.to_account_id}"
    return f"❌ Token transfer not yet implemented in SDK wrapper"

async def transfer_nft(input: TransferNftInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Transferred NFT {input.token_id}#{input.serial_number} to {input.to_account_id}"
    return f"❌ NFT transfer not yet implemented in SDK wrapper"

async def freeze_token_account(input: FreezeTokenAccountInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Frozen account {input.account_id} on token {input.token_id}"
    return f"❌ Token freeze not yet implemented in SDK wrapper"

async def unfreeze_token_account(input: UnfreezeTokenAccountInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Unfrozen account {input.account_id} on token {input.token_id}"
    return f"❌ Token unfreeze not yet implemented in SDK wrapper"

async def grant_kyc(input: GrantKycInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Granted KYC for account {input.account_id} on token {input.token_id}"
    return f"❌ KYC grant not yet implemented in SDK wrapper"

async def revoke_kyc(input: RevokeKycInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Revoked KYC for account {input.account_id} on token {input.token_id}"
    return f"❌ KYC revoke not yet implemented in SDK wrapper"

async def pause_token(input: PauseTokenInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Paused token {input.token_id}"
    return f"❌ Token pause not yet implemented in SDK wrapper"

async def unpause_token(input: UnpauseTokenInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Unpaused token {input.token_id}"
    return f"❌ Token unpause not yet implemented in SDK wrapper"

async def wipe_token_account(input: WipeTokenAccountInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Wiped {input.amount} tokens of {input.token_id} from account {input.account_id}"
    return f"❌ Token wipe not yet implemented in SDK wrapper"

async def wipe_token_account_nft(input: WipeTokenAccountNftInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Wiped NFT serials {input.serial_numbers} of token {input.token_id} from account {input.account_id}"
    return f"❌ NFT wipe not yet implemented in SDK wrapper"

async def token_airdrop(input: TokenAirdropInput) -> str:
    if not SDK_AVAILABLE:
        results = [f"{acct} (+{amount})" for acct, amount in input.recipients]
        return f"🧪 Mock: Airdropped token {input.token_id} to accounts: " + ", ".join(results)
    return f"❌ Token airdrop not yet implemented in SDK wrapper"

async def get_token_info(input: GetTokenInfoInput) -> str:
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Token {input.token_id}: MOCK (MockToken), total supply 10000"
    return f"❌ Token info query not yet implemented in SDK wrapper" 