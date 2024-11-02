# app/db.py
from pymongo import MongoClient
from utils.constant import MONGODB_URI, DATABASE_NAME, USER_COLLECTION

client = MongoClient(MONGODB_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client[DATABASE_NAME]


try:
    sample_document = db[USER_COLLECTION].find_one()
    if sample_document:
        print("Sample Document Attributes:", sample_document.keys())
    else:
        print("No documents found in the collection.")
except Exception as e:
    print("Error accessing collection:", e)