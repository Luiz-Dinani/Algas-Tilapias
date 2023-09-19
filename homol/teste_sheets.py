import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import mysql.connector
from decimal import Decimal
def conectarBancoDeDados():
    db = mysql.connector.connect(
        host="database-1.cucfdybb1rps.us-east-1.rds.amazonaws.com",
        user="tilapiasUser",
        password="tilapiasSenha"
    )
    if db.is_connected():
        return db
    return None

def criarCursor(db):
    cursor = db.cursor()
    cursor.execute("use samaka")
    return cursor

def coleta_dados_monitoramento_tanque_funcionario(id_funcionario):
    try:
        db = conectarBancoDeDados()
        cursor=criarCursor(db)
        with db:
            cursor.callproc('proc_sheets', [id_funcionario])
            for result in cursor.stored_results():
                resultado = result.fetchall()
            resultado = [[float(item) if isinstance(item, Decimal) else item for item in row] for row in resultado]
            return pd.DataFrame(resultado)
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)
def gerarClient():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('projetosamaka.json', scope)
    client = gspread.authorize(creds)
    return client
def coletarDadosPlanilha(idCliente):
    resultado = coleta_dados_monitoramento_tanque_funcionario(idCliente)
    numero_de_colunas = resultado.shape[1]
    ultima_coluna = resultado.iloc[:, numero_de_colunas - 1]
    cargo = ultima_coluna[0]
    gc = gerarClient()
    if cargo==1:
        spreadsheet_id = '1mS630A4CHShc1urxREXo_gh5g97Yl2AvbKs9A7WefwY'
        folha_id = 294443338
        resultado = resultado.drop(columns=[numero_de_colunas - 1])
        planilha = gc.open_by_key(spreadsheet_id)
        folha = planilha.get_worksheet_by_id(folha_id)
        valores = folha.get_all_values()
        if len(valores)>2:
            folha.delete_rows(2, len(valores))
        resultado[5] = pd.to_datetime(resultado[5])
        resultado[5] = resultado[5].dt.strftime('%Y-%m-%d')
        dados = resultado.values.tolist()
        folha.insert_rows(dados, 2, value_input_option='RAW')
    elif cargo==2:
        spreadsheet_id = '13Bdb0xRaetqakzeqP0UzqoF9n1VrAlDlyehSBK6JksI'
        folha_id = 121551296
        resultado = resultado.drop(columns=[numero_de_colunas - 1])
        planilha = gc.open_by_key(spreadsheet_id)
        folha = planilha.get_worksheet_by_id(folha_id)
        valores = folha.get_all_values()
        if len(valores)>2:
            folha.delete_rows(2, len(valores))
        resultado[3] = pd.to_datetime(resultado[3])
        resultado[3] = resultado[3].dt.strftime('%Y-%m-%d')
        resultado[8] = resultado[4]*resultado[5]*resultado[7]
        resultado[8] = [float(x) for x in resultado[8]]
        dados = resultado.values.tolist()
        folha.append_rows(dados)
    else:
        spreadsheet_id = '1JGsA1wuMqGjeFnXgmizvT2oCkXGpJ4GMUzLRePDv-aE'
        folha_id = 294443338
        resultado = resultado.drop(columns=[numero_de_colunas - 1])
        resultado[5] = pd.to_datetime(resultado[5])
        resultado[5] = resultado[5].dt.strftime('%Y-%m-%d')
        resultado[21] = pd.to_datetime(resultado[21])
        resultado[21] = resultado[21].dt.strftime('%Y-%m-%d')
        planilha = gc.open_by_key(spreadsheet_id)
        folha = planilha.get_worksheet_by_id(folha_id)
        valores = folha.get_all_values()
        if len(valores)>2:
            folha.delete_rows(2, len(valores))
        resultadoMon = resultado.iloc[:, range(16)]
        dados = resultadoMon.values.tolist()
        folha.insert_rows(dados, 2, value_input_option='RAW')
        resultadoFun = resultado.iloc[:, range(17, 24)]
        resultadoFun[7] = resultado.iloc[:, 35]
        folha_id = 1205342963
        folha = planilha.get_worksheet_by_id(folha_id)
        valores = folha.get_all_values()
        if len(valores)>2:
            folha.delete_rows(2, len(valores))
        dados = resultadoFun.values.tolist()
        folha.insert_rows(dados, 2, value_input_option='RAW')
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/"
print(coletarDadosPlanilha(5))