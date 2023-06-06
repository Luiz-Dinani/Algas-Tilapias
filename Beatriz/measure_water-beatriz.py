#IMPORTS
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime
import time 
import sys


#  CONEXÃO COM O BANCO
connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "vit221bRomans8.0",
            database = "testeMemoTable"
    )

cursor1 = connection.cursor()


try:
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("select database();")
        db = cursor.fetchone()
        print("Você está conectado ao banco de dados: ", db)

    # FUNÇÃO DE MEDIÇÕES

    def water_measure(connection, cursor): 
        listTemp = []  
        listph = []
        listAmmonia = []

        ammonia_size_list = []
        ph_size_list = []
        temp_size_list = []

        # INSERÇÃO NO BANCO

        cursor.execute("DROP TABLE IF EXISTS tbWaterData")   
        cursor.execute("CREATE TABLE tbWaterData (idExecution INT PRIMARY KEY AUTO_INCREMENT, temperature INT, ph FLOAT, ammonia FLOAT, weekDay VARCHAR(10), month VARCHAR(10), day INT, time VARCHAR(8), year INT)") 

        rangeNum = 5000

        for i in range(rangeNum):
            start_capture = time.time()


            temperature = random.randint(24, 32)
            listTemp.append(temperature)
            print("temperature:", temperature)

            tempMemoSize = sys.getsizeof(listTemp)
            temp_size_list.append(tempMemoSize)


            ph  = random.uniform(6, 8)
            listph.append(ph)
            print("ph:", ph) 

            phMemoSize = sys.getsizeof(listph)
            ph_size_list.append(phMemoSize)


            ammonia = random.uniform(0, 4)
            listAmmonia.append(ammonia)
            print("ammonia:", ammonia)

            ammoniaMemoSize = sys.getsizeof(listAmmonia)
            ammonia_size_list.append(ammoniaMemoSize)

            registerWeekDay = datetime.now().strftime('%A') 
            registerMonth = datetime.now().strftime('%B') 
            registerDay = datetime.now().day 
            registerHour = datetime.now().strftime('%H') 
            registerMin = datetime.now().strftime('%M') 
            registerSec = datetime.now().strftime('%S') 
            registerTime =  (f'{registerHour}:{registerMin}:{registerSec}')

            registerYear = datetime.now().year

            memory = ammonia_size_list + ph_size_list + temp_size_list

            insertRange = ("INSERT INTO tbWaterData (temperature, ph, ammonia, weekDay, month, day, time, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            values = (temperature, ph, ammonia, registerWeekDay, registerMonth, registerDay, registerTime, registerYear, )

            cursor.execute(insertRange, values)
            connection.commit()       

            end_capture = time.time()
            totalTime = end_capture - start_capture
            print(f'Resgistered at {registerWeekDay} {registerMonth} {registerDay} {registerTime} {registerYear}')
            print("-------------------")

        print("Total time capturing: ",round(totalTime,4), "-", "total memory size: ",sum(memory), "Bytes")

        # plt.title("Temperature")
        # plt.plot(listTemp, label="Temperature")
        # plt.legend(loc = "upper left")
        # plt.show()

            # plt.title("Ammonia")
            # plt.plot(listAmmonia, label="Ammonia")
            # plt.legend(loc = "upper left")
            # plt.show()
            
            # plt.title("PH")
            # plt.plot(listph, label="PH")
            # plt.legend(loc = "upper left")
            # plt.show()

            # plt.title("Total Ammonia Data Memory")
            # plt.plot(ammonia_size_list, label="Memory")
            # plt.legend(loc = "upper left")
            # plt.show()

            # plt.title("Total PH Data Memory")
            # plt.plot(ph_size_list, label="Memory")
            # plt.legend(loc = "upper left")
            # plt.show()

            # plt.title("Total Temperature Data Memory")
            # plt.plot(temp_size_list, label="Memory")
            # plt.legend(loc = "upper left")
            # plt.show()

            # plt.title("Total Memory")
            # plt.plot(memory, label="Memory")
            # plt.legend(loc = "upper left")
            # plt.show()

    water_measure(connection, cursor1)

except Error as e:
    print("Erro ao conectar ao MySQL", e)

    mycursor = connection.cursor()
    mycursor.execute("SHOW TABLES")

    for x in mycursor:
        print(x)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("A conexão MySQL está fechada")

