import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Replace with your bot token and admin ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html?type="  # Base URL for different forms

# ✅ Enable Logging (For Debugging)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Start Command - Show Form Selection Menu
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🛬 Airport Pickup", web_app=WebAppInfo(url=f"{WEB_APP_URL}airport"))],
        [InlineKeyboardButton("🏨 Hotel Booking", web_app=WebAppInfo(url=f"{WEB_APP_URL}hotel"))],
        [InlineKeyboardButton("🔖 Visa Application", web_app=WebAppInfo(url=f"{WEB_APP_URL}visa"))],
        [InlineKeyboardButton("🏤 House Rental", web_app=WebAppInfo(url=f"{WEB_APP_URL}rental"))],
        [InlineKeyboardButton("📦 Logistics Request", web_app=WebAppInfo(url=f"{WEB_APP_URL}logistics"))],
        [InlineKeyboardButton("🥗 Canteen Order", web_app=WebAppInfo(url=f"{WEB_APP_URL}canteen"))],
        [InlineKeyboardButton("🛒 Shopping Order", web_app=WebAppInfo(url=f"{WEB_APP_URL}shop"))]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📋 Select a form to fill:", reply_markup=reply_markup)

# ✅ Handle Form Data Submission
async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            logger.info(f"🔍 Raw WebApp Data: {form_data_json}")

            form_data = json.loads(form_data_json)
            logger.info(f"✅ Parsed WebApp Data: {form_data}")

            user_id = form_data.get("user_id", "N/A")
            username = "@" + form_data.get("username", "N/A")
            form_type = form_data.get("form_type", "N/A")

            message = f"📋 *New Form Submission*\n\n🆔 *User ID:* `{user_id}`\n👤 *Username:* `{username}`\n📄 *Form Type:* `{form_type}`\n"

            for key, value in form_data.items():
                if key not in ["user_id", "username", "form_type"]:
                    message += f"🔹 *{key}:* `{value}`\n"

            await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="MarkdownV2")
            await update.message.reply_text("✅ Your form has been submitted successfully!")

    except Exception as e:
        logger.error(f"❌ Error processing form data: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")

# ✅ Run the Bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))
    
    application.run_polling()

if __name__ == "__main__":
    main()
