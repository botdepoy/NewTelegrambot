import json
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Replace with your bot token and admin ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"  # Replace with your hosted form

# ✅ Enable Logging (For Debugging)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Store Users and Broadcast Messages
USER_DB = "users.json"
MESSAGE_DB = "messages.json"

# ✅ Menu structure (Reply Keyboard)
MENU = [
    [KeyboardButton("📝 Fill Form"), KeyboardButton("✈ Airport Pickup")],
    [KeyboardButton("🏤 Housing Info"), KeyboardButton("🏩 Hotel Booking")],
    [KeyboardButton("🔖 Document Processing"), KeyboardButton("🔔 Logistic Updates")]
]

# ✅ Responses for menu selections
RESPONSE_DATA = {
    "✈ Airport Pickup": {
        "photo": "images/airport.jpg",
        "caption": "🛬 Welcome! Need airport pickup service? Join our channel below:",
        "buttons": [[InlineKeyboardButton("📢 Join Airport Pickup", url="https://t.me/your_channel")]]
    },
    "🏤 Housing Info": {
        "photo": "images/housing.jpg",
        "caption": "🏡 Find the best housing deals. Contact us below:",
        "buttons": [[InlineKeyboardButton("📞 Contact Support", url="https://t.me/your_contact")]]
    },
    "🏩 Hotel Booking": {
        "photo": "images/hotel.jpg",
        "caption": "🏨 Book your hotel at discounted prices.",
        "buttons": [[InlineKeyboardButton("🛏️ Hotel Booking", url="https://t.me/your_channel")]]
    },
    "🔖 Document Processing": {
        "photo": "images/documents.jpg",
        "caption": "📋 Need passport, visa, or work permit assistance?",
        "buttons": [[InlineKeyboardButton("📄 Document Services", url="https://t.me/your_channel")]]
    },
    "🔔 Logistic Updates": {
        "photo": "images/logistics.jpg",
        "caption": "🚚 Stay updated with the latest logistics information.",
        "buttons": [[InlineKeyboardButton("🔔 Subscribe", url="https://t.me/your_channel")]]
    }
}

# ✅ Load and save users
def load_users():
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# ✅ Start Command (Menu & Form Button)
async def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)

    keyboard = [[InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    menu_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)

    await update.message.reply_text("📌 Please select an option:", reply_markup=menu_markup)
    await update.message.reply_text("Click below to open the form inside Telegram:", reply_markup=reply_markup)

# ✅ Handle Menu Selection
async def handle_menu(update: Update, context: CallbackContext):
    text = update.message.text
    if text in RESPONSE_DATA:
        data = RESPONSE_DATA[text]
        buttons = data.get("buttons", [])
        reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
        if "photo" in data:
            await update.message.reply_photo(photo=open(data["photo"], "rb"), caption=data["caption"], reply_markup=reply_markup)
        else:
            await update.message.reply_text(data["caption"], reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"✅ You selected: {text}")

# ✅ Handle Form Data Submission
async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            logger.info(f"🔍 Raw WebApp Data: {form_data_json}")

            form_data = json.loads(form_data_json)
            logger.info(f"✅ Parsed WebApp Data: {form_data}")

            formatted_data = (
                f"📋 *New User Info Received:*\n\n"
                f"🆔 *User ID:* `{form_data.get('user_id', 'N/A')}`\n"
                f"🔹 *First Name:* `{form_data.get('first_name', 'N/A')}`\n"
                f"🔹 *Last Name:* `{form_data.get('last_name', 'N/A')}`\n"
                f"💠 *Username:* `{form_data.get('username', 'N/A')}`\n"
                f"🌍 *Language:* `{form_data.get('language', 'N/A')}`\n"
                f"📞 *Contact:* `{form_data.get('contact', 'N/A')}`\n\n"
                f"📅 *Date:* `{form_data.get('date', 'N/A')}`\n"
                f"📞 *Number:* `{form_data.get('number', 'N/A')}`"
            )

            logger.info(f"📤 Sending message to {ADMIN_ID}...")
            await context.bot.send_message(chat_id=ADMIN_ID, text=formatted_data, parse_mode="MarkdownV2")

            await update.message.reply_text("✅ Your form has been submitted successfully!")

    except Exception as e:
        logger.error(f"❌ Error processing form data: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")

# ✅ Broadcast Message
async def broadcast_message(update: Update, context: CallbackContext):
    text = "📢 This is a global announcement!"
    users = load_users()
    sent_messages = {}

    for user_id in users:
        try:
            message = await context.bot.send_message(user_id, text)
            sent_messages[user_id] = message.message_id
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

    with open(MESSAGE_DB, "w") as f:
        json.dump(sent_messages, f)

# ✅ Update Broadcast Message
async def update_broadcast(update: Update, context: CallbackContext):
    text = "📢 This is an updated message!"
    
    try:
        with open(MESSAGE_DB, "r") as f:
            sent_messages = json.load(f)
    except FileNotFoundError:
        return

    for user_id, message_id in sent_messages.items():
        try:
            await context.bot.edit_message_text(chat_id=user_id, message_id=message_id, text=text)
        except Exception as e:
            print(f"Failed to update message for {user_id}: {e}")

# ✅ Delete Broadcast Message
async def delete_broadcast(update: Update, context: CallbackContext):
    try:
        with open(MESSAGE_DB, "r") as f:
            sent_messages = json.load(f)
    except FileNotFoundError:
        return

    for user_id, message_id in sent_messages.items():
        try:
            await context.bot.delete_message(chat_id=user_id, message_id=message_id)
        except Exception as e:
            print(f"Failed to delete message for {user_id}: {e}")

    with open(MESSAGE_DB, "w") as f:
        json.dump({}, f)

# ✅ Run the Bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast_message))
    application.add_handler(CommandHandler("update_broadcast", update_broadcast))
    application.add_handler(CommandHandler("delete_broadcast", delete_broadcast))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))

    application.run_polling()

if __name__ == "__main__":
    main()
