# ProgPro1
This prosject uses the [Frost API](https://frost.met.no/) provided by MET Norway and allows us to access MET Norway's historical archive of weather data


## Usage
Insert your client ID you can request from [here](https://frost.met.no/auth/requestCredentials.html) into `config_ex.ini` and rename the file to `config.ini`

## Functions in this project
### Api.py
Retreives data in the specified time frame from the Frost API

To use the `getData()` function from `API.py` you have to give a dates in the format: `reftime="yyyy-mm-dd/yyyy-mm-dd"` and how many lines you want to retrieve in the format `n_lines=1`. It returns a dataframe containing a relevant data

To change what elements are retrieved or the sources of the data, change it in the `config.ini` file

### Data handler
Turns long data into wide data to be easier to process in seaborn and matplotlib

To use the `fixTable()` function specify a dataframe to "fix" and it returns a formatted version of the dataframe