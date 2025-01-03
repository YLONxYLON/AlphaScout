import numpy as np
from utils import process_token_data
import logging

# Set up logging
logger = logging.getLogger(__name__)

def find_support_resistance(prices):
    """
    Find potential support and resistance levels based on the price history.
    Args:
    - prices: list - Historical price data.
    Returns:
    - dict: Contains support and resistance levels.
    """
    support = np.min(prices)
    resistance = np.max(prices)
    
    return {'support': support, 'resistance': resistance}

def analyze_token_data(contract_data):
    """
    Analyze token contract data and determine entry/exit points.
    Args:
    - contract_data: list - Raw contract data.
    Returns:
    - dict: Analysis results containing entry, exit points, support, and resistance.
    """
    prices = process_token_data(contract_data)
    
    if len(prices) < 2:
        logger.warning("Not enough data to perform analysis.")
        return None
    
    # Find support and resistance levels
    support_resistance = find_support_resistance(prices)
    
    # Determine entry and exit points based on thresholds
    entry_point = support_resistance['support'] * 1.05  # Example: 5% above support for entry
    exit_point = support_resistance['resistance'] * 0.95  # Example: 5% below resistance for exit
    
    analysis = {
        'entry_point': entry_point,
        'exit_point': exit_point,
        'support': support_resistance['support'],
        'resistance': support_resistance['resistance']
    }
    
    logger.info(f"Analysis complete. Entry: {entry_point}, Exit: {exit_point}")
    return analysis
