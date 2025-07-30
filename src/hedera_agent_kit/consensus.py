"""
Hedera Consensus Operations

Comprehensive consensus service operations using the Hedera SDK.
"""

from dataclasses import dataclass
from typing import Optional
import asyncio

from .client import client_manager, SDK_AVAILABLE

if SDK_AVAILABLE:
    from hiero_sdk_python import (
        TopicCreateTransaction, TopicDeleteTransaction, TopicUpdateTransaction,
        TopicMessageSubmitTransaction, TopicInfoQuery, TopicMessageQuery,
        TopicId, AccountId
    )

@dataclass
class CreateTopicInput:
    memo: Optional[str] = None

@dataclass
class UpdateTopicInput:
    topic_id: str
    memo: str

@dataclass
class DeleteTopicInput:
    topic_id: str

@dataclass
class SubmitMessageInput:
    topic_id: str
    message: str

@dataclass
class GetTopicInfoInput:
    topic_id: str

@dataclass
class GetTopicMessagesInput:
    topic_id: str
    limit: Optional[int] = None

async def create_topic(input: CreateTopicInput) -> str:
    """Create a new consensus topic"""
    
    if not client_manager.is_configured:
        return f"🧪 Mock: Topic created with memo '{input.memo or 'none'}', ID: 0.0.345678"
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Topic created with memo '{input.memo or 'none'}', ID: 0.0.345678"
    
    try:
        client = client_manager.client
        
        # Create topic transaction
        transaction = TopicCreateTransaction()
        
        if input.memo:
            transaction.set_memo(input.memo)
        
        # Set operator and node account IDs for proper signing
        operator_id = AccountId.from_string(client_manager.operator_id)
        transaction.operator_account_id = operator_id
        node_ids = client.get_node_account_ids()
        if node_ids:
            transaction.node_account_id = node_ids[0]
        
        # Execute transaction
        receipt = transaction.execute(client)
        
        
        topic_id = receipt.topicId
        
        return f"✅ Topic created: {topic_id}" + (f" with memo '{input.memo}'" if input.memo else "")
        
    except Exception as e:
        return f"❌ Error creating topic: {str(e)}"

async def update_topic(input: UpdateTopicInput) -> str:
    """Update a consensus topic"""
    
    if not client_manager.is_configured:
        return "❌ Error: Hedera client not configured. Please set OPERATOR_ID and OPERATOR_KEY."
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Topic {input.topic_id} updated with memo '{input.memo}'"
    
    try:
        client = client_manager.client
        topic_id = TopicId.from_string(input.topic_id)
        
        # Create update transaction
        transaction = TopicUpdateTransaction()\
            .set_topic_id(topic_id)\
            .set_memo(input.memo)
        
        # Execute transaction
        receipt = transaction.execute(client)
        
        
        return f"✅ Topic {input.topic_id} updated with memo '{input.memo}'"
        
    except Exception as e:
        return f"❌ Error updating topic: {str(e)}"

async def delete_topic(input: DeleteTopicInput) -> str:
    """Delete a consensus topic"""
    
    if not client_manager.is_configured:
        return "❌ Error: Hedera client not configured. Please set OPERATOR_ID and OPERATOR_KEY."
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Topic {input.topic_id} deleted"
    
    try:
        client = client_manager.client
        topic_id = TopicId.from_string(input.topic_id)
        
        # Create delete transaction
        transaction = TopicDeleteTransaction()\
            .set_topic_id(topic_id)
        
        # Execute transaction
        receipt = transaction.execute(client)
        
        
        return f"✅ Topic {input.topic_id} deleted"
        
    except Exception as e:
        return f"❌ Error deleting topic: {str(e)}"

async def submit_message(input: SubmitMessageInput) -> str:
    """Submit a message to a consensus topic"""
    
    if not client_manager.is_configured:
        return "❌ Error: Hedera client not configured. Please set OPERATOR_ID and OPERATOR_KEY."
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Message '{input.message}' submitted to topic {input.topic_id}"
    
    try:
        client = client_manager.client
        topic_id = TopicId.from_string(input.topic_id)
        
        # Create message submit transaction
        transaction = TopicMessageSubmitTransaction()\
            .set_topic_id(topic_id)\
            .set_message(input.message.encode('utf-8'))
        
        # Execute transaction
        receipt = transaction.execute(client)
        
        
        return f"✅ Message submitted to topic {input.topic_id}. Transaction: {response.transaction_id}"
        
    except Exception as e:
        return f"❌ Error submitting message: {str(e)}"

async def get_topic_info(input: GetTopicInfoInput) -> str:
    """Get information about a consensus topic"""
    
    if not client_manager.is_configured:
        return "❌ Error: Hedera client not configured. Please set OPERATOR_ID and OPERATOR_KEY."
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Topic {input.topic_id} - memo: 'mock_memo', sequence: 42"
    
    try:
        client = client_manager.client
        topic_id = TopicId.from_string(input.topic_id)
        
        # Create topic info query
        query = TopicInfoQuery()\
            .set_topic_id(topic_id)
        
        # Execute query
        info = query.execute(client)
        
        memo = getattr(info, 'topic_memo', 'No memo')
        sequence = getattr(info, 'sequence_number', 0)
        
        return f"✅ Topic {input.topic_id}: memo='{memo}', messages={sequence}"
        
    except Exception as e:
        return f"❌ Error getting topic info: {str(e)}"

async def get_topic_messages(input: GetTopicMessagesInput) -> str:
    """Get messages from a consensus topic"""
    
    if not client_manager.is_configured:
        return "❌ Error: Hedera client not configured. Please set OPERATOR_ID and OPERATOR_KEY."
    
    if not SDK_AVAILABLE:
        return f"🧪 Mock: Found {input.limit or 3} messages in topic {input.topic_id}: [msg1, msg2, msg3]"
    
    try:
        client = client_manager.client
        topic_id = TopicId.from_string(input.topic_id)
        
        # Create topic message query
        query = TopicMessageQuery()\
            .set_topic_id(topic_id)
        
        if input.limit:
            query.set_limit(input.limit)
        
        # Note: This is a simplified implementation
        # Real message querying requires handling streaming responses
        messages = query.execute(client)
        
        if not messages:
            return f"✅ No messages found for topic {input.topic_id}"
        
        # Format messages for display
        message_list = [str(msg) for msg in messages[:input.limit if input.limit else 10]]
        return f"✅ Messages from topic {input.topic_id}: {message_list}"
        
    except Exception as e:
        return f"❌ Error getting topic messages: {str(e)}" 