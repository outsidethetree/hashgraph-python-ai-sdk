import asyncio
import types
import pytest
from hedera_agent_kit import accounts

# Ensure the accounts module has the hedera_account namespace for patching
if not hasattr(accounts, "hedera_account"):
    accounts.hedera_account = types.SimpleNamespace()

def test_create_account_generates_key(monkeypatch):
    dummy_priv = "PRIVATE_KEY_ABC"
    dummy_pub = "PUBLIC_KEY_ABC"
    async def fake_generate_key():
        return (dummy_priv, dummy_pub)
    async def fake_create_account(initial_balance, public_key):
        # 1 HBAR -> 100,000,000 tinybars
        assert initial_balance == 100_000_000 and public_key == dummy_pub
        return "0.0.1001"
    monkeypatch.setattr(accounts.hedera_account, "generate_key", fake_generate_key)
    monkeypatch.setattr(accounts.hedera_account, "create_account", fake_create_account)
    inp = accounts.CreateAccountInput(initial_balance=1)
    result = asyncio.get_event_loop().run_until_complete(accounts.create_account(inp))
    assert "ID: 0.0.1001" in result
    assert dummy_priv in result and dummy_pub in result

def test_create_account_with_existing_key(monkeypatch):
    async def fake_create_account(initial_balance, public_key):
        assert initial_balance == 500_000_000 and public_key == "EXISTING_PUB_KEY"
        return "0.0.2002"
    async def fake_generate_key():
        raise AssertionError("generate_key should not be called")
    monkeypatch.setattr(accounts.hedera_account, "create_account", fake_create_account)
    monkeypatch.setattr(accounts.hedera_account, "generate_key", fake_generate_key)
    inp = accounts.CreateAccountInput(initial_balance=5, public_key="EXISTING_PUB_KEY")
    result = asyncio.get_event_loop().run_until_complete(accounts.create_account(inp))
    assert result == "Account created. ID: 0.0.2002"

def test_update_and_delete_account(monkeypatch):
    flags = {"update": False, "delete": False}
    async def fake_update_account(account_id, new_public_key):
        flags["update"] = True
        assert account_id == "0.0.1234" and new_public_key == "NEW_PUB_KEY"
    async def fake_delete_account(account_id, transfer_account_id):
        flags["delete"] = True
        assert account_id == "0.0.1234" and transfer_account_id == "0.0.4321"
    monkeypatch.setattr(accounts.hedera_account, "update_account", fake_update_account)
    monkeypatch.setattr(accounts.hedera_account, "delete_account", fake_delete_account)
    inp_upd = accounts.UpdateAccountInput(account_id="0.0.1234", new_public_key="NEW_PUB_KEY")
    res_upd = asyncio.get_event_loop().run_until_complete(accounts.update_account(inp_upd))
    assert flags["update"] and "updated" in res_upd
    inp_del = accounts.DeleteAccountInput(account_id="0.0.1234", transfer_account_id="0.0.4321")
    res_del = asyncio.get_event_loop().run_until_complete(accounts.delete_account(inp_del))
    assert flags["delete"] and "deleted" in res_del

def test_transfer_hbar(monkeypatch):
    captured = {}
    async def fake_transfer_hbar(to_account_id, amount, memo=""):
        captured["to"] = to_account_id
        captured["amount"] = amount
        captured["memo"] = memo
    monkeypatch.setattr(accounts.hedera_account, "transfer_hbar", fake_transfer_hbar)
    inp = accounts.TransferHbarInput(to_account_id="0.0.5555", amount=2.5, memo="Test Payment")
    result = asyncio.get_event_loop().run_until_complete(accounts.transfer_hbar(inp))
    assert captured["to"] == "0.0.5555"
    assert captured["amount"] == 250_000_000  # 2.5 HBAR in tinybars
    assert captured["memo"] == "Test Payment"
    assert "Transferred 2.5 HBAR" in result

def test_get_balance(monkeypatch):
    async def fake_get_balance_no_arg():
        return 750_000_000  # 7.5 HBAR in tinybars
    async def fake_get_balance_with_arg(account_id=None):
        assert account_id == "0.0.9999"
        return 100_000_000  # 1 HBAR in tinybars
    # No account_id provided
    monkeypatch.setattr(accounts.hedera_account, "get_balance", fake_get_balance_no_arg)
    inp = accounts.GetBalanceInput()
    res = asyncio.get_event_loop().run_until_complete(accounts.get_balance(inp))
    assert "7.5" in res and "HBAR" in res
    # With specific account_id
    monkeypatch.setattr(accounts.hedera_account, "get_balance", fake_get_balance_with_arg)
    inp2 = accounts.GetBalanceInput(account_id="0.0.9999")
    res2 = asyncio.get_event_loop().run_until_complete(accounts.get_balance(inp2))
    assert "1" in res2 and "HBAR" in res2

def test_get_account_info(monkeypatch):
    async def fake_get_account_info(account_id):
        assert account_id == "0.0.1111"
        return {"balance": 12300000000, "public_key": "TESTPUBKEY"}  # 123 HBAR
    monkeypatch.setattr(accounts.hedera_account, "get_account_info", fake_get_account_info)
    inp = accounts.GetAccountInfoInput(account_id="0.0.1111")
    res = asyncio.get_event_loop().run_until_complete(accounts.get_account_info(inp))
    assert "balance 123" in res and "TESTPUBKEY" in res

def test_approve_allowances(monkeypatch):
    called = {"hbar": False, "token": False}
    async def fake_approve_hbar_allowance(spender_account_id, amount):
        called["hbar"] = True
        assert spender_account_id == "0.0.2222" and amount == 500_000_000  # 5 HBAR
    async def fake_approve_token_allowance(token_id, spender_account_id, amount):
        called["token"] = True
        assert token_id == "0.0.3333" and spender_account_id == "0.0.4444" and amount == 1000
    monkeypatch.setattr(accounts.hedera_account, "approve_hbar_allowance", fake_approve_hbar_allowance)
    monkeypatch.setattr(accounts.hedera_account, "approve_token_allowance", fake_approve_token_allowance)
    inp_hbar = accounts.ApproveHbarAllowanceInput(spender_account_id="0.0.2222", amount=5)
    res_hbar = asyncio.get_event_loop().run_until_complete(accounts.approve_hbar_allowance(inp_hbar))
    assert called["hbar"] and "Approved allowance" in res_hbar
    inp_token = accounts.ApproveTokenAllowanceInput(token_id="0.0.3333", spender_account_id="0.0.4444", amount=1000)
    res_token = asyncio.get_event_loop().run_until_complete(accounts.approve_token_allowance(inp_token))
    assert called["token"] and "Approved allowance" in res_token

def test_sign_schedule(monkeypatch):
    done = {"called": False}
    async def fake_sign_schedule(schedule_id):
        done["called"] = True
        assert schedule_id == "0.0.5555"
    monkeypatch.setattr(accounts.hedera_account, "sign_schedule", fake_sign_schedule)
    inp = accounts.SignScheduleInput(schedule_id="0.0.5555")
    res = asyncio.get_event_loop().run_until_complete(accounts.sign_schedule(inp))
    assert done["called"] and "Signed scheduled transaction" in res 