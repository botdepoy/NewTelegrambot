import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Bot Token and Admin ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = 8101143576  # Replace with your Telegram ID

# ✅ Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ✅ Start Command - Sends a Button to Open the Web Form
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url="https://botdepoy.github.io/NewTelegrambot/form.html"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Click below to fill the form inside Telegram WebApp:",
        reply_markup=reply_markup
    )

# ✅ Handle Form Submission from Web App
async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            form_data = json.loads(form_data_json)

            # ✅ Extract Form Details
            user_info = update.effective_user
            user_id = user_info.id

            # ✅ Ensure all fields are present
            name = form_data.get('telegram_name', 'N/A')
            username = form_data.get('telegram_username', 'N/A')
            telegram_id = form_data.get('telegram_id', 'N/A')
            date = form_data.get('date', 'N/A')
            number = form_data.get('number', 'N/A')

            # ✅ Format Message to Send
            formatted_data = (
                f"📋 **New Form Submission:**\n\n"
                f"👤 *Name:* {name}\n"
                f"🆔 *ID:* {telegram_id}\n"
                f"🔹 *Username:* {username}\n"
                f"📅 *Date:* {date}\n"
                f"📞 *Contact:* {number}"
            )

            # ✅ Send Form Data to Admin
            await context.bot.send_message(chat_id=ADMIN_ID, text=formatted_data, parse_mode="Markdown")

            # ✅ Confirm Submission to User
            await update.message.reply_text("✅ Your form has been submitted successfully!")

        else:
            await update.message.reply_text("⚠️ No data received. Please try again.")

    except Exception as e:
        logging.error(f"❌ Error processing form data: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")

# ✅ Main Function to Run the Bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # ✅ Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))

    # ✅ Start Polling
    application.run_polling()

if __name__ == "__main__":
    main()
