import numpy as np
import logging

# Set up logging
logger = logging.getLogger(__name__)

def moving_average(prices, window=14):
    """
    Calculate the simple moving average (SMA) for a given window.
    Args:
    - prices: list - Historical price data (e.g., closing prices).
    - window: int - The window size for the moving average.
    Returns:
    - list: Calculated moving average values.
    """
    return np.convolve(prices, np.ones(window), 'valid') / window

def relative_strength_index(prices, window=14):
    """
    Calculate the Relative Strength Index (RSI) for a given window.
    Args:
    - prices: list - Historical price data.
    - window: int - The window size for calculating RSI.
    Returns:
    - float: The RSI value for the given price data.
    """
    delta = np.diff(prices)
    gain = (delta.where(delta > 0, 0)).mean()
    loss = (-delta.where(delta < 0, 0)).mean()
    
    rs = gain / loss if loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def macd(prices, fast=12, slow=26, signal=9):
    """
    Calculate the MACD (Moving Average Convergence Divergence) for a given series of prices.
    Args:
    - prices: list - Historical price data.
    - fast: int - The fast EMA window size.
    - slow: int - The slow EMA window size.
    - signal: int - The signal line window size.
    Returns:
    - dict: Contains the MACD line and Signal line.
    """
    ema_fast = moving_average(prices, fast)
    ema_slow = moving_average(prices, slow)
    
    macd_line = ema_fast - ema_slow
    signal_line = moving_average(macd_line, signal)
    
    return {'macd': macd_line, 'signal': signal_line}

def strategy_analysis(prices):
    """
    Apply multiple strategies and generate entry/exit signals.
    Args:
    - prices: list - Historical price data.
    Returns:
    - dict: Entry and exit signals based on strategies.
    """
    signals = {}
    
    # Moving Average Strategy
    sma = moving_average(prices, window=14)
    signals['sma_entry'] = prices[-1] > sma[-1]
    
    # RSI Strategy
    rsi_value = relative_strength_index(prices, window=14)
    signals['rsi_entry'] = rsi_value < 30  # Buy when RSI is below 30
    
    # MACD Strategy
    macd_values = macd(prices)
    signals['macd_entry'] = macd_values['macd'][-1] > macd_values['signal'][-1]  # MACD crossing above signal
    
    logger.info(f"Strategy signals: {signals}")
    return signals
