import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Replace with your bot token and admin ID
BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 8101143576  # Replace with your Telegram ID
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"  # Host your form

# ✅ Enable Logging (For Debugging)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Start Command - Opens the Form Inside Telegram
async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Click below to open the form inside Telegram:",
        reply_markup=reply_markup
    )

# ✅ Handle Form Data Submission
async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            form_data = json.loads(form_data_json)  # Convert JSON string to Python dictionary

            # ✅ Log received data (for debugging)
            logger.info(f"Received form data: {form_data}")

            # ✅ Extract User Information
            user_id = form_data.get("user_id", "N/A")
            first_name = form_data.get("first_name", "N/A")
            last_name = form_data.get("last_name", "N/A")
            username = form_data.get("username", "N/A")
            language = form_data.get("language", "N/A")
            date = form_data.get("date", "N/A")
            number = form_data.get("number", "N/A")

            # ✅ Format Message
            formatted_data = (
                f"📋 *New User Info Received:*\n\n"
                f"🆔 *User ID:* `{user_id}`\n"
                f"🔹 *First Name:* `{first_name}`\n"
                f"🔹 *Last Name:* `{last_name}`\n"
                f"💠 *Username:* `{username}`\n"
                f"🌍 *Language:* `{language}`\n\n"
                f"📅 *Date:* `{date}`\n"
                f"📞 *Number:* `{number}`"
            )

            # ✅ Send Data to Admin
            await context.bot.send_message(chat_id=ADMIN_ID, text=formatted_data, parse_mode="MarkdownV2")

            # ✅ Confirm Submission to User
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
