import datetime
import time
from client import Client
from paho.mqtt import client as mqtt_client
import threading

class OuterClient(Client):
    def __init__(self, broker, port, topic, q=None) -> None:
        super().__init__(broker, port, topic, q)
        self.client_id = f'python-mqtt-{6}'
        self.access = False
        self.connect_mqtt()

    def publish(self, msg):
        result = self.client.publish(self.topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")
    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            msg = int(msg.payload.decode())
            if msg == 1:
                self.access = True

        self.client.subscribe('fromAccess')
        self.client.on_message = on_message

if __name__ == '__main__':
    broker = '192.168.1.192'
    port = 1883
    topic = "getAccess"
    outClient = OuterClient(broker, port, topic)
    sub = threading.Thread(target=outClient.run_subscribe)
    sub.start()
    outClient.publish(1)
    st = datetime.datetime.now()
    while (datetime.datetime.now()-st).seconds < 10:
        if outClient.access:
            print('Access successful')
            time.sleep(15)
            outClient.publish(0)
            exit()
    print('Access denied')   
    outClient.publish(0) 