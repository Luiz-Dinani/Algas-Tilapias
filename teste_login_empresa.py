import mysql.connector as mysql
def conectarBancoDeDados():
    db = mysql.connect(
        host="database-1.cucfdybb1rps.us-east-1.rds.amazonaws.com",
        user="tilapiasUser",
        password="tilapiasSenha"
    )
    if db.is_connected():
        db_Info = db.get_server_info()
        print("Conectado ao MySQL Server versão ", db_Info)
        cursor = db.cursor()
    return cursor