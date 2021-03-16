import requests
from bs4 import BeautifulSoup as BS
def latest_update():
    page = requests.get('https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/dados-estatisticos')
    soup = BS(page.content, 'html.parser')
    last_update = soup.find_all('span', class_ = 'value')[1].text

    return last_update
