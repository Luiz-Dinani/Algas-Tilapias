import mysql.connector
import random    
from datetime import datetime, timedelta
import numpy as np
import tracemalloc as tm
import time
import subprocess as sp
#from geradorTemperatura import geracao_temp

def conectarBancoDeDados():
    # conectar ao banco de dados MySQL
    db = mysql.connector.connect(
        host="localhost",
        #host="3.224.136.146",
        user="tilapiasUser",
        password="998072Lu"
    )
    cursor = db.cursor()
    cursor.execute("create database if not exists tilapiasOtimizado")
    cursor.execute("use tilapiasOtimizado")
    return db

def criarTabelas(db):
    #criar tabela com os ips das maquinas e preencher ela
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ipsMaquinas (
        ipOrigem VARCHAR(20) PRIMARY KEY,
        nome varchar(20) NOT NULL
    )
    """)
    
    try:
        cursor.execute("""
        INSERT INTO ipsMaquinas values ("44.215.14.181", "algas1"),
                                       ("23.22.238.8", "algas2"),
                                       ("187.34.208.124", "notebook Santana"),
                                       ("138.36.58.189", "Taubate");

        """)
    except Exception:
        print("Ips ja inseridos")

    # criar uma tabela para os dados dos Sensores
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dadosSensores (
        id INT AUTO_INCREMENT PRIMARY KEY,
        temperatura FLOAT NOT NULL,
        ph FLOAT NOT NULL,
        amonia FLOAT NOT NULL,
        qualidadeAgua FLOAT NOT NULL,
        biomassa FLOAT NOT NULL,
        qtdPeixes FLOAT NOT NULL,
        pesoMedioPeixes FLOAT NOT NULL,
        dataHora DATETIME NOT NULL,
        ipOrigem varchar(20) NOT NULL,
        FOREIGN KEY(ipOrigem) REFERENCES ipsMaquinas(ipOrigem)
    )
    """)

    # criar uma tabela para os dados de dadosExecucao
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dadosExecucao (
        id INT AUTO_INCREMENT PRIMARY KEY,
        memoria FLOAT NOT NULL,
        numAmostras FLOAT NOT NULL,
        tempo FLOAT NOT NULL,
        ipOrigem VARCHAR(20) NOT NULL,
        FOREIGN KEY(ipOrigem) REFERENCES ipsMaquinas(ipOrigem)
    )
    """)

#region Constantes
AUMENTO_PESO_DIARIO = 0.00545 #kg ((800g - 200g)/110dias) / 1000. --Valor por tilápia
#Mortalidade é calculada por ciclo de engorda, que dura 110 dias.
MORTALIDADE_DIARIA_BAIXA = 1 - (0.005/110) #1 - random.uniform(0.01, 0.05)/90 
MORTALIDADE_DIARIA_MEDIA = 1 - (0.02/110) #1 - random.uniform(0.05, 0.09)/90
MORTALIDADE_DIARIA_ALTA = 1 - (0.05/110) #1 - 0.15/90
MORTALIDADE_DIARIA_ALTISSIMA = 1 - 1/15 #Toda a produção pode morrer em 15 dias
TAMANHO_UTIL_TANQUE =  40 #m³ -- 10 Tanques-Rede com 4 m³
#Valores dos Conceitos de biomassa para uma produção do tipo tanques-rede de até 6m³
CAPACIDADE_SUPORTE_TANQUE = 3000
#endregion

def calcularQualidadeAgua(temperatura, amonia, ph):
    #Ínidice de 1 a 4 onde o ideal é 4, 3 = Crescimento Lento, 2 = Sem repoducao e 1 = Mortalidade Altissima
    #Verifica se o pH está fora do range adequado
    if ph <= 4 or ph >= 11:
        return 1
    elif (ph > 4 and ph <= 5) :
        return 2
    elif (ph > 5  and ph < 6.5) or (ph > 9 and ph <= 10):
        return 3

    #Verifica se a temperatura está fora do range adequado
    if temperatura < 14 or temperatura > 38:
        return 1
    elif (temperatura >= 14 and temperatura < 20):
        return 2
    elif (temperatura >= 20 and temperatura < 25):
        return 3
    
    #Range ideal de pH e temperatura, verificando a concentração de amonia tóxica de acordo com o pH, a temperatura e a quantidade total de amonia
    #Coloquei os ifs das amonias com valores ligeiramente maiores para que, por exemplo uma medição 0.26 não seja tratada como uma de 0.5 ao invés de 0.25
    if amonia <= 0.35: #Seria 0.25
        if(ph <= 8.09) or (ph <= 8.29 and temperatura <= 27.9):
            return 4
        elif(ph <= 8.49) or (ph <= 8.69 and temperatura <= 27.9):
            return 3
    elif amonia <= 0.75: #Seria 0.5
        if ph <= 7.89:
            return 4
        elif(ph <= 8.09) or (ph <= 8.29 and temperatura <= 27.9):
            return 3
    elif amonia <= 1.25: #Seria 1
        if(ph <= 7.59):
            return 4
        elif(ph <= 7.89):
            return 3
    elif amonia <= 2:
        if (ph <= 7.19) or (ph <= 7.39 and temperatura <= 27.9):
            return 4
        elif ph <= 7.59:
            return 3
    elif amonia <= 3.5:
        if (ph <= 6.9):
            return 4
        elif ph <= 7.39:
            return 3
    else:
        if(ph <= 6.79 and temperatura <= 27.9):
            return 4
        elif ph <= 6.9 or (ph <= 7.19 and temperatura <= 27.9):
            return 3
    
    return 1 #Se chegou aqui é pq a amônia não se encaixou em nenhum dos ifs de qualidade alta ou média

def calcularPesoEQtdPeixes(qualidadeAgua, biomassaAtualTanque, pesoMedioPeixes, qtdPeixes):
    if qualidadeAgua == 4 and biomassaAtualTanque < CAPACIDADE_SUPORTE_TANQUE:
        pesoMedioPeixes += AUMENTO_PESO_DIARIO
        qtdPeixes *= MORTALIDADE_DIARIA_BAIXA            
    elif qualidadeAgua == 3 and biomassaAtualTanque < CAPACIDADE_SUPORTE_TANQUE:
        pesoMedioPeixes += AUMENTO_PESO_DIARIO * 0.75
        qtdPeixes *= MORTALIDADE_DIARIA_MEDIA
    elif qualidadeAgua == 2 or (qualidadeAgua > 1 and biomassaAtualTanque >= CAPACIDADE_SUPORTE_TANQUE):
        qtdPeixes *= MORTALIDADE_DIARIA_ALTA
    elif qualidadeAgua == 1:
        qtdPeixes *= MORTALIDADE_DIARIA_ALTISSIMA
    
    return pesoMedioPeixes, qtdPeixes

def calcularAmonia(temperatura, pesoMedioPeixes, qtdPeixes, amonia):
    if temperatura < 20 or temperatura > 25:  
        variacaoAmonia = (((temperatura - 25) * ((pesoMedioPeixes) * 0.1)) * 0.3)/1000 * qtdPeixes if temperatura > 25 else (((temperatura - 23) * ((pesoMedioPeixes) * 0.05)) * 0.3)/1000 * qtdPeixes#((5% de variação de consumo de ração (10% do peso do peixe) para cada grau acima de 25ºC ou abaixo de 23) * 30% da ração virando amonia e sendo expelida nas fezes))/1000 para transformar gramas em mg
        # Não vou usar a variação do pH em função da variação de amônia pq ela na verdade sofre muito mais influencia do pH do que o contrário #variacaoPh = (0.7 * (2/3 * variacaoAmonia))/100 #ΔpH = (0,7 x ΔHCO3-)/Alc e ΔHCO3- = (2/3) x ΔNH3, assumindo que a alcalinidade do ambiente se mantenha no ideal de 100mg/L
        amonia += variacaoAmonia
    
    if amonia > 1.25: #Tirar para mostrar o pior caso. 
       amonia = 0.05 #O neutralizador é capaz de agir no mesmo dia, diminuindo bruscamente a amônia
    
    return amonia

def gerarDados(numAmostras):
    dados = []
    data = datetime.now()
    
    #Inicia as métricas no range ideal
    qtdPeixes = 15_000 #Unidades
    pesoMedioPeixes = 0.200 #kg
    temperatura = random.uniform(25, 32) #ºC
    minPh, maxPh = 5, 10
    #minClorof, maxClorof = 25, 50 #ug/L
    minAmonia, maxAmonia = 0.05, 1 #mg/L
    
    #Geração inicial dos valores - Testar também resultados com essas gerações dentro do for
    #phsGerados = np.random.uniform(minPh, maxPh, 20) #Como o ph não varia muito na vida real, tiro uma média entre 20 gerações
    #ph = np.mean(phsGerados)
    #clorofila =  20 #random.uniform(minClorof, maxClorof)
    amonia = random.uniform(minAmonia, maxAmonia)    

    for i in range(numAmostras):        
        temperatura += random.uniform(-1, 1)
        phsGerados = np.random.uniform(minPh, maxPh, 20) #Como o ph não varia muito na vida real, tiro uma média entre 20 gerações
        ph = np.mean(phsGerados)
        #clorofila =  20 #random.uniform(minClorof, maxClorof)
        
        biomassaAtualTanque = pesoMedioPeixes*qtdPeixes/TAMANHO_UTIL_TANQUE
        
        #Efeito das métricas na qualidade da água
        qualidadeAgua = calcularQualidadeAgua(temperatura, amonia, ph) 
        
        #Efeito da qualidade da água na produção
        pesoMedioPeixes, qtdPeixes = calcularPesoEQtdPeixes(qualidadeAgua, biomassaAtualTanque, pesoMedioPeixes, qtdPeixes)
        
        #Efeito da temperatura na alimentação dos peixes, consequentemente na amônia
        amonia = calcularAmonia(temperatura, pesoMedioPeixes, qtdPeixes, amonia)
        
        qualidadeAgua = 4 if qualidadeAgua > 4 else 1 if qualidadeAgua < 1 else qualidadeAgua
        pesoMedioPeixes = pesoMedioPeixes if pesoMedioPeixes < 800 else pesoMedioPeixes + random.uniform(-5, -15)
        amonia = 0 if amonia < 0 else amonia

        if(i % 111 == 0): #Acabou o ciclo de engorda, os peixes sao removidos, a agua recebe manutencao, fica em repouso e sao colocados novos peixes
            temperatura = random.uniform(27, 30) #ºC
            amonia = 0.00
            qualidadeAgua = 4
            data = data + timedelta(days=6)
            qtdPeixes = 15_000
            pesoMedioPeixes = 0.200

        dados.append((temperatura, ph, amonia, qualidadeAgua, biomassaAtualTanque, qtdPeixes, pesoMedioPeixes, data))
        data = data + timedelta(days=1)
    return dados

def inserirDados(db, dados, ipOrigem):
    for temperatura, ph, amonia, qualidadeAgua, biomassa, qtdPeixes, pesoMedioPeixes, dataHora in dados:
        # inserir dados 
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO dadosSensores (temperatura, ph, amonia, qualidadeAgua, biomassa, qtdPeixes, pesoMedioPeixes, dataHora, ipOrigem) VALUES ({temperatura}, {ph}, {amonia}, {qualidadeAgua}, {biomassa}, {qtdPeixes}, {pesoMedioPeixes}, "{dataHora}", "{ipOrigem}")')
        db.commit()
        print(f"""Temperatura: {temperatura:.1f}°C,
                   pH: {ph:.1f},
                   Amonia: {amonia:.1f},
                   Qualidade da Agua: {qualidadeAgua:.1f},
                   Biomassa: {biomassa:.1f},
                   Quantidade de Peixes: {qtdPeixes:.1f},
                   Peso médio dos peixes: {pesoMedioPeixes:.1f} inseridos no banco de dados""")
        
def inserirDadosExecucao(db, dadosExecucao, ipOrigem):
    # inserir dados execucao
    cursor = db.cursor()
    cursor.execute("INSERT INTO dadosExecucao (memoria, numAmostras, tempo, ipOrigem) VALUES (%s, %s, %s, %s)", (dadosExecucao[0][0], dadosExecucao[1], dadosExecucao[2], ipOrigem))
    db.commit()

def main():
    ipOrigem = sp.check_output(["curl", "http://checkip.amazonaws.com"])
    ipOrigem = ipOrigem.decode().strip()
    tm.start()    
    tempoInicio = time.time()

    db = conectarBancoDeDados()
    criarTabelas(db)
    numAmostras = 720
    dados = gerarDados(numAmostras)        
    inserirDados(db, dados, ipOrigem)

    memoriaUsada = tm.get_traced_memory()
    tm.stop()    
    tempoDecorrido = time.time() - tempoInicio
    dadosExecucao = (memoriaUsada, numAmostras, tempoDecorrido)
    inserirDadosExecucao(db, dadosExecucao, ipOrigem)


main()