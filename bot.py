import json
import time
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Get the Bot Token from environment variable (for security)
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8101143576  # The ID to receive form responses

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

# Response data for menu selections (Updated with Telegram Web App Form)
RESPONSE_DATA = {
    "✈ 落地接机": {
        "photo": "images/接机.jpg",
        "caption": "🌟 欢迎加入【后勤接机】群 🌟\n\n✅ 请核对信息，如有更改，请联系客服！",
        "buttons": [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), 
                     InlineKeyboardButton("✈ 接机频道", url="https://t.me/+pqM959ERihBkYTc9")],
                    [InlineKeyboardButton("📝 填写表单", web_app=WebAppInfo(url="https://botdepoy.github.io/NewTelegrambot/form.html"))]]
    },
    "🔖 证照办理": {
        "photo": "images/passport.jpg",
        "caption": "📋 证照办理服务：\n\n✔️ 提供快速办理签证、护照及其他相关证件的服务。\n📞 点击客服咨询更多详情。",
        "buttons": [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"), 
                     InlineKeyboardButton("🔖 证件办理频道", url="https://t.me/+sINSVji28vM4ZDJl")],
                    [InlineKeyboardButton("📝 填写表单", web_app=WebAppInfo(url="https://botdepoy.github.io/NewTelegrambot/form.html"))]]
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

# Start Command
async def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)
    reply_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text("📌 请选择一个选项:", reply_markup=reply_markup)

# Handle Menu Selection
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

# Handle Form Submission
async def receive_form(update: Update, context: CallbackContext):
    try:
        # ✅ Debugging Log
        print(f"Received WebApp Data: {update}")

        form_data = json.loads(update.effective_message.web_app_data.data)  # ✅ FIXED
        user_info = update.effective_user  # ✅ Ensures correct user data
        user_id = user_info.id  # ✅ Gets user's Telegram ID

        formatted_data = (
            f"📋 **用户填写的表单:**\n\n"
            f"👤 用户名: {user_info.full_name}\n"
            f"🆔 用户ID: {user_info.id}\n"
            f"📌 服务类型: {form_data.get('service_type', 'N/A')}\n"
            f"📆 到期日期: {form_data.get('expiry_date', 'N/A')}\n"
            f"📄 其他信息: {form_data.get('additional_info', 'N/A')}"
        )

        # ✅ Send Data to Admin (8101143576)
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 **New Form Submission:**\n{formatted_data}", parse_mode="Markdown")

        # ✅ Send Data Back to User Who Filled the Form
        await context.bot.send_message(chat_id=user_id, text=f"✅ **Your Form Submission:**\n{formatted_data}", parse_mode="Markdown")

        # ✅ Send Confirmation Message to User
        await update.message.reply_text("✅ 您的表单已提交！请检查您的 Telegram 消息。")

    except Exception as e:
        print(f"Error processing form data: {e}")
        await update.message.reply_text("⚠️ 提交失败，请重试！")



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


# Main Function
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast_message))
    application.add_handler(CommandHandler("update_broadcast", update_broadcast))
    application.add_handler(CommandHandler("delete_broadcast", delete_broadcast))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))  # Handles form submission

    application.run_polling()

if __name__ == "__main__":
    main()
