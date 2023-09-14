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

#TODO Remover a função de Obter Credenciais e fazer o select com join funcionar: SELECT * from monitoracaoCiclo where fkTanque in (select idTanque from tanque where fkFuncionario in (select idFuncionario from funcionario where fkEmpresa = l_idEmpresa)) order by fkTanque;
def obterCredenciais(idCliente):
    try:
        db = conectarBancoDeDados()
        cursor = criarCursor(db)
        resultado = cursor.execute(f"select email, senha from funcionario where idFuncionario = {idCliente}")
        credenciais = RequestLoginModel(resultado[0], resultado[1])
        return credenciais
    except mysql.connector.Error as e:
        raise e

def coletaDados(idCliente):
    try:
        db = conectarBancoDeDados()
        with db:
            credenciais = obterCredenciais(idCliente)
            select = f"select *, (select nomeEmpresa from empresa where email={credenciais.email} and senha={credenciais.senha}) as empresa from monitoracaoCiclo where fkTanque in (select idTanque from tanque where fkFuncionario in (select idFuncionario from funcionario where fkEmpresa=(select idEmpresa from empresa where email={credenciais.email} and senha={credenciais.senha}))) order by fkTanque asc"
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