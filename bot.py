import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import CommandHandler
import time
from telegram.ext import CallbackQueryHandler


BOT_TOKEN = "7472767533:AAFDewMWR-lN1BMEPffa0AwjAvffUMUXHyg"
ADMIN_ID = "1799744741"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

USER_DB = "users.json"
MESSAGE_DB = "messages.json"

MENU = [
    [KeyboardButton("✈️ 交通服务"), KeyboardButton("📜 证照办理"), KeyboardButton("🌍 翻译与商务对接")],
    [KeyboardButton("🏛️ 企业落地支持"), KeyboardButton("🏨 酒店与租凭"), KeyboardButton("🚀 综合增值服务")],
    [KeyboardButton("👩‍💻 人工客服")]
]

RESPONSE_DATA = {
        "✈️ 交通服务": {
        "photo": "images/接机.jpg",
        "caption": "🚖 交通服务 | Transportation Services 、\n\n"
                    "✨ 提供专业出行方案，助您畅行无忧！ ✨\n"
                    "🚗 机场接送 – 准时接送，轻松出行 🛫\n"
                   " 🚘 专车服务 – 商务用车 / 高端专车 / VIP接待 💼\n"
                   " 🧑‍✈️ 司机租赁 – 经验丰富，安全可靠 🏆\n" 
                  "  ✅ 安全 | 🚀 高效 | 💎 舒适\n\n"
                   " 无论是商务出行还是尊享专车，我们都为您提供最佳方案！ 🌍✨\n",
        "buttons":  [[InlineKeyboardButton("专车服务", callback_data="car_service"), InlineKeyboardButton("✈ 机场接送", callback_data="transportation")],
                    [InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF")]]
        },
         "transportation": {
                "photo": "images/接机.jpg",  # Change to your image path or URL
                "caption": "🚖 交通服务 | Transportation Services\n\n"
                           "✨ 提供专业出行方案，助您畅行无忧！ ✨\n"
                           "🚗 机场接送 – 准时接送，轻松出行 🛫\n"
                           "🚘 专车服务 – 商务用车 / 高端专车 / VIP接待 💼\n"
                           "🧑‍✈️ 司机租赁 – 经验丰富，安全可靠 🏆\n"
                           "✅ 安全 | 🚀 高效 | 💎 舒适\n\n"
                           "无论是商务出行还是尊享专车，我们都为您提供最佳方案！ 🌍✨",
                "buttons": [
                    [InlineKeyboardButton("🚗 专车服务", callback_data="car_service")],
                    [InlineKeyboardButton("✈ 接机频道", callback_data="airport_service")],
                    [InlineKeyboardButton("🔙 返回", callback_data="start")]
                ]
            },
            "car_service": {
                "photo": "images/专车.jpg",
                "caption": "🚗 **专车服务**\n\n"
                           "🔹 高端商务用车 🚘\n"
                           "🔹 VIP接待 🏆\n"
                           "🔹 舒适 & 便捷\n"
                           "💎 尊享您的出行体验！",
                "buttons": [[InlineKeyboardButton("🔙 返回", callback_data="transportation")]]
            }
        
}
# Handle Button Clicks
def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()  # Acknowledge the button press
    send_response(query.message, query.data)

# Function to Send or Update Response
def send_response(message, key):
    if key in RESPONSE_DATA:
        data = RESPONSE_DATA[key]
        keyboard = InlineKeyboardMarkup(data["buttons"])
        
        # Check if editing an existing message or sending a new one
        if message.photo:
            message.edit_media(
                media=InputMediaPhoto(data["photo"], caption=data["caption"]),
                reply_markup=keyboard
            )
        else:
            message.reply_photo(photo=data["photo"], caption=data["caption"], reply_markup=keyboard)
def load_users():
    try:
        with open(USER_DB, "r") as f:
            users = json.load(f)
            # Ensure the loaded data is a dictionary
            if isinstance(users, dict):
                return users
            else:
                return {}  # Return an empty dictionary if the file is corrupted
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return an empty dictionary if the file doesn't exist or is invalid

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)


async def start(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)  # Convert to string for consistency
    users = load_users()
    
    # Add the user if they don't exist, or update their last interaction time
    users[user_id] = {"last_interaction": time.time()}
    
    save_users(users)
    menu_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text("📌 Please select an option:", reply_markup=menu_markup)

async def handle_menu(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    users = load_users()
    if str(user_id) in users:
        users[str(user_id)]["last_interaction"] = time.time()
    else:
        users[str(user_id)] = {"last_interaction": time.time()}
    save_users(users)
    
    text = update.message.text
    if text in RESPONSE_DATA:
        data = RESPONSE_DATA[text]
        buttons = InlineKeyboardMarkup(data["buttons"])
        await update.message.reply_photo(photo=open(data["photo"], "rb"), caption=data["caption"], reply_markup=buttons)
    else:
        await update.message.reply_text("❌ Invalid option. Please select a valid menu item.")


def get_active_users(users, active_threshold=3600):  # active_threshold in seconds (e.g., 1 hour)
    current_time = time.time()
    active_users = [user_id for user_id, user_data in users.items() if current_time - user_data["last_interaction"] <= active_threshold]
    return active_users

async def active_users(update: Update, context: CallbackContext):
    users = load_users()
    active_users = get_active_users(users)
    await update.message.reply_text(f"Active users: {len(active_users)}")

async def contact(update: Update, context: CallbackContext):
    """Handles the /contact command and sends an image with a clickable Telegram link."""
    
    contact_link = "https://t.me/LUODISWKF"  # Replace with your actual Telegram contact link
    image_path = "images/217798948_117810053917589_7233136944671638590_n.png"  # Replace with your actual image path
    text_message = "📞 **联系我们:**\n点击下方按钮联系在线客服。"

    # Create button
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
        # If the image is missing, send text only
        await update.message.reply_text(
            text=text_message, 
            parse_mode="Markdown", 
            reply_markup=InlineKeyboardMarkup(buttons)
        )


async def broadcast(update: Update, context: CallbackContext):
    text_messages = [
        "📢 **Global Announcement!**",
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
    # Ensure the USER_DB file exists and is initialized
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f:
            json.dump({}, f)  # Initialize with an empty dictionary

    # Ensure the MESSAGE_DB file exists and is initialized
    if not os.path.exists(MESSAGE_DB):
        with open(MESSAGE_DB, "w") as f:
            json.dump({}, f)  # Initialize with an empty dictionary

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("update_broadcast", update_broadcast))
    application.add_handler(CommandHandler("delete_broadcast", delete_broadcast))
    application.add_handler(CommandHandler("active_users", active_users))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.run_polling()

if __name__ == "__main__":
    main()
