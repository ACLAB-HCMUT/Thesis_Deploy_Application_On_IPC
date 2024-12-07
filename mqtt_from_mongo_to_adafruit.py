import sys
import json
import time
from pymongo import MongoClient
from Adafruit_IO import MQTTClient

# Tải biến môi trường (có thể bỏ qua nếu không sử dụng .env)
# load_dotenv()

# Kết nối với MongoDB Atlas
mongodb_uri = "mongodb+srv://db_iot_user:qwer1234@cluster0.zlnpp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongodb_uri)

# Truy cập vào database và collection
db = client["db_iot"]
collection_relay = db["relay"]  # Relay collection

# Thông tin Adafruit
AIO_USERNAME = "Vinhnguyen20"
AIO_KEY = "aio_nOYm19Z21drHgorHsKjsOqH0QlcW"

# Cấu hình MQTT
def connected(client):
    print("Ket noi thanh cong ...")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter = 1


def main():
    with collection_relay.watch() as stream:
        print("Đang theo dõi sự thay đổi trong collection relay...")
        for change in stream:
            if change["operationType"] == "update":
                updated_relay = collection_relay.find_one({"_id": change["documentKey"]["_id"]})
                print(updated_relay['relayName'] + " " + updated_relay['status'])
                client.publish (updated_relay['relayName'], 1 if updated_relay['status'] == 'ON' else 0)

if __name__ == "__main__":
    main()
