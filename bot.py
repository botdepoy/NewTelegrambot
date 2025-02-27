from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace with your actual bot token
BOT_TOKEN = "BOT_TOKEN"

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user  # Get user info
    user_info = f"""
    📌 User Info:
    🔹 ID: {user.id}
    🔹 Username: @{user.username if user.username else 'N/A'}
    🔹 First Name: {user.first_name}
    🔹 Last Name: {user.last_name if user.last_name else 'N/A'}
    """
    
    update.message.reply_text(f"Welcome, {user.first_name}! 😊\n\n{user_info}")

    # Optional: Save to a file or database
    with open("user_data.txt", "a") as file:
        file.write(f"{user.id},{user.username},{user.first_name},{user.last_name}\n")

# Set up the bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))  # When user starts the bot

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
