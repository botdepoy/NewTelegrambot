import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = 8101143576  # Replace with your Telegram ID
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"  # Host your form

# ✅ Start Command - Opens Popup Form
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Click below to open the form inside Telegram:",
        reply_markup=reply_markup
    )

# ✅ Receive Data from Form Submission
async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            form_data = json.loads(form_data_json)

            # ✅ Format Message
            formatted_data = (
                f"📋 *New Form Submission:*\n\n"
                f"🆔 *User ID:* `{form_data.get('user_id', 'N/A')}`\n"
                f"💠 *Username:* `{form_data.get('username', 'N/A')}`\n"
                f"🔹 *First Name:* `{form_data.get('name', 'N/A')}`\n"
                f"🗓 *Date:* `{form_data.get('date', 'N/A')}`\n"
                f"📞 *Number:* `{form_data.get('number', 'N/A')}`"
            )

            # ✅ Send Data to Admin
            await context.bot.send_message(chat_id=ADMIN_ID, text=formatted_data, parse_mode="MarkdownV2")

            # ✅ Confirm Submission to User
            await update.message.reply_text("✅ Your form has been submitted successfully!")

    except Exception as e:
        print(f"❌ Error processing form data: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")

# ✅ Run the Bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))
    application.run_polling()

if __name__ == "__main__":
    main()
