# hedera_agent_kit package initialization
import os
from dotenv import load_dotenv

__version__ = "0.1.0"

# Load environment variables from .env file
load_dotenv()

# Hedera network configuration
HEDERA_NETWORK = os.getenv("HEDERA_NETWORK", "testnet")
OPERATOR_ID = os.getenv("OPERATOR_ID")
OPERATOR_KEY = os.getenv("OPERATOR_KEY") 