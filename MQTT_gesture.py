import paho.mqtt.client as mqtt
import json

# URL = "127.0.0.1" #change to cloud IP
URL = "54.255.221.131"
SENSOR = "GRITS/Sensor"
MOTION = "GRITS/Motion_Data"
GESTURE = "GRITS/Gesture"
USERID = "Daryl"
PASSWORD = "wmk9199"

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe(GESTURE)

def on_message(client, userdata, msg):
	print("Prediction JSON: " + msg.payload)
	result = json.loads(msg.payload)
	print("Prediction: " + result)

client = mqtt.Client()
client.username_pw_set(USERID, PASSWORD) #AUTHENTICATE
client.on_connect = on_connect
client.on_message = on_message

print("Connecting")
client.connect(URL, 1883, 60)
client.loop_forever()