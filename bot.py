from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import logging

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your bot token and chat ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
YOUR_CHAT_ID = "8101143576"  # Your Telegram account ID

# Define conversation states
DATE, NUMBER = range(2)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # Store user info in context
    context.user_data['first_name'] = user.first_name
    context.user_data['last_name'] = user.last_name if user.last_name else ""
    context.user_data['username'] = f"@{user.username}" if user.username else "No username"
    context.user_data['user_id'] = user.id

    # Ask for date
    await update.message.reply_text("Please enter the date (YYYY/MM/DD):")
    return DATE

# Handle date input
async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['date'] = update.message.text

    # Ask for number
    await update.message.reply_text("Please enter your number:")
    return NUMBER

# Handle number input and finish
async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['number'] = update.message.text

    # Prepare the message with all data
    message = (
        f"📩 *New Form Submission:*\n"
        f"💠 *Name:* {context.user_data['first_name']} {context.user_data['last_name']}\n"
        f"🆔 *ID:* {context.user_data['user_id']}\n"
        f"🔷 *Username:* {context.user_data['username']}\n"
        f"📅 *Date:* {context.user_data['date']}\n"
        f"📞 *Number:* {context.user_data['number']}"
    )

    # Send the message to your account
    await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=message, parse_mode="Markdown")

    # Reply to the user
    await update.message.reply_text("Thank you for your submission!")

    # End the conversation
    return ConversationHandler.END

# Cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Submission cancelled.")
    return ConversationHandler.END

def main():
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Define conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_number)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add conversation handler
    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
