import pandas as pd
import gender_guesser.detector as gender
import random as r
import sys
sys.path.append('../Arquivos_back_end')
from hash import hash_password
vetor_email = []
vetor_senha = []
vetor_aniversario=[]
vetor_genero=[]
vetor_empresa=[]
vetor_funcao=[]
d = gender.Detector()
dados_cliente = pd.read_csv('../Arquivos_back_end/arquivoAnonimizado.csv', encoding='UTF-8', sep=';')
nomes_clientes = dados_cliente.NomeCliente
for teste in range(len(nomes_clientes)):
    nome = dados_cliente.iloc[teste].NomeCliente.split(' ')
    genero = d.get_gender(nome[0][0]+nome[0][1:].lower())
    if genero =='female':
        vetor_genero.append('M')
    elif genero =='male':
        vetor_genero.append('H')
    else:
        vetor_genero.append('U')
    ano = 2023-r.randint(25,40)
    aniversario = f"{ano}-{str(r.randint(1,12)).zfill(2)}-{str(r.randint(1,28)).zfill(2)}"
    vetor_aniversario.append(aniversario)
    vetor_email.append(f"{nome[0].lower()}_{nome[-1].lower() if len(nome)>2 else ano}@gmail.com")
    vetor_senha.append(hash_password(f"{nome[0].lower()}_{ano}"))
    
dados_cliente['Genero']=vetor_genero
dados_cliente['Aniversario']=vetor_aniversario
dados_cliente['Email'] = vetor_email
dados_cliente['Senha'] = vetor_senha
dados_cliente = dados_cliente.loc[dados_cliente['Genero']!='U'].sample(75)
for i in range(10):
    for _ in range(12-i):
        vetor_empresa.append(i+1)
    for _ in range(10-i):
        vetor_funcao.append(1)
    vetor_funcao.append(2)
    vetor_funcao.append(3)
dados_cliente['Empresa'] = vetor_empresa
dados_cliente['Funcao'] = vetor_funcao
dados_cliente['Aut'] = 'null'
dados_grupo = {'NomeCliente':
               ['BEATRIZ ******* ******* CARDOSO','IGOR ** ****** ******* ** SILVA','JUAN ******** ** SILVA','KEVIN ********* DIAS','LUIZ ****** ****** ******* FILHO','PEDRO ***** BONACELLI'],
               'CPF':
               ['289*******1','567*******2','748*******3','636*******4','482*******5','367*******6'],
               'Genero':
                ['M','H','H','H','H','H'],
                'Aniversario':
                ['20/12/2002','10/02/2001','31/07/2001','22/12/2003','20/03/2003','20/10/2003'],
                'Email':
                ['beatriz_cardoso@gmail.com','igor_silva@gmail.com','juan_silva@gmail.com','kevin_dias@gmail.com','luiz_filho@gmail.com','pedro_bonacelli@gmail.com'],
                'Senha':
                [hash_password('beatriz_2002'),hash_password('igor_2001'),hash_password('juan_2001'),hash_password('kevin_2003'),hash_password('luiz_2003'),hash_password('pedro_2003')],
                'Empresa':
                [1,2,3,4,5,6],
                'Funcao':
                [1,1,2,2,3,3],
                'Aut':
                ['null','null','null','null','null','null']
               }
dados_grupo = pd.DataFrame.from_dict(dados_grupo)
dados_cliente=dados_cliente.drop(dados_cliente.loc[(dados_cliente['Empresa']==1) & (dados_cliente['Funcao']==1)].sample(n=1).index[0])
dados_cliente=dados_cliente.drop(dados_cliente.loc[(dados_cliente['Empresa']==2) & (dados_cliente['Funcao']==1)].sample(n=1).index[0])
dados_cliente=dados_cliente.drop(dados_cliente.loc[(dados_cliente['Empresa']==3) & (dados_cliente['Funcao']==2)].sample(n=1).index[0])
dados_cliente=dados_cliente.drop(dados_cliente.loc[(dados_cliente['Empresa']==4) & (dados_cliente['Funcao']==2)].sample(n=1).index[0])
dados_cliente=dados_cliente.drop(dados_cliente.loc[(dados_cliente['Empresa']==5) & (dados_cliente['Funcao']==3)].sample(n=1).index[0])
dados_cliente=dados_cliente.drop(dados_cliente.loc[(dados_cliente['Empresa']==6) & (dados_cliente['Funcao']==3)].sample(n=1).index[0])
dados_grupo['Aniversario']=pd.to_datetime(dados_grupo['Aniversario'], format='%d/%m/%Y')
dados_cliente=pd.concat([dados_grupo, dados_cliente])
dados_cliente = dados_cliente.reset_index()
dados_cliente = dados_cliente.drop(columns=['index'])
dados_cliente.to_csv('funcionario.csv', index=False, encoding='UTF-8', sep=';', header=False)