import requests
import pandas as pd
from datetime import datetime
from config import SOLANA_API_URL
import logging

# Set up logging
logger = logging.getLogger(__name__)

def fetch_historical_data(contract_address, start_date, end_date):
    """
    Fetch historical token data for a given contract address and date range.
    Args:
    - contract_address: str - The contract address to fetch historical data for.
    - start_date: str - The start date in YYYY-MM-DD format.
    - end_date: str - The end date in YYYY-MM-DD format.
    Returns:
    - pd.DataFrame: DataFrame containing historical data.
    """
    url = f"{SOLANA_API_URL}/historical_data"
    params = {
        'contract_address': contract_address,
        'start_date': start_date,
        'end_date': end_date
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        logger.info(f"Historical data fetched for {contract_address} from {start_date} to {end_date}.")
        return pd.DataFrame(data)
    else:
        logger.error(f"Failed to fetch historical data for {contract_address}: {response.text}")
        return pd.DataFrame()

def analyze_historical_data(contract_address, start_date, end_date):
    """
    Perform analysis on historical data (e.g., moving average crossover).
    Args:
    - contract_address: str - Contract address.
    - start_date: str - Start date for data.
    - end_date: str - End date for data.
    Returns:
    - dict: Analysis results.
    """
    df = fetch_historical_data(contract_address, start_date, end_date)
    
    if df.empty:
        return {}
    
    # Simple example: Calculate moving averages for historical data
    prices = df['price'].tolist()
    sma = moving_average(prices, window=14)
    
    analysis = {
        'sma': sma[-1],  # Latest SMA value
        'entry_signal': prices[-1] > sma[-1],  # Entry signal when price crosses above SMA
        'exit_signal': prices[-1] < sma[-1],  # Exit signal when price crosses below SMA
    }
    
    logger.info(f"Historical analysis for {contract_address}: {analysis}")
    return analysis
