import random
import datetime
import time

def criar_arquivo_sensor():
    try:
        sensor = open("sensor.config", "r").readlines()[0]
    except:
        sensor = "Sensor_cinco"
        open("sensor.config", "w").write("Sensor_cinco")
    return sensor
    

def gerar_dados(dados):
    vetor_alarme = [8, 26, 20, 6]
    vetor_bol=['A', 'A', 'A', 'A']
    sql_insert="insert into dados_aquario (sensor, ph, temperatura, turbidez, oxigenio, data_registro) VALUES "
    tempo_inicial = (time.time())
    now = datetime.datetime(2023,2,random.randint(1,28),0,0,0)
    vetor_ultima_medidas=[(random.randint(0,8)/10)+7, 
                          (random.randint(0,9)/10)+random.randint(0,5)+20, 
                          (random.randint(0,9)/10)+random.randint(0,8)+10, 
                          (random.randint(0,8)/10)+5]
    for j in range(dados):
        sql_insert+=f"('{criar_arquivo_sensor()}',"
        sql_insert+=f"{round(float(vetor_ultima_medidas[0]),2)},"
        sql_insert+=f"{round(float(vetor_ultima_medidas[1]),2)},"
        sql_insert+=f"{round(float(vetor_ultima_medidas[2]),2)},"
        sql_insert+=f"{round(float(vetor_ultima_medidas[3]),2)},"
        sql_insert+=f"'{now}'),"
        vetor_restart = [(random.randint(0,8)/10)+7, 
                         (random.randint(0,9)/10)+random.randint(0,5)+20, 
                         (random.randint(0,9)/10)+random.randint(0,8)+10, 
                         (random.randint(0,8)/10)+5]
        now+=datetime.timedelta(minutes=10)
        for m in range(4):
            if vetor_bol[m]=='A':
                vetor_ultima_medidas[m]+= random.randint(0,10)/100
            elif vetor_bol[m]=='D':
                vetor_ultima_medidas[m]-= random.randint(0,10)/100
        if vetor_bol[2]=='A':
            vetor_ultima_medidas[2]+= random.randint(50, 200)/100
        elif vetor_bol[2]=='D':
            vetor_ultima_medidas[2]-= random.randint(50, 200)/100
        for k in range(4):
            if vetor_ultima_medidas[k] >= vetor_alarme[k]:
                vetor_bol[k]='D'
            elif vetor_ultima_medidas[k] <= vetor_restart[k]:
                vetor_bol[k]='A'
    #conectDB.inserirDados(sql_insert[0:-1]+';')
    tempo_final= (time.time())
    print(f"Finalizado em {round(tempo_final-tempo_inicial,2)} com {dados} dados!")
    #conectDB.inserirDadosExecucao(criar_arquivo_sensor(), dados, round(tempo_final-tempo_inicial,2))
for i in range(5):
    gerar_dados(int(input(f"Quantos dados voce deseja inserir no banco? ({i+1}º cenário)\n").replace("_","")))
