import pandas as pd
import pathlib

from assets import handlers
from colorama import Fore, Back, Style

flight_data = pd.DataFrame()

root_url = 'https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/dados-estatisticos/arquivos/resumo_anual_'

# Get flight data from ANAC website
for year in range(2016, 2022):
    try:
        url = root_url + str(year) + '.csv'
        print(Fore.GREEN + f'Extracting data from {year}.')
        data = pd.read_csv(url, encoding='ISO-8859-1', sep=';')
        flight_data = pd.concat([data, flight_data])
    except:
        print(Fore.RED + f'Error extracting flight data from {year}')

# Clean dataset for better handling
flight_data.columns = flight_data.columns.str.lower()

flight_data = flight_data.drop(columns = handlers.ANAC_DROP_COLUMNS)

# Rename remaining columns for better understanding
flight_data = flight_data.rename(columns = handlers.ANAC_RENAME_COLUMNS)

# Change Brazilian state names for their code (Rio Grande do Sul -> RS, Bahia -> BA)
flight_data = flight_data.replace({'airport_origin_state' : handlers.ESTADOS, 'airport_destination_state' : handlers.ESTADOS})

# Change Airline names for a short version (Gol Transportes Aéreos -> Gol, Azul Linhas Aéreas -> Azul)
flight_data = flight_data.replace({'airline_name' : handlers.AIRLINE_NAMES})

# Create a year_month column
flight_data['month'] = flight_data['month'].map("{:02}".format)
flight_data['year_month'] = (flight_data['year'].astype(str) + '-' + flight_data['month'].astype(str))

# Get current directory and save data to /datasets folder
PATH = pathlib.Path(__file__).parent.absolute()
DESTINATION_PATH = PATH.joinpath("./datasets").joinpath('flights.csv')
flight_data.to_csv(DESTINATION_PATH, index=False)