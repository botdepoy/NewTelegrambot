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
    }
}

def load_users():
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

def broadcast_message(context: CallbackContext, text: str, photo: str = None, buttons: list = None):
    users = load_users()
    sent_messages = {}
    for user_id in users:
        try:
            if photo:
                message = context.bot.send_photo(user_id, photo=open(photo, "rb"), caption=text, reply_markup=InlineKeyboardMarkup(buttons) if buttons else None)
            else:
                message = context.bot.send_message(user_id, text, reply_markup=InlineKeyboardMarkup(buttons) if buttons else None)
            sent_messages[user_id] = message.message_id
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")
    with open(MESSAGE_DB, "w") as f:
        json.dump(sent_messages, f)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", lambda update, context: broadcast_message(context, "📢 这是一个全局通知！", "images/announcement.jpg", [[InlineKeyboardButton("🔗 访问链接", url="https://example.com")]])))
    application.add_handler(CommandHandler("update_broadcast", lambda update, context: update_broadcast(context, "📢 这是一个更新后的消息！", None, [[InlineKeyboardButton("🔗 新链接", url="https://example.com/new")]])))
    application.add_handler(CommandHandler("delete_broadcast", delete_broadcast))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.run_polling()

if __name__ == "__main__":
    main()
