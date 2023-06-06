import random as r
import time
import datetime
# import matplotlib.pyplot as plt
import sys
import numpy as np
import mysql.connector
import tracemalloc as tm
AUMENTO_PESO_DIARIO = 0.00545 #kg ((800g - 200g)/110dias) / 1000. --Valor por tilápia
#Mortalidade é calculada por ciclo de engorda, que dura 110 dias.
MORTALIDADE_DIARIA_BAIXA = 1 - (0.005/110) #1 - random.uniform(0.01, 0.05)/90 
MORTALIDADE_DIARIA_MEDIA = 1 - (0.02/110) #1 - random.uniform(0.05, 0.09)/90
MORTALIDADE_DIARIA_ALTA = 1 - (0.05/110) #1 - 0.15/90
MORTALIDADE_DIARIA_ALTISSIMA = 1 - 1/15 #Toda a produção pode morrer em 15 dias
TAMANHO_UTIL_TANQUE =  40 #m³ -- 10 Tanques-Rede com 4 m³
#Valores dos Conceitos de biomassa para uma produção do tipo tanques-rede de até 6m³
CAPACIDADE_SUPORTE_TANQUE = 3000
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

def gerarDados():
    oxigen = 9.5
    temp = 0
    day = datetime.date.today()
    init_day = datetime.date(day.year - 1, 12, 31)
    cap_temp = []
    cap_oxi = []
    cap_dias = []
    cap_ph=[]
    cap_sal=[]
    cap_turb=[]
    cap_vis=[]
    cap_amonia=[]
    cap_qualid=[]
    cap_biomassa=[]
    cap_quant=[]
    cap_peso=[]
    amonia = 0
    for x in range(1, 6, 1):
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
        cap_temp.append(temp)
        ph_total = []
        for p in range(1, 25):
            ph_total.append(round(r.uniform(6.0, 8.5), 1))
        results = sum(ph_total)
        cap_ph.append(round(results / len(ph_total), 1))
        sal_total = []
        for s in range(1, 25):
            sal_total.append(round(r.uniform(25, 35), 1))
        result = sum(sal_total)
        cap_sal.append(round(result / len(sal_total), 1))
        turb_total = []
        for t in range(1, 25):
            turb_total.append(round(r.uniform(10, 20), 1))
        results = sum(turb_total)
        cap_turb.append(round(results / len(turb_total), 1))
        if len(cap_turb)==1:
            cap_vis.append(geracao_vis(20, 40))
        else:
            if cap_turb[-1]>cap_turb[-2]:
                cap_vis.append(geracao_vis(20, int(round(cap_vis[-1]))))
            elif cap_turb[-1]<cap_turb[-2]:
                cap_vis.append(geracao_vis(int(round(cap_vis[-1]+1)), 40))
            else:
                cap_vis.append(cap_vis[-1])
        qtdPeixes = 15_000 #Unidades
        pesoMedioPeixes = 0.200 #kg
        temperatura = cap_temp[-1] #ºC cap_temp[-1]
        #minClorof, maxClorof = 25, 50 #ug/L
        minAmonia, maxAmonia = 0.05, 1 #mg/L
        if x==1:
            amonia = r.uniform(minAmonia, maxAmonia)
        else:
            amonia = calcularAmonia(temperatura, pesoMedioPeixes, qtdPeixes, amonia)
        biomassaAtualTanque = pesoMedioPeixes*qtdPeixes/TAMANHO_UTIL_TANQUE
        qualidadeAgua = calcularQualidadeAgua(temperatura, amonia, cap_ph[-1]) 
        pesoMedioPeixes, qtdPeixes = calcularPesoEQtdPeixes(qualidadeAgua, biomassaAtualTanque, pesoMedioPeixes, qtdPeixes)
        qualidadeAgua = 4 if qualidadeAgua > 4 else 1 if qualidadeAgua < 1 else qualidadeAgua
        pesoMedioPeixes = pesoMedioPeixes if pesoMedioPeixes < 800 else pesoMedioPeixes + r.uniform(-5, -15)
        amonia = 0 if amonia < 0 else amonia
        if(x % 111 == 0): #Acabou o ciclo de engorda, os peixes sao removidos, a agua recebe manutencao, fica em repouso e sao colocados novos peixes
            amonia = 0.00
            qualidadeAgua = 4
            qtdPeixes = 15_000
            pesoMedioPeixes = 0.200
        cap_amonia.append(amonia)
        cap_biomassa.append(biomassaAtualTanque)
        cap_qualid.append(qualidadeAgua)
        cap_quant.append(int(round(qtdPeixes,0)))
        cap_peso.append(pesoMedioPeixes)
        cap_dias.append(day)
    return [cap_oxi, cap_temp, cap_ph, cap_sal, cap_turb, cap_vis, cap_amonia, cap_peso, cap_biomassa, cap_qualid, cap_quant, cap_dias]

def geracao_vis(inicio, fim):
    for v in range(1, 25):
        vis_total = []
        vis_total.append(round(r.uniform(inicio, fim), 1))
    results = sum(vis_total)
    return round(results / len(vis_total), 1)

tm.start()    
tempoInicio = time.time()
vetorDados = gerarDados()
memoriaUsada = tm.get_traced_memory()
tm.stop()    
tempoDecorrido = time.time() - tempoInicio

teste=[]
for i in range(5):
    dados=[]
    payload = {
        'messageId': i+1,
        'oxi':vetorDados[0][i],
        'temp':vetorDados[1][i],
        'ph':vetorDados[2][i],
        'sal':vetorDados[3][i],
        'turb':vetorDados[4][i],
        'vis':vetorDados[5][i],
        'amonia':vetorDados[6][i],
        'peso':vetorDados[7][i],
        'biomassa':vetorDados[8][i],
        'qualid':vetorDados[9][i],
        'quant':vetorDados[10][i],
        'dias':vetorDados[11][i],
    }
    teste.append(payload)

print(teste)