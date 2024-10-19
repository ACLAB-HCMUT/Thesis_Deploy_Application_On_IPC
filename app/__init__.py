from flask import Flask
from app.databases.databases import init_db
from app.routes.routes import init_routes

def create_app():
    app = Flask(__name__)

    # Khởi tạo database
    try:
        init_db(app)
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return None  # Nếu kết nối thất bại, trả về None để dừng việc tạo app

    # Khởi tạo routes nếu kết nối database thành công
    init_routes(app)

    return app
