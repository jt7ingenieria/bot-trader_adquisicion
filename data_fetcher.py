
import ccxt.async_support as ccxt_async
import pandas as pd
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any, List
from loguru import logger

class AsyncCryptoDataFetcher:
    def __init__(self, exchange_id: str, exchange_options: Optional[Dict[str, Any]] = None):
        self.exchange_id = exchange_id
        self.exchange_options = exchange_options or {}

    @asynccontextmanager
    async def get_exchange(self):
        exchange = getattr(ccxt_async, self.exchange_id)(self.exchange_options)
        try:
            await exchange.load_markets()
            yield exchange
        finally:
            await exchange.close()

    async def fetch_historical_data(self, symbol: str, timeframe: str, start_date: str, end_date: str) -> pd.DataFrame:
        logger.info(f"Fetching historical data for {symbol} from {start_date} to {end_date}")
        all_ohlcv = []
        async with self.get_exchange() as exchange:
            since = exchange.parse8601(f"{start_date}T00:00:00Z")
            end_timestamp = exchange.parse8601(f"{end_date}T23:59:59Z")

            while since < end_timestamp:
                ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, since)
                if not ohlcv:
                    break
                all_ohlcv.extend(ohlcv)
                since = ohlcv[-1][0] + exchange.parse_timeframe(timeframe) * 1000

        df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    async def fetch_latest_ohlcv(self, symbol: str, timeframe: str) -> Optional[pd.DataFrame]:
        logger.info(f"Fetching latest OHLCV for {symbol}")
        async with self.get_exchange() as exchange:
            ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=1)
            if not ohlcv:
                return None

            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
