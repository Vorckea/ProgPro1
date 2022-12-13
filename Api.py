import configparser
from datetime import datetime
import requests
import pandas as pd
from os.path import exists

config = configparser.ConfigParser()


endpoint = "https://frost.met.no/observations/v0.jsonld"


def getData(reftime: str = "2020-04-01/2020-5-01", n_lines: int = 1) -> pd.DataFrame:
    """_summary_
    reftime format: 2010-04-01/2010-04-03
    n_lines: int number
    returns a pd.DataFrame
    """
    metadata = pd.DataFrame()
    config.read("config.ini")
    client_id = config["DEFAULT"]["client_id"]
    
    if(exists("dataframe.csv")) and (exists("metadata.json")):
        metadata = pd.read_json("metadata.json")
        print("Found dataframe.csv, retrieved", metadata["date_retrieved"][0])
        if metadata["reftime"][0] == reftime and metadata["n_lines"][0] == n_lines:
            df = pd.read_csv("dataframe.csv")
            return df
        else:
            print("Existing dataframe doesn't match params. New data will be retrieved")
    
    
    params = {
    "sources": config["DEFAULT"]["sources"],
    "elements": config["DEFAULT"]["elements"],
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
    metadata["date_retrieved"] = [datetime.now().strftime("%m/%d/%y %H:%M")]
    metadata["n_lines"] = [n_lines]
    
    df.to_csv("dataframe.csv")
    metadata.to_json("metadata.json")
    
    return df