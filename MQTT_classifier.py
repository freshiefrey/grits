import paho.mqtt.client as mqtt
import numpy as np
import json

from keras.models import load_model
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
import numpy as np

MODEL_NAME = 'lstm_models/lstm_model_100_50_96%'

# URL = "127.0.0.1" #change to cloud IP
URL = "54.255.221.131"
SENSOR = "GRITS/Sensor"
MOTION = "GRITS/Motion_Data"
GESTURE = "GRITS/Gesture"
classes = ["Buddha clap", "Knob", "Pushback", "Swipe"]


session = tf.compat.v1.Session(graph=tf.compat.v1.Graph())

with session.graph.as_default():
	set_session(session)
	model = load_model(MODEL_NAME)


def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Successfully connected to broker.")
		client.subscribe(MOTION)

	else:
		print("Connection failed with code: %d." % rc)

def classify_gesture(data):
	print("Start classifying")
	with session.graph.as_default():
		set_session(session)
		prediction = model.predict(data)
		index = np.argmax(prediction)
	print("Done.")
	return classes[index]

def on_message(client, userdata, msg):
	# Payload is in msg. We convert it back to a np 3D array
	new = json.loads(msg.payload)

	# Recreate the data
	data = np.array(new)
	print(data)
	result = classify_gesture(data)


	print("Sending results: ", result)
	client.publish(GESTURE, json.dumps(result))

def setup(hostname):
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(hostname)
	client.loop_start()
	return client

def main():
	setup(URL)

	while True:
		pass

if __name__ == '__main__':
	main()
