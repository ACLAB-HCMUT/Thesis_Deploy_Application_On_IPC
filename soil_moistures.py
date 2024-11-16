import time
import minimalmodbus
import json
from Adafruit_IO import MQTTClient
import serial

# Thông tin Adafruit IO
ADAFRUIT_IO_USERNAME = ''
ADAFRUIT_IO_KEY = ''

# Thông tin kết nối Modbus RTU
MODBUS_PORT = 'COM7'
MODBUS_BAUDRATE = 9600
RELAY_ADDRESS = 1  # Địa chỉ thiết bị Modbus

# Kết nối Modbus qua cổng COM7 cho cả relay và cảm biến
instrument = minimalmodbus.Instrument(MODBUS_PORT, RELAY_ADDRESS)
instrument.serial.baudrate = MODBUS_BAUDRATE
instrument.serial.timeout = 1  # Thời gian chờ (1 giây)

# Định nghĩa lệnh Modbus cho relay
relay_ON = {
    0: b'\x01\x0F\x00\x00\x00\x08\x01\xFF\xBE\xD5',
    1: b'\x01\x05\x00\x00\xFF\x00\x8C\x3A',
    2: b'\x01\x05\x00\x01\xFF\x00\xDD\xFA',
    3: b'\x01\x05\x00\x02\xFF\x00\x2D\xFA',
    4: b'\x01\x05\x00\x03\xFF\x00\x7C\x3A'
}

relay_OFF = {
    0: b'\x01\x0F\x00\x00\x00\x08\x01\x00\xFE\x95',
    1: b'\x01\x05\x00\x00\x00\x00\xCD\xCA',
    2: b'\x01\x05\x00\x01\x00\x00\x9C\x0A',
    3: b'\x01\x05\x00\x02\x00\x00\x6C\x0A',
    4: b'\x01\x05\x00\x03\x00\x00\x3D\xCA'
}

humidity_command = bytes([0x02, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x39])
temperature_command = bytes([0x02, 0x03, 0x00, 0x01, 0x00, 0x01, 0xD5, 0xF9])

def send_modbus_command(command):
    try:
        instrument.serial.write(command)
        time.sleep(0.1)
    except Exception as e:
        print(f"Lỗi khi gửi lệnh Modbus: {e}")

def handle_command(feed_id, payload):
    try:
        command_data = json.loads(payload)
        for key, command in command_data.items():
            feed_name = ''.join(filter(str.isalpha, key))
            feed_number = int(''.join(filter(str.isdigit, key)))
            if command.lower() == 'on':
                send_modbus_command(relay_ON[feed_number])
                print(f"Bật {feed_name} {feed_number}")
            elif command.lower() == 'off':
                send_modbus_command(relay_OFF[feed_number])
                print(f"Tắt {feed_name} {feed_number}")
            else:
                print(f"Lệnh không hợp lệ: {command}")
    except json.JSONDecodeError:
        print("Lỗi: Payload không phải là JSON hợp lệ")
    except Exception as e:
        print(f"Lỗi khi xử lý lệnh: {e}")

def connected(client):
    print('Đã kết nối tới Adafruit IO! Đăng ký các feed...')
    for feed in ['relay', 'pump', 'area', 'solution', 'schedules']:
        client.subscribe(feed)
        print(f"Đã đăng ký feed: {feed}")

def disconnected(client):
    print('Mất kết nối từ Adafruit IO!')
    exit(1)

def message(client, feed_id, payload):
    print(f"Nhận lệnh từ {feed_id}: {payload}")
    handle_command(feed_id, payload)

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

client.connect()
client.loop_background()

def read_register(command):
    try:
        instrument.serial.write(command)
        time.sleep(0.1)
        response = instrument.serial.read(7)
        return response
    except Exception as e:
        print(f"Lỗi khi đọc Modbus: {e}")
        return None

def parse_response(response):
    if len(response) >= 5 and response[1] == 0x03:
        value = int.from_bytes(response[3:5], byteorder='big')
        return value
    else:
        print("Lỗi: Phản hồi không hợp lệ")
        return None

while True:
    humidity_response = read_register(humidity_command)
    humidity = parse_response(humidity_response)
    if humidity is not None:
        humidity_value = humidity / 10.0
        print(f"Humidity: {humidity_value}% RH")

    temperature_response = read_register(temperature_command)
    temperature = parse_response(temperature_response)
    if temperature is not None:
        temperature_value = temperature / 10.0
        print(f"Temperature: {temperature_value}°C")

    time.sleep(20)  # Đọc cảm biến mỗi 20 giây
