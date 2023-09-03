import mysql.connector

def bancoDados(insert):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="S@opaulo18",
            database="algas"
        )

        if mydb.is_connected():
            db_Info = mydb.get_server_info()
            mycursor = mydb.cursor()
            mycursor.execute(insert)
            mydb.commit()
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if(mydb.is_connected()):
            mycursor.close()
            mydb.close()

insert = 'insert into empresa (cnpj, nomeEmpresa, email, senha) values \n'
for dados in open('empresa.csv', 'r', encoding='UTF-8'):
    info = dados.split(';')
    insert+=f"('{info[0].zfill(14)}','{info[1]}','{info[2]}','{info[3]}'),\n"
insert = insert[:-2]
insert += ';'
bancoDados(insert)
insert = 'insert into funcionario (nome,cpf,email,idade,genero,senha,fkEmpresa,funcao) values \n'
for dados in open('funcionario.csv', 'r', encoding='UTF-8'):
    info = dados.split(';')
    insert+=f"('{info[0]}','{info[1].zfill(11)}','{info[4]}',{info[3]},'{info[2]}','{info[5]}',{int(info[7])},'{info[6]}'),\n"
insert = insert[:-2]
insert += ';'
bancoDados(insert)
insert = 'insert into tanque (fkFuncionario,cep,cidade,bairro,rua,estado) values \n'
for dados in open('dados.csv', 'r', encoding='UTF-8'):
    info = dados.split(';')
    insert+=f"({int(info[5])},'{info[0].zfill(8)}','{info[1]}','{info[2]}','{info[3]}','{info[4]}'),\n"
insert = insert[:-2]
insert += ';'
bancoDados(insert)