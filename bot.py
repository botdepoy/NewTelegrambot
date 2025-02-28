import json
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Replace with your bot token and admin ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html?type="  # Hosted form URL

# ✅ Enable Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Menu structure (Reply Keyboard)
MENU = [
    [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
    [KeyboardButton("🏩 酒店预订"), KeyboardButton("🥗 食堂频道"), KeyboardButton("🛒 生活用品")],
    [KeyboardButton("🔔 后勤生活信息频道")]
]

# ✅ Responses for menu selections (Corrected Button Syntax)
RESPONSE_DATA = {
    "✈ 落地接机": {
        "photo": "images/接机.jpg",
        "caption": "🛬 Welcome! \n🌟 欢迎加入【后勤接机】群 🌟\n\n✅ 请核对信息，如有更改，请联系客服！",
        "buttons": [
            [InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
             InlineKeyboardButton("✈ 接机频道", url="https://t.me/+pqM959ERihBkYTc9")],
            [InlineKeyboardButton("📝 Fill Form", url=f"{WEB_APP_URL}airport")]
        ]
    },
    "🔖 证照办理": {
        "photo": "images/passport.jpg",
        "caption": "📋 证照办理服务：\n✔️ 提供快速办理签证、护照及其他相关证件的服务。",
        "buttons": [
            [InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
             InlineKeyboardButton("🔖 证件办理频道", url="https://t.me/+sINSVji28vM4ZDJl")],
            [InlineKeyboardButton("📝 Fill Form", url=f"{WEB_APP_URL}visa")]
        ]
    },
    "🏤 房产凭租": {
        "photo": "images/resized-image.jpg",
        "caption": "🏤 房产租赁信息：\n✔️ 提供房产出租和购房服务。",
        "buttons": [
            [InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
             InlineKeyboardButton("🏤 房产信息频道", url="https://t.me/+8i7xQLV_UiY2NTY1")],
            [InlineKeyboardButton("📝 Fill Form", url=f"{WEB_APP_URL}rental")]
        ]
    },
    "🏩 酒店预订": {
        "photo": "images/sofietel.jpg",
        "caption": "🏨 高端酒店预订代办服务 | 索菲特 & 瑰丽酒店 |🏨",
        "buttons": [
            [InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
             InlineKeyboardButton("🏩 酒店详情频道", url="https://t.me/+M5Q_hf4xyG00YzRl")],
            [InlineKeyboardButton("📝 Fill Form", url=f"{WEB_APP_URL}hotel")]
        ]
    },
    "🥗 食堂频道": {
        "photo": "images/食堂.jpg",
        "caption": "🍽️ 食堂频道信息",
        "buttons": [
            [InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/DINGCHUANG001"),
             InlineKeyboardButton("🥗 食堂频道", url="https://t.me/+M0su9kfTZHk2ODU1")],
            [InlineKeyboardButton("📝 Fill Form", url=f"{WEB_APP_URL}canteen")]
        ]
    },
    "🛒 生活用品": {
        "photo": "images/生活用品.jpg",
        "caption": "🛍️ 生活用品信息",
        "buttons": [
            [InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
             InlineKeyboardButton("🛒 详细了解", url="https://t.me/+M5Q_hf4xyG00YzRl")],
            [InlineKeyboardButton("📝 Fill Form", url=f"{WEB_APP_URL}shop")]
        ]
    }
}

# ✅ Start Command
async def start(update: Update, context: CallbackContext):
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
                f"📋 *New Form Submission*\n\n"
                f"🆔 *User ID:* `{form_data.get('user_id', 'N/A')}`\n"
                f"👤 *Username:* `{form_data.get('username', 'N/A')}`\n"
                f"📄 *Form Type:* `{form_data.get('form_type', 'N/A')}`\n"
            )

            logger.info(f"📤 Sending message to {ADMIN_ID}...")
            await context.bot.send_message(chat_id=ADMIN_ID, text=formatted_data, parse_mode="MarkdownV2")

            await update.message.reply_text("✅ Your form has been submitted successfully!")

        else:
            await update.message.reply_text("❌ No Web App Data Received")

    except Exception as e:
        logger.error(f"❌ Error processing form data: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")

# ✅ Run the Bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))  # Handle menu selection

    application.run_polling()

if __name__ == "__main__":
    main()
