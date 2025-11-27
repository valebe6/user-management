from datetime import datetime
from bson import ObjectId
from pymongo import ASCENDING
from app.db import get_db

COLLECTION = "users"

def _serialize_user(doc):
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
        "age": doc.get("age"),
        "created_at": doc["created_at"],
        "updated_at": doc.get("updated_at"),
    }

def ensure_indexes():
    db = get_db()
    db[COLLECTION].create_index([("email", ASCENDING)], unique=True)

def create_user(data):
    db = get_db()
    ensure_indexes()
    now = datetime.utcnow()
    user_doc = {
        "name": data["name"],
        "email": data["email"].lower().strip(),
        "age": data.get("age"),
        "created_at": now,
        "updated_at": None,
    }
    res = db[COLLECTION].insert_one(user_doc)
    user_doc["_id"] = res.inserted_id
    return _serialize_user(user_doc)

def list_users(page=1, limit=10):
    db = get_db()
    skip = (page - 1) * limit
    cursor = db[COLLECTION].find().skip(skip).limit(limit).sort("created_at", -1)
    return [_serialize_user(doc) for doc in cursor]

def get_user(user_id):
    db = get_db()
    doc = db[COLLECTION].find_one({"_id": ObjectId(user_id)})
    if not doc:
        return None
    return _serialize_user(doc)

def update_user(user_id, data):
    db = get_db()
    updates = {}
    if "name" in data:
        updates["name"] = data["name"]
    if "email" in data:
        updates["email"] = data["email"].lower().strip()
    if "age" in data:
        updates["age"] = data["age"]

    updates["updated_at"] = datetime.utcnow()

    res = db[COLLECTION].find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": updates},
        return_document=True
    )
    if not res:
        return None
    return _serialize_user(res)

def delete_user(user_id):
    db = get_db()
    res = db[COLLECTION].delete_one({"_id": ObjectId(user_id)})
    return res.deleted_count > 0
