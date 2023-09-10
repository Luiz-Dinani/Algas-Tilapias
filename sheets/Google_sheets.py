import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
import time
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('projetosamaka.json', scope)
client = gspread.authorize(creds)
def gerarPlanilha(nome, funcao):
    nova_planilha = client.create('Minha Nova Planilha')
    nova_planilha.share('', perm_type='anyone', role='reader')
    url_planilha = nova_planilha.url
    driver = webdriver.Edge()
    driver.get(url_planilha)
    guia = driver.window_handles[0]
    while True:
        if guia not in driver.window_handles:
            break
        time.sleep(1)
    driver.quit()