import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'requests'])
import configparser
from datetime import date

import requests
import pandas as pd
from os.path import exists

config = configparser.ConfigParser()
config.read("config.ini")
client_id = config["DEFAULT"]["client_id"]

endpoint = "https://frost.met.no/observations/v0.jsonld"

"""_summary_
reftime format: 2010-04-01/2010-04-03
n_lines: returns every nth line
returns a pd.DataFrame
"""
def getData(reftime: str, n_lines: int) -> pd.DataFrame:
    metadata = pd.DataFrame()
    
    if(exists("dataframe.csv")) and (exists("metadata.json")):
        metadata = pd.read_json("metadata.json")
        print("Found dataframe.csv, retrieved", metadata["date_retrieved"][0])
        if metadata["reftime"][0] == reftime and metadata["n_lines"][0] == n_lines:
            df = pd.read_csv("dataframe.csv")
            return df
        else:
            print("Dataframe, doesn't match params. New data will be retrieved")
    
    
    params = {
    "sources": "SN18700",
    "elements": "mean(air_temperature P1D),sum(precipitation_amount P1D),mean(air_pressure_at_sea_level P1D),mean(wind_speed P1D),sum(water_evaporation_amount P1D),mean(relative_humidity P1D),mean(cloud_area_fraction P1D),sum(duration_of_sunshine P1D)",
    'referencetime': reftime,
    }
    
    r = requests.get(endpoint, params, auth=(client_id, ""))

    json = r.json()
    
    if r.status_code == 200: 
        data = json ["data"]
        print("Data retrieved")
    else: 
        print('Error! Returned status code %s' % r.status_code)
        print('Message: %s' % json['error']['message'])
        print('Reason: %s' % json['error']['reason'])
        raise Exception("Error! Returned status code {status_code} \n Message: {msg} \n Reason {reason} %".format(status_code=r.status_code, msg=json['error']['message'], reason=json['error']['reason']))
        return None

    df = pd.DataFrame()
    for i in range(0, len(data), n_lines):
        row = pd.DataFrame(data[i]["observations"])
        row["referenceTime"] = data[i]["referenceTime"]
        row["sourceId"] = data[i]["sourceId"]
        df = df.append(row)
    
    df = df.reset_index()
    
    metadata["sources"] = [params["sources"]]
    metadata["elements"] = [params["elements"]]
    metadata["reftime"] = [reftime]
    metadata["rows"] = [len(df)]
    metadata["date_retrieved"] = [date.today()]
    metadata["n_lines"] = [n_lines]
    
    df.to_csv("dataframe.csv")
    metadata.to_json("metadata.json")
    
    return df