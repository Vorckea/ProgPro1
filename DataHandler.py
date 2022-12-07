import pandas as pd
from os.path import exists

def fixTable(df: pd.DataFrame) -> pd.DataFrame:
    if(exists("dataframeFixed.csv")):
        print("Found dataframeFixed.csv")
        df = pd.read_csv("dataframeFixed.csv")
        return df
    
    df = df.pivot_table(index="referenceTime", columns="elementId", values="value", aggfunc="mean")
    df = df.reset_index()
    df.to_csv("dataframeFixed.csv")
    return df

