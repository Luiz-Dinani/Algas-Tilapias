import mysql.connector
import pandas as pd
from  features.login.models.RequestLoginModel import RequestLoginModel
from  features.login.models.ResponseLoginModel import ResponseLoginModel
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
        cursor = criarCursor(db)
        resultado = cursor.execute(f"Select idFuncionario, 2FA from funcionario where email = {login.email} and senha = {login.senha}")
        if resultado <= 0:
            resultado = cursor.execute(f"Select idEmpresa, 2FA from empresa where email = {login.email} and senha = {login.senha}")
        db.close()
        retorno = ResponseLoginModel(resultado[0], resultado[1])
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
        mydb = conectarBancoDeDados()
        credenciais = obterCredenciais(idCliente)
        select = f"select *, (select nomeEmpresa from empresa where email={credenciais.email} and senha={credenciais.senha}) as empresa from monitoracaoCiclo where fkTanque in (select idTanque from tanque where fkFuncionario in (select idFuncionario from funcionario where fkEmpresa=(select idEmpresa from empresa where email={credenciais.email} and senha={credenciais.senha}))) order by fkTanque asc"
        return pd.read_sql(select, mydb)
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if(mydb.is_connected()):
            mydb.close()