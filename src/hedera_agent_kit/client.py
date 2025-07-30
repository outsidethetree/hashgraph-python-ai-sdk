"""
Hedera Client Manager

Centralized client configuration and network management for the agent kit.
"""

import os
from typing import Optional
from dotenv import load_dotenv

try:
    from hiero_sdk_python import Client, PrivateKey, AccountId, Network
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    # Mock classes for development
    class Client:
        @classmethod
        def for_testnet(cls): return cls()
        @classmethod
        def for_mainnet(cls): return cls()
        def set_operator(self, account_id, private_key): pass
    
    class PrivateKey:
        @classmethod
        def from_string(cls, key_str): return cls()
    
    class AccountId:
        @classmethod
        def from_string(cls, id_str): return cls()
    
    class Network:
        TESTNET = "testnet"
        MAINNET = "mainnet"

# Load environment variables
load_dotenv()

class HederaClientManager:
    """Manages Hedera client connections and configuration"""
    
    def __init__(self):
        self._client: Optional[Client] = None
        self._operator_id: Optional[str] = None
        self._operator_key: Optional[str] = None
        self._network: str = "testnet"
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment variables"""
        self._network = os.getenv("HEDERA_NETWORK", "testnet").lower()
        self._operator_id = os.getenv("OPERATOR_ID")
        self._operator_key = os.getenv("OPERATOR_KEY")
        
        # Only try to setup client if we have both credentials
        if self._operator_id and self._operator_key and self._operator_id.strip() and self._operator_key.strip():
            self._setup_client()
        else:
            print("⚠️  No Hedera credentials provided - running in mock mode")
    
    def _setup_client(self):
        """Set up the Hedera client with operator credentials"""
        if not SDK_AVAILABLE:
            print("⚠️  Running in mock mode - hiero-sdk-python not available")
            self._client = Client()
            return
        
        try:
            # Create client (SDK will use default network configuration)
            self._client = Client()
            
            # Set operator account if provided
            if self._operator_id and self._operator_key:
                operator_id = AccountId.from_string(self._operator_id)
                operator_key = PrivateKey.from_string(self._operator_key)
                self._client.set_operator(operator_id, operator_key)
                
                print(f"✅ Hedera client initialized for {self._network}")
                print(f"   Operator: {self._operator_id}")
            else:
                print("⚠️  No operator credentials provided - some operations may fail")
                
        except Exception as e:
            print(f"❌ Failed to initialize Hedera client: {e}")
            self._client = None
    
    @property
    def client(self) -> Optional[Client]:
        """Get the configured Hedera client"""
        return self._client
    
    @property
    def is_configured(self) -> bool:
        """Check if client is properly configured"""
        return self._client is not None
    
    @property
    def network(self) -> str:
        """Get the current network"""
        return self._network
    
    @property
    def operator_id(self) -> Optional[str]:
        """Get the operator account ID"""
        return self._operator_id
    
    def update_config(self, network: Optional[str] = None, 
                     operator_id: Optional[str] = None, 
                     operator_key: Optional[str] = None):
        """Update client configuration"""
        if network:
            self._network = network
        if operator_id:
            self._operator_id = operator_id
        if operator_key:
            self._operator_key = operator_key
        
        self._setup_client()

# Global client manager instance
client_manager = HederaClientManager() 