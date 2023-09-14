import gspread
from oauth2client.service_account import ServiceAccountCredentials

import webbrowser
new=2
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('projetosamaka.json', scope)
client = gspread.authorize(creds)
def gerarPlanilha(nome, funcao, df):
    vetor_id_tanque=[]
    vetor_dias =[]
    for dias in df['dias']:
        vetor_dias.append(dias.strftime('%d/%m/%Y'))
    df['dias']=vetor_dias
    if funcao == "A":
        for i in df.fkTanque:
            if i not in vetor_id_tanque:
                vetor_id_tanque.append(i)
        nova_planilha = client.create(nome)
        for id in vetor_id_tanque:
            nova_planilha.add_worksheet(title='Tanque'+str(id), rows=300, cols=26)
            dados = df.loc[df['fkTanque']==id].drop(columns=['fkTanque']).values.tolist()
            nova_planilha.worksheet('Tanque'+str(id)).insert_rows([['Ciclo', 'Restam (dias)', 'Amonia', 'Biomassa', 'Data', 'Oxigenio', 'Peso Peixe', 'PH', 'Qualidade Agua', 'Quantidade Peixe', 'Salinidade', 'Temperatura', 'Turbidez', 'Visibilidade']], 1)
            nova_planilha.worksheet('Tanque'+str(id)).insert_rows(dados, 2)
        nova_planilha.del_worksheet_by_id(0)
        nova_planilha.share('', perm_type='anyone', role='writer')
        url_planilha = nova_planilha.url
        webbrowser.open(url_planilha,new=new)
    elif funcao == "G":
        nova_planilha = client.create(nome)
        nova_planilha.add_worksheet(title='Tanque'+str(id), rows=300, cols=26)
        dados = df.loc[df['fkTanque']==id].drop(columns=['fkTanque']).values.tolist()
        nova_planilha.worksheet('Tanque'+str(id)).insert_rows([['Ciclo', 'Restam (dias)', 'Amonia', 'Biomassa', 'Data', 'Oxigenio', 'Peso Peixe', 'PH', 'Qualidade Agua', 'Quantidade Peixe', 'Salinidade', 'Temperatura', 'Turbidez', 'Visibilidade']], 1)
        nova_planilha.worksheet('Tanque'+str(id)).insert_rows(dados, 2)
        nova_planilha.del_worksheet_by_id(0)
        nova_planilha.share('', perm_type='anyone', role='writer')
        url_planilha = nova_planilha.url
        webbrowser.open(url_planilha,new=new)

        