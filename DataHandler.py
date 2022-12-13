import pandas as pd
from os.path import exists
from datetime import datetime

def fixTable(df: pd.DataFrame) -> pd.DataFrame:
    metadata = pd.DataFrame()
    metadata = pd.read_json("metadata.json")
    if(exists("dataframeFixed.csv")) and metadata['date_retrieved'][0] != datetime.now().strftime("%m/%d/%y %H:%M"):
        print("Found dataframeFixed.csv")
        df = pd.read_csv("dataframeFixed.csv")
        return df
    
    df = df.pivot_table(index="referenceTime", columns="elementId", values="value", aggfunc="mean")
    df = df.reset_index()
    df.to_csv("dataframeFixed.csv")
    return df

