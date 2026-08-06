import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "فایل خود را ارسال کنید تا لینک دانلود دریافت کنید."
    )


async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message

    if msg.document:
        file = await msg.document.get_file()

        file_name = msg.document.file_name

        path = f"/tmp/{file_name}"

        await file.download_to_drive(path)

        await msg.reply_text("⏳ در حال ساخت لینک...")

        # این بخش بعداً به فضای ذخیره‌سازی وصل می‌شود
        # فعلاً لینک آزمایشی تولید می‌شود

        await msg.reply_text(
            f"✅ فایل دریافت شد:\n{file_name}\n\n"
            "مرحله اتصال فضای ذخیره‌سازی در نسخه بعد اضافه می‌شود."
        )

    else:
        await msg.reply_text("لطفاً یک فایل ارسال کنید.")


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            file_handler
        )
    )

    print("Bot started...")

    app.run_polling()


if __name__ == "__main__":
    main()
