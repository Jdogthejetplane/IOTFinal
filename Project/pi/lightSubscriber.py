#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

BROKER_HOST = "10.183.240.78"  
BROKER_PORT = 1883
CMD_TOPIC   = "iot/cmd/light"
LIGHT_PIN   = 22  

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.output(LIGHT_PIN, GPIO.LOW)  # start OFF

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with rc =", rc)
    if rc == 0:
        client.subscribe(CMD_TOPIC, qos=1)
        print(f"Subscribed to {CMD_TOPIC}")
    else:
        print("MQTT connection failed")

def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip().upper()
    print(f"Got command on {msg.topic}: {payload!r}")

    if payload == "ON":
        GPIO.output(LIGHT_PIN, GPIO.HIGH)
        print("Light ON")
    elif payload == "OFF":
        GPIO.output(LIGHT_PIN, GPIO.LOW)
        print("Light OFF")
    else:
        print("Unknown command:", payload)

client = mqtt.Client(client_id="pi-light-controller")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT, 60)
client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
    GPIO.cleanup()
