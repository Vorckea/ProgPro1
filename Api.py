import requests
import pandas as pd

client_id = "<client id>"

endpoint = "https://frost.met.no/observations/v0.jsonld"

"""_summary_
reftime format: 2010-04-01/2010-04-03
"""
def getData(reftime: str) -> pd.DataFrame():
    
    params = {
    "sources": "SN18700,SN90450",
    "elements": "mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)",
    'referencetime': reftime,
    }
    
    r = requests.get(endpoint, params, auth=(client_id, ""))

    json = r.json

    if r.status_code == 200: 
        data = json ["data"]
        print("Data retrieved")
    else: 
        print('Error! Returned status code %s' % r.status_code)
        print('Message: %s' % json['error']['message'])
        print('Reason: %s' % json['error']['reason'])

    df = pd.DataFrame()
    for i in range(len(data)):
        row = pd.DataFrame(data[i]["observations"])
        row["referenceTime"] = data[i]["referenceTime"]
        row["sourceId"] = data[i]["sourceId"]
        df = df.append(row)
    
    df = df.reset_index()