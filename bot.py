import telebot
from flask import Flask, request, jsonify

# Replace with your actual Telegram Bot Token
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"  # Your Telegram ID to receive form data

bot = telebot.TeleBot(BOT_TOKEN)

# Flask app for receiving form data
app = Flask(__name__)

# Store user data temporarily
user_data = {}

# Step 1: Bot sends a form link with a button
@bot.message_handler(commands=['start', 'form'])
def send_form(message):
    chat_id = str(message.chat.id)
    user = message.from_user

    # Ensure user details are stored correctly
    user_info = {
        "User ID": chat_id,
        "First Name": user.first_name or "N/A",
        "Last Name": user.last_name or "N/A",
        "Username": f"@{user.username}" if user.username else "N/A"
    }

    # Save user info temporarily
    user_data[chat_id] = {"telegram_info": user_info}

    # Form URL (Modify if needed)
    form_url = "https://botdepoy.github.io/NewTelegrambot/form.html"

    # Create an inline button
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton("📋 Fill Out Form", url=form_url)
    markup.add(button)

    bot.send_message(chat_id, "📝 Click the button below to fill out the form:", reply_markup=markup)

# Step 2: Flask Receives Form Data
@app.route('/receive_form_data', methods=['POST'])
def receive_form_data():
    data = request.json  # Expecting JSON payload
    chat_id = str(data.get('chat_id'))  # Ensure chat_id is stored as a string

    if chat_id:
        # Ensure user info is stored
        if chat_id in user_data:
            user_data[chat_id]["form_data"] = data
        else:
            user_data[chat_id] = {"form_data": data, "telegram_info": {"User ID": chat_id}}

        # Retrieve user info
        user_info = user_data[chat_id].get("telegram_info", {})

        # Format message with user details and form data
        message_text = f"📩 **New Form Submission:**\n\n"
        message_text += f"💠 **Name:** {user_info.get('First Name', 'N/A')} {user_info.get('Last Name', '')}\n"
        message_text += f"🆔 **ID:** `{user_info.get('User ID', 'Unknown')}`\n"
        message_text += f"🔷 **Username:** {user_info.get('Username', 'N/A')}\n\n"

        message_text += "📄 **Form Data:**\n"
        for key, value in data.items():
            if key != "chat_id":
                message_text += f"🔹 {key}: {value}\n"

        # Notify the user
        bot.send_message(chat_id, "✅ Your form has been submitted successfully!")

        # Send full data to the admin (You)
        bot.send_message(ADMIN_ID, message_text, parse_mode="Markdown")

        return jsonify({"status": "success"}), 200
    return jsonify({"status": "failed"}), 400

# Step 3: Retrieve User Data Manually
@bot.message_handler(commands=['getdata'])
def get_user_data(message):
    chat_id = str(message.chat.id)
    
    if chat_id in user_data and "form_data" in user_data[chat_id]:
        user_info = user_data[chat_id].get("telegram_info", {})
        form_info = user_data[chat_id].get("form_data", {})

        response = "📌 **Your Submitted Data:**\n"
        response += f"🔹 Name: {user_info.get('First Name', 'N/A')} {user_info.get('Last Name', '')}\n"
        response += f"🔹 Username: {user_info.get('Username', 'N/A')}\n\n"

        for key, value in form_info.items():
            if key != "chat_id":
                response += f"🔹 {key}: {value}\n"

        bot.send_message(chat_id, response, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "❌ No form data found for you!")

# Step 4: Run Flask and Bot
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
