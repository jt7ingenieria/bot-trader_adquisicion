
import argparse
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.logger_config import setup_logger
from modes import historical, indicators, realtime
import preprocessing, backtesting_engine, strategy, performance_analyzer
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def main():
    parser = argparse.ArgumentParser(description="Crypto Data Fetcher")
    parser.add_argument("--mode", choices=["historical", "indicators", "realtime", "preprocessing", "backtest"], required=True, help="The mode to run.")
    parser.add_argument("--filepath", type=str, help="The path to the file to preprocess or backtest.")
    parser.add_argument("--strategy", choices=["moving_average_crossover_strategy", "ema_volume_strategy"], default="moving_average_crossover_strategy", help="The trading strategy to use for backtesting.")
    args = parser.parse_args()

    setup_logger()

    if args.mode == "historical":
        await historical.run()
    elif args.mode == "indicators":
        indicators.run()
    elif args.mode == "realtime":
        await realtime.run()
    elif args.mode == "preprocessing":
        if not args.filepath:
            print("Please provide a filepath to preprocess.")
            return
        preprocessing.run(args.filepath)
    elif args.mode == "backtest":
        if not args.filepath:
            print("Please provide a filepath to backtest.")
            return
        df = pd.read_csv(args.filepath)
        if args.strategy == "moving_average_crossover_strategy":
            df = strategy.moving_average_crossover_strategy(df)
        elif args.strategy == "ema_volume_strategy":
            df = strategy.ema_volume_strategy(df)
        portfolio = backtesting_engine.run_backtest(df)
        performance_analyzer.analyze_performance(portfolio)

@app.get("/api/performance")
async def get_performance():
    """Endpoint para obtener métricas de performance"""
    # Implementar lógica para devolver datos de performance
    return {"message": "Performance data will be here"}

@app.get("/api/signals")
async def get_signals():
    """Endpoint para obtener señales de trading"""
    # Implementar lógica para devolver señales
    return {"message": "Signals data will be here"}

if __name__ == "__main__":
    asyncio.run(main())
