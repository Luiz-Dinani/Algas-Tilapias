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
        db = conectarBancoDeDados()        

        if db.is_connected():
            db_Info = db.get_server_info()
            print("Conectado ao MySQL Server versão ", db_Info)
            cursor = db.cursor()
            cursor.execute("use samaka")
            cursor.execute(insert)
            db.commit()
            print(cursor.rowcount, "registro inserido")
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if(db.is_connected()):
            cursor.close()
            db.close()
            print("Conexão com MySQL está fechada\n")

insert = 'insert into empresa (cnpj, nomeEmpresa) values \n'
for dados in open('..\Arquivos_back_end\CNPJ.csv', 'r', encoding='UTF-8'):
    info = dados.split(';')
    info[1] = info[1].replace('\n','')
    insert+=f"('{info[0].zfill(14)}','{info[1]}'),\n"
insert = insert[:-2]
insert += ';'
inserirDados(insert)
insert = 'insert into funcionario (nome,cpf,genero,nasc,email,senha,fkEmpresa,fkCargo,autenticacao) values \n'
for dados in open('funcionario.csv', 'r', encoding='UTF-8'):
    info = dados.split(';')
    insert += f"('{info[0]}','{info[1].zfill(11)}','{info[2]}','{info[3]}','{info[4]}','{info[5]}',{int(info[6])},{int(info[7])}, {info[8]}),\n"
insert = insert[:-2]
insert += ';'
inserirDados(insert)
insert = 'insert into tanque (fkFuncionario,cep,cidade,bairro,rua,estado) values \n'
def anonimizar_string(texto):
    texto_separado = texto.split()
    len_texto = len(texto_separado)
    if len_texto <= 2:
        len_metade_palavra = len(texto_separado[-1]) // 2
        texto_separado[-1] = "*" * len_metade_palavra + texto_separado[-1][len_metade_palavra:]
    else:
        i = 0
        for palavra in texto_separado:
            if i != 0 and ((i != len_texto - 1 and len_texto != 2) or len(texto_separado[i-1]) <= 3):
                texto_separado[i] = len(palavra) * "*"
            i += 1
    texto_anonimizado = " ".join(texto_separado)
    return texto_anonimizado
def anonimizar_endereco(cep, cidade, bairro, rua):
    cep_anonimizado = cep[:2] + "*" * (len(cep)-2) + cep[len(cep)-1:]
    cidade_anonimizado = anonimizar_string(cidade)
    bairro_anonimizado = anonimizar_string(bairro)
    rua_anonimizado = anonimizar_string(rua)
    estado_anonimizado = 'XX'
    return cep_anonimizado, cidade_anonimizado, bairro_anonimizado, rua_anonimizado, estado_anonimizado
for dados in open('dados.csv', 'r', encoding='UTF-8'):
    info = dados.split(';')
    cep, cidade, bairro, rua, estado = info[0], info[1], info[2], info[3], info[4]
    cep_anonimizado, cidade_anonimizado, bairro_anonimizado, rua_anonimizado, estado_anonimizado = anonimizar_endereco(cep, cidade, bairro, rua)
    insert += f"({int(info[5])},'{cep_anonimizado.zfill(8)}','{cidade_anonimizado}','{bairro_anonimizado}','{rua_anonimizado}','{estado_anonimizado}'),\n"
insert = insert[:-2]
insert += ';'
inserirDados(insert)