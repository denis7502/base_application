from client import Client
from detection import Detection
from paho.mqtt import client as mqtt_client
import numpy as np
import time
import threading
from get_fromWeb import ParseWeb

class getImage(Client):
    def __init__(self, broker, port, topic, q=None) -> None:
        super().__init__(broker, port, topic, q)
        self.client_id = f'python-mqtt-{5}'
        self.dt = Detection()
        self.frame = np.zeros((480,480,3))
        self.msg = bytearray(self.frame)

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"Connected to MQTT Broker! {self.topic}")
            else:
                print("Failed to connect, return code %d\n", rc)
        # Set Connecting Client ID
        client = mqtt_client.Client(self.client_id)
        #client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def subscribe(self):
        def on_message(client, userdata, msg):
            self.publish()


        self.client.subscribe(self.topic)
        self.client.on_message = on_message

    def publish(self):
        while True:
            fr = img.frame   
            self.frame = self.dt.run(fr)
            byteArr = bytearray(self.frame)
            if self.dt.drink:
                self.client.publish('fromAccess', 1)
            self.client.publish('videoOut', byteArr)
            time.sleep(0.1)
            #self.q.put(byteArr)


    
    def run(self):
        self.client = self.connect_mqtt()
        self.client.loop_start()
        self.publish()

if __name__ == '__main__':
    broker = '192.168.1.192'
    port = 1883
    topic = "video"
    img = ParseWeb()
    stream = getImage(broker, port, topic)
    client = threading.Thread(target=img.getImg)
    client.daemon = True
    client.start()
    #client.join()
    stream.run()
