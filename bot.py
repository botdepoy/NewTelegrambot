import json
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Replace with your bot token and admin ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html?type=canteen"  # Replace with your hosted form

# ✅ Enable Logging (For Debugging)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Store Users and Broadcast Messages
USER_DB = "users.json"
MESSAGE_DB = "messages.json"

# ✅ Menu structure (Reply Keyboard)
MENU = [
    [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
    [KeyboardButton("🏩 酒店预订"), KeyboardButton("🥗 食堂频道"), KeyboardButton("🛒 生活用品")],
    [KeyboardButton("🔔 后勤生活信息频道")]
]

# ✅ Responses for menu selections
RESPONSE_DATA = {
    "✈ 落地接机": {
        "photo": "images/接机.jpg",
        "caption": "🛬 Welcome! \n"
                    "🌟 欢迎加入【后勤接机】群 🌟\n\n✅ 请核对信息，如有更改，请联系客服！",
        "buttons":  [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), InlineKeyboardButton("✈ 接机频道", url="https://t.me/+pqM959ERihBkYTc9")]]
    },
    "🔖 证照办理": {
        "photo": "images/passport.jpg",
        "caption": "📋 证照办理服务：\n\n✔️ 提供快速办理签证、护照及其他相关证件的服务。\n📞 点击客服咨询更多详情。",
        "buttons":  [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), InlineKeyboardButton("🔖 证件办理频道", url="https://t.me/+sINSVji28vM4ZDJl")]]
    },
    "🏤 房产凭租": {
        "photo": "images/resized-image.jpg",
        "caption": "🏤 房产租赁信息：\n\n✔️ 提供房产出租和购房服务，涵盖各类房型。\n🔍 点击下方按钮了解更多。",
        "buttons":  [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), InlineKeyboardButton("🏤 房产信息频道", url="https://t.me/+8i7xQLV_UiY2NTY1")]]
    },
    "🏩 酒店预订": {
        "photo": "images/sofietel.jpg",
        "caption":  "🏨高端酒店预订代办服务| 索菲特 & 瑰丽酒店 |🏨\n\n✨ 奢华体验，优惠价格，预订更省心！ ✨\n\n📞 联系我们，轻松享受高端住宿！",
        "buttons":  [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), InlineKeyboardButton("🏩 酒店详情频道", url="https://t.me/+M5Q_hf4xyG00YzRl")]]
    },
    "🥗 食堂频道": {
            "photo": "images/食堂.jpg",
            "caption": "🍽️ 食堂频道信息",
            "buttons": [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/DINGCHUANG001"), InlineKeyboardButton("🥗 食堂频道", url="https://t.me/+M0su9kfTZHk2ODU1")]]
    },

    "🛒 生活用品": {
        "photo": "images/生活用品.jpg",
        "caption": "🛍️ 生活用品信息",
        "buttons": [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), InlineKeyboardButton("🛒 详细了解", url="https://t.me/+M5Q_hf4xyG00YzRl")]]
    },
    "🔔 后勤生活信息频道": {
        "photo": "images/logistic.png",
        "caption": "📌 主要提供各种后勤管理和生活服务，确保用户能够方便、高效地获取信息和帮助。",
        "buttons": [[InlineKeyboardButton("🔔 详细了解", url="https://t.me/+QQ56RVTKshQxMDU1")]]
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
    text = "📢 Global Announcement!"
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
