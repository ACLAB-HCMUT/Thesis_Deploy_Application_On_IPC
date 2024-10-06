from pymongo import MongoClient
import datetime

def connect_database(parameter_collection):
    # Tạo kết nối đến MongoDB
    server = MongoClient("mongodb+srv://tutorial:Abc123456789@cluster0.qokz2tg.mongodb.net/NodeJSTutorial2023?retryWrites=true&w=majority&appName=Cluster0")  # Thay thế địa chỉ nếu bạn kết nối đến MongoDB từ xa

    # Chọn cơ sở dữ liệu
    db = server["NodeJSTutorial2023"]  

    # Chọn collection
    collection = db[parameter_collection]

    # Lấy data trong collection
    data = list(collection.find())

    # Kiểm tra kết nối và in ra danh sách cơ sở dữ liệu hiện có
    return data

print(connect_database("test"))

