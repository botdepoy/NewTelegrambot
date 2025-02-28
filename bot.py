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
        if update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            logger.info(f"🔍 Received WebApp Data: {form_data_json}")
            form_data = json.loads(form_data_json)

            message = f"📋 *New Submission Received:*\n\n🆔 *User ID:* `{form_data['user_id']}`\n"
            message += f"👤 *Name:* `{form_data['first_name']} {form_data['last_name']}`\n"
            message += f"📄 *Form Type:* `{form_data['form_type']}`\n"

            for key, value in form_data.items():
                if key not in ["user_id", "first_name", "last_name", "form_type"]:
                    message += f"🔹 *{key}:* `{value}`\n"

            await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="MarkdownV2")
            await update.message.reply_text("✅ Form submitted successfully!")

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))
    application.run_polling()

if __name__ == "__main__":
    main()
