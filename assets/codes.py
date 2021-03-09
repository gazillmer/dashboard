import pathlib
import json
import pandas as pd
import numpy as np

CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
DATA_PATH = CURRENT_PATH.joinpath("./json")
FILE = DATA_PATH.joinpath("airports.json")

# Read json file with airport data such as iata code, lat, long and airport name
with open(FILE, 'r') as airports_json:
    airport_list_raw = airports_json.read()
airport_list = json.loads(airport_list_raw)

# Transform the json file into a modifiable dataframe, removing unnecessary data and missing airport codes
airports = pd.DataFrame(data = airport_list)
airports = airports[['code', 'lat', 'lon', 'name', 'city', 'country', 'icao']]
airports.rename(columns = {'code':'airport_iata', 'icao':'airport_icao'}, inplace=True)
airports['airport_icao'] = airports['airport_icao'].replace('', np.nan)
airports.dropna(inplace=True)

# Save in /datasets folder
CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
DATA_PATH = CURRENT_PATH.joinpath("../datasets")
FILE = DATA_PATH.joinpath("airport_list.csv")

airports.to_csv(FILE, index=False)