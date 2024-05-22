# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import time
from random import uniform

# !/usr/bin/env python3
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

count = 0

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

FLAG_EXIT = False
TOPIC = "env/test/TEMPERATURE"


def reply():
    # global count
    publish_mqtt('I heard you!')  # count = 0


# The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     if rc==0:
#         client.connected_flag=True #set flag
#         print("connected OK")
#         print("Connected with result code " + str(rc))
#         # Subscribing in on_connect() means that if we lose the connection and
#         # reconnect then subscriptions will be renewed.
#         client.subscribe("env/test/TEMPERATURE")
#     else:
#         print("Bad connection Returned code=",rc)

def on_connect(self, userdata, flags, rc):

    # value of rc determines success or not
    if rc == 0:
        print("on_connect: client connection successful")
        print("Connected with result code " + str(rc))
        client.connected_flag = True
        client.subscribe("env/test/TEMP")
    elif rc == 1:
        print("on_connect: client connection refused - incorrect protocol version")
    elif rc == 2:
        print("on_connect: client connection refused - invalid client identifier")
    elif rc == 3:
        print("on_connect: client connection refused - server unavailable")
    elif rc == 4:
        print("on_connect: client connection refused - bad username or password")
    elif rc == 5:
        print("on_connect: client connection refused - not authorised")
    else:
        print("Bad connection returned code = " + str(rc))
        client.loop_stop()


# The callback for when a message is received from the server.
def on_message(client, userdata, msg):
    print("recieved: " + msg.topic + " " + str(msg.payload))
    words = msg.payload.split()
    if words[0] == 'run':  # If 'run' is the first word of the message
        globals()[words[1]]()  # Run the function named by the second word in the message


def on_log(client, userdata, level, buff):  # mqtt logs function
    print(buff)


def on_disconnect(client, userdata, rc):  # disconnect to mqtt broker function
    print("Client disconnected OK")


def on_publish(client, userdata, mid):  # publish to mqtt broker
    print("In on_pub callback mid=" + str(mid))


def on_subscribe(client, userdata, mid, granted_qos):  # subscribe to mqtt broker
    print("Subscribed", userdata)


def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
    global FLAG_EXIT
    FLAG_EXIT = True


def publish(client):
    msg_count = 0
    while not FLAG_EXIT:
        msg_dict = {'msg': msg_count}
        msg = json.dumps(msg_dict)
        if not client.is_connected():
            logging.error("publish: MQTT client is not connected!")
            time.sleep(1)
            continue
        result = client.publish(TOPIC, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f'Send `{msg}` to topic `{TOPIC}`')
        else:
            print(f'Failed to send message to topic {TOPIC}')
        msg_count += 1
        time.sleep(1)


def publish_mqtt(payload):
    """
    Send an MQTT mesage to javaScript client
    """
    topic = 'uicomm/p-j'
    try:
        # publish.single(topic, payload, hostname='wss://test.mosquitto.org', port=8081, retain=False, qos=0)
        # publish.publish(topic, payload, hostname='test.mosquitto.org', port=8081, retain=False, qos=0)
        publish.publish(topic, payload)
    except Exception as err:
        print
        "Couldn't publish :" + str(err)
        pass


# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# client.on_connect = on_connect
# client.on_message = on_message
# # client.ws_set_options(path="wss://", headers=None)
# # client.connect("test.mosquitto.org",8081,60)
# client.connect("localhost",1883,60)

# Start Loop

# count = 0
# try:
#     topic = 'uicomm/p-j'
#     # client.publish(topic, "message number ", hostname='wss://test.mosquitto.org', port=8081, retain=False, qos=0)
#     # client.publish(topic, "message number ")
#     while True:
#         publish_mqtt("message number " + str(count))
#         topic = 'uicomm/p-j'
#         # client.publish(topic, "message number ", hostname='wss://test.mosquitto.org', port=8081, retain=False, qos=0)
#         # client.publish(topic, "message number ")
#
#         count += 1
#         print(count)
#         time.sleep(2)
# except Exception as err:
#     print('Error: ', err)
# finally:
#     client.loop_stop()
# # GPIO.cleanup() anyone?


# last_count = 0
# while True:
#     time.sleep(1)
#     new_count = count
#     print(f"{new_count - last_count}")
#     last_count = new_count


def Pump_callback(client, userdata, message):
    # print("Received message '" + str(message.payload) + "' on topic '"
    #    + message.topic + "' with QoS " + str(message.qos))
    print(str(message.payload))
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.ws_set_options(path="wss://", headers=None)
client.message_callback_add("env/test/TEMP", Pump_callback)
# client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect('test.mosquitto.org')
client.loop_start()
# client.subscribe("env/test/TEMPERATURE")
client.subscribe("env/test/TEMP", 1)

client.publish(topic="env/test/TEMPERATURE",
               payload='{"RPC": "onbekend", "VAL": "onbekend", "clientid": "onbekende gebruiker"}', qos=1, retain=False)
# client.loop_start()
# client.loop_forever()
client.publish(topic="env/test/TEMPERATURE", payload="Beppie en cokkie", qos=1, retain=False)
client.publish(topic="TestingTopic", payload='beppie en kokkie', qos=1, retain=False)
while True:
    randNumber = uniform(20.0, 21.0)

    client.publish(topic="env/test/TEMPERATURE",
                   payload='{"RPC": "onbekend", "VAL": "onbekend", "clientid": "onbekende gebruiker"}', qos=1,
                   retain=False)
    # client.loop_start()
    # client.loop_forever()
    client.publish("env/test/TEMPERATURE", randNumber)
    client.publish(topic="env/test/TEMPERATURE", payload="Beppie en cokkie", qos=1, retain=False)
    client.publish(topic="TestingTopic", payload='beppie en kokkie', qos=1, retain=False)
    # client.loop()

    print("Just published " + str(randNumber) + " to topic TEMPERATURE")
    time.sleep(2)
