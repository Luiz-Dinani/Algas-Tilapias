import dbcontext.samaka_db_context as _context
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
def coletarDadosPlanilha(idCliente):
    resultado = _context.coleta_dados_monitoramento_tanque_funcionario(idCliente)
    cargo = resultado['fkCargo'].head(1)
    gc = gerarClient()
    if cargo==1:
        spreadsheet_id = '16WkRvINOX8bdcoGvWG4QHLGv1FHNjb9mazqwuAOgwhE'
        folha_id = 294443338
    planilha = gc.open_by_key(spreadsheet_id)
    folha = planilha.get_worksheet_by_id(folha_id)
    valores = folha.get_all_values()
    print(len(valores))
    if len(valores)>2:
        folha.delete_rows(2, len(valores))
    print(idCliente)
    resultado['dia'] = pd.to_datetime(resultado['dia'])
    resultado['dia'] = resultado['dia'].dt.strftime('%Y-%m-%d')
    dados = resultado.values.tolist()
    folha.insert_rows(dados, 2, value_input_option='RAW')
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/"

def gerarClient():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('projetosamaka.json', scope)
    client = gspread.authorize(creds)
    return client