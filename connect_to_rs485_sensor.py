import serial
import serial.tools.list_ports
import time
from pymongo import MongoClient
import datetime
import sys
from Adafruit_IO import MQTTClient
import time
import random
from connect_to_rs485_sensor import *

# AIO_FEED_ID = ["nutnhan1", "nutnhan2"]
# AIO_USERNAME = "Vinhnguyen20"
# AIO_KEY = "aio_aCdO74zXuAtwKCtrHqd966HOmDvI"

# def connected(client):
#     print("Ket noi thanh cong ...")
#     for topic in AIO_FEED_ID:
#         client.subscribe(topic)

# def subscribe(client , userdata , mid , granted_qos):
#     print("Subscribe thanh cong ...")

# def disconnected(client):
#     print("Ngat ket noi ...")
#     sys.exit (1)

# # def message(client , feed_id , payload):
# #     print("Nhan du lieu: " + payload + ", feedID: " + feed_id)
# #     if feed_id == "nutnhan1":
# #         if payload == "0":
# #             writeData("1")
# #         else:
# #             writeData("2")
    
# #     if feed_id == "nutnhan2":
# #         if payload == "0":
# #             writeData("3")
# #         else:
# #             writeData("4")


# client = MQTTClient(AIO_USERNAME , AIO_KEY)
# client.on_connect = connected
# client.on_disconnect = disconnected
# # client.on_message = message
# client.on_subscribe = subscribe
# client.connect()
# client.loop_background()


# Get port
def get_all_Port():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort


def connect_to_port():
    portName = get_all_Port()

    # Cấu hình cổng serial
    ser = serial.Serial(
        port = portName,  
        baudrate=9600,
        # parity=serial.PARITY_NONE,
        # stopbits=serial.STOPBITS_ONE,
        # bytesize=serial.EIGHTBITS,
        # timeout=1  
    )

    return ser

# Hàm khởi tạo kết nối
def modbus_init():
    if connect_to_port().is_open:
        print("MODBUS_INITIALIZED")
    else:
        print("Failed to initialize MODBUS")


def modbus_send_req():
    buffer_transmit = [0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B]

    ser = connect_to_port()
    
    ser.write(bytearray(buffer_transmit))
    time.sleep(1) 
    

    response_length = ser.in_waiting
    if response_length > 0:
        data_resp = ser.read(response_length)
        print("Raw data received:", data_resp)
        
        if len(data_resp) >= 7:  
            temperature_raw = data_resp[3] << 8 | data_resp[4]  
            humidity_raw = data_resp[5] << 8 | data_resp[6]      
            
            temperature = temperature_raw / 10.0 
            humidity = humidity_raw / 10.0       
            
            print(f"Temperature: {temperature:.2f}°C --- Humidity: {humidity:.2f}%")

            # push data from sensor to feed id
            # client.publish("cambien1", temperature)
            # client.publish("cambien2", humidity)
            
            # Chèn dữ liệu vào database
            # data = {
            #     "temperature": temperature,
            #     "humidity": humidity,
            #     "timestamp": datetime
            # }

            print("Data inserted successfully!")
        else:
            print("Response is too short")
    else:
        print("No response received")


modbus_send_req()