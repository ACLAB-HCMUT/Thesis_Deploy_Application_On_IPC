from pymongo import MongoClient

client = None
db = None

def init_db(app):
    try:
        client = MongoClient(
            "mongodb+srv://tutorial:Abc123456789@cluster0.qokz2tg.mongodb.net/NodeJSTutorial2023?retryWrites=true&w=majority",
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        db = client["NodeJSTutorial2023"]
        print("Connected to database:", db.name)
        # app.config['db'] = db
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        raise Exception("Database connection failed!")
