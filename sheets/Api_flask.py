from flask import Flask
import mysql.connector
import hashlib
from Google_sheets import gerarPlanilha as gp
import pandas as pd

def conectarBancoDeDados():
    db = mysql.connector.connect(
        host="database-1.cucfdybb1rps.us-east-1.rds.amazonaws.com",
        user="tilapiasUser",
        password="tilapiasSenha"
    )
    cursor = db.cursor()
    cursor.execute("use samaka")
    return db
def coletaDados(select):
    try:
        mydb = conectarBancoDeDados()
        if mydb.is_connected():
            return pd.read_sql(select, mydb)
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if(mydb.is_connected()):
            mydb.close()
def hash_password(password):
  hash_object = hashlib.sha256()
  hash_object.update(password.encode("utf-8"))
  return hash_object.hexdigest()
app = Flask(__name__)
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" 
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response
@app.route("/<email>/<senha>")
def funcao(email, senha):
    senha=hash_password(senha)
    resultado = coletaDados(f"select *, (select nomeEmpresa from empresa where email='{email}' and senha='{senha}') as empresa from monitoracaoCiclo where fkTanque in (select idTanque from tanque where fkFuncionario in (select idFuncionario from funcionario where fkEmpresa=(select idEmpresa from empresa where email='{email}' and senha='{senha}'))) order by fkTanque asc;")
    if len(resultado)>0:
        gp(resultado.empresa[0],'A',resultado.drop(columns=['empresa', 'idMonitoracaoCiclo']))
        return 'Planilha feita com sucesso'
    else:
        return 'Erro de login'
    # if resultado[0][0]>0:
    #     return "A"
    # else:
    #     resultado = coletaDados(f"select count(*), funcao from funcionario where email = '{email}' and senha = '{senha}';")
    #     if resultado[0][0]>0:
    #         return resultado[0][1]
    #     else:
    #         return 'erro'
        
#
# funcao('atacado_peixe@atacado.com','atacado_peixe')