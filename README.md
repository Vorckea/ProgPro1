# ProgPro1
This is a prosject to plot and visualize localized weather data and practice statistical analysis. It uses the [Frost API](https://frost.met.no/) provided by MET Norway and allows us to access MET Norway's historical archive of weather data from many different years


## Basic Usage
Insert your client ID you can request from [here](https://frost.met.no/auth/requestCredentials.html) into `config_ex.ini` and rename the file to `config.ini`

# Functions in this project
All the functions in this are located in the `Utils.py` file so to use it start with `import Utils`

## getdata()
Retreives data in the specified time frame from the Frost API, requires API key to be located in `config.ini`

The `getData()` function requires a date-range in the format: `reftime="yyyy-mm-dd/yyyy-mm-dd"` and how many lines you want to retrieve in the format `n_lines=1`. It returns a dataframe containing a relevant data. `getData()` is located in the ApiAndDataHandeling class

Example use:
```Python 
df = Utils.ApiAndDataHandeling.getData(reftime="2020-04-01/2020-04-14", n_lines=1)
```

To change what elements are retrieved or the sources of the data, change it in the `config.ini` file

## fixTable()
Turns long data into wide data and removes unnecessary colums to be easier to process in seaborn, pyplot and matplotlib

To use the `fixTable()` function specify a dataframe to "fix" and it returns a formatted version of the dataframe. The `fixTable()` function is in the ApiAndDataHandeling class  

Example use:
```Python 
df = Utils.ApiAndDataHandeling.fixTable(df)
```

## fit_sin()
Fit sin to the input data, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"

Requires two Pandas Series, one to represent each axis. 

Example use:
```Python 
res = Utils.regression.fit_sin(df.index, df["mean(air_temperature P1D)"])
```

## make_markdown_table()
Turns a Pandas array into a markdown table to be easier to read and present

Input: Python list with rows of table as lists\
First element as list of headers. \
Output: String to copy into a .md file

Example code:
```Python
liste = [["Data","Gjennomsnitt","Median", "Standaravikk"]]
for i in range(len(elements)):
    if i == 8: break
    a = []
    a.append(elements[i])
    a.append(str(mean[i]))
    a.append(str(median[i]))
    a.append(str(std[i]))
    liste.append(a)
print(utils.markdown.make_markdown_table(liste))
```