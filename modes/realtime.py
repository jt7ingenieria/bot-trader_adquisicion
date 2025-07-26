
import asyncio
import pandas as pd
import pandas_ta as ta
from loguru import logger
from config import Config
from data_fetcher import AsyncCryptoDataFetcher
import os

async def run():
    logger.info("Starting real-time data fetching...")
    fetcher = AsyncCryptoDataFetcher(Config.EXCHANGE_ID)

    while True:
        for symbol in Config.SYMBOLS_TO_FETCH:
            # 1. Fetch raw data
            df_raw = await fetcher.fetch_latest_ohlcv(symbol, Config.TIMEFRAME)

            if df_raw is None or df_raw.empty:
                logger.warning(f"Could not fetch latest OHLCV for {symbol}. Skipping.")
                continue

            # 2. Save raw data
            raw_filename = f"{Config.EXCHANGE_ID}_{symbol.replace('/', '_')}_{Config.TIMEFRAME}_realtime_raw.csv"
            raw_output_path = Config.get_output_path(raw_filename)
            df_raw.to_csv(raw_output_path, mode='a', header=not os.path.exists(raw_output_path), index=False)
            logger.info(f"Saved raw real-time data for {symbol} to {raw_output_path}")

            # 3. Calculate indicators
            df_indicators = df_raw.copy()
            df_indicators.ta.sma(length=Config.SMA_LENGTHS[0], append=True)
            df_indicators.ta.ema(length=Config.EMA_LENGTHS[0], append=True)
            df_indicators.ta.bbands(length=Config.BOLLINGER_WINDOW, std=Config.BOLLINGER_STD_DEV, append=True)
            df_indicators.ta.macd(fast=Config.MACD_FAST, slow=Config.MACD_SLOW, signal=Config.MACD_SIGNAL, append=True)
            df_indicators.ta.rsi(length=Config.RSI_WINDOW, append=True)

            # 4. Save data with indicators
            indicators_filename = f"{Config.EXCHANGE_ID}_{symbol.replace('/', '_')}_{Config.TIMEFRAME}_realtime_indicators.csv"
            indicators_output_path = Config.get_output_path(indicators_filename)
            df_indicators.to_csv(indicators_output_path, mode='a', header=not os.path.exists(indicators_output_path), index=False)
            logger.info(f"Saved real-time data with indicators for {symbol} to {indicators_output_path}")

        await asyncio.sleep(Config.REALTIME_FETCH_INTERVAL_SECONDS)
