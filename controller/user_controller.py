# app/controller/user_controller.py
from db import db

class UserController:
    @staticmethod
    def get_user_data(user_id):
        user_data = db["users"].find_one({"_id": user_id})
        return user_data

    @staticmethod
    def add_user(data):
        result = db["users"].insert_one(data)
        return result.inserted_id
