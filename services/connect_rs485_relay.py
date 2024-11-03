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
portName = getPort()
print(portName)


# Kiểm tra và thực hiện kết nối đến với cổng com đó với baudrate 9600 nghĩa là với tốc độ 9600 bit/s
if portName != "None":
    #serial dùng để giao tiếp với các thiết bị
    ser = serial.Serial(port=portName, baudrate=9600)
    print("Port opened successfully")
else:
    print("Cannot open port")



# Thực hiện việc điều khiển relay.
def setDevice(id, state):
    if state == True:
        # print(relay_ON[id])
        ser.write(relay_ON[id])
    else:
        # print(relay_OFF[id])
        ser.write(relay_OFF[id])