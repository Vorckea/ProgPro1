import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
import configparser
from datetime import datetime
from os.path import exists

import numpy
import pandas as pd
import requests
import scipy.optimize

config = configparser.ConfigParser()   
endpoint = "https://frost.met.no/observations/v0.jsonld"

class ApiAndDataHandeling:
    def getData(reftime: str = "2020-04-01/2020-5-01") -> pd.DataFrame:
        """_summary_
        reftime format: 2010-04-01/2010-04-03
        returns a pd.DataFrame
        """
        metadata = pd.DataFrame()
        config.read("config.ini")
        client_id = config["DEFAULT"]["client_id"]
        
        if(exists("dataframe.csv")) and (exists("metadata.json")):
            metadata = pd.read_json("metadata.json")
            print("Found dataframe.csv, retrieved", metadata["date_retrieved"][0])
            if metadata["reftime"][0] == reftime:
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
        for i in range(0, len(data)):
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
        
        df.to_csv("dataframe.csv")
        metadata.to_json("metadata.json")
        
        return df
    
    def fixTable(df: pd.DataFrame, n_lines: int = 1) -> pd.DataFrame:
        metadata = pd.DataFrame()
        metadata = pd.read_json("metadata.json")
        
        if(exists("dataframeFixed.csv")) and metadata['date_retrieved'][0] != datetime.now().strftime("%m/%d/%y %H:%M") and metadata["n_lines"][0] == n_lines:
            print("Found dataframeFixed.csv")
            df = pd.read_csv("dataframeFixed.csv")
            return df
        elif metadata["n_lines"][0] != n_lines:
            print("n_lines didn't match, refixing dataframe")
            df = pd.read_csv("dataframeFixed.csv")
            NEWDF = pd.DataFrame
            NEWDF = (df.iloc[::n_lines, :])
            metadata["n_lines"] = [n_lines]
            metadata.to_json("metadata.json")
            return NEWDF
        df = df.pivot_table(index="referenceTime", columns="elementId", values="value", aggfunc="mean")
        df = df.reset_index()
        df.to_csv("dataframeFixed.csv")
        metadata["n_lines"] = [n_lines]
        metadata.to_json("metadata.json")
        return df
    
class regression:
    def fit_sin(tt, yy):
        '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
        tt = numpy.array(tt)
        yy = numpy.array(yy)
        ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
        Fyy = abs(numpy.fft.fft(yy))
        guess_freq = abs(ff[numpy.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
        guess_amp = numpy.std(yy) * 2.**0.5
        guess_offset = numpy.mean(yy)
        guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, 0., guess_offset])

        def sinfunc(t, A, w, p, c):  return A * numpy.sin(w*t + p) + c
        popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
        A, w, p, c = popt
        f = w/(2.*numpy.pi)
        fitfunc = lambda t: A * numpy.sin(w*t + p) + c
        return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}



class markdown:
    def make_markdown_table(array):
        """ Input: Python list with rows of table as lists
            First element as header. 
            Output: String to put into a .md file 
        
        x Input: 
            [["Name", "Age", "Height"],
             ["Jake", 20, 5'10],
             ["Mary", 21, 5'7]] 
        """
    
        nl = "\n"

        markdown = nl
        markdown += f"| {' | '.join(array[0])} |"

        markdown += nl
        markdown += f"| {' | '.join(['---']*len(array[0]))} |"

        markdown += nl
        for entry in array[1:]:
            markdown += f"| {' | '.join(entry)} |{nl}"

        return markdown