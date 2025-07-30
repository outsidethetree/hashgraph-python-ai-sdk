import asyncio
import types
import pytest
from hedera_agent_kit import consensus

if not hasattr(consensus, "hedera_consensus"):
    consensus.hedera_consensus = types.SimpleNamespace()

def test_create_topic(monkeypatch):
    async def fake_create_topic_no_arg():
        return "0.0.11111"
    async def fake_create_topic_with_memo(memo=None):
        assert memo == "MyTopic"
        return "0.0.22222"
    monkeypatch.setattr(consensus.hedera_consensus, "create_topic", fake_create_topic_no_arg)
    inp_no = consensus.CreateTopicInput()
    res_no = asyncio.get_event_loop().run_until_complete(consensus.create_topic(inp_no))
    assert res_no == "Topic created: 0.0.11111"
    monkeypatch.setattr(consensus.hedera_consensus, "create_topic", fake_create_topic_with_memo)
    inp_mem = consensus.CreateTopicInput(memo="MyTopic")
    res_mem = asyncio.get_event_loop().run_until_complete(consensus.create_topic(inp_mem))
    assert res_mem == "Topic created: 0.0.22222"

def test_update_and_delete_topic(monkeypatch):
    flags = {"update": False, "delete": False}
    async def fake_update_topic(topic_id, memo):
        flags["update"] = True
        assert topic_id == "0.0.33333" and memo == "NewMemo"
    async def fake_delete_topic(topic_id):
        flags["delete"] = True
        assert topic_id == "0.0.33333"
    monkeypatch.setattr(consensus.hedera_consensus, "update_topic", fake_update_topic)
    monkeypatch.setattr(consensus.hedera_consensus, "delete_topic", fake_delete_topic)
    inp_up = consensus.UpdateTopicInput(topic_id="0.0.33333", memo="NewMemo")
    res_up = asyncio.get_event_loop().run_until_complete(consensus.update_topic(inp_up))
    assert flags["update"] and "updated" in res_up
    inp_del = consensus.DeleteTopicInput(topic_id="0.0.33333")
    res_del = asyncio.get_event_loop().run_until_complete(consensus.delete_topic(inp_del))
    assert flags["delete"] and "deleted" in res_del

def test_submit_message(monkeypatch):
    done = {"called": False}
    async def fake_submit_message(topic_id, message):
        done["called"] = True
        assert topic_id == "0.0.44444" and message == "Hello World"
    monkeypatch.setattr(consensus.hedera_consensus, "submit_message", fake_submit_message)
    inp = consensus.SubmitMessageInput(topic_id="0.0.44444", message="Hello World")
    res = asyncio.get_event_loop().run_until_complete(consensus.submit_message(inp))
    assert done["called"] and "submitted to topic 0.0.44444" in res

def test_get_topic_info(monkeypatch):
    async def fake_get_topic_info(topic_id):
        assert topic_id == "0.0.55555"
        return {"memo": "TopicMemo", "sequence_number": 10}
    monkeypatch.setattr(consensus.hedera_consensus, "get_topic_info", fake_get_topic_info)
    inp = consensus.GetTopicInfoInput(topic_id="0.0.55555")
    res = asyncio.get_event_loop().run_until_complete(consensus.get_topic_info(inp))
    assert "memo='TopicMemo'" in res and "message_count=10" in res

def test_get_topic_messages(monkeypatch):
    async def fake_get_topic_messages(topic_id, limit=None):
        assert topic_id == "0.0.66666"
        if limit == 2:
            return ["msg1", "msg2"]
        else:
            return []
    monkeypatch.setattr(consensus.hedera_consensus, "get_topic_messages", fake_get_topic_messages)
    inp_empty = consensus.GetTopicMessagesInput(topic_id="0.0.66666")
    res_empty = asyncio.get_event_loop().run_until_complete(consensus.get_topic_messages(inp_empty))
    assert "No messages" in res_empty
    inp_some = consensus.GetTopicMessagesInput(topic_id="0.0.66666", limit=2)
    res_some = asyncio.get_event_loop().run_until_complete(consensus.get_topic_messages(inp_some))
    assert "msg1" in res_some and "msg2" in res_some 