#!/usr/bin/env python3
import time
import json
import paho.mqtt.client as mqtt
import adafruit_dht
import board
import signal
import sys

MQTT_BROKER_IP = "10.183.240.78"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/sensors/env"

dht_sensor = adafruit_dht.DHT11(board.D17)

client = mqtt.Client(client_id="pi-sensor-publisher", callback_api_version=1)
client.connect(MQTT_BROKER_IP, MQTT_PORT, 60)
client.loop_start()

print("Starting MQTT sensor publisher on GPIO17...")

def cleanup(*args):
    print("\nCleaning up GPIO and exiting...")
    try:
        dht_sensor.exit()
    except Exception as e:
        print("Error cleaning up:", e)

    client.loop_stop()
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)
def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_millideg = int(f.read().strip())
        return temp_millideg / 1000.0
    except: 
        return None

    
while True:
    try:
        humidity = dht_sensor.humidity
        dht_temp = dht_sensor.temperature
    except Exception:
        humidity = None
        dht_temp = None
    cpu_temp = get_cpu_temp()
    payload = {
        "timestamp": int(time.time()),
        "temp_c": dht_temp,
        "humidity_percent": humidity,
        "cpu_temp_c":cpu_temp
    }

    print("Published:", payload)
    client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)

    time.sleep(5)
