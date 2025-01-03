import time
import logging
from solana.rpc.api import Client
from solana.publickey import PublicKey
from config import SOLANA_API_URL
from telegram_bot import send_telegram_alert

# Set up logging
logger = logging.getLogger(__name__)

# Solana client
solana_client = Client(SOLANA_API_URL)

def monitor_contract(contract_address):
    """
    Continuously monitor a specific Solana contract.
    Args:
    - contract_address: str - The contract address to monitor.
    """
    logger.info(f"Monitoring contract {contract_address} in real-time.")
    
    previous_data = None
    
    while True:
        try:
            contract_data = solana_client.get_token_accounts_by_owner(PublicKey(contract_address), {'mint': 'mint_address_here'})
            
            if contract_data['result']:
                current_data = contract_data['result']['value']
                
                if previous_data != current_data:
                    logger.info(f"Change detected in contract {contract_address}")
                    send_telegram_alert(f"Change detected in contract {contract_address}")
                    
                    previous_data = current_data
            else:
                logger.warning(f"No data found for contract {contract_address}.")
            
            time.sleep(10)  # Adjust as needed for real-time frequency
            
        except Exception as e:
            logger.error(f"Error monitoring contract {contract_address}: {e}")
            time.sleep(10)  # Reattempt after some time

if __name__ == "__main__":
    contract_address = "5H8tW8f6Hx8TtD5h8gHfJ8N8xLz32Hw53N3y1m1dfYF1"  # Example contract address
    monitor_contract(contract_address)
