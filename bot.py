import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
from datetime import datetime

BOT_TOKEN = "7472767533:AAFDewMWR-lN1BMEPffa0AwjAvffUMUXHyg"
ADMIN_ID = "1799744741"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

USER_DB = "users.json"
MESSAGE_DB = "messages.json"

MENU = [
    [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
    [KeyboardButton("🏩 酒店预订"), KeyboardButton("🥗 食堂频道"), KeyboardButton("🛒 生活用品")],
    [KeyboardButton("🔔 后勤生活信息频道")]
]

RESPONSE_DATA = {
    # ... (your existing RESPONSE_DATA)
}

def load_users():
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

async def start(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)  # Convert to string for JSON storage
    current_month = datetime.now().strftime("%Y-%m")  # Get current month (YYYY-MM)

    users = load_users()

    # If user is new or hasn't interacted this month, update the database
    if user_id not in users or users[user_id] != current_month:
        users[user_id] = current_month  # Update last active month
        save_users(users)

    # Count unique users active in the current month
    active_users = sum(1 for month in users.values() if month == current_month)

    menu_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    welcome_message = f"📌 Please select an option:\n\n📊 Monthly Active Users: {active_users}"
    await update.message.reply_text(welcome_message, reply_markup=menu_markup)

# ... (rest of your existing functions)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("update_broadcast", update_broadcast))
    application.add_handler(CommandHandler("delete_broadcast", delete_broadcast))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.run_polling()

if __name__ == "__main__":
    main()
