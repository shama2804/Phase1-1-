from pymongo import MongoClient
from datetime import datetime, timezone

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["resume_ranking_db"]
collection = db["form_extractions"]

# Function to save extracted form data
def save_to_db(data: dict):
    data["submitted_at"] = datetime.now(timezone.utc)
    result = collection.insert_one(data)
    print("✅ Saved to DB! ID:", result.inserted_id)
    return str(result.inserted_id)
