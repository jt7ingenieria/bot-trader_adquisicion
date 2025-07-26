
import asyncio
import pandas as pd
from loguru import logger
from config import Config
from data_fetcher import AsyncCryptoDataFetcher

import pandas_ta as ta

async def run():
    logger.info("Starting historical data download...")
    fetcher = AsyncCryptoDataFetcher(Config.EXCHANGE_ID)

    for symbol in Config.SYMBOLS_TO_FETCH:
        # 1. Fetch raw data
        df_raw = await fetcher.fetch_historical_data(symbol, Config.TIMEFRAME, Config.START_DATE, Config.END_DATE)
        
        if df_raw.empty:
            logger.warning(f"No historical data found for {symbol}. Skipping.")
            continue

        # 2. Save raw data
        raw_filename = f"{Config.EXCHANGE_ID}_{symbol.replace('/', '_')}_{Config.TIMEFRAME}_raw.csv"
        raw_output_path = Config.get_output_path(raw_filename)
        df_raw.to_csv(raw_output_path, index=False)
        logger.info(f"Saved raw historical data for {symbol} to {raw_output_path}")

        # 3. Calculate indicators
        df_indicators = df_raw.copy()
        for length in Config.SMA_LENGTHS:
            df_indicators.ta.sma(length=length, append=True)
        for length in Config.EMA_LENGTHS:
            df_indicators.ta.ema(length=length, append=True)
        df_indicators.ta.bbands(length=Config.BOLLINGER_WINDOW, std=Config.BOLLINGER_STD_DEV, append=True)
        df_indicators.ta.macd(fast=Config.MACD_FAST, slow=Config.MACD_SLOW, signal=Config.MACD_SIGNAL, append=True)
        df_indicators.ta.rsi(length=Config.RSI_WINDOW, append=True)

        # 4. Save data with indicators
        indicators_filename = f"{Config.EXCHANGE_ID}_{symbol.replace('/', '_')}_{Config.TIMEFRAME}_indicators.csv"
        indicators_output_path = Config.get_output_path(indicators_filename)
        df_indicators.to_csv(indicators_output_path, index=False)
        logger.info(f"Saved data with indicators for {symbol} to {indicators_output_path}")
