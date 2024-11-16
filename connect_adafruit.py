import matplotlib.pyplot as plt
from constant import *
from Adafruit_IO import MQTTClient
import sys
# from connect_to_rs485_sensor import *
from connect_to_rs485_relay import *
from constant import *

AIO_FEED_ID = ["nutnhan1", "nutnhan2", "nutnhan3", "nutnhan4"]
AIO_USERNAME = AIO_USERNAME_ADAFRUIT
AIO_KEY = AIO_KEY_ADAFRUIT

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + ", feedID: " + feed_id)
    nutnhan = feed_id[-1]
    if payload == "1":
        setDevice(nutnhan, True)
        print("Turn relay", nutnhan, "On")
    else:
        setDevice(nutnhan, False)
        print("Turn relay", nutnhan, "Off")



client = MQTTClient ( AIO_USERNAME , AIO_KEY )
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect ()
client.loop_background ()


while True :
    time.sleep (1)

