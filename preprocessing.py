
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from loguru import logger

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Handling missing values...")
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    return df

def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Normalizing data...")
    for col in ['open', 'high', 'low', 'close']:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    return df

def scale_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Scaling data...")
    scaler = MinMaxScaler()
    numerical_cols = df.select_dtypes(include=['number']).columns
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    return df

def run(filepath: str):
    logger.info(f"Preprocessing data for {filepath}...")
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return

    df = handle_missing_values(df)
    df = normalize_data(df)
    df = scale_data(df)

    output_filename = filepath.replace(".csv", "_processed.csv")
    df.to_csv(output_filename, index=False)
    logger.info(f"Saved preprocessed data to {output_filename}")
