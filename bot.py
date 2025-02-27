import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Replace with your bot token and admin ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html?type="  # Base URL for different forms

# ✅ Enable Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Escape Markdown characters
def escape_markdown(text):
    """Escape MarkdownV2 special characters"""
    if not text:
        return "N/A"
    return text.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]")

# ✅ Start Command - Display Form Selection Menu
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🛬 Airport Pickup", web_app=WebAppInfo(url=f"{WEB_APP_URL}airport"))],
        [InlineKeyboardButton("🏨 Hotel Booking", web_app=WebAppInfo(url=f"{WEB_APP_URL}hotel"))],
        [InlineKeyboardButton("🔖 Visa Application", web_app=WebAppInfo(url=f"{WEB_APP_URL}visa"))],
        [InlineKeyboardButton("🏤 House Rental", web_app=WebAppInfo(url=f"{WEB_APP_URL}rental"))],
        [InlineKeyboardButton("📦 Logistics Request", web_app=WebAppInfo(url=f"{WEB_APP_URL}logistics"))],
        [InlineKeyboardButton("🥗 Canteen Order", web_app=WebAppInfo(url=f"{WEB_APP_URL}canteen"))],
        [InlineKeyboardButton("🛒 Shopping Order", web_app=WebAppInfo(url=f"{WEB_APP_URL}shop"))]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📋 Select a form to fill:", reply_markup=reply_markup)

# ✅ Handle Form Data Submission
async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            logger.info(f"🔍 Raw WebApp Data: {form_data_json}")

            form_data = json.loads(form_data_json)
            logger.info(f"✅ Parsed WebApp Data: {form_data}")

            # Extract Data & Escape Markdown
            user_id = escape_markdown(str(form_data.get("user_id", "N/A")))
            username = "@" + escape_markdown(form_data.get("username", "N/A"))
            form_type = escape_markdown(form_data.get("form_type", "N/A"))

            # ✅ Format Message Based on Form Type
            message = f"📋 *New Form Submission*\n\n🆔 *User ID:* `{user_id}`\n👤 *Username:* `{username}`\n📄 *Form Type:* `{form_type}`\n"

            # 🛬 Airport Pickup Form
            if form_type == "airport":
                message += (
                    f"📅 *Arrival Date:* `{escape_markdown(form_data.get('arrival_date', 'N/A'))}`\n"
                    f"✈ *Flight Number:* `{escape_markdown(form_data.get('flight_number', 'N/A'))}`\n"
                )

            # 🏨 Hotel Booking Form
            elif form_type == "hotel":
                message += (
                    f"🏨 *Hotel Name:* `{escape_markdown(form_data.get('hotel_name', 'N/A'))}`\n"
                    f"📅 *Check-in Date:* `{escape_markdown(form_data.get('checkin_date', 'N/A'))}`\n"
                )

            # 🔖 Visa Application Form
            elif form_type == "visa":
                message += (
                    f"🆔 *Full Name:* `{escape_markdown(form_data.get('full_name', 'N/A'))}`\n"
                    f"🛂 *Passport Number:* `{escape_markdown(form_data.get('passport_number', 'N/A'))}`\n"
                )

            # 🏤 House Rental Form
            elif form_type == "rental":
                message += (
                    f"📍 *Location:* `{escape_markdown(form_data.get('location', 'N/A'))}`\n"
                    f"💰 *Budget Range:* `{escape_markdown(form_data.get('budget', 'N/A'))}`\n"
                )

            # 📦 Logistics Request Form
            elif form_type == "logistics":
                message += (
                    f"📦 *Package Type:* `{escape_markdown(form_data.get('package_type', 'N/A'))}`\n"
                    f"📅 *Delivery Date:* `{escape_markdown(form_data.get('delivery_date', 'N/A'))}`\n"
                )

            # 🥗 Canteen Order Form
            elif form_type == "canteen":
                message += (
                    f"🍽️ *Meal Type:* `{escape_markdown(form_data.get('meal_type', 'N/A'))}`\n"
                    f"🔢 *Quantity:* `{escape_markdown(str(form_data.get('quantity', 'N/A')))}`\n"
                )

            # 🛒 Shopping Order Form
            elif form_type == "shop":
                message += (
                    f"🛍️ *Product Name:* `{escape_markdown(form_data.get('product_name', 'N/A'))}`\n"
                    f"🔢 *Quantity:* `{escape_markdown(str(form_data.get('shop_quantity', 'N/A')))}`\n"
                )

            # ✅ Send to Admin
            await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="MarkdownV2")
            await update.message.reply_text("✅ Your form has been submitted successfully!")

    except Exception as e:
        logger.error(f"❌ Error processing form data: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")

# ✅ Run the Bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))

    application.run_polling()

if __name__ == "__main__":
    main()
