from flask import Flask
import paho.mqtt.publish as publish

MQTT_BROKER = "10.183.240.78"
LED_TOPIC = "iot/cmd/light"

app = Flask(__name__)

@app.route("/led/on")
def led_on():
    publish.single(LED_TOPIC, "on", hostname=MQTT_BROKER)
    return "LED turned on"

@app.route("/led/off")
def led_off():
    publish.single(LED_TOPIC, "off", hostname=MQTT_BROKER)
    return "LED turned off"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
