
import pandas as pd
import pandas_ta as ta
from loguru import logger
from config import Config

def run():
    logger.info("Calculating indicators...")
    for symbol in Config.SYMBOLS_TO_FETCH:
        filename = f"{Config.EXCHANGE_ID}_{symbol.replace('/', '_')}_{Config.TIMEFRAME}_raw.csv"
        input_path = Config.get_output_path(filename)

        try:
            df = pd.read_csv(input_path)
        except FileNotFoundError:
            logger.warning(f"Historical data for {symbol} not found. Please run historical mode first.")
            continue

        # Calculate indicators using pandas_ta
        df.ta.sma(length=Config.SMA_LENGTHS[0], append=True)
        df.ta.ema(length=Config.EMA_LENGTHS[0], append=True)
        df.ta.bbands(length=Config.BOLLINGER_WINDOW, std=Config.BOLLINGER_STD_DEV, append=True)
        df.ta.macd(fast=Config.MACD_FAST, slow=Config.MACD_SLOW, signal=Config.MACD_SIGNAL, append=True)
        df.ta.rsi(length=Config.RSI_WINDOW, append=True)

        output_filename = f"{Config.EXCHANGE_ID}_{symbol.replace('/', '_')}_{Config.TIMEFRAME}_with_indicators.csv"
        output_path = Config.get_output_path(output_filename)
        df.to_csv(output_path, index=False)
        logger.info(f"Saved data with indicators for {symbol} to {output_path}")
