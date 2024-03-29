import mysql.connector
import pandas as pd
from features.login.models.RequestLoginModel import RequestLoginModel
from features.login.models.ResponseLoginModel import ResponseLoginModel
def conectarBancoDeDados():
    db = mysql.connector.connect(
        host="database-1.cucfdybb1rps.us-east-1.rds.amazonaws.com",
        user="tilapiasUser",
        password="tilapiasSenha"
    )
    if db.is_connected():
        return db
    return None

def criarCursor(db):
    cursor = db.cursor()
    cursor.execute("use samaka")
    return cursor

def login(login: RequestLoginModel):
    try:
        db = conectarBancoDeDados()
        with db:
            cursor = criarCursor(db)
            cursor.execute(f'Select idFuncionario, autenticacao from funcionario where email = "{login.email}" and senha = "{login.senha}"')
            resultado = cursor.fetchone()

        if resultado is None:
            return None
        idFuncionario, validacao = resultado[0], resultado[1]
        validacao = True if validacao == 1 else False
        retorno = ResponseLoginModel(idFuncionario, validacao)
        return retorno
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)

def coleta_dados_monitoramento_tanque_funcionario(id_funcionario):
    try:
        db = conectarBancoDeDados()
        criarCursor(db)
        with db:
            select = f"""select mon.*, fun.fkCargo from monitoracaoCiclo mon 
            join tanque tan on mon.fkTanque = tan.idTanque join funcionario fun 
            on tan.fkFuncionario=fun.idFuncionario where fun.idFuncionario = {id_funcionario}; 
                     """
            return pd.read_sql(select, db)
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)

def obterEmailByIdFuncionario(idFuncionario):
    db = conectarBancoDeDados()
    with db:
        cursor = criarCursor(db)
        cursor.execute(f"select email from funcionario where IdFuncionario = {idFuncionario}")
        resultado = cursor.fetchone()

    if resultado is None:
        return None
    return resultado[0]


def obterNomeEmailByIdFuncionario(idFuncionario):
    db = conectarBancoDeDados()
    with db:
        cursor = criarCursor(db)
        cursor.execute(f"select nome, email from funcionario where IdFuncionario = {idFuncionario}")
        resultado = cursor.fetchone()

    if resultado is None:
        return None
    return resultado[0], resultado[1]


def atualizarAutenticacao(id_funcionario):
    db = conectarBancoDeDados()
    with db:
        cursor = criarCursor(db)
        cursor.execute(f"Update funcionario set autenticacao = 1 where idFuncionario = {id_funcionario}")
        cursor.execute(f"commit;")
        cursor.execute(f"select autenticacao from funcionario where idFuncionario = {id_funcionario}")
        resultado = cursor.fetchone()
    return True if resultado is not None and resultado[0] == 1 else False