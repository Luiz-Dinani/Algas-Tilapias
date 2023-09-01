import pandas as pd
import gender_guesser.detector as gender
import random as r
vetorMulher=[]
vetorHomem=[]
vetorOutros = []
d = gender.Detector()
dados_cliente = pd.read_csv('./arquivoAnonimizado.csv', encoding='UTF-8', sep=';')
dados_cliente = dados_cliente.drop(columns='Endereco')
dados_cliente = dados_cliente.drop(columns='RG')
dados_nomes = dados_cliente.to_csv(index=False, header=False, encoding='UTF-8')
dados_nomes = dados_nomes.replace('\r', '').split('\n')
ch=0
cm=0
import hashlib

def hash_password(password):
  hash_object = hashlib.sha256()
  hash_object.update(password.encode("utf-8"))
  return hash_object.hexdigest()
fkEmpM=0
fkEmpF=0
strCsv = 'NOME;CPF;GENERO;IDADE;EMAIL;SENHA;FUNCAO;EMP\n'
funcM = 'G'
funcF = 'G'
for dados in dados_nomes:
    if dados != "":
        dados = dados.split(",")
        nome = dados[0].split(' ')
        genero = d.get_gender(nome[0][0]+nome[0][1:].lower())
        if genero == "male" and ch<32:
            ch+=1
            if ch==6: #A - 5
                fkEmpM+=1
            elif ch==11: #B - 5 +
                fkEmpM+=1
            elif ch==15: #C - 4
                fkEmpM+=1
            elif ch==18: #D - 3 -
                fkEmpM+=1
            elif ch==21: #E - 3
                fkEmpM+=1
            elif ch==24: #F - 3 +
                fkEmpM+=1
            elif ch==26: #G - 2
                fkEmpM+=1   
            elif ch==27: #H - 1 -
                fkEmpM+=1 
            elif ch==28: #I - 1
                fkEmpM=0
                funcM = 'F'
            elif ch==29:
                fkEmpM=2
            elif ch==30:
                fkEmpM=4
            elif ch==31:
                fkEmpM=6
            elif ch==32:
                fkEmpM=8
            idade = r.randint(25,60)
            strCsv += f'{dados[0]};{dados[1]};H;{idade};{nome[0].lower()}_{nome[-1].lower() if len(nome)>2 else 2023-idade}@gmail.com;{hash_password(nome[0].lower()+"_"+str(2023-idade))};{funcM};{fkEmpM}\n'
        elif genero == "female" and cm<33:
            cm+=1
            if cm==6: #A - 5
                fkEmpF+=1
            elif cm==10: #B - 5 +
                fkEmpF+=1
            elif cm==14: #C - 4
                fkEmpF+=1
            elif cm==18: #D - 3 -
                fkEmpF+=1
            elif cm==21: #E - 3
                fkEmpF+=1
            elif cm==23: #F - 3 +
                fkEmpF+=1
            elif cm==25: #G - 2
                fkEmpF+=1   
            elif cm==27: #H - 1 -
                fkEmpF+=1 
            elif cm==29:
                funcF='F'
                fkEmpF=1
            elif cm==30:
                fkEmpF=3
            elif cm==31:
                fkEmpF=5
            elif cm==32:
                fkEmpF=7
            elif cm==33:
                fkEmpF=9
            idade = r.randint(23,55)
            strCsv += f'{dados[0]};{dados[1]};M;{idade};{nome[0].lower()}_{nome[-1].lower() if len(nome)>2 else 2023-idade}@gmail.com;{hash_password(nome[0].lower()+"_"+str(2023-idade))};{funcF};{fkEmpF}\n'
open('funcionario.csv', 'w').write(strCsv)
dados_empresa = pd.read_csv('./CNPJ.csv', encoding='UTF-8', sep=';')
dados_email = dados_empresa['NOME'].to_csv(index=False, header=False, encoding='UTF-8')
dados_email = dados_email.replace('\r', '').split("\n")
vetor_email = []
vetor_senha = []
for email in dados_email:
    if not email=="":
        email = email.split(" ")
        vetor_email.append(f"{email[0].lower()}_{email[-2].lower()}@{email[0].lower()}.com")
        vetor_senha.append(f"{hash_password(email[0].lower()+'_'+email[-2].lower())}")
dados_empresa['EMAIL'] = vetor_email
dados_empresa['SENHA'] = vetor_senha
dados_empresa.to_csv('empresa.csv', index=False, encoding='UTF-8', sep=';')