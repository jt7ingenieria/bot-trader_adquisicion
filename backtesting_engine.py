
import pandas as pd
from loguru import logger

def run_backtest(df: pd.DataFrame, initial_capital: float = 10000.0, commission: float = 0.001):
    logger.info("Running backtest...")
    capital = initial_capital
    positions = 0
    portfolio = pd.DataFrame(index=df.index)
    portfolio['holdings'] = 0.0
    portfolio['cash'] = initial_capital
    portfolio['total'] = initial_capital

    for i in range(len(df)):
        if df['signal'].iloc[i] == 1 and positions == 0:
            # Buy
            positions = capital / df['close'].iloc[i]
            capital = 0
            portfolio.loc[df.index[i], 'holdings'] = positions * df['close'].iloc[i]
            portfolio.loc[df.index[i], 'cash'] = capital

        elif df['signal'].iloc[i] == -1 and positions > 0:
            # Sell
            capital = positions * df['close'].iloc[i] * (1 - commission)
            positions = 0
            portfolio.loc[df.index[i], 'holdings'] = 0
            portfolio.loc[df.index[i], 'cash'] = capital

        portfolio.loc[df.index[i], 'total'] = capital + positions * df['close'].iloc[i]

    return portfolio
