import pandas as pd

def fixTable(df: pd.DataFrame) -> pd.DataFrame:
    attributes = df["elementId"].tolist()
    df = df.pivot_table(index="referenceTime", columns="elementId", values="value", aggfunc="mean")
    df = df.reset_index()
    return df

