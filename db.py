import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# ***************************************************************
# تم دمج المتغيرات مباشرة هنا بدلاً من الاعتماد على os.getenv
# ***************************************************************
MONGO_URI = "mongodb+srv://ammar:ammarsa2006@zeroxteambot.yoqqrcf.mongodb.net/bot?retryWrites=true&w=majority&appName=ZeroxTeambot"
MONGO_DB_NAME = "bot"

# التأكد من وجود URI قبل الاتصال
if not MONGO_URI:
    # هذا السطر لن يتم تنفيذه الآن بما أننا حددنا القيمة مباشرة
    raise ValueError("MONGO_URI is not set. Database connection failed.")

try:
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    db = mongo_client[MONGO_DB_NAME]
    
    # محاولة الاتصال للتأكد
    # لاحظ أن motor يتصل عند الحاجة، لكن هذا يساعد في اكتشاف الأخطاء مبكراً
    async def check_connection():
        try:
            await db.command('ping')
            print(f"MongoDB connection to database '{MONGO_DB_NAME}' established successfully.")
        except Exception as e:
            print(f"ERROR: Could not connect to MongoDB. Please check your URI and network settings. Details: {e}")

    # يجب استدعاء check_connection بشكل غير متزامن إذا أردت التأكد من الاتصال
    # في هذا السيناريو، سنكتفي بتهيئة العميل ونترك motor يتعامل مع الاتصال في وقت الحاجة.
    
except Exception as e:
    print(f"Error initializing MongoDB client: {e}")
    # يجب التعامل مع هذا الخطأ بشكل أفضل في تطبيق حقيقي
    raise e


users_collection = db["users"]


async def add_user(user_id: int, first_name: str = "", last_name: str = "", username: str = "", language_code: str = ""):
    """يضيف مستخدماً جديداً أو يحدث بيانات مستخدم حالي."""
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
    """يحصل على عدد جميع المستخدمين في قاعدة البيانات."""
    try:
        count = await users_collection.count_documents({})
        return count
    except Exception as e:
        print(f"Database error in get_users_count: {e}")
        return 0


async def get_all_user_ids():
    """جلب جميع معرفات المستخدمين (user_id) لغرض الإشعارات الجماعية."""
    try:
        # Projection to only return the user_id field
        cursor = users_collection.find({}, {"user_id": 1, "_id": 0})
        # استخراج user_id من كل وثيقة
        user_ids = [doc["user_id"] for doc in await cursor.to_list(length=None)]
        return user_ids
    except Exception as e:
        print(f"Database error in get_all_user_ids: {e}")
        return []