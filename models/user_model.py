class UserModel:
    def __init__(self):
        # Example user data (this could be replaced with a database)
        self.users = {
            "admin": "1234",  # username: password
        }

    def login(self, username, password):
        # Validate login credentials
        if username in self.users and self.users[username] == password:
            return True
        return False

    def register(self, username, password):
        # Register a new user
        if username in self.users:
            return False  # User already exists
        self.users[username] = password
        return True
