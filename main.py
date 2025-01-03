import os
import time
import requests
import logging
from solana.rpc.api import Client
from solana.rpc.types import TokenAccountOpts
from datetime import datetime
from config import SOLANA_API_URL, BOT_TOKEN, CHAT_ID, SEND_ALERTS, ALERT_THRESHOLD, CACHE_ENABLED, CACHE_DIR, CACHE_TIMEOUT, SOLANA_NETWORK, SOLSCAN_API_URL, DEBUG_MODE
from solana.publickey import PublicKey
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Solana client
solana_client = Client(SOLANA_API_URL)

# Global cache variable
contract_cache = {}

# Fetch contract data from Solana blockchain
def fetch_contract_data(contract_address):
    """
    Function to fetch contract data from Solana blockchain using the given contract address.
    Args:
    - contract_address: str - The address of the Solana contract to analyze.
    Returns:
    - dict: The contract data (e.g., token balances, historical transactions, etc.)
    """
    # Check if contract is in cache
    if contract_address in contract_cache and time.time() - contract_cache[contract_address]['timestamp'] < CACHE_TIMEOUT:
        logger.debug(f"Using cached data for contract {contract_address}")
        return contract_cache[contract_address]['data']
    
    # Fetch data from the blockchain (Solana)
    logger.info(f"Fetching data for contract {contract_address}")
    
    try:
        # Example: Fetch the token accounts related to the contract address
        result = solana_client.get_token_accounts_by_owner(
            PublicKey(contract_address),
            TokenAccountOpts()
        )
        
        # Check the response
        if result.get('result') is not None:
            contract_data = result['result']['value']
            logger.info(f"Successfully fetched contract data for {contract_address}")
        else:
            logger.error(f"No data found for contract {contract_address}")
            contract_data = None
        
        # Cache the data
        if CACHE_ENABLED:
            contract_cache[contract_address] = {
                'timestamp': time.time(),
                'data': contract_data
            }

        return contract_data
    
    except Exception as e:
        logger.error(f"Error fetching contract data: {e}")
        return None


# Analyzing contract data for entry and exit points
def analyze_contract_data(contract_data):
    """
    Function to analyze contract data and find entry and exit points based on support and resistance.
    Args:
    - contract_data: list - List of contract data (e.g., token balances, transaction history).
    Returns:
    - dict: The analysis results with entry/exit points.
    """
    # Placeholder for analysis (you can enhance with your own logic)
    if not contract_data:
        return None
    
    logger.info("Analyzing contract data for entry/exit points...")
    
    # Example: Find high and low token balance values (just as a sample logic)
    balances = [entry['account']['data']['parsed']['info']['tokenAmount']['uiAmount']
                for entry in contract_data if 'account' in entry]
    
    if not balances:
        return None

    max_balance = max(balances)
    min_balance = min(balances)
    
    # Define entry and exit points based on simple support/resistance logic
    entry_point = min_balance * (1 + ALERT_THRESHOLD)
    exit_point = max_balance * (1 - ALERT_THRESHOLD)
    
    return {
        'entry_point': entry_point,
        'exit_point': exit_point,
        'max_balance': max_balance,
        'min_balance': min_balance
    }


# Send Telegram alert with analysis results
def send_telegram_alert(message):
    """
    Function to send an alert to the Telegram bot.
    Args:
    - message: str - The message to send.
    """
    if SEND_ALERTS and CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': CHAT_ID,
                'text': message
            }
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                logger.info(f"Alert sent to Telegram chat {CHAT_ID}")
            else:
                logger.error(f"Failed to send alert. Response: {response.text}")
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {e}")
    else:
        logger.warning("Telegram alerts are not enabled or CHAT_ID is missing.")


# Analyze and send alerts for a given contract
def analyze_and_alert(contract_address):
    """
    Main function to fetch, analyze, and send alerts based on contract data.
    Args:
    - contract_address: str - The address of the Solana contract.
    """
    logger.info(f"Analyzing contract {contract_address}")
    
    # Fetch contract data
    contract_data = fetch_contract_data(contract_address)
    
    if not contract_data:
        logger.error(f"No contract data found for {contract_address}. Skipping analysis.")
        return
    
    # Analyze the contract data
    analysis_results = analyze_contract_data(contract_data)
    
    if analysis_results:
        entry_point = analysis_results['entry_point']
        exit_point = analysis_results['exit_point']
        max_balance = analysis_results['max_balance']
        min_balance = analysis_results['min_balance']
        
        # Prepare message
        message = (
            f"Contract Analysis for {contract_address}:\n"
            f"Entry Point: ${entry_point:.2f}\n"
            f"Exit Point: ${exit_point:.2f}\n"
            f"Max Balance: ${max_balance:.2f}\n"
            f"Min Balance: ${min_balance:.2f}\n"
        )
        
        # Send Telegram alert
        send_telegram_alert(message)
    else:
        logger.warning(f"No valid analysis found for contract {contract_address}.")


# Example function to check for new contracts and analyze them
def monitor_new_contracts():
    """
    Function to monitor new contracts and analyze them.
    """
    logger.info("Monitoring new contracts for analysis...")
    
    # Example: Predefined list of contract addresses (you can replace with actual fetching)
    contract_addresses = [
        "5H8tW8f6Hx8TtD5h8gHfJ8N8xLz32Hw53N3y1m1dfYF1",  # Example contract 1
        "5TnxP8f8Tn9tW33Hh8SHyH8tT8y6H8W5iTk9gk3b8fk6"   # Example contract 2
    ]
    
    for contract_address in contract_addresses:
        analyze_and_alert(contract_address)
        time.sleep(5)  # Delay between contract analyses to prevent too many requests


if __name__ == "__main__":
    # Example of continuously monitoring and analyzing contracts
    while True:
        monitor_new_contracts()
        time.sleep(300)  # Wait for 5 minutes before next iteration


Explanation of the Code:
Fetching Contract Data:

The fetch_contract_data() function pulls data related to the specified contract address. In this case, it retrieves token account data from the Solana blockchain using Solana's RPC API. The data is cached for a specified amount of time to optimize performance and reduce API calls.
Contract Data Analysis:

The analyze_contract_data() function processes the fetched contract data to calculate support and resistance levels. For simplicity, it identifies the minimum and maximum balances for the token associated with the contract and uses a basic entry and exit point strategy based on a configurable alert threshold.
Sending Alerts via Telegram:

The send_telegram_alert() function sends a message to a specific Telegram chat via a bot. The message contains the results of the analysis, including the entry and exit points for the token.
Main Monitoring Logic:

The monitor_new_contracts() function simulates monitoring a predefined list of contracts (you can replace this with actual contract discovery logic). Each contract is fetched and analyzed, and alerts are sent to Telegram based on the analysis results.
Continuous Monitoring:

The while True loop in the __main__ block repeatedly checks for new contracts every 5 minutes (this can be adjusted). This mimics an ongoing monitoring system where new contracts are continually analyzed.
Next Steps:
Enhance the Analysis Logic: You can implement more sophisticated analysis, such as technical analysis on price data, to detect more precise entry and exit points.
Integrate More Data Sources: You could integrate other data sources, like Solscan or CoinGecko, for more detailed token and market information.
Expand the Contract Monitoring: Modify the script to monitor contracts in real-time by integrating with a Solana event listener, rather than just checking a static list.

Installation Dependencies:
You'll need to install requests, solana, and python-dotenv for this script to work:

pip install requests solana python-dotenv



