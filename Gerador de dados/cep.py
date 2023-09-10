import pandas as pd
dados_cliente = pd.read_csv('Arquivos_CSV/ceps.csv', encoding='UTF-8', sep=';')
cidade_estado = dados_cliente['CIDADE']
vetor_cidade = []
vetor_estado = []
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
dados_funcionario = pd.read_csv('funcionario.csv', encoding='UTF-8', sep=';', header=None)
dados_funcionario.columns=['NOME','CPF','GENERO','IDADE','EMAIL','SENHA','FUNCAO','EMP']
matriz_empresa = [[3,3,3,3,2,2,2,1,0,0],	[3,2,2,3,3,2,1,1,1,0],	[2,2,2,1,1,1,1,1,1,1],	[1,1,1,0,0,0,0,0,0,0],	[1,1,0,0,0,0,0,0,0,0]]
strCsv_endereco=''
teste_vetor = []
for i in range(5):
    for x in range(10):
        if matriz_empresa[i][x]!=0:
            for contador in range(matriz_empresa[i][x]):
                valor = dados_funcionario.loc[(dados_funcionario['EMP']==x+1) & (dados_funcionario['FUNCAO']=='G')].sample(n=1).index[0]
                dados_funcionario=dados_funcionario.drop(valor)
                teste_vetor.append(valor+1)
    for j in range(2):
        strCsv_endereco+=dados_cliente.loc[dados_cliente['ESTADO']==matriz_regioes[i][j]].sample(n=matriz_estados[i][j]).to_csv(index=False, sep=';', header=False)
open('dados.csv', 'w', encoding='UTF-8').write(strCsv_endereco)
dados = pd.read_csv('dados.csv', encoding='UTF-8', sep=';', header=None)
dados['Funcionario'] = teste_vetor
dados.to_csv('dados.csv', index=False, encoding='UTF-8', sep=';', header=False)