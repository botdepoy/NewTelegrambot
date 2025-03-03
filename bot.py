import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
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
    "✈ 落地接机": {
        "photo": "images/接机.jpg",
        "caption": "🛬 Welcome! \n🌟 欢迎加入【后勤接机】群 🌟\n\n✅ 请核对信息，如有更改，请联系客服！",
        "buttons": [[InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=WEB_APP_URL)), InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), InlineKeyboardButton("✈ 接机频道", url="https://t.me/+pqM959ERihBkYTc9")]]
    },
    "🔖 证照办理": {
        "photo": "images/passport.jpg",
        "caption": "📋 证照办理服务：\n\n✔️ 提供快速办理签证、护照及其他相关证件的服务。\n📞 点击客服咨询更多详情。",
        "buttons": [[InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=WEB_APP_URL)), InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), InlineKeyboardButton("🔖 证件办理频道", url="https://t.me/+sINSVji28vM4ZDJl")]]
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


async def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)
    menu_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text("📌 Please select an option:", reply_markup=menu_markup)

async def handle_menu(update: Update, context: CallbackContext):
    text = update.message.text
    if text in RESPONSE_DATA:
        data = RESPONSE_DATA[text]
        buttons = InlineKeyboardMarkup(data["buttons"])
        await update.message.reply_photo(photo=open(data["photo"], "rb"), caption=data["caption"], reply_markup=buttons)
    else:
        await update.message.reply_text("❌ Invalid option. Please select a valid menu item.")

async def broadcast(update: Update, context: CallbackContext):
    text_messages = [
        "📢 **Global Announcement!**",
        "🚀 This is a multi-part message with text, images, and buttons!"
    ]
    images = ["images/image1.jpg", "images/image2.jpg"]  # Add your images here
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

async def update_broadcast(update: Update, context: CallbackContext):
    new_text_messages = [
        "📢 **Updated Announcement!**",
        "✨ This message has been updated!"
    ]
    buttons = [[InlineKeyboardButton("🔍 More Info", url="https://example.com")],
               [InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=WEB_APP_URL))]]

    try:
        with open(MESSAGE_DB, "r") as f:
            sent_messages = json.load(f)
    except FileNotFoundError:
        return

    for user_id, message_ids in sent_messages.items():
        try:
            # Update text messages
            for i, new_text in enumerate(new_text_messages):
                await context.bot.edit_message_text(chat_id=user_id, message_id=message_ids[i], text=new_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))
        except Exception as e:
            print(f"Failed to update message for {user_id}: {e}")

async def delete_broadcast(update: Update, context: CallbackContext):
    try:
        with open(MESSAGE_DB, "r") as f:
            sent_messages = json.load(f)
    except FileNotFoundError:
        return

    for user_id, message_ids in sent_messages.items():
        try:
            for msg_id in message_ids:
                await context.bot.delete_message(chat_id=user_id, message_id=msg_id)
        except Exception as e:
            print(f"Failed to delete message for {user_id}: {e}")

    with open(MESSAGE_DB, "w") as f:
        json.dump({}, f)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("update_broadcast", update_broadcast))
    application.add_handler(CommandHandler("delete_broadcast", delete_broadcast))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.run_polling()

if __name__ == "__main__":
    main()
