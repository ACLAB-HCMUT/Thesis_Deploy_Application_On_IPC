import time
import serial.tools.list_ports
from constant import *



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
    portName = getPort()

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



# Thực hiện việc điều khiển relay.
# def setDevice(id, state):
#     if state == True:
#         # print(relay_ON[id])
#         ser.write(relay_ON.get(int(id), b''))
#     else:
#         # print(relay_OFF[id])
#         ser.write(relay_OFF.get(int(id), b''))


def setDevice(id, state):
    ser = connect_to_port()
    if state == True:
        # print(relay_ON[id])
        ser.write(relay_ON[1])
    else:
        # print(relay_OFF[id])
        ser.write(relay_OFF[1])


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


state = False
counter = 3

while True:
    counter = counter - 1
    if counter <= 0:
        counter = 3
        #ToDo
        setDevice(2, state)
        print('relay1:', state)
        state = not state
        modbus_send_req()

    #Not use long time wait, but only use time delay 1s
    time.sleep(1)
    pass