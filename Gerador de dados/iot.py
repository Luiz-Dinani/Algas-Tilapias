import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
endpoint = "a3t4xzcgwjbhgf-ats.iot.us-east-1.amazonaws.com"
client_id = "samaka_thing"
path_certificate = "4ba5ee22179b79f0c31f15b7687b4f19112f1609b8ac89a6730795fecf85ee4f-certificate.pem.crt"
path_privatekey = "4ba5ee22179b79f0c31f15b7687b4f19112f1609b8ac89a6730795fecf85ee4f-private.pem.key"
path_rootca1 = "AmazonRootCA1.pem"
my_awsmqtt_client = AWSIoTPyMQTT.AWSIoTMQTTClient(client_id)
my_awsmqtt_client.configureEndpoint(endpoint, 8883)
my_awsmqtt_client.configureCredentials(path_rootca1, path_privatekey, path_certificate)
my_awsmqtt_client.connect()
topic = "monitoramento/peixes"
def awsmqtt(msg, i):
    print("Enviando a mensagem: "+str(i))
    my_awsmqtt_client.publish(topic, msg, 1)
    
def desligar():
    my_awsmqtt_client.disconnect()