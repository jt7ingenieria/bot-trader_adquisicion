
import pandas as pd
import numpy as np
from config import Config

def moving_average_crossover_strategy(df: pd.DataFrame) -> pd.DataFrame:
    df['signal'] = np.nan # Initialize with NaN
    
    sma_short = f"SMA_{Config.SMA_LENGTHS[0]}"
    sma_long = f"SMA_{Config.SMA_LENGTHS[1]}"
    
    df.loc[df[sma_short] > df[sma_long], 'signal'] = 1  # Buy signal
    df.loc[df[sma_short] < df[sma_long], 'signal'] = -1 # Sell signal
    return df

def ema_volume_strategy(df: pd.DataFrame) -> pd.DataFrame:
    df['signal'] = np.nan # Initialize with NaN

    ema_short = f"EMA_{Config.EMA_LENGTHS[0]}"
    ema_medium = f"EMA_{Config.EMA_LENGTHS[1]}"
    ema_long = f"EMA_{Config.EMA_LENGTHS[2]}"

    # Buy signal: Short EMA crosses above Medium EMA, Medium EMA crosses above Long EMA, and volume is above average
    df.loc[(df[ema_short] > df[ema_medium]) & 
           (df[ema_medium] > df[ema_long]) & 
           (df['volume'] > df['volume'].rolling(window=20).mean()), 'signal'] = 1

    # Sell signal: Short EMA crosses below Medium EMA, Medium EMA crosses below Long EMA, and volume is above average
    df.loc[(df[ema_short] < df[ema_medium]) & 
           (df[ema_medium] < df[ema_long]) & 
           (df['volume'] > df['volume'].rolling(window=20).mean()), 'signal'] = -1
    
    return df
