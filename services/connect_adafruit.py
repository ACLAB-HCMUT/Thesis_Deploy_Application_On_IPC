
import matplotlib.pyplot as plt
from constant import *
from Adafruit_IO import MQTTClient
import sys
from connect_to_rs485_sensor import *
from constant import *

AIO_FEED_ID = ["nutnhan1", "nutnhan2"]
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

# def message(client , feed_id , payload):
#     print("Nhan du lieu: " + payload + ", feedID: " + feed_id)
#     if feed_id == "nutnhan1":
#         if payload == "0":
#             writeData("1")
#         else:
#             writeData("2")
    
#     if feed_id == "nutnhan2":
#         if payload == "0":
#             writeData("3")
#         else:
#             writeData("4")


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
# client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter = 10



while True:
    counter = counter - 1
    if counter <= 0:
        counter = 10
        #ToDo
        modbus_send_req(client)

    #Not use long time wait, but only use time delay 1s
    time.sleep(1)
    pass
