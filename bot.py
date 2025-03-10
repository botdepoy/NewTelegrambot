import json
import logging
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Bot Configuration
BOT_TOKEN = "7472767533:AAFDewMWR-lN1BMEPffa0AwjAvffUMUXHyg"
ADMIN_ID = "1799744741"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"

# Logging Configuration
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Files
USER_DB = "users.json"
MESSAGE_DB = "messages.json"

# Menu Layout
MENU = [
    [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
    [KeyboardButton("🏩 酒店预订"), KeyboardButton("🥗 食堂频道"), KeyboardButton("🛒 生活用品")],
    [KeyboardButton("🔔 后勤生活信息频道")]
]

# Load user data from JSON
def load_users():
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save user data to JSON
def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

# Command: Start (Track users)
async def start(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)  # Convert to string for JSON storage
    current_month = datetime.now().strftime("%Y-%m")  # Get current month (YYYY-MM)

    users = load_users()

    # If user is new or hasn't interacted this month, update the database
    if user_id not in users or users[user_id] != current_month:
        users[user_id] = current_month  # Update last active month
        save_users(users)

    menu_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text("📌 Please select an option:", reply_markup=menu_markup)

# Command: Get Monthly Active Users
async def get_monthly_users(update: Update, context: CallbackContext):
    users = load_users()
    current_month = datetime.now().strftime("%Y-%m")

    # Count users active in the current month
    active_users = sum(1 for month in users.values() if month == current_month)

    await update.message.reply_text(f"📊 Monthly Active Users: {active_users}")

# Command: Handle Menu Buttons
async def handle_menu(update: Update, context: CallbackContext):
    text = update.message.text
    if text in RESPONSE_DATA:
        data = RESPONSE_DATA[text]
        buttons = InlineKeyboardMarkup(data["buttons"])

        # Handle file errors
        try:
            with open(data["photo"], "rb") as photo_file:
                await update.message.reply_photo(photo=photo_file, caption=data["caption"], reply_markup=buttons)
        except FileNotFoundError:
            await update.message.reply_text("❌ Image file not found.")

    else:
        await update.message.reply_text("❌ Invalid option. Please select a valid menu item.")

# Command: Contact Information
async def contact(update: Update, context: CallbackContext):
    contact_link = "https://t.me/LUODISWKF"
    image_path = "images/217798948_117810053917589_7233136944671638590_n.png"
    text_message = "📞 **联系我们:**\n点击下方按钮联系在线客服。"

    buttons = [[InlineKeyboardButton("💬 联系客服", url=contact_link)]]

    # Check if the image exists
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            await update.message.reply_photo(
                photo=image_file,
                caption=text_message,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    else:
        await update.message.reply_text(text=text_message, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))

# Command: Broadcast Message (Admin Only)
async def broadcast(update: Update, context: CallbackContext):
    text_messages = ["📢 **Global Announcement!**"]
    images = ["images/image1.jpg", "images/image2.jpg"]
    buttons = [[InlineKeyboardButton("🔍 View Details", url="https://example.com")],
               [InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=WEB_APP_URL))]]

    users = load_users()
    sent_messages = {}

    for user_id in users:
        sent_messages[user_id] = []
        try:
            # Send multiple text messages
            for text in text_messages:
                message = await context.bot.send_message(user_id, text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))
                sent_messages[user_id].append(message.message_id)

            # Send images
            media_group = [InputMediaPhoto(open(img, "rb"), caption="📷 Check these images!") for img in images]
            photo_messages = await context.bot.send_media_group(user_id, media=media_group)
            sent_messages[user_id].extend([msg.message_id for msg in photo_messages])
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

    with open(MESSAGE_DB, "w") as f:
        json.dump(sent_messages, f)

# Command: Delete Broadcast Messages
async def delete_broadcast(update: Update, context: CallbackContext):
    try:
        with open(MESSAGE_DB, "r") as f:
            sent_messages = json.load(f)
    except FileNotFoundError:
        return

    for user_id, message_ids in sent_messages.items():
        for msg_id in message_ids:
            try:
                await context.bot.delete_message(chat_id=user_id, message_id=msg_id)
            except Exception as e:
                print(f"Failed to delete message for {user_id}: {e}")

    with open(MESSAGE_DB, "w") as f:
        json.dump({}, f)

# Main function to run the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("monthly_users", get_monthly_users))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("delete_broadcast", delete_broadcast))

    # Message handler for menu options
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    application.run_polling()

if __name__ == "__main__":
    main()
