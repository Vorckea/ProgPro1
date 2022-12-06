import pandas as pd

def fixTable(df: pd.DataFrame) -> pd.DataFrame:
    attributes = df["elementId"].tolist()
    return df.pivot_table(index="referenceTime", columns="elementId", values="value", aggfunc="mean")
