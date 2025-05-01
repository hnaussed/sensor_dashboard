import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
import datetime

class MQTTClient:
    def __init__(self, broker_address, port, username, password, socketio: SocketIO ):
        self.client = mqtt.Client()
        self.broker_address = broker_address
        self.port = port
        self.username = username
        self.password = password
        self.socketio = socketio  # Pass the SocketIO instance to the MQTT client


        # Set up MQTT callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

      

    def on_connect(self, client, userdata, flags, rc):
        # Callback function when the client successfully connects to the broker
        if rc == 0:
            print("Connected to MQTT broker")
            # Subscribe to MQTT topics here

    def on_message(self, client, userdata, msg):
        # Callback function for when a message is received
        # Process incoming MQTT messages here
        
        payload = msg.payload.decode("utf-8")
        topic = msg.topic

        print("Got value"+topic+payload)


        # Emit the received data via WebSocket to the dashboard
        self.socketio.emit('sensor_data', {'topic': topic, 'timestamp':str(datetime.datetime.now()),'payload': payload})

    def connect(self):
        # Connect to the MQTT broker
        self.client.username_pw_set( self.username, self.password)
        self.client.connect(self.broker_address, self.port)

    def subscribe(self, topic):
        # Subscribe to an MQTT topic
        self.client.subscribe(topic)

    def start(self):
        # Start the MQTT client loop (non-blocking)
        self.client.loop_start()

    def stop(self):
        # Stop the MQTT client loop
        self.client.loop_stop()