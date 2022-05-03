from paho.mqtt import client as mqtt_client
import time
import random

class Client():
    def __init__(self, broker, port, topic, q = None) -> None:
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = f'python-mqtt-{1}'
        self.q = q
        self.msg = None
    
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

    def publish(self, client, msg):
        pass

    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            self.msg = msg.payload.decode()



        client.subscribe(self.topic)
        client.on_message = on_message


    def run_subscribe(self):
        self.client = self.connect_mqtt()
        self.client.loop_start()
        self.subscribe(self.client)
