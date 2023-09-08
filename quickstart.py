from googleapiclient.discovery import build
from conexao_sheets import CONEXAO

vetor_dados=[]
arquivo = open("Arquivo_Temperatura.csv", 'r', encoding='UTF-8')
dados = arquivo.readlines()
for dado in dados:
    vetor_dados.append(dado.replace('\n','').split(";"))

service = build('sheets', 'v4', credentials=CONEXAO)
sheet = service.spreadsheets()
valores = vetor_dados
result = sheet.values().update(spreadsheetId='17YOVJR--2xMkAtDlJnpe_ZoiW-ivZuc8yH1PFVdv59Y', range='Clima!A1', valueInputOption="RAW", body={"values":valores}).execute()
