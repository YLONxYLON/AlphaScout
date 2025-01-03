import os
import json
import time
from config import CACHE_ENABLED, CACHE_DIR, CACHE_TIMEOUT
from datetime import datetime
import logging

# Set up logging for utilities
logger = logging.getLogger(__name__)

# Function to load and save cache data
def load_cache_data(contract_address):
    """
    Load cached contract data from a file if cache is enabled.
    Args:
    - contract_address: str - Contract address to check the cache for.
    Returns:
    - dict: Cached contract data or None.
    """
    if CACHE_ENABLED:
        cache_file = os.path.join(CACHE_DIR, f"{contract_address}.json")
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                cached_data = json.load(f)
                if time.time() - cached_data['timestamp'] < CACHE_TIMEOUT:
                    logger.info(f"Cache hit for {contract_address}.")
                    return cached_data['data']
                else:
                    logger.info(f"Cache expired for {contract_address}.")
        else:
            logger.info(f"No cache found for {contract_address}.")
    return None

def save_cache_data(contract_address, data):
    """
    Save contract data to cache.
    Args:
    - contract_address: str - Contract address to save the data for.
    - data: dict - Contract data to be cached.
    """
    if CACHE_ENABLED:
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        cache_file = os.path.join(CACHE_DIR, f"{contract_address}.json")
        cache_data = {
            'timestamp': time.time(),
            'data': data
        }
        with open(cache_file, "w") as f:
            json.dump(cache_data, f)
        logger.info(f"Cache saved for {contract_address}.")

def process_token_data(contract_data):
    """
    Process raw contract data into a more usable format.
    Args:
    - contract_data: list - Raw data from Solana API.
    Returns:
    - list: Processed data.
    """
    processed_data = []
    for entry in contract_data:
        token_amount = entry['account']['data']['parsed']['info']['tokenAmount']['uiAmount']
        processed_data.append(float(token_amount))
    return processed_data
