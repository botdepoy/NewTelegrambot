from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler
import logging

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your bot token and chat ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
YOUR_CHAT_ID = "8101143576"  # Your Telegram account ID

# Define conversation states
SERVICE_TYPE, DATE, NUMBER = range(3)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # Store user info in context
    context.user_data['first_name'] = user.first_name
    context.user_data['last_name'] = user.last_name if user.last_name else ""
    context.user_data['username'] = f"@{user.username}" if user.username else "No username"

    # Ask for service type using inline keyboard
    keyboard = [
        [InlineKeyboardButton("Cleaning", callback_data="Cleaning")],
        [InlineKeyboardButton("Repair", callback_data="Repair")],
        [InlineKeyboardButton("Consultation", callback_data="Consultation")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select the type of service:", reply_markup=reply_markup)

    return SERVICE_TYPE

# Handle service type selection
async def get_service_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Store selected service type
    context.user_data['service_type'] = query.data

    # Ask for date using inline keyboard
    keyboard = [
        [InlineKeyboardButton("2025/02/14", callback_data="2025-02-14")],
        [InlineKeyboardButton("2025/02/15", callback_data="2025-02-15")],
        [InlineKeyboardButton("2025/02/16", callback_data="2025-02-16")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Please select the date:", reply_markup=reply_markup)

    return DATE

# Handle date selection
async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Store selected date
    context.user_data['date'] = query.data

    # Ask for number using inline keyboard
    keyboard = [
        [InlineKeyboardButton("123", callback_data="123")],
        [InlineKeyboardButton("456", callback_data="456")],
        [InlineKeyboardButton("789", callback_data="789")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Please select a number:", reply_markup=reply_markup)

    return NUMBER

# Handle number selection and finish
async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Store selected number
    context.user_data['number'] = query.data

    # Prepare the message with all data
    message = (
        f"New User Submission:\n"
        f"First Name: {context.user_data['first_name']}\n"
        f"Last Name: {context.user_data['last_name']}\n"
        f"Username: {context.user_data['username']}\n"
        f"Service Type: {context.user_data['service_type']}\n"
        f"Date: {context.user_data['date']}\n"
        f"Number: {context.user_data['number']}"
    )

    # Send the message to your account
    await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=message)

    # Reply to the user
    await query.edit_message_text("Thank you for your submission!")

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
            SERVICE_TYPE: [CallbackQueryHandler(get_service_type)],
            DATE: [CallbackQueryHandler(get_date)],
            NUMBER: [CallbackQueryHandler(get_number)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add conversation handler
    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
