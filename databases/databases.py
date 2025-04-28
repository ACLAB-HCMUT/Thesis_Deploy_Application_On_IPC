from pymongo import MongoClient
import gridfs
import requests
import sys
from Adafruit_IO import MQTTClient
import os
from dotenv import load_dotenv

# Đường dẫn tuyệt đối hoặc tương đối đến tệp .env bạn muốn sử dụng
env_path = os.path.join('config', '.env')  # Thay 'config' bằng thư mục chứa .env của bạn nếu cần

# Tải tệp .env từ đường dẫn đã chỉ định
load_dotenv(env_path)

# In ra đường dẫn đang được load
print(f"Loading environment variables from: {env_path}")

# Tải các biến môi trường từ tệp .env


#MongoDB
mongodb_uri = os.getenv("MONGO_URI")

client = MongoClient(mongodb_uri)

db = client["db_da_nganh"]

fs = gridfs.GridFS(db)

collection_sensor = db["sensors"]
collection_user = db["users"]
collection_relay = db["relay"]
collection_setup_temperature = db["setup_temperature"]
collection_setup_pir = db["setup_pir"]
collection_setup_light = db["setup_light"]
collection_notification = db["notification"]
collection_setup_scheduler = db["scheduler"]
collection_setup_threshold = db["threshold"]


