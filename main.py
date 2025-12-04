from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, handle_message
import os
from keep_alive import keep_alive
import asyncio
import nest_asyncio

TOKEN = os.getenv("TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "bot")


async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    commands = [
        ("start", "بدء استخدام البوت والعودة للقائمة الرئيسية")
    ]
    await application.bot.set_my_commands(commands)

    print("ITGenix Academy Bot started successfully!")
    await application.run_polling()


if __name__ == "__main__":
    keep_alive()
    nest_asyncio.apply()
    asyncio.run(main())
