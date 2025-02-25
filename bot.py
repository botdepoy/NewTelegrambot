import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# ✅ Set Bot Token and Admin ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"  # 🔹 Replace with your real bot token
ADMIN_ID = 8101143576  # 🔹 Your Telegram ID

# ✅ Set WebApp Form URL
FORM_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"

# ✅ Start Command (Creates a button to open the form)
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📝 填写表单", web_app=WebAppInfo(url=FORM_URL))]  # ✅ Button to open form
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("📌 点击下面的按钮填写表单:", reply_markup=reply_markup)

# ✅ Function to handle form submissions
async def receive_form(update: Update, context: CallbackContext):
    try:
        # ✅ Debugging Log
        print(f"🔍 Received Update: {update}")

        # ✅ Extract Web App Data from Update
        if update.effective_message.web_app_data:
            form_data = json.loads(update.effective_message.web_app_data.data)
        else:
            await update.message.reply_text("⚠️ No form data received.")
            return

        user_info = update.effective_user  # ✅ Get user info
        user_id = user_info.id  # ✅ Get user's Telegram ID

        formatted_data = (
            f"📋 **New Form Submission:**\n\n"
            f"👤 **User:** {user_info.full_name}\n"
            f"🆔 **User ID:** `{user_id}`\n"
            f"📌 **Service Type:** {form_data.get('service_type', 'N/A')}\n"
            f"📆 **Expiry Date:** {form_data.get('expiry_date', 'N/A')}\n"
            f"📄 **Additional Info:** {form_data.get('additional_info', 'N/A')}"
        )

        # ✅ Send Data to Admin (8101143576)
        await context.bot.send_message(chat_id=ADMIN_ID, text=formatted_data, parse_mode="Markdown")

        # ✅ Send Confirmation Message to User
        await context.bot.send_message(chat_id=user_id, text="✅ Your form has been submitted successfully!", parse_mode="Markdown")

    except Exception as e:
        print(f"❌ Error processing form data: {e}")
        await update.message.reply_text("⚠️ Submission failed. Please try again!")

# ✅ Main function to run the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))  # Handles form submission

    application.run_polling()

if __name__ == "__main__":
    main()
