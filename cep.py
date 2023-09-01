import pandas as pd
dados_cliente = pd.read_csv('./ceps.csv', encoding='ANSI', sep=';')
cidade_estado = dados_cliente['CIDADE']
vetor_cidade = []
vetor_estado = []
for cidade in cidade_estado:
    cidade = cidade.split('/')
    vetor_cidade.append(cidade[0])
    vetor_estado.append(cidade[1][0:2])
dados_cliente['CIDADE']=vetor_cidade
dados_cliente['ESTADO']=vetor_estado
dados_cliente=dados_cliente.drop(dados_cliente[dados_cliente['RUA'].isnull()].index)
dados_cliente=dados_cliente.drop(dados_cliente[dados_cliente['BAIRRO'].isnull()].index)

matriz_regioes = [
    ['AM', 'PA'], #8 E 11
    ['BA', 'MA'], #8 E 10
    ['RJ', 'SP'], #6 E 7
    ['PR', 'RS'], # 1 E 2
    ['DF', 'GO'] # 1 E 1
]

matriz_estados = [
    [8,11],
    [8,10],
    [6,7],
    [1,2],
    [1,1]
]
strCsv_endereco=''
for i in range(5):
    for j in range(2):
        strCsv_endereco+=dados_cliente.loc[dados_cliente['ESTADO']==matriz_regioes[i][j]].sample(n=matriz_estados[i][j]).to_csv(index=False, sep=';')
open('endereco.csv', 'w', encoding='UTF-8').write(strCsv_endereco)