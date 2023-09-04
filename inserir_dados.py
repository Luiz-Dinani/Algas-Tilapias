import mysql.connector

def conectarBancoDeDados():
    db = mysql.connector.connect(
        host="database-1.cucfdybb1rps.us-east-1.rds.amazonaws.com",
        user="tilapiasUser",
        password="tilapiasSenha"
    )

    return db

def criarBanco():
    db = conectarBancoDeDados()
    cursor = db.cursor()
    cursor.execute("create database if not exists samaka")

def criarTabelas():
    db = conectarBancoDeDados()
    cursor = db.cursor()
    cursor.execute("use samaka")
    # criar uma tabela para os dados dos Sensores
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresa(
          idEmpresa INT AUTO_INCREMENT PRIMARY KEY,
          nomeEmpresa varchar(255),
          email varchar(50),
          senha varchar(255),
          cnpj char(14)
        );
        
        CREATE TABLE IF NOT EXISTS funcionario (
          idFuncionario INT AUTO_INCREMENT PRIMARY KEY,
          nome VARCHAR(255),
          cpf VARCHAR(11),
          email VARCHAR(255),
          idade INT(3),
          genero CHAR(1),
          senha varchar(255),
          fkEmpresa INT,
          funcao char(1),
          FOREIGN KEY (fkEmpresa) REFERENCES empresa(idEmpresa)
        );
                
        CREATE TABLE IF NOT EXISTS tanque (
          idTanque INT NOT NULL AUTO_INCREMENT,
          fkFuncionario INT,
          cep char(8),
          cidade varchar(100),
          bairro varchar(100),
          rua varchar(100),
          estado varchar(100),
          PRIMARY KEY (idTanque),
          FOREIGN KEY (fkFuncionario) REFERENCES funcionario (idFuncionario)
        );
                
        CREATE TABLE IF NOT EXISTS monitoracaoCiclo (
          idMonitoracaoCiclo INT AUTO_INCREMENT PRIMARY KEY,
          idCiclo INT,
          diasRestante INT ,
          amonia DECIMAL(3,2),
          biomassa DECIMAL(5,2),
          dias DATE,
          oxigenio DECIMAL(3,1),
          peso_peixe DECIMAL(7,1),
          ph DECIMAL(3,1),
          qualidade_agua DECIMAL(5,2),
          quantidade_peixe INT,
          salinidade DECIMAL(5,2),
          temperatura DECIMAL(5,2),
          turbidez DECIMAL(5,2),
          visibilidade DECIMAL(5,2),
          fkTanque INT,
          FOREIGN KEY (fkTanque) REFERENCES tanque (idTanque)
          );
    """)

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

criarBanco()
criarTabelas()

insert = 'insert into empresa (cnpj, nomeEmpresa, email, senha) values \n'
for dados in open('empresa.csv', 'r', encoding='UTF-8'):
    info = dados.split(';')
    insert+=f"('{info[0].zfill(14)}','{info[1]}','{info[2]}','{info[3]}'),\n"
insert = insert[:-2]
insert += ';'
inserirDados(insert)
insert = 'insert into funcionario (nome,cpf,email,idade,genero,senha,fkEmpresa,funcao) values \n'
for dados in open('funcionario.csv', 'r', encoding='UTF-8'):
    info = dados.split(';')
    insert+=f"('{info[0]}','{info[1].zfill(11)}','{info[4]}',{info[3]},'{info[2]}','{info[5]}',{int(info[7])},'{info[6]}'),\n"
insert = insert[:-2]
insert += ';'
inserirDados(insert)
insert = 'insert into tanque (fkFuncionario,cep,cidade,bairro,rua,estado) values \n'
for dados in open('dados.csv', 'r', encoding='UTF-8'):
    info = dados.split(';')
    insert+=f"({int(info[5])},'{info[0].zfill(8)}','{info[1]}','{info[2]}','{info[3]}','{info[4]}'),\n"
insert = insert[:-2]
insert += ';'
inserirDados(insert)