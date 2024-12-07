import time
import serial.tools.list_ports
from constant import *
import threading
from constant import *
from Adafruit_IO import MQTTClient
import sys
from constant import *

AIO_FEED_ID = ["nutnhan1", "nutnhan2", "nutnhan3", "nutnhan4"]
AIO_USERNAME = ADAFRUIT_AIO_USERNAME
AIO_KEY = ADAFRUIT_AIO_KEY


# Lock để đồng bộ truy cập cổng COM
ser = None
serial_lock = threading.Lock()


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


# Kiểm tra tất cả port được kết nối
def getPort():
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

# Lấy port có kết nối đến với cổng com của bản thân
def connect_to_port():
    global ser
    portName = getPort()

    if ser is None or not ser.is_open:  # Chỉ mở nếu chưa kết nối
        ser = serial.Serial(
            port=portName,
            baudrate=9600,
            timeout=1
        )
    return ser

def setDevice(id, state):
    global ser
    with serial_lock:  # Đảm bảo chỉ có 1 luồng truy cập cổng COM tại một thời điểm
        if state:
            ser.write(relay_ON[int(id)])
        else:
            ser.write(relay_OFF[int(id)])

def modbus_send_req():
    global ser
    buffer_transmit = [0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B]

    with serial_lock:
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
                client.publish("cambien1", temperature)
                client.publish("cambien2", humidity)
            else:
                print("Response is too short")
        else:
            print("No response received")

# Publisher Thread
def publisher_thread():
    counter = 5
    while True:
        counter = counter - 1
        if counter <= 0:
            counter = 5
            modbus_send_req()
        time.sleep(1)  # Interval between Modbus requests

# Subscriber Thread
def subscriber_thread():
    client.loop_background()

# MQTT Client Initialization
client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()

# Main
if __name__ == "__main__":
    connect_to_port()  # Khởi tạo cổng COM

    pub_thread = threading.Thread(target=publisher_thread, daemon=True)
    sub_thread = threading.Thread(target=subscriber_thread, daemon=True)

    pub_thread.start()
    sub_thread.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Đang thoát...")
            if ser and ser.is_open:
                ser.close()
            break