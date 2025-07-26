
import pandas as pd
import numpy as np
from loguru import logger

def analyze_performance(portfolio: pd.DataFrame):
    logger.info("Analyzing performance...")
    returns = portfolio['total'].pct_change().dropna()
    
    total_return = (portfolio['total'].iloc[-1] / portfolio['total'].iloc[0]) - 1
    sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std() # Annualized Sharpe Ratio
    max_drawdown = (portfolio['total'] / portfolio['total'].cummax() - 1).min()

    performance = {
        "total_return": f"{total_return:.2%}",
        "sharpe_ratio": f"{sharpe_ratio:.2f}",
        "max_drawdown": f"{max_drawdown:.2%}"
    }

    logger.info(f"Performance: {performance}")
    return performance
