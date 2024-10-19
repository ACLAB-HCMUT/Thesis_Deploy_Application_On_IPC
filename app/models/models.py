from app.databases.databases import db

# Collection cụ thể từ MongoDB
if db is None:
    raise Exception("Database connection failed!")

collection_name = db["test"]

print(collection_name)
