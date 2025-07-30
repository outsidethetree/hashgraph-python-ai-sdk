import asyncio
import types
import pytest
from hedera_agent_kit import tokens

if not hasattr(tokens, "hedera_token"):
    tokens.hedera_token = types.SimpleNamespace()

def test_create_tokens(monkeypatch):
    captured = {}
    async def fake_create_fungible_token(name, symbol, initial_supply, decimals, treasury_account_id=None):
        captured["fungible"] = (name, symbol, initial_supply, decimals, treasury_account_id)
        return "0.0.5001"
    async def fake_create_non_fungible_token(name, symbol, treasury_account_id=None):
        captured["nft"] = (name, symbol, treasury_account_id)
        return "0.0.5002"
    monkeypatch.setattr(tokens.hedera_token, "create_fungible_token", fake_create_fungible_token)
    monkeypatch.setattr(tokens.hedera_token, "create_non_fungible_token", fake_create_non_fungible_token)
    inp_f = tokens.CreateFungibleTokenInput(name="TokenA", symbol="TKA", initial_supply=1000, decimals=2)
    res_f = asyncio.get_event_loop().run_until_complete(tokens.create_fungible_token(inp_f))
    # 1000 with decimals=2 -> 100000 lowest units
    assert captured["fungible"][2] == 1000 * (10 ** 2)
    assert "TokenA" in res_f and "TKA" in res_f and "0.0.5001" in res_f
    inp_nft = tokens.CreateNonFungibleTokenInput(name="MyNFT", symbol="MNFT")
    res_nft = asyncio.get_event_loop().run_until_complete(tokens.create_non_fungible_token(inp_nft))
    assert captured["nft"][0] == "MyNFT" and captured["nft"][1] == "MNFT"
    assert "Non-fungible token created" in res_nft and "0.0.5002" in res_nft

def test_update_token(monkeypatch):
    async def fake_update_token(token_id, name=None, symbol=None):
        assert token_id == "0.0.6006"
        # Ensure at least one of name or symbol is provided
        assert name is not None or symbol is not None
    monkeypatch.setattr(tokens.hedera_token, "update_token", fake_update_token)
    inp_none = tokens.UpdateTokenInput(token_id="0.0.6006")
    with pytest.raises(ValueError):
        asyncio.get_event_loop().run_until_complete(tokens.update_token(inp_none))
    inp_name = tokens.UpdateTokenInput(token_id="0.0.6006", name="NewName")
    res_name = asyncio.get_event_loop().run_until_complete(tokens.update_token(inp_name))
    assert "updated" in res_name
    inp_sym = tokens.UpdateTokenInput(token_id="0.0.6006", symbol="NEWSYM")
    res_sym = asyncio.get_event_loop().run_until_complete(tokens.update_token(inp_sym))
    assert "updated" in res_sym

def test_mint_and_burn_tokens(monkeypatch):
    called = {"mint": False, "burn": False}
    async def fake_mint_token(token_id, amount):
        called["mint"] = True
        assert token_id == "0.0.7007" and amount == 500
        return 1500
    async def fake_burn_token(token_id, amount):
        called["burn"] = True
        assert token_id == "0.0.7007" and amount == 200
    monkeypatch.setattr(tokens.hedera_token, "mint_token", fake_mint_token)
    monkeypatch.setattr(tokens.hedera_token, "burn_token", fake_burn_token)
    inp_mint = tokens.MintTokenInput(token_id="0.0.7007", amount=500)
    res_mint = asyncio.get_event_loop().run_until_complete(tokens.mint_token(inp_mint))
    assert called["mint"] and "Minted 500" in res_mint
    inp_burn = tokens.BurnTokenInput(token_id="0.0.7007", amount=200)
    res_burn = asyncio.get_event_loop().run_until_complete(tokens.burn_token(inp_burn))
    assert called["burn"] and "Burned 200" in res_burn

def test_mint_and_burn_nft(monkeypatch):
    called = {"mint": False, "burn": False}
    async def fake_mint_nft(token_id, metadata):
        called["mint"] = True
        assert token_id == "0.0.8008" and isinstance(metadata, list) and len(metadata) == 2
        return 2
    async def fake_burn_nft(token_id, serial_numbers):
        called["burn"] = True
        assert token_id == "0.0.8008" and serial_numbers == [1, 2]
    monkeypatch.setattr(tokens.hedera_token, "mint_nft", fake_mint_nft)
    monkeypatch.setattr(tokens.hedera_token, "burn_nft", fake_burn_nft)
    meta_list = [b'NFT1', b'NFT2']
    inp_mint = tokens.MintNftInput(token_id="0.0.8008", metadata=meta_list)
    res_mint = asyncio.get_event_loop().run_until_complete(tokens.mint_nft(inp_mint))
    assert called["mint"] and "Minted 2 NFT(s)" in res_mint
    inp_burn = tokens.BurnNftInput(token_id="0.0.8008", serial_numbers=[1, 2])
    res_burn = asyncio.get_event_loop().run_until_complete(tokens.burn_nft(inp_burn))
    assert called["burn"] and "Burned 2 NFT(s)" in res_burn

def test_transfer_token_conversion(monkeypatch):
    async def fake_get_token_info(token_id):
        return {"decimals": 3}
    captured = {}
    async def fake_transfer_token(token_id, to_account_id, amount):
        captured["token_id"] = token_id
        captured["to"] = to_account_id
        captured["amount"] = amount
    monkeypatch.setattr(tokens.hedera_token, "get_token_info", fake_get_token_info)
    monkeypatch.setattr(tokens.hedera_token, "transfer_token", fake_transfer_token)
    inp = tokens.TransferTokenInput(token_id="0.0.9009", to_account_id="0.0.1111", amount=5.5)
    res = asyncio.get_event_loop().run_until_complete(tokens.transfer_token(inp))
    # decimals=3, 5.5 -> 5500 in lowest units
    assert captured["token_id"] == "0.0.9009"
    assert captured["to"] == "0.0.1111"
    assert captured["amount"] == 5500
    assert "Transferred 5.5" in res

def test_transfer_nft(monkeypatch):
    done = {"called": False}
    async def fake_transfer_nft(token_id, to_account_id, serial_number):
        done["called"] = True
        assert token_id == "0.0.9999" and to_account_id == "0.0.2222" and serial_number == 42
    monkeypatch.setattr(tokens.hedera_token, "transfer_nft", fake_transfer_nft)
    inp = tokens.TransferNftInput(token_id="0.0.9999", to_account_id="0.0.2222", serial_number=42)
    res = asyncio.get_event_loop().run_until_complete(tokens.transfer_nft(inp))
    assert done["called"] and "Transferred token 0.0.9999 serial 42" in res

def test_associate_and_freeze_and_kyc(monkeypatch):
    flags = {"assoc": False, "dissoc": False, "freeze": False, "unfreeze": False, "grant": False, "revoke": False}
    async def fake_associate_token(account_id, token_id):
        flags["assoc"] = True
        assert account_id == "0.0.aaaa" and token_id == "0.0.TOKEN"
    async def fake_dissociate_token(account_id, token_id):
        flags["dissoc"] = True
        assert account_id == "0.0.aaaa" and token_id == "0.0.TOKEN"
    async def fake_freeze_token_account(token_id, account_id):
        flags["freeze"] = True
        assert token_id == "0.0.TKN" and account_id == "0.0.bbbb"
    async def fake_unfreeze_token_account(token_id, account_id):
        flags["unfreeze"] = True
        assert token_id == "0.0.TKN" and account_id == "0.0.bbbb"
    async def fake_grant_kyc(token_id, account_id):
        flags["grant"] = True
        assert token_id == "0.0.KYC" and account_id == "0.0.cccc"
    async def fake_revoke_kyc(token_id, account_id):
        flags["revoke"] = True
        assert token_id == "0.0.KYC" and account_id == "0.0.cccc"
    monkeypatch.setattr(tokens.hedera_token, "associate_token", fake_associate_token)
    monkeypatch.setattr(tokens.hedera_token, "dissociate_token", fake_dissociate_token)
    monkeypatch.setattr(tokens.hedera_token, "freeze_token_account", fake_freeze_token_account)
    monkeypatch.setattr(tokens.hedera_token, "unfreeze_token_account", fake_unfreeze_token_account)
    monkeypatch.setattr(tokens.hedera_token, "grant_kyc", fake_grant_kyc)
    monkeypatch.setattr(tokens.hedera_token, "revoke_kyc", fake_revoke_kyc)
    # Associate & Dissociate
    inp_assoc = tokens.AssociateTokenInput(account_id="0.0.aaaa", token_id="0.0.TOKEN")
    res_assoc = asyncio.get_event_loop().run_until_complete(tokens.associate_token(inp_assoc))
    assert flags["assoc"] and "Associated" in res_assoc
    inp_diss = tokens.DissociateTokenInput(account_id="0.0.aaaa", token_id="0.0.TOKEN")
    res_diss = asyncio.get_event_loop().run_until_complete(tokens.dissociate_token(inp_diss))
    assert flags["dissoc"] and "Dissociated" in res_diss
    # Freeze & Unfreeze
    inp_freeze = tokens.FreezeTokenAccountInput(token_id="0.0.TKN", account_id="0.0.bbbb")
    res_freeze = asyncio.get_event_loop().run_until_complete(tokens.freeze_token_account(inp_freeze))
    assert flags["freeze"] and "Frozen" in res_freeze
    inp_unfreeze = tokens.UnfreezeTokenAccountInput(token_id="0.0.TKN", account_id="0.0.bbbb")
    res_unfreeze = asyncio.get_event_loop().run_until_complete(tokens.unfreeze_token_account(inp_unfreeze))
    assert flags["unfreeze"] and "Unfrozen" in res_unfreeze
    # KYC Grant & Revoke
    inp_grant = tokens.GrantKycInput(token_id="0.0.KYC", account_id="0.0.cccc")
    res_grant = asyncio.get_event_loop().run_until_complete(tokens.grant_kyc(inp_grant))
    assert flags["grant"] and "Granted KYC" in res_grant
    inp_revoke = tokens.RevokeKycInput(token_id="0.0.KYC", account_id="0.0.cccc")
    res_revoke = asyncio.get_event_loop().run_until_complete(tokens.revoke_kyc(inp_revoke))
    assert flags["revoke"] and "Revoked KYC" in res_revoke

def test_pause_and_wipe(monkeypatch):
    flags = {"pause": False, "unpause": False, "wipe": False, "wipe_nft": False}
    async def fake_pause_token(token_id):
        flags["pause"] = True
        assert token_id == "0.0.PAUSE"
    async def fake_unpause_token(token_id):
        flags["unpause"] = True
        assert token_id == "0.0.PAUSE"
    async def fake_get_token_info(token_id):
        return {"decimals": 2}
    async def fake_wipe_token_account(token_id, account_id, amount):
        flags["wipe"] = True
        assert token_id == "0.0.WIPE" and account_id == "0.0.dddd" and amount == 550
    async def fake_wipe_token_account_nft(token_id, account_id, serial_numbers):
        flags["wipe_nft"] = True
        assert token_id == "0.0.WIPE" and account_id == "0.0.dddd" and serial_numbers == [10, 11]
    monkeypatch.setattr(tokens.hedera_token, "pause_token", fake_pause_token)
    monkeypatch.setattr(tokens.hedera_token, "unpause_token", fake_unpause_token)
    monkeypatch.setattr(tokens.hedera_token, "get_token_info", fake_get_token_info)
    monkeypatch.setattr(tokens.hedera_token, "wipe_token_account", fake_wipe_token_account)
    monkeypatch.setattr(tokens.hedera_token, "wipe_token_account_nft", fake_wipe_token_account_nft)
    inp_pause = tokens.PauseTokenInput(token_id="0.0.PAUSE")
    res_pause = asyncio.get_event_loop().run_until_complete(tokens.pause_token(inp_pause))
    assert flags["pause"] and "Paused token" in res_pause
    inp_unpause = tokens.UnpauseTokenInput(token_id="0.0.PAUSE")
    res_unpause = asyncio.get_event_loop().run_until_complete(tokens.unpause_token(inp_unpause))
    assert flags["unpause"] and "Unpaused token" in res_unpause
    inp_wipe = tokens.WipeTokenAccountInput(token_id="0.0.WIPE", account_id="0.0.dddd", amount=5.5)
    res_wipe = asyncio.get_event_loop().run_until_complete(tokens.wipe_token_account(inp_wipe))
    assert flags["wipe"] and "Wiped 5.5 tokens" in res_wipe
    inp_wipe_nft = tokens.WipeTokenAccountNftInput(token_id="0.0.WIPE", account_id="0.0.dddd", serial_numbers=[10, 11])
    res_wipe_nft = asyncio.get_event_loop().run_until_complete(tokens.wipe_token_account_nft(inp_wipe_nft))
    assert flags["wipe_nft"] and "Wiped NFT serials" in res_wipe_nft

def test_token_airdrop(monkeypatch):
    async def fake_get_token_info(token_id):
        return {"decimals": 0}
    transfers = []
    async def fake_transfer_token(token_id, to_account_id, amount):
        transfers.append((to_account_id, amount))
    monkeypatch.setattr(tokens.hedera_token, "get_token_info", fake_get_token_info)
    monkeypatch.setattr(tokens.hedera_token, "transfer_token", fake_transfer_token)
    recipients = [("0.0.X1", 10), ("0.0.X2", 20)]
    inp = tokens.TokenAirdropInput(token_id="0.0.AAAA", recipients=recipients)
    res = asyncio.get_event_loop().run_until_complete(tokens.token_airdrop(inp))
    assert ("0.0.X1", 10) in transfers and ("0.0.X2", 20) in transfers
    assert "0.0.X1" in res and "0.0.X2" in res and "Airdropped token 0.0.AAAA" in res

def test_get_token_info(monkeypatch):
    async def fake_get_token_info(token_id):
        if token_id == "0.0.FUNG":
            return {"name": "FToken", "symbol": "FT", "total_supply": 5000000, "decimals": 2}
        if token_id == "0.0.NFT":
            return {"name": "NToken", "symbol": "NT", "total_supply": 5, "decimals": 0}
    monkeypatch.setattr(tokens.hedera_token, "get_token_info", fake_get_token_info)
    inp_f = tokens.GetTokenInfoInput(token_id="0.0.FUNG")
    res_f = asyncio.get_event_loop().run_until_complete(tokens.get_token_info(inp_f))
    assert "FT" in res_f and "FToken" in res_f and "50000" in res_f  # 5000000 w/decimals=2 -> 50000.00
    inp_n = tokens.GetTokenInfoInput(token_id="0.0.NFT")
    res_n = asyncio.get_event_loop().run_until_complete(tokens.get_token_info(inp_n))
    assert "NT" in res_n and "NToken" in res_n and "5" in res_n 