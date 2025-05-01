from flask import Flask, render_template
from flask_socketio import SocketIO
from mqtt_client import MQTTClient  
import mqtt_config

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app)

# MQTT Broker Details
broker_address = "localhost"
port = 1883
mqtt_topic = "sensors/temperature/bedroom"  # Replace with your MQTT topic
username = mqtt_config.user
password = mqtt_config.password

# Create an MQTT client instance
mqtt_client = MQTTClient(broker_address, port, username, password, socketio )

# Callback function for when the MQTT client successfully connects to the broker
def on_mqtt_connect(client, userdata, flags, rc):
    print("connect")
    if rc == 0:
        print("Connected to MQTT broker")
        mqtt_client.subscribe(mqtt_topic)  # Subscribe to the MQTT topic when connected

# Set the on_connect callback function for the MQTT client
mqtt_client.client.on_connect = on_mqtt_connect

@app.route('/static/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    mqtt_client.connect()
    mqtt_client.start()
    socketio.run(app, debug=True)
