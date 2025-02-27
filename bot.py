from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your bot token
BOT_TOKEN = '7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg'
# Replace with your admin chat ID
ADMIN_CHAT_ID = '8101143576'

# Command to start the bot and request contact
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create a button to request contact
    contact_button = KeyboardButton("Share Contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("Please share your contact to proceed:", reply_markup=reply_markup)

# Handle the contact shared by the user
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    contact = update.message.contact

    # Save user info
    user_data = {
        'username': user.username,
        'name': user.first_name,
        'contact': contact.phone_number
    }

    # Prepare the message for admin
    admin_message = (
        f"New form submission:\n"
        f"Username: @{user_data['username']}\n"
        f"Name: {user_data['name']}\n"
        f"Contact: {user_data['contact']}"
    )

    # Send the message to admin
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)

    # Notify the user
    await update.message.reply_text("Thank you! Your information has been submitted.", reply_markup=ReplyKeyboardRemove())

# Main function to run the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
