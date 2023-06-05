import random
import time
import sys
import matplotlib.pyplot as plt

import mysql.connector

db = mysql.connector.connect(
    host=,
    user=,
    password=
)

#Permite a execução de comandos SQL no banco de dados. 
cursor = db.cursor()

sql_create0 = "create database if not exists camaroes"
cursor.execute(sql_create0)

# escolhemos a database
sql_create1 = "USE camaroes"
cursor.execute(sql_create1)

# Vriação de tabelas
sql_create2 = "CREATE TABLE IF NOT EXISTS medicoes (maquina VARCHAR(15),medicoes int primary key auto_increment, str VARCHAR(255), temperatura INT, ph DECIMAL(3,1), sanilidade DECIMAL(3,1))"
cursor.execute(sql_create2)

sql_create3 = "CREATE TABLE IF NOT EXISTS resultados_simulacao (maquina VARCHAR(15),idSimulacao int primary key auto_increment, simulacao VARCHAR(255), medicoes INT, tempo_total FLOAT, memoria_usada INT)"
cursor.execute(sql_create3)

# Função de simulação
def simulacao(str, n:int):
    maquina = "local1"
    temperatura = []
    ph = []
    salinidade = []
    tempo = []
    memoria = []
    medicao = []
    tempo_inicio = time.time()
    for x in range(1, n+1):  
        
        #Sensor usado Sensor PT1000 – Temperatura 
        simulacao_temp = random.randint(26, 30)
        
        #Sensor de Salinidade/Conductivity S300 
        simulacao_salinidade = random.randint(25, 35)

        #Sensor InPro 3250 – PH
        simulacao_ph = round(random.uniform(7.5, 8.5), 1)

        temperatura.append(simulacao_temp)
        salinidade.append(simulacao_salinidade)
        ph.append(simulacao_ph)

        mem_usada = sys.getsizeof(temperatura) + sys.getsizeof(salinidade) + sys.getsizeof(ph)
        memoria.append(mem_usada)

        var = (maquina,str, simulacao_temp, simulacao_ph, simulacao_salinidade)
        sql_insert = "INSERT INTO medicoes (maquina,str, temperatura, ph, sanilidade) VALUES (%s,%s, %s, %s, %s)"

        cursor.execute(sql_insert, var) 

    tempo_fim = time.time()
    tempo_total = tempo_fim - tempo_inicio
    tempo.append(tempo_total)

    var1 = (maquina,str, n, sum(tempo), sum(memoria))
    sql_insert2 = "INSERT INTO resultados_simulacao (maquina,simulacao, medicoes, tempo_total, memoria_usada) VALUES (%s,%s, %s, %s, %s)"
    cursor.execute(sql_insert2, var1)

    medicao.append({'simulação': str, 'medicoes': n, 'temperatura': temperatura, 'salinidade': salinidade, 'ph': ph, 'tempo_total': sum(tempo), 'memoria_usada': sum(memoria)})

    return medicao

medicoes = []

# Execução das simulações
simulacao1 = simulacao("insercao1", 500)
simulacao2 = simulacao("insercao2", 750)

medicoes.append(simulacao1)
medicoes.append(simulacao2)

# Finalização da conexão com o banco de dados
db.commit()
db.close()