import pandas as pd
import mysql.connector
def conectarBancoDeDados():
    db = mysql.connector.connect(
        host="database-1.cucfdybb1rps.us-east-1.rds.amazonaws.com",
        user="tilapiasUser",
        password="tilapiasSenha"
    )
    cursor = db.cursor()
    cursor.execute("use samaka")
    return db
def inserirDados(insert):
    try:
        mydb = conectarBancoDeDados()

        if mydb.is_connected():
            db_Info = mydb.get_server_info()
            print("Conectado ao MySQL Server versão ", db_Info)
            mycursor = mydb.cursor()
            mycursor.execute(insert)
            mydb.commit()
            print(mycursor.rowcount, "registro inserido")
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if(mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("Conexão com MySQL está fechada\n")
dados_preco = pd.read_csv('../Arquivos_back_end/preco.csv', encoding='UTF-8', sep=';')
dados_preco['dia'] = pd.to_datetime(dados_preco['dia'], format='%d/%m/%Y')
dados = dados_preco.to_csv(index=False, header=False, sep=';')
dados = dados.split('\n')
insert = 'insert into preco (dia, preco) values \n'
for dado in dados:
    vetor_dados = dado.replace('\r','').split(';')
    if len(vetor_dados) > 1:
        insert+=f"('{vetor_dados[0]}', {vetor_dados[1]}),\n"
insert = insert[:-2]
insert += ';'
inserirDados(insert)