# app/model/user_model.py
from pymongo import MongoClient
from utils.constant import MONGODB_URI, DATABASE_NAME, USER_COLLECTION
import bcrypt

class UserModel:
    def __init__(self):
        # Initialize the MongoDB connection
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DATABASE_NAME]
        self.user_collection = self.db[USER_COLLECTION]

    def validate_user(self, username, password):
        """Validate user credentials against MongoDB."""
        user = self.user_collection.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            return True
        return False

    def check_user_exists(self, username):
        """Check if a username already exists in MongoDB."""
        return self.user_collection.find_one({"username": username}) is not None

    def add_user(self, username, password):
        """Add a new user with a hashed password to MongoDB."""
        if not self.check_user_exists(username):
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.user_collection.insert_one({
                "username": username,
                "password": hashed_password
            })
            return True
        return False
