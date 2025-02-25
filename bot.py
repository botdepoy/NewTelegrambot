import json
import time
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Get the Bot Token from environment variable (for security)
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = "https://example.com/form"

# Database Files
USER_DB = "users.json"
USER_ACTIVITY_DB = "user_activity.json"
MESSAGE_DB = "messages.json"

# Menu structure
MENU = [
    [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
    [KeyboardButton("🏩 酒店预订"), KeyboardButton("🥗 食堂频道"), KeyboardButton("🛒 生活用品")],
    [KeyboardButton("🔔 后勤生活信息频道")]
]

# Response data for menu selections
RESPONSE_DATA = {
        "✈ 落地接机": {
        "photo": "images/接机.jpg",
        "caption": "🌟 欢迎加入【后勤接机】群 🌟\n\n✅ 请核对信息，如有更改，请联系客服！",
        "buttons": [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), InlineKeyboardButton("✈ 接机频道", url="https://t.me/+pqM959ERihBkYTc9")]]
    },
    "🔖 证照办理": {
        "photo": "images/passport.jpg",
        "caption": "📋 证照办理服务：\n\n✔️ 提供快速办理签证、护照及其他相关证件的服务。\n📞 点击客服咨询更多详情。",
        "buttons": [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), InlineKeyboardButton("🔖 证件办理频道", url="https://t.me/+sINSVji28vM4ZDJl")]]
    },
    "🏤 房产凭租": {
        "photo": "images/resized-image.jpg",
        "caption": "🏤 房产租赁信息：\n\n✔️ 提供房产出租和购房服务，涵盖各类房型。\n🔍 点击下方按钮了解更多。",
        "buttons": [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), InlineKeyboardButton("🏤 房产信息频道", url="https://t.me/+8i7xQLV_UiY2NTY1")]]
    },
    "🏩 酒店预订": {
        "photo": "images/sofietel.jpg",
        "caption": "🏨高端酒店预订代办服务| 索菲特 & 瑰丽酒店 |🏨\n\n✨ 奢华体验，优惠价格，预订更省心！ ✨\n\n📞 联系我们，轻松享受高端住宿！",
        "buttons": [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), InlineKeyboardButton("🏩 酒店详情频道", url="https://t.me/+M5Q_hf4xyG00YzRl")]]
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

# Load and save user data
def load_users():
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# Start command
async def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)
    reply_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text("📌 请选择一个选项:", reply_markup=reply_markup)

# Handle menu selection
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
        await update.message.reply_text(f"✅ 你选择了: {text}")

# Send a broadcast message
async def broadcast_message(update: Update, context: CallbackContext):
    text = "📢 这是一个全局通知！"
    photo = "images/image.jpg"
    buttons = [[InlineKeyboardButton("🔗 hi", url="https://example.com")]]

    users = load_users()
    sent_messages = {}
    for user_id in users:
        try:
            if photo:
                message = await context.bot.send_photo(user_id, photo=open(photo, "rb"), caption=text, reply_markup=InlineKeyboardMarkup(buttons) if buttons else None)
            else:
                message = await context.bot.send_message(user_id, text, reply_markup=InlineKeyboardMarkup(buttons) if buttons else None)
            sent_messages[user_id] = message.message_id
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")
    with open(MESSAGE_DB, "w") as f:
        json.dump(sent_messages, f)

# Update a broadcast message
async def update_broadcast(update: Update, context: CallbackContext):
    text = "📢 这是一个更新后的消息！"
    photo = "images/noimage.jpg"
    buttons = [[InlineKeyboardButton("🔗 update", url="https://example.com/new")]]

    try:
        with open(MESSAGE_DB, "r") as f:
            sent_messages = json.load(f)
    except FileNotFoundError:
        return

    for user_id, message_id in sent_messages.items():
        try:
            if photo:
                await context.bot.edit_message_media(
                    chat_id=user_id,
                    message_id=message_id,
                    media=InputMediaPhoto(media=open(photo, "rb"), caption=text),
                    reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
                )
            else:
                await context.bot.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=text,
                    reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
                )
        except Exception as e:
            print(f"Failed to update message for {user_id}: {e}")

# Delete a broadcast message
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

# Main function to run the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast_message))
    application.add_handler(CommandHandler("update_broadcast", update_broadcast))
    application.add_handler(CommandHandler("delete_broadcast", delete_broadcast))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    application.run_polling()

if __name__ == "__main__":
    main()
