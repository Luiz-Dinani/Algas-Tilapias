from flask import Flask
import mysql.connector
import hashlib
from teste_gs import gerarPlanilha as gp

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
            mycursor = mydb.cursor()
            mycursor.execute(select)
            return mycursor.fetchall()
    except mysql.connector.Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if(mydb.is_connected()):
            mycursor.close()
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
    resultado = coletaDados(f"select count(*) from empresa where email = '{email}' and senha = '{hash_password(senha)}';")
    if resultado[0][0]>0:
        return "A"
    else:
        resultado = coletaDados(f"select count(*), funcao from funcionario where email = '{email}' and senha = '{hash_password(senha)}';")
        if resultado[0][0]>0:
            return resultado[0][1]