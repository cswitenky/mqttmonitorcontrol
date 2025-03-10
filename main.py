import json
import os
import threading
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

import topics
import discovery
import monitor

load_dotenv()
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_BROKER_ADDRESS = os.getenv("MQTT_BROKER_ADDRESS", "localhost")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
DISPLAY_POLL_INTERVAL = int(os.getenv("DISPLAY_POLL_INTERVAL", 60))

def publish_current_states(client):
    # Get current monitor brightness and publish it
    current_brightness = monitor.get_monitor_brightness(log=False)
    if current_brightness is not None:
        client.publish(topics.BRIGHTNESS_STATE_TOPIC, str(current_brightness))

    # Get current monitor input state and set effect
    current_input = monitor.get_current_monitor_input(log=False)
    if current_input is not None:
        client.publish(topics.EFFECTS_STATE_TOPIC, current_input)

    # Get current monitor power state and publish it
    current_power = monitor.get_monitor_power_state(log=False)
    if current_power is not None:
        if current_power == "0x01":
            client.publish(topics.BRIGHTNESS_STATE_TOPIC, "ON")
        else:
            client.publish(topics.BRIGHTNESS_STATE_TOPIC, "OFF")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: %d" % rc)
    client.subscribe(topics.BRIGHTNESS_COMMAND_TOPIC)
    client.subscribe(topics.EFFECTS_COMMAND_TOPIC)
    client.publish(topics.MONITOR_CONFIG_TOPIC, json.dumps(
        discovery.LIGHT_DISCOVERY), retain=True)

    publish_current_states(client)


def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print("Message received: %s on topic: %s" % (message, msg.topic))
    if msg.topic == topics.BRIGHTNESS_COMMAND_TOPIC:
        try:
            brightness = int(message)
            if 0 <= brightness <= 100:
                monitor.set_monitor_brightness(brightness)
                client.publish(topics.BRIGHTNESS_STATE_TOPIC, str(brightness))
        except ValueError:
            if message == "OFF":
                monitor.toggle_monitor_power_state(False)
                client.publish(topics.BRIGHTNESS_STATE_TOPIC,
                               "OFF")
            elif message == "ON":
                monitor.toggle_monitor_power_state(True)
                client.publish(topics.BRIGHTNESS_STATE_TOPIC,
                               "ON")
            else:
                print("Invalid brightness value: %s" % message)
    elif msg.topic == topics.EFFECTS_COMMAND_TOPIC:
        # Handle effects command
        effect = message
        if effect in discovery.LIGHT_DISCOVERY["effect_list"]:
            # Apply the effect (you need to implement this function)
            monitor.set_monitor_input(effect)
            client.publish(topics.EFFECTS_STATE_TOPIC, effect)
        else:
            print(f"Invalid effect: {effect}")


def poll_monitor_current_states(client):
    while True:
        publish_current_states(client)
        time.sleep(DISPLAY_POLL_INTERVAL)


def init():
    # Create a new MQTT client instance
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Attach the callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the broker
    try:
        print('Connecting to MQTT broker: %s at port %d' %
              (MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT))
        client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT, 60)
    except Exception as e:
        print("Connection failed: %s" % e)
        exit(1)

    # Start the polling thread
    polling_thread = threading.Thread(
        target=poll_monitor_current_states, args=(client,))
    polling_thread.daemon = True
    polling_thread.start()

    # Start the network loop to handle messages and keep the client alive
    client.loop_forever()


if __name__ == "__main__":
    init()


# subprocess.run(["ddcutil", 'setvcp', '10', '100'])
