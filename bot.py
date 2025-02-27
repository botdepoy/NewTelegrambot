import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '7892503550:AAHczDCOpkPQSlq_v48xYfnKiBUM592BXXM'

# Replace 'TARGET_USER_ID' with the Telegram account ID you want to send data to
TARGET_USER_ID = 8101143576  # Example: 8101143576

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create a button to open the popup form
    keyboard = [
        [InlineKeyboardButton("📝 Open Form", web_app=WebAppInfo(url="https://botdepoy.github.io/NewTelegrambot/form.html"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the button to the user
    await update.message.reply_text(
        "Click the button below to open the form:",
        reply_markup=reply_markup
    )

# Handle form submission from Web App
async def handle_form_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message and update.message.web_app_data:
            # Parse the form data
            form_data_json = update.message.web_app_data.data
            form_data = json.loads(form_data_json)

            # Get user info from Telegram (only when the form is submitted)
            user = update.message.from_user
            user_info = (
                f"User ID: {user.id}\n"
                f"First Name: {user.first_name}\n"
                f"Last Name: {user.last_name}\n"
                f"Username: @{user.username}\n"
                f"Language: {user.language_code}"
            )

            # Combine form data and user info
            formatted_data = (
                f"📋 *Form Submission:*\n\n"
                f"👤 *User Info:*\n"
                f"{user_info}\n\n"
                f"📝 *Form Data:*\n"
                f"{json.dumps(form_data, indent=2)}"
            )

            # Send the combined data to the target account
            await context.bot.send_message(
                chat_id=TARGET_USER_ID,
                text=formatted_data,
                parse_mode="MarkdownV2"
            )

            # Confirm submission to the user
            await update.message.reply_text("✅ Thank you! Your form has been submitted.")

    except Exception as e:
        logging.error(f"❌ Error processing form data: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")

# Main function to run the bot
def main():
    # Create the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Add the handler for form submissions
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_form_submission))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
