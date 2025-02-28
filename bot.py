import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click below to open the form inside Telegram:", reply_markup=reply_markup)

async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            logger.info(f"🔍 Raw WebApp Data Received: {form_data_json}")

            # ✅ Debug: Send raw data to admin
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 Raw Data Received:\n```{form_data_json}```", parse_mode="MarkdownV2")

            # ✅ Parse JSON Data
            form_data = json.loads(form_data_json)
            logger.info(f"✅ Parsed Data: {form_data}")

            # ✅ Construct Message
            message = f"📋 *New Form Submission*\n\n"
            message += f"🆔 *User ID:* `{form_data.get('user_id', 'N/A')}`\n"
            message += f"👤 *Name:* `{form_data.get('first_name', 'N/A')} {form_data.get('last_name', 'N/A')}`\n"
            message += f"📄 *Form Type:* `{form_data.get('form_type', 'N/A')}`\n"

            for key, value in form_data.items():
                if key not in ["user_id", "first_name", "last_name", "form_type"]:
                    message += f"🔹 *{key}:* `{value}`\n"

            # ✅ Send Data to Admin
            await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="MarkdownV2")
            await update.message.reply_text("✅ Your form has been submitted successfully!")

    except Exception as e:
        logger.error(f"❌ Error processing form data: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))
    application.run_polling()

if __name__ == "__main__":
    main()
