import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
credentials = ServiceAccountCredentials.from_json_keyfile_name('projetosamaka.json', ['https://spreadsheets.google.com/feeds'])
gc = gspread.authorize(credentials)
spreadsheet_id = '16WkRvINOX8bdcoGvWG4QHLGv1FHNjb9mazqwuAOgwhE'
planilha = gc.open_by_key(spreadsheet_id)
folha_id = 294443338
folha = planilha.get_worksheet_by_id(folha_id)
valores = folha.get_all_values()
folha.delete_rows(2, len(valores))
def gerarPlanilha(df):
    df['dia'] = pd.to_datetime(df['dia'])
    df['dia'] = df['dia'].dt.strftime('%Y-%m-%d')
    dados = df.values.tolist()
    folha.insert_rows(dados, 2, value_input_option='RAW')