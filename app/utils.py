import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Example cleaning: drop columns with all NaNs, fill remaining NaNs
    df = df.dropna(axis=1, how='all')
    df = df.fillna(0)
    return df
