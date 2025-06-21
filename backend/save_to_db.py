from pymongo import MongoClient
from datetime import datetime

def save_to_db(data):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["resume_data"]  # ✅ your DB name
    collection = db["applications"]  # ✅ your collection name

    data["submitted_at"] = datetime.utcnow()

    result = collection.insert_one(data)
    return result.inserted_id
