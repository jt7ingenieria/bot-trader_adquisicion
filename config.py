
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Config:
    EXCHANGE_ID: str = os.getenv('EXCHANGE_ID', 'binance')
    TIMEFRAME: str = os.getenv('TIMEFRAME', '1d')
    SYMBOLS_TO_FETCH: List[str] = os.getenv('SYMBOLS_TO_FETCH', 'SOL/USDT').split(',')
    START_DATE: str = os.getenv('START_DATE', '2022-01-01')
    END_DATE: str = os.getenv('END_DATE', '2022-12-31')

    # Indicator settings
    SMA_LENGTHS: List[int] = [int(x) for x in os.getenv('SMA_LENGTHS', '20,50').split(',')]
    EMA_LENGTHS: List[int] = [int(x) for x in os.getenv('EMA_LENGTHS', '10,20,50').split(',')]
    BOLLINGER_WINDOW: int = int(os.getenv('BOLLINGER_WINDOW', 20))
    BOLLINGER_STD_DEV: int = int(os.getenv('BOLLINGER_STD_DEV', 2))
    MACD_FAST: int = int(os.getenv('MACD_FAST', 12))
    MACD_SLOW: int = int(os.getenv('MACD_SLOW', 26))
    MACD_SIGNAL: int = int(os.getenv('MACD_SIGNAL', 9))
    RSI_WINDOW: int = int(os.getenv('RSI_WINDOW', 14))

    # Realtime settings
    REALTIME_FETCH_INTERVAL_SECONDS: int = int(os.getenv('REALTIME_FETCH_INTERVAL_SECONDS', 60))

    # Output settings
    OUTPUT_FOLDER: str = 'data'

    @staticmethod
    def get_output_path(filename: str) -> str:
        return os.path.join(Config.OUTPUT_FOLDER, filename)

