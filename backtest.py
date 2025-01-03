import pandas as pd
from strategy import strategy_analysis
import logging

# Set up logging
logger = logging.getLogger(__name__)

def backtest_strategy(contract_address, historical_data):
    """
    Backtest a trading strategy using historical data.
    Args:
    - contract_address: str - Contract address for the backtest.
    - historical_data: pd.DataFrame - DataFrame containing historical price data.
    Returns:
    - dict: Backtest results (profit/loss, entry/exit points).
    """
    results = []
    initial_balance = 1000  # Starting balance for backtest
    
    for i in range(14, len(historical_data)):
        prices = historical_data['price'][:i]
        signals = strategy_analysis(prices)
        
        if signals['sma_entry'] and initial_balance > 0:
            entry_price = historical_data['price'][i]
            results.append({
                'entry': entry_price,
                'balance': initial_balance,
                'action': 'buy'
            })
            initial_balance -= entry_price
        
        elif signals['macd_entry'] and initial_balance > 0:
            exit_price = historical_data['price'][i]
            results.append({
                'exit': exit_price,
                'balance': initial_balance,
                'action': 'sell
