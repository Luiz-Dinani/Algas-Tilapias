import sys
import time
import json
import logging
import datetime
from azure.iot.device import IoTHubDeviceClient, Message
from function import geracao_ph, geracao_vis
import GeradorFinalAWS as gerador

DEVICE_ID = 'sensor'
CONNECTION_STRING = 'HostName=IoT-Tilapias.azure-devices.net;DeviceId=algas-device;SharedAccessKey=wddO98wZ8iQO0sU4i32rVlwVri2pXsyv7bWV+pR1Fjg='

def send_message(client: IoTHubDeviceClient, dados: list):

    dados_mensagem = json.dumps(dados)
    message = Message(dados_mensagem)
    message.content_type = 'application/json'
    message.content_encoding = 'utf-8'

    client.send_message(message)
    logging.info("Mensagem enviada para o IoT Hub")


def gerar_dados(client: IoTHubDeviceClient):
    msg_count = 1
    bateria = 100_00

    while bateria:
        dados = gerador.gerarDados(365)

        payload = {
            'messageId': msg_count,
            'bateria': f'{bateria / 100.0}%',
            'ph': ph,
            'visibilidade': visibilidade,
            'deviceId': DEVICE_ID,
            'data_hora_coleta': f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f}',
        }

        dados.append(payload)
        logging.info(f'Dado gerado: {payload = }')
        msg_count += 1
        

        tamanho_payload = sys.getsizeof(dados)

        logging.info(f'Dados sendo enviados para Iot Hub {tamanho_payload = }')

        send_message(client, dados)

        bateria -= 0.5

        time.sleep(1)


if __name__ == "__main__":
    # Conectar ao IoT Hub
    logging.basicConfig(
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s.%(msecs)03d - %(levelname)s: %(message)s',
        level='DEBUG',
    )

    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    logging.info("Conectado ao IoT Hub")

    # Gerar (1 em 1 minuto) e enviar dados (a cada 5 minutos)
    gerar_dados(client)