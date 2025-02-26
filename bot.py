import telebot

# Replace with your actual Telegram Bot Token
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"  # Your Telegram ID to receive form data

bot = telebot.TeleBot(BOT_TOKEN)

# Step 1: Bot sends a form link with a button
@bot.message_handler(commands=['start', 'form'])
def send_form(message):
    chat_id = message.chat.id
    form_url = "https://botdepoy.github.io/NewTelegrambot/form.html"

    # Create an inline button with the form link
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("📋 Fill Out Form", url=form_url)
    markup.add(button)

    bot.send_message(chat_id, "📝 Click the button below to fill out the form:", reply_markup=markup)

# Step 2: Bot receives user messages and forwards to ADMIN_ID
@bot.message_handler(func=lambda message: True)
def forward_user_message(message):
    chat_id = message.chat.id
    user = message.from_user

    # Format message
    message_text = f"📌 **New User Message**\n\n"
    message_text += f"👤 **User Info:**\n"
    message_text += f"🔹 User ID: `{chat_id}`\n"
    message_text += f"🔹 Name: {user.first_name or 'N/A'} {user.last_name or ''}\n"
    message_text += f"🔹 Username: @{user.username if user.username else 'N/A'}\n\n"
    message_text += f"📄 **Message:**\n{message.text}"

    # Forward to admin
    bot.send_message(ADMIN_ID, message_text, parse_mode="Markdown")

    # Confirm message receipt to user
    bot.send_message(chat_id, "✅ Message received! We will review it shortly.")

# Step 3: Run the bot
print("🤖 Bot is running...")
bot.polling()
