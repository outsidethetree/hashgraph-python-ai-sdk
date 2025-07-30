from typing import Type, Any
from hedera_agent_kit import accounts, tokens, consensus

# Map of tool name to (input schema class, tool function)
_tools = {
    # Account management tools
    "create_account": (accounts.CreateAccountInput, accounts.create_account),
    "update_account": (accounts.UpdateAccountInput, accounts.update_account),
    "delete_account": (accounts.DeleteAccountInput, accounts.delete_account),
    "transfer_hbar": (accounts.TransferHbarInput, accounts.transfer_hbar),
    "get_balance": (accounts.GetBalanceInput, accounts.get_balance),
    "get_account_info": (accounts.GetAccountInfoInput, accounts.get_account_info),
    "approve_hbar_allowance": (accounts.ApproveHbarAllowanceInput, accounts.approve_hbar_allowance),
    "approve_token_allowance": (accounts.ApproveTokenAllowanceInput, accounts.approve_token_allowance),
    "sign_schedule": (accounts.SignScheduleInput, accounts.sign_schedule),
    # Token Service (HTS) tools
    "create_fungible_token": (tokens.CreateFungibleTokenInput, tokens.create_fungible_token),
    "create_non_fungible_token": (tokens.CreateNonFungibleTokenInput, tokens.create_non_fungible_token),
    "update_token": (tokens.UpdateTokenInput, tokens.update_token),
    "delete_token": (tokens.DeleteTokenInput, tokens.delete_token),
    "mint_token": (tokens.MintTokenInput, tokens.mint_token),
    "mint_nft": (tokens.MintNftInput, tokens.mint_nft),
    "burn_token": (tokens.BurnTokenInput, tokens.burn_token),
    "burn_nft": (tokens.BurnNftInput, tokens.burn_nft),
    "transfer_token": (tokens.TransferTokenInput, tokens.transfer_token),
    "transfer_nft": (tokens.TransferNftInput, tokens.transfer_nft),
    "associate_token": (tokens.AssociateTokenInput, tokens.associate_token),
    "dissociate_token": (tokens.DissociateTokenInput, tokens.dissociate_token),
    "freeze_token_account": (tokens.FreezeTokenAccountInput, tokens.freeze_token_account),
    "unfreeze_token_account": (tokens.UnfreezeTokenAccountInput, tokens.unfreeze_token_account),
    "grant_kyc": (tokens.GrantKycInput, tokens.grant_kyc),
    "revoke_kyc": (tokens.RevokeKycInput, tokens.revoke_kyc),
    "pause_token": (tokens.PauseTokenInput, tokens.pause_token),
    "unpause_token": (tokens.UnpauseTokenInput, tokens.unpause_token),
    "wipe_token_account": (tokens.WipeTokenAccountInput, tokens.wipe_token_account),
    "wipe_token_account_nft": (tokens.WipeTokenAccountNftInput, tokens.wipe_token_account_nft),
    "token_airdrop": (tokens.TokenAirdropInput, tokens.token_airdrop),
    "get_token_info": (tokens.GetTokenInfoInput, tokens.get_token_info),
    # Consensus Service (HCS) tools
    "create_topic": (consensus.CreateTopicInput, consensus.create_topic),
    "update_topic": (consensus.UpdateTopicInput, consensus.update_topic),
    "delete_topic": (consensus.DeleteTopicInput, consensus.delete_topic),
    "submit_message": (consensus.SubmitMessageInput, consensus.submit_message),
    "get_topic_info": (consensus.GetTopicInfoInput, consensus.get_topic_info),
    "get_topic_messages": (consensus.GetTopicMessagesInput, consensus.get_topic_messages)
}

def get_schema(tool_name: str) -> Type[Any]:
    """Return the dataclass schema for the given tool name."""
    if tool_name not in _tools:
        raise KeyError(f"Tool '{tool_name}' not found")
    return _tools[tool_name][0]

async def call_tool(tool_name: str, args: dict) -> Any:
    """Instantiate the tool's input schema with args and execute the tool."""
    if tool_name not in _tools:
        raise KeyError(f"Tool '{tool_name}' not found")
    schema_cls, func = _tools[tool_name]
    input_obj = schema_cls(**args)
    return await func(input_obj) 