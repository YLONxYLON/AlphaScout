import requests
from solana.rpc.api import Client
from config import SOLANA_API_URL, SOLANA_API_KEY
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Solana client setup
solana_client = Client(SOLANA_API_URL)

def fetch_solana_token_data(contract_address):
    """
    Fetch token data from Solana blockchain using contract address.
    Args:
    - contract_address: str - The contract address to fetch data for.
    Returns:
    - dict: Contract data or None if the data cannot be fetched.
    """
    logger.info(f"Fetching data for contract: {contract_address}")
    try:
        result = solana_client.get_token_accounts_by_owner(
            contract_address, {'mint': 'mint_address_here'}
        )
        if result.get('result'):
            logger.info(f"Data fetched successfully for {contract_address}")
            return result['result']['value']
        else:
            logger.warning(f"No data found for {contract_address}")
            return None
    except Exception as e:
        logger.error(f"Error fetching contract data for {contract_address}: {e}")
        return None

def fetch_contract_info(contract_address):
    """
    Fetch and return contract information such as balances, transaction data, etc.
    Args:
    - contract_address: str - The contract address to fetch detailed information.
    Returns:
    - dict: Information regarding the contract or None.
    """
    try:
        contract_data = fetch_solana_token_data(contract_address)
        if contract_data:
            # Process contract data further or return as is
            return contract_data
        else:
            return None
    e
