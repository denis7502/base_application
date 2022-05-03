from paho.mqtt import client as mqtt_client
import time
import random

class Client():
    def __init__(self, broker, port, topic, q = None) -> None:
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = f'python-mqtt-{6}'
        self.q = q
        self.flag = None
        self.connect_mqtt()
    
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"Connected to MQTT Broker! {self.topic}")
            else:
                print("Failed to connect, return code %d\n", rc)
        # Set Connecting Client ID
        self.client = mqtt_client.Client(self.client_id)
        #client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)

    def publish(self, client, msg):
        msg_count = 0
        while True:
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = client.publish(self.topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}")
            msg_count += 1

    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            msg = int(msg.payload.decode())
            if msg == 1:
                self.flag = 1
            else:
                self.flag = 0

        self.client.subscribe(self.topic)
        self.client.on_message = on_message


    def run_subscribe(self):
        self.client.loop_start()
        self.subscribe(self.client)
