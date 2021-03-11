import pandas as pd
import numpy as np
import datetime
import time
import pathlib

from selenium import webdriver

website_list = [
    'melhoresdestinos.com.br',
    'decolar.com',
    'passagensimperdiveis.com.br',
    'submarinoviagens.com.br',
    'cvc.com.br',
    'www.maxmilhas.com.br'
]

website_names = [
    'Melhores Destinos',
    'Decolar.com',
    'Passagens Imperdíveis',
    'Submarino Viagens',
    'CVC',
    'MaxMilhas'
]

def get_year_month(my_date, num_months):
    current_month = my_date.month
    current_year = my_date.year

    result = []
    for i in range(num_months):
        if current_month == 0:
            current_month = 12
            current_year -= 1
        result.append(str(current_year) + '-' + '{:02}'.format(current_month))
        current_month -= 1

    return result[1:]

month_list = get_year_month(datetime.date.today(), 7)
month_list.sort()

website_traffic = pd.DataFrame(data = {'year_month' : month_list})

for i in range(len(website_list)):
    try:
        driver = webdriver.Firefox()
        url = 'https://www.similarweb.com/website/' + website_list[i]
        driver.get(url)
        data = driver.execute_script('return window.Highcharts.charts[0].series[0].options.data')
        driver.close()
        data = np.array(data)[:,1]
        website_traffic[website_names[i]] = data
        print(f'Traffic from {website_names[i]} extracted successfully!')
        time.sleep(10)
    except:
        print(f'Error extracting traffic from {website_names[i]} :(')

PATH = pathlib.Path(__file__).parent.absolute()
DESTINATION_PATH = PATH.joinpath("./datasets")
FILE = DESTINATION_PATH.joinpath('traffic.csv')

website_traffic.to_csv(FILE, index=False)
    