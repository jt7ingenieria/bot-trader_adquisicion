from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
from src import strategy, backtesting_engine, performance_analyzer
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/api/v1/data', methods=['GET'])
def get_data_files():
    """Devuelve la lista de archivos de datos disponibles."""
    try:
        data_files = [f for f in os.listdir('data') if f.endswith('_indicators.csv')]
        return jsonify(data_files)
    except Exception as e:
        app.logger.error(f"Error listing data files: {e}")
        return jsonify({"error": "Could not list data files"}), 500

@app.route('/api/v1/backtest', methods=['POST'])
def run_backtest_api():
    """Ejecuta un backtest y devuelve los resultados."""
    data = request.get_json()
    filepath = data.get('filepath')
    strategy_name = data.get('strategy_name')

    if not filepath or not strategy_name:
        return jsonify({"error": "Missing filepath or strategy_name"}), 400

    app.logger.info(f"API - Selected file: {filepath}, Selected strategy: {strategy_name}")

    try:
        df = pd.read_csv(os.path.join('data', filepath), index_col='timestamp', parse_dates=True)
        app.logger.info("API - Dataframe loaded successfully.")
    except Exception as e:
        app.logger.error(f"API - Error loading data: {e}")
        return jsonify({"error": f"Error loading data: {e}"}), 500

    try:
        if strategy_name == "moving_average_crossover_strategy":
            df = strategy.moving_average_crossover_strategy(df)
        elif strategy_name == "ema_volume_strategy":
            df = strategy.ema_volume_strategy(df)
        else:
            return jsonify({"error": "Invalid strategy_name"}), 400
        app.logger.info("API - Strategy applied successfully.")
    except Exception as e:
        app.logger.error(f"API - Error applying strategy: {e}")
        return jsonify({"error": f"Error applying strategy: {e}"}), 500
    
    try:
        portfolio = backtesting_engine.run_backtest(df)
        performance = performance_analyzer.analyze_performance(portfolio)
        app.logger.info("API - Backtest and performance analysis completed.")
    except Exception as e:
        app.logger.error(f"API - Error during backtest or performance analysis: {e}")
        return jsonify({"error": f"Error during backtest or performance analysis: {e}"}), 500

    return jsonify(performance)

if __name__ == '__main__':
    app.run(debug=True)