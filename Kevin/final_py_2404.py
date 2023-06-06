### ---------------------------------------------------------------------------------------
### Cenário de 1 ano - Ótimo
### ---------------------------------------------------------------------------------------



# Importação das bibliotecas
import random as r
import time
import datetime
# import matplotlib.pyplot as plt
import sys
import numpy as np
import mysql.connector
    
# Conexão com o banco de dados.
connection = mysql.connector.connect(host="localhost",
        user="user",
        passwd="",
        db="monitor")
cursor = connection.cursor()
    
# Criação da tabela que armazenará as capturas das métricas.
sql_drop = f"DROP TABLE IF EXISTS cap1anosemana"
cursor.execute(sql_drop)
sql_create1 = f"CREATE TABLE cap1anosemana (idCaptura INT PRIMARY KEY AUTO_INCREMENT, dia DATE NOT NULL, trimestre INT, temperatura INT, oxigenio DECIMAL(3,1), ph DECIMAL(3,1), visibilidade INT)"
cursor.execute(sql_create1)
    
# Vetor de métricas de monitoramento: medidas de campo.
cap_temp = []
cap_ph = []
cap_oxi = []
cap_vis = []
cap_dias = []
cap_tri = []

# Vetor de métricas de monitoramento: medidas de campo.
cap_mem = []

# Função de geração de pH - média de 24 gerações
def geracao_ph ():
    ph_total = []
    for x in range(1, 169):
        ph_total.append(round(r.uniform(6.0, 8.5), 1))
    results = sum(ph_total)
    return(round(results / len(ph_total), 1))
    
# Função de geração de visibilidade - média de 24 gerações
def geracao_vis ():
    vis_total = []
    for x in range(1, 169):
        vis_total.append(round(r.randint(20, 40), 1))
    results = sum(vis_total)
    return(round(results / len(vis_total), 1))
    
# Função de cálculo do total de memória alocada
def calc_mem ():
    total_size_current = [sys.getsizeof(cap_temp),
            sys.getsizeof(cap_vis),
            sys.getsizeof(cap_ph),
            sys.getsizeof(cap_oxi),
            sys.getsizeof(cap_tri),
            sys.getsizeof(geracao_ph),
            sys.getsizeof(geracao_vis)]
    mem_alloc = sum(total_size_current)
    return mem_alloc
    
# Definição de variáveis iniciais
day = datetime.date.today()
init_day = datetime.date(day.year - 1, 12, 31)
time_init_cap = (time.time())
oxigen = 9.5
temp = 0

# Adicionador de 7 dias
variador = 0

# Geração de dados com alcance definido - 1 ano.
for x in range(1, 53, 1):
        
    # Mudança das datas do cenário 1 - Anual
    day = init_day + datetime.timedelta(days=+variador)
    variador += 7
        
    # Divisor de período - Anual
    y = x % 52
    if (y % 367 == 0):
        y = 1

    # Gerador de temperatura:
    if (y < 13):
        #Temperatura - trimestre 1
        temp = r.randint(24, 31)
        if (temp > 29):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(round(r.uniform((oxigen - 2.5), (oxigen + 0.3)), 1))
        elif (temp > 25 and temp < 30):
            # Gerador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(round(r.uniform((oxigen - 2), (oxigen + 0.5)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
        # Indicador de trimestre
        cap_tri.append(1)
    elif (y > 12 and y < 27):
        #Temperatura - trimestre
        temp = r.randint(19, 27)
        if (temp > 25):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(round(r.uniform((oxigen - 2), (oxigen + 0.5)), 1))
        elif (temp > 21 and temp < 26):
            # Gerador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(round(r.uniform((oxigen - 1.2), (oxigen + 1)), 1))
        # Indicador de trimestre
        cap_tri.append(2)
    elif (y > 26 and y < 40):
        #Temperatura - trimestre 3
        temp = r.randint(17, 26)
        if (temp > 25):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(round(r.uniform((oxigen - 2), (oxigen + 0.5)), 1))
        elif (temp > 21 and temp < 26):
           # Gerador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(round(r.uniform((oxigen - 1.2), (oxigen + 1)), 1))
        # Indicador de trimestre
        cap_tri.append(3)
    else:
        #Temperatura - trimestre 4
        temp = r.randint(21, 29)
        if (temp > 25 and temp < 30):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(round(r.uniform((oxigen - 2.5), (oxigen + 0.5)), 1))
        elif (temp > 21 and temp < 26):
            # erador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(round(r.uniform((oxigen - 1.2), (oxigen + 1)), 1))
        # Indicador de trimestre
        cap_tri.append(4)
        
    # Incrementação dos itens capturados nos vetores correspondentes
    cap_dias.append(day)
    cap_temp.append(temp)
    cap_ph.append(geracao_ph())
    cap_vis.append(geracao_vis())
        
    # Cálculo do total de memória alocada (Listas e Funções) - no momento da captura
    cap_mem.append(calc_mem())
    
# Cálculo do total de memória alocada (Listas e Funções)
mem_alloc = calc_mem()
    
# Inclusão dos dados no banco
for i in range(0, len(cap_dias)):
    var = (cap_dias[i], cap_tri[i], cap_temp[i], cap_oxi[i], cap_ph[i], cap_vis[i])
    sql_insert_increment = f"INSERT INTO cap1anosemana (dia, trimestre, temperatura, oxigenio, ph, visibilidade) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql_insert_increment, var)
    
# Perpetuação das alterações feitas no banco de dados e encerramento da conexão.
connection.commit()  
time_cap_results = time.time() - time_init_cap
    
print(f"Tempo de execução - {round(time_cap_results,5)}s // Total memória alocada - {round(mem_alloc / 1000, 1)}Kb")
    
# print(cap_temp)
# print(cap_vis)
# print(cap_ph)
# print(cap_oxi)
# print(cap_dias)
# print(cap_dias)



# plt.plot(cap_dias, cap_temp)
# plt.title("Temperatura da água captada durante o ano - Por dia", loc='center')
# plt.xlabel("Mês")
# plt.ylabel("Temperatura C°")
# plt.grid(axis='y')
# plt.show()

# plt.plot(cap_tri, cap_temp, 'o')
# plt.title("Temperatura MIN e MAX durante o ano - Por trimestre", loc='center')
# plt.xlabel("Trimestre")
# plt.ylabel("Temperatura C°")
# plt.grid(axis='y')
# plt.xticks([1, 2, 3, 4])
# plt.show()

# plt.plot(cap_ph, label='Ph')
# plt.title("Captura de Ph", loc='center')
# plt.xlabel("Nº Captura")
# plt.ylabel("Ph 0 - 14")
# plt.grid(axis='y')
# plt.show()

# plt.plot(cap_oxi, color='orange', label='Oxigênio')
# plt.title("Captura de Oxigênio diluído", loc='center')
# plt.xlabel("Nº Captura")
# plt.ylabel("Oxigênio mg/L")
# plt.grid(axis='y')
# plt.show()

# plt.hist(cap_vis, label='Visibilidade')
# plt.title("Visibilidade da água", loc='center')
# plt.ylabel("Qtd. Captura")
# plt.xlabel("Visibilidade cm")
# plt.legend()
# plt.show()

# plt.plot(cap_mem, label='Memória')
# plt.title("Memória total alocada durante a execução", loc='center')
# plt.ylabel("Memória alocada Bytes")
# plt.xlabel("Qtd. Captura")
# plt.legend()
# plt.grid(True)
# plt.show()



### ---------------------------------------------------------------------------------------
### Cenário de 1 ano - Normal
### ---------------------------------------------------------------------------------------



# Criação da tabela que armazenará as capturas das métricas.
sql_drop = f"DROP TABLE IF EXISTS cap1anodia"
cursor.execute(sql_drop)
sql_create1 = f"CREATE TABLE cap1anodia (idCaptura INT PRIMARY KEY AUTO_INCREMENT, dia DATE NOT NULL, trimestre INT, temperatura INT, oxigenio DECIMAL(3,1), ph DECIMAL(3,1), visibilidade INT)"
cursor.execute(sql_create1)

# Vetor de métricas de monitoramento: medidas de campo.
cap_temp = []
cap_ph = []
cap_oxi = []
cap_vis = []
cap_dias = []
cap_tri = []

# Vetor de métricas de monitoramento: medidas de campo.
cap_mem = []

# Função de geração de pH - média de 24 gerações
def geracao_ph ():
    ph_total = []
    for x in range(1, 25):
        ph_total.append(round(r.uniform(6.0, 8.5), 1))
    results = sum(ph_total)
    return(round(results / len(ph_total), 1))
    
# Função de geração de visibilidade - média de 24 gerações
def geracao_vis ():
    vis_total = []
    for x in range(1, 25):
        vis_total.append(round(r.randint(20, 40), 1))
    results = sum(vis_total)
    return(round(results / len(vis_total), 1))
    
# Função de cálculo do total de memória alocada
def calc_mem ():
    total_size_current = [sys.getsizeof(cap_temp),
            sys.getsizeof(cap_vis),
            sys.getsizeof(cap_ph),
            sys.getsizeof(cap_oxi),
            sys.getsizeof(cap_tri),
            sys.getsizeof(geracao_ph),
            sys.getsizeof(geracao_vis)]
    mem_alloc = sum(total_size_current)
    return mem_alloc
    
# Definição de variáveis iniciais
day = datetime.date.today()
init_day = datetime.date(day.year - 1, 12, 31)
time_init_cap = (time.time())
oxigen = 9.5
temp = 0
    
# Geração de dados com alcance definido - 1 ano.
# 1 ano - 367
# 1 semestre - 184
# 1 trimestre - 92
# 1 mes - 32
for x in range(1, 367, 1):
        
    # Mudança das datas do cenário 1 - Anual
    day = init_day + datetime.timedelta(days=+x)
        
    # Divisor de período - Anual
    y = x % 367
    if (y % 367 == 0):
        y = 1

    # Gerador de temperatura:
    if (y < 92):
        #Temperatura - trimestre 1
        temp = r.randint(24, 31)
        if (temp > 29):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(round(r.uniform((oxigen - 2.5), (oxigen + 0.3)), 1))
        elif (temp > 25 and temp < 30):
            # Gerador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(round(r.uniform((oxigen - 2), (oxigen + 0.5)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
        # Indicador de trimestre
        cap_tri.append(1)
    elif (y > 91 and y < 183):
        #Temperatura - trimestre
        temp = r.randint(19, 27)
        if (temp > 25):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(round(r.uniform((oxigen - 2), (oxigen + 0.5)), 1))
        elif (temp > 21 and temp < 26):
            # Gerador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(round(r.uniform((oxigen - 1.2), (oxigen + 1)), 1))
        # Indicador de trimestre
        cap_tri.append(2)
    elif (y > 182 and y < 275):
        #Temperatura - trimestre 3
        temp = r.randint(17, 26)
        if (temp > 25):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(round(r.uniform((oxigen - 2), (oxigen + 0.5)), 1))
        elif (temp > 21 and temp < 26):
           # Gerador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(round(r.uniform((oxigen - 1.2), (oxigen + 1)), 1))
        # Indicador de trimestre
        cap_tri.append(3)
    else:
        #Temperatura - trimestre 4
        temp = r.randint(21, 29)
        if (temp > 25 and temp < 30):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(round(r.uniform((oxigen - 2.5), (oxigen + 0.5)), 1))
        elif (temp > 21 and temp < 26):
            # erador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(round(r.uniform((oxigen - 1.2), (oxigen + 1)), 1))
        # Indicador de trimestre
        cap_tri.append(4)
        
    # Incrementação dos itens capturados nos vetores correspondentes
    cap_dias.append(day)
    cap_temp.append(temp)
    cap_ph.append(geracao_ph())
    cap_vis.append(geracao_vis())
        
    # Cálculo do total de memória alocada (Listas e Funções) - no momento da captura
    cap_mem.append(calc_mem())
    
# Cálculo do total de memória alocada (Listas e Funções)
mem_alloc = calc_mem()
    
# Inclusão dos dados no banco
for i in range(0, len(cap_dias)):
    var = (cap_dias[i], cap_tri[i], cap_temp[i], cap_oxi[i], cap_ph[i], cap_vis[i])
    sql_insert_increment = f"INSERT INTO cap1anodia (dia, trimestre, temperatura, oxigenio, ph, visibilidade) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql_insert_increment, var)
    
#Perpetuação das alterações feitas no banco de dados e encerramento da conexão.
connection.commit()
# connection.close()
    
# Cálculo de tempo
time_cap_results = time.time() - time_init_cap
    
print(f"Tempo de execução - {round(time_cap_results,5)}s // Total memória alocada - {round(mem_alloc / 1000, 1)}Kb")
    
# print(cap_temp)
# print(cap_vis)
# print(cap_ph)
# print(cap_oxi)
# print(cap_dias)
# print(cap_dias)



# plt.plot(cap_dias, cap_temp)
# plt.title("Temperatura da água captada durante o ano - Por dia", loc='center')
# plt.xlabel("Mês")
# plt.ylabel("Temperatura C°")
# plt.grid(axis='y')
# plt.show()

# plt.plot(cap_tri, cap_temp, 'o')
# plt.title("Temperatura MIN e MAX durante o ano - Por trimestre", loc='center')
# plt.xlabel("Trimestre")
# plt.ylabel("Temperatura C°")
# plt.grid(axis='y')
# plt.xticks([1, 2, 3, 4])
# plt.show()

# plt.plot(cap_ph, label='Ph')
# plt.title("Captura de Ph", loc='center')
# plt.xlabel("Nº Captura")
# plt.ylabel("Ph 0 - 14")
# plt.grid(axis='y')
# plt.show()

# plt.plot(cap_oxi, color='orange', label='Oxigênio')
# plt.title("Captura de Oxigênio diluído", loc='center')
# plt.xlabel("Nº Captura")
# plt.ylabel("Oxigênio mg/L")
# plt.grid(axis='y')
# plt.show()

# plt.hist(cap_vis, label='Visibilidade')
# plt.title("Visibilidade da água", loc='center')
# plt.ylabel("Qtd. Captura")
# plt.xlabel("Visibilidade cm")
# plt.legend()
# plt.show()

# plt.plot(cap_mem, label='Memória')
# plt.title("Memória total alocada durante a execução", loc='center')
# plt.ylabel("Memória alocada Bytes")
# plt.xlabel("Qtd. Captura")
# plt.legend()
# plt.grid(True)
# plt.show()



### ---------------------------------------------------------------------------------------
### Cenário de 1 ano - Crítico
### ---------------------------------------------------------------------------------------



# Criação da tabela que armazenará as capturas das métricas.
sql_drop = f"DROP TABLE IF EXISTS cap1anohora"
cursor.execute(sql_drop)
sql_create1 = f"CREATE TABLE cap1anohora (idCaptura INT PRIMARY KEY AUTO_INCREMENT, dia_e_hora DATETIME NOT NULL, turno VARCHAR(5), trimestre INT, temperatura INT, oxigenio DECIMAL(3,1), ph DECIMAL(3,1), visibilidade INT)"
cursor.execute(sql_create1)

# Vetor de métricas de monitoramento: medidas de campo.
cap_temp = []
cap_ph = []
cap_oxi = []
cap_vis = []
cap_date = []
cap_tri = []
cap_turno = []

# Vetor de métricas de monitoramento: medidas sistêmicas.
cap_mem = []

# Função de geração de oxigênio com base na temperatura do dia e do trimestre:
def geracao_oxi(tri, temp):
    if (tri == 1):
        if (temp > 29):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(
                round(r.uniform((oxigen - 2.5), (oxigen + 0.3)), 1))
        elif (temp > 25 and temp < 30):
            # Gerador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(
                round(r.uniform((oxigen - 2), (oxigen + 0.5)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(
                round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
    elif (tri == 2):
        if (temp > 25):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(
                round(r.uniform((oxigen - 2), (oxigen + 0.5)), 1))
        elif (temp > 21 and temp < 26):
            # Gerador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(
                round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(
                round(r.uniform((oxigen - 1.2), (oxigen + 1)), 1))
    elif (tri == 3):
        if (temp > 25):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(
                round(r.uniform((oxigen - 2), (oxigen + 0.5)), 1))
        elif (temp > 21 and temp < 26):
           # Gerador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(
                round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(
                round(r.uniform((oxigen - 1.2), (oxigen + 1)), 1))
    else:
        if (temp > 25 and temp < 30):
            # Gerador de oxigênio dissolvido na água - MÁXIMO:
            cap_oxi.append(
                round(r.uniform((oxigen - 2.5), (oxigen + 0.5)), 1))
        elif (temp > 21 and temp < 26):
            # erador de oxigênio dissolvido na água - MÉDIO:
            cap_oxi.append(
                round(r.uniform((oxigen - 1.7), (oxigen + 0.8)), 1))
        else:
            # Gerador de oxigênio dissolvido na água - MÍNIMO:
            cap_oxi.append(
                round(r.uniform((oxigen - 1.2), (oxigen + 1)), 1))

# Funçãode de geração de temperatura com base no período do dia:
def geracao_temp(tri, agora):
    turno = ""
    temp = 0
    if (agora < 12):
        cap_turno.append("MANHA")
        turno = "manha"
        if (tri == 1):
            temp = r.randint(24, 26)
        elif (tri == 2):
            temp = r.randint(19, 21)
        elif (tri == 3):
            temp = r.randint(17, 19)
        else:
            temp = r.randint(21, 23)
    elif (agora > 11 and agora < 19):
        cap_turno.append("TARDE")
        turno = "tarde"
        if (tri == 1):
            temp = r.randint(24, 31)
        elif (tri == 2):
            temp = r.randint(19, 27)
        elif (tri == 3):
            temp = r.randint(17, 26)
        else:
            temp = r.randint(21, 29)
    else:
        cap_turno.append("NOITE")
        turno = "noite"
        if (tri == 1):
            temp = r.randint(24, 28)
        elif (tri == 2):
            temp = r.randint(19, 24)
        elif (tri == 3):
            temp = r.randint(17, 21)
        else:
            temp = r.randint(21, 25)
    cap_temp.append(temp)
    geracao_oxi(turno, temp)
    return turno, temp

# Função de geração de pH - média de 24 gerações
def geracao_ph():
        ph_total = []
        for x in range(1, 25):
            ph_total.append(round(r.uniform(6.0, 8.5), 1))
        results = sum(ph_total)
        return (round(results / len(ph_total), 1))

# Função de geração de visibilidade - média de 24 gerações
def geracao_vis():
        vis_total = []
        for x in range(1, 25):
            vis_total.append(round(r.randint(20, 40), 1))
        results = sum(vis_total)
        return (round(results / len(vis_total), 1))

# Função de cálculo do total de memória alocada
def calc_mem():
    total_size_current = [sys.getsizeof(cap_temp),
                        sys.getsizeof(cap_vis),
                        sys.getsizeof(cap_ph),
                        sys.getsizeof(cap_oxi),
                        sys.getsizeof(cap_date),
                        sys.getsizeof(cap_tri),
                        sys.getsizeof(cap_turno),
                        sys.getsizeof(geracao_oxi),
                        sys.getsizeof(geracao_temp),
                        sys.getsizeof(geracao_ph),
                        sys.getsizeof(geracao_vis)]
    mem_alloc = sum(total_size_current)
    return mem_alloc

# Definição de variáveis iniciais
time_init_cap = (time.time())
day = datetime.date.today()
init_hour = datetime.datetime(day.year - 1, 12, 31, 23, 00)
oxigen = 9.5

# Geração de dados com alcance definido - 1 ano.
# 1 ano - 367
# 1 semestre - 184
# 1 trimestre - 92
# 1 mes - 32
for x in range(1, 8767, 1):

    # Mudança das horas do cenário 1 - Anual
    agora = init_hour + datetime.timedelta(hours=+x)

    # Divisor de período - Anual
    y = x % 8767
    if (y % 8767 == 0):
        y = 1

    # Gerador de oxigênio dissolvido na água:
    if (y < 2192):
        geracao_temp(1, agora.hour)
        cap_tri.append(1)
    elif (y > 2191 and y < 4283):
        geracao_temp(2, agora.hour)
        cap_tri.append(2)
    elif (y > 4282 and y < 6575):
        geracao_temp(3, agora.hour)
        cap_tri.append(3)
    else:
        geracao_temp(4, agora.hour)
        cap_tri.append(4)

    # Incrementação dos itens capturados nos vetores correspondentes
    cap_date.append(agora)
    cap_ph.append(geracao_ph())
    cap_vis.append(geracao_vis())

    # Cálculo do total de memória alocada (Listas e Funções) - no momento da captura
    cap_mem.append(calc_mem())

# Cálculo do total de memória alocada (Listas e Funções)
mem_alloc_total = calc_mem()

# Inclusão dos dados no banco
for i in range(0, len(cap_vis)):
    var = (cap_date[i], cap_turno[i], cap_tri[i], cap_temp[i], cap_oxi[i], cap_ph[i], cap_vis[i])
    sql_insert_increment = f"INSERT INTO cap1anohora (dia_e_hora, turno, trimestre, temperatura, oxigenio, ph, visibilidade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql_insert_increment, var)

# Perpetuação das alterações feitas no banco de dados e encerramento da conexão.
connection.commit()
connection.close()

# Cálculo de tempo
time_cap_results = time.time() - time_init_cap
print(f"Tempo de execução - {round(time_cap_results,5)}s // Total memória alocada - {round(mem_alloc_total / 1000, 1)}Kb")

# print(cap_temp)
# print(cap_vis)
# print(cap_ph)
# print(cap_oxi)
# print(cap_dias)
# print(cap_temp)
# print(cap_turno)
# print(cap_mem)
# print(len(cap_vis))



# plt.plot(cap_date, cap_temp)
# plt.title("Temperatura captada durante o ano - Por dia", loc='center')
# plt.xlabel("Mês")
# plt.ylabel("Temperatura C°")
# plt.grid(axis='y')
# plt.show()

# plt.plot(cap_tri, cap_temp, 'o')
# plt.title("Temperatura MIN e MAX durante o ano - Por trimestre", loc='center')
# plt.xlabel("Trimestre")
# plt.ylabel("Temperatura C°")
# plt.grid(axis='y')
# plt.xticks([1, 2, 3, 4])
# plt.show()

# plt.plot(cap_ph, label='Ph')
# plt.title("Captura de Ph", loc='center')
# plt.xlabel("Nº Captura")
# plt.ylabel("Ph 0 - 14")
# plt.grid(axis='y')
# plt.show()

# plt.plot(cap_oxi, color='orange', label='Oxigênio')
# plt.title("Captura de Oxigênio diluído", loc='center')
# plt.xlabel("Nº Captura")
# plt.ylabel("Oxigênio mg/L")
# plt.grid(axis='y')
# plt.show()

# plt.hist(cap_vis, label='Visibilidade')
# plt.title("Visibilidade da água", loc='center')
# plt.ylabel("Qtd. Captura")
# plt.xlabel("Visibilidade cm")
# plt.legend()
# plt.show()

# plt.plot(cap_mem, label='Memória')
# plt.title("Memória total alocada durante a execução", loc='center')
# plt.ylabel("Memória alocada Bytes")
# plt.xlabel("Qtd. Captura")
# plt.legend()
# plt.grid(True)
# plt.show()