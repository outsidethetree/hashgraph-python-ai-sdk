import asyncio
import pytest
from hedera_agent_kit import agent_registry
from hedera_agent_kit.accounts import CreateAccountInput

def test_get_schema_and_call_tool(monkeypatch):
    schema_cls = agent_registry.get_schema("create_account")
    assert schema_cls is CreateAccountInput
    async def dummy_create_account(input_obj):
        assert isinstance(input_obj, CreateAccountInput)
        return "DUMMY_ACCOUNT_CREATED"
    orig_schema, orig_func = agent_registry._tools["create_account"]
    monkeypatch.setitem(agent_registry._tools, "create_account", (orig_schema, dummy_create_account))
    result = asyncio.get_event_loop().run_until_complete(agent_registry.call_tool("create_account", {"initial_balance": 10, "public_key": "dummy"}))
    assert result == "DUMMY_ACCOUNT_CREATED"

def test_call_tool_various(monkeypatch):
    async def dummy_token_tool(input_obj):
        return f"CALLED_{getattr(input_obj, 'symbol', 'TOKEN')}"
    async def dummy_consensus_tool(input_obj):
        return f"CALLED_TOPIC_{getattr(input_obj, 'memo', '')}"
    orig_schema_token, orig_func_token = agent_registry._tools["create_fungible_token"]
    monkeypatch.setitem(agent_registry._tools, "create_fungible_token", (orig_schema_token, dummy_token_tool))
    orig_schema_cons, orig_func_cons = agent_registry._tools["create_topic"]
    monkeypatch.setitem(agent_registry._tools, "create_topic", (orig_schema_cons, dummy_consensus_tool))
    token_args = {"name": "TokenX", "symbol": "TKX", "initial_supply": 0, "decimals": 0}
    res_token = asyncio.get_event_loop().run_until_complete(agent_registry.call_tool("create_fungible_token", token_args))
    assert res_token == "CALLED_TKX"
    topic_args = {"memo": "TestMemo"}
    res_topic = asyncio.get_event_loop().run_until_complete(agent_registry.call_tool("create_topic", topic_args))
    assert res_topic.startswith("CALLED_TOPIC_")

def test_call_tool_unknown():
    with pytest.raises(KeyError):
        asyncio.get_event_loop().run_until_complete(agent_registry.call_tool("nonexistent_tool", {})) 