import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'requests'])
import configparser

import requests
import pandas as pd
from os.path import exists

config = configparser.ConfigParser()
config.read("config.ini")
clientid = config["DEFAULT"]["client_id"]

endpoint = "https://frost.met.no/observations/v0.jsonld"

"""_summary_
reftime format: 2010-04-01/2010-04-03
returns a pd.DataFrame
"""
def getData(reftime: str) -> pd.DataFrame:
    
    if(exists("dataframe.csv")):
        print("Found dataframe.csv")
        df = pd.read_csv("dataframe.csv")
        return df
    
    params = {
    "sources": "SN19430",
    "elements": "mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)",
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
    for i in range(len(data)):
        row = pd.DataFrame(data[i]["observations"])
        row["referenceTime"] = data[i]["referenceTime"]
        row["sourceId"] = data[i]["sourceId"]
        df = df.append(row)
    
    df = df.reset_index()
    
    df.to_csv("dataframe.csv")
    
    return df