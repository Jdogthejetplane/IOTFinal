#!/usr/bin/env python3
import json, time, logging
from prometheus_client import Gauge, start_http_server
import paho.mqtt.client as mqtt

BROKER_HOST = "10.183.240.83"
BROKER_PORT = 1883
MQTT_TOPIC  = "iot/sensors/env"

g_up   = Gauge("mqtt_up", "1 if connected, else 0")
g_seen = Gauge("sensor_last_msg_unixtime", "Last message time")
g_t    = Gauge("sensor_temp_c", "Temperature C")
g_h    = Gauge("sensor_humidity_percent", "Humidity %")

def on_connect(c,u,f,rc,props=None):
    print(f"[MQTT] Connected rc={rc}")
    g_up.set(1 if rc == 0 else 0)
    if rc == 0:
        c.subscribe(MQTT_TOPIC, qos=1)

def on_disconnect(c,u,rc,props=None):
    print(f"[MQTT] Disconnected rc={rc}")
    g_up.set(0)

def on_message(c,u,msg):
    try:
        d = json.loads(msg.payload.decode())

        # Your payload uses these keys:
        # "ds18b20_temp_c" and "humidity_percent"
        if "ds18b20_temp_c" in d and d["ds18b20_temp_c"] is not None:
            g_t.set(float(d["ds18b20_temp_c"]))

        if "humidity_percent" in d and d["humidity_percent"] is not None:
            g_h.set(float(d["humidity_percent"]))

        g_seen.set(time.time())
    except Exception as e:
        print("Bad payload:", e)



if __name__ == "__main__":
    print("[HTTP] Metrics on :9641/metrics")
    start_http_server(9641)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="mqtt")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.enable_logger(logging.getLogger("paho"))

    print(f"[MQTT] Connecting to {BROKER_HOST}:{BROKER_PORT} ...")
    client.connect_async(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()

    # Keep the process alive
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        client.loop_stop()
