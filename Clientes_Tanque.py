import pandas as pd
dados_cliente = pd.read_csv('./arquivoAnonimizado.csv', encoding='UTF-8', sep=';')
dados_cliente = dados_cliente.drop(columns='Endereco')
dados_cliente = dados_cliente.drop(columns='RG')
dados_nomes = dados_cliente.to_csv(index=False, header=False)
dados_nomes = dados_nomes.replace('\r', '').split('\n')
vetorMulher=[]
vetorHomem=[]
vetorOutros = []
strCsv = 'Mulher;Homem;Outros\n'
for dados in dados_nomes:
    if dados != "":
        dados = dados.split(",")
        nome = dados[0].split(' ')
        if nome[0][-1]=='A' or  nome[0][-1]=='E':
            vetorMulher.append(nome[0])
        elif nome[0][-1]=='O' or nome[0][-1]=='R' or nome[0][-1]=='S':
            vetorHomem.append(nome[0])
        else:
            vetorOutros.append(nome[0])
for i in range(len(vetorMulher)):
    if i<len(vetorOutros):
        strCsv+=f'{vetorMulher[i]};{vetorHomem[i]};{vetorOutros[i]}\n'
    elif i<len(vetorHomem):
        strCsv+=f'{vetorMulher[i]};{vetorHomem[i]};\n'
    else:
        strCsv+=f'{vetorMulher[i]};\n'
open('teste.csv', 'w').write(strCsv)