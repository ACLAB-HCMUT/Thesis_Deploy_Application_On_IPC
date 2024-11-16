import serial
import time

# Cấu hình kết nối serial
ser = serial.Serial(
    port='COM3',        
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1
)

def read_register(command):
    ser.write(command)
    time.sleep(0.1)  

    response = ser.read(7)  
    return response

humidity_command = bytes([0x02, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x39])

temperature_command = bytes([0x02, 0x03, 0x00, 0x01, 0x00, 0x01, 0xD5, 0xF9])


def parse_response(response):
    if len(response) >= 5 and response[1] == 0x03: 
        value = int.from_bytes(response[3:5], byteorder='big')
        return value
    else:
        print("Lỗi: Phản hồi không hợp lệ")
        return None

def get_humidity():
    humidity_response = read_register(humidity_command)
    humidity = parse_response(humidity_response)
    if humidity is not None:
        humidity_value = humidity / 10.0  
        print(f"Humidity: {humidity_value}% RH")


def get_temperature():
    temperature_response = read_register(temperature_command)
    temperature = parse_response(temperature_response)
    if temperature is not None:
        temperature_value = temperature / 10.0  
        print(f"Temperature: {temperature_value}°C")


ser.close()
