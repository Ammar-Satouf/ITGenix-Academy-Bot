from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, handle_message
# تم إزالة استيراد os و dotenv
from keep_alive import keep_alive
import asyncio
import nest_asyncio

# المتغيرات الآن مباشرة هنا كما طلبت
TOKEN = "8093884743:AAEGBJSI_YB9eveHH0tHpJL9nhIlAy0RImk"
MONGO_URI = "mongodb+srv://ammar:ammarsa2006@zeroxteambot.yoqqrcf.mongodb.net/bot?retryWrites=true&w=majority&appName=ZeroxTeambot"
MONGO_DB_NAME = "bot"

# لتمرير المتغيرات إلى db.py، يجب تعريفها كمتغيرات بيئة قبل الاستيراد
# أو تعديل db.py لاستقبالها كمعاملات.
# سنستخدم الطريقة الأسهل: تعريفها في os.environ هنا ليتمكن db.py من قراءتها
import os
os.environ["TOKEN"] = TOKEN
os.environ["MONGO_URI"] = MONGO_URI
os.environ["MONGO_DB_NAME"] = MONGO_DB_NAME

# الآن يمكن استيراد db (سيتم تعديله في الخطوة التالية)
# تأكد من أن هذا الملف لا يستدعي db بشكل مباشر
# (هذا الملف لا يستدعي db.py، لكنه يعتمد على أن db.py يجد المتغيرات)

async def main():
    # التحقق من وجود التوكن
    if not TOKEN:
        print("خطأ: لم يتم العثور على توكن البوت.")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    commands = [
        ("start", "بدء استخدام البوت والعودة للقائمة الرئيسية")
    ]
    await application.bot.set_my_commands(commands)

    print("ITGenix Academy Bot started successfully!")
    # قم بتعديل طباعة MONGO_URI لحماية كلمة المرور
    print(f"Connecting to MongoDB URI: {MONGO_URI.split('@')[1]}")
    
    application.run_polling()


if __name__ == "__main__":
    keep_alive()
    nest_asyncio.apply()
    asyncio.run(main())