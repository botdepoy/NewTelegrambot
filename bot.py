import json
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Replace with your bot token and admin ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
WEB_APP_BASE_URL = "https://botdepoy.github.io/NewTelegrambot/form.html?type="  # Base form URL

# ✅ Enable Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Menu structure (Reply Keyboard)
MENU = [
    [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
    [KeyboardButton("🏩 酒店预订"), KeyboardButton("🥗 食堂频道"), KeyboardButton("🛒 生活用品")],
    [KeyboardButton("🔔 后勤生活信息频道")]
]

# ✅ Form Types Mapping
FORM_TYPES = {
    "✈ 落地接机": "airport",
    "🔖 证照办理": "visa",
    "🏤 房产凭租": "rental",
    "🏩 酒店预订": "hotel",
    "🥗 食堂频道": "canteen",
    "🛒 生活用品": "shop",
    "🔔 后勤生活信息频道": "logistics"
}

# ✅ Start Command (Menu & Form Button)
async def start(update: Update, context: CallbackContext):
    menu_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text("📌 Please select an option:", reply_markup=menu_markup)

# ✅ Handle Menu Selection & Provide Form Link
async def handle_menu(update: Update, context: CallbackContext):
    text = update.message.text
    if text in FORM_TYPES:
        form_url = WEB_APP_BASE_URL + FORM_TYPES[text]
        buttons = [[InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=form_url))]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(f"📌 You selected: {text}\nClick below to fill the form:", reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"✅ You selected: {text}")

# ✅ Handle Form Data Submission
async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            logger.info(f"🟢 Raw WebApp Data Received: {form_data_json}")

            # ✅ Convert JSON string to dictionary
            form_data = json.loads(form_data_json)
            logger.info(f"✅ Parsed Form Data: {form_data}")

            # ✅ Extract Form Information
            user_id = form_data.get("user_id", "N/A")
            username = "@" + form_data.get("username", "N/A")
            form_type = form_data.get("form_type", "N/A")

            # ✅ Build Message for Admin
            message = f"📋 *New Form Submission*\n\n🆔 *User ID:* `{user_id}`\n👤 *Username:* `{username}`\n📄 *Form Type:* `{form_type}`\n"

            # ✅ Add Form Data
            for key, value in form_data.items():
                if key not in ["user_id", "username", "form_type"]:
                    message += f"🔹 *{key.replace('_', ' ').title()}:* `{value}`\n"

            # ✅ Send Form Data to Admin
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": ADMIN_ID, "text": message, "parse_mode": "MarkdownV2"}
            )

            await update.message.reply_text("✅ Your form has been submitted successfully!")

    except Exception as e:
        logger.error(f"❌ Error processing form data: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")

# ✅ Run the Bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))

    application.run_polling()

if __name__ == "__main__":
    main()
