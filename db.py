import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "bot")

mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]

users_collection = db["users"]
ratings_collection = db["content_ratings"]


async def add_user(user_id: int, first_name: str = "", last_name: str = "", username: str = "", language_code: str = ""):
    try:
        exists = await users_collection.find_one({"user_id": user_id})
        if not exists:
            user_data = {
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "language_code": language_code,
                "joined_at": datetime.now()
            }
            await users_collection.insert_one(user_data)
            print(f"New user added: {first_name} {last_name} (@{username}) - ID: {user_id}")
            return True
        else:
            await users_collection.update_one(
                {"user_id": user_id},
                {"$set": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "language_code": language_code,
                    "last_seen": datetime.now()
                }}
            )
        return False
    except Exception as e:
        print(f"Database error in add_user: {e}")
        return False


async def get_users_count():
    try:
        count = await users_collection.count_documents({})
        return count
    except Exception as e:
        print(f"Database error in get_users_count: {e}")
        return 0


async def add_content_rating(user_id: int, content_id: str, rating: int, review: str = ""):
    try:
        rating_data = {
            "user_id": user_id,
            "content_id": content_id,
            "rating": rating,
            "review": review,
            "timestamp": datetime.now()
        }
        await ratings_collection.insert_one(rating_data)
        return True
    except Exception as e:
        print(f"Database error in add_content_rating: {e}")
        return False


async def get_content_average_rating(content_id: str):
    try:
        pipeline = [
            {"$match": {"content_id": content_id}},
            {"$group": {
                "_id": "$content_id",
                "average_rating": {"$avg": "$rating"},
                "total_ratings": {"$sum": 1}
            }}
        ]
        result = await ratings_collection.aggregate(pipeline).to_list(1)
        if result:
            return result[0]["average_rating"], result[0]["total_ratings"]
        return 0, 0
    except Exception as e:
        print(f"Database error in get_content_average_rating: {e}")
        return 0, 0
