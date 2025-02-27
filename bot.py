import json
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Replace with your bot token and admin ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"  # Replace with your hosted form

# ✅ Enable Logging (For Debugging)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Store Users and Broadcast Messages
USER_DB = "users.json"
MESSAGE_DB = "messages.json"

# ✅ Menu structure (Reply Keyboard)
MENU = [
    [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
    [KeyboardButton("🏩 酒店预订"), KeyboardButton("🥗 食堂频道"), KeyboardButton("🛒 生活用品")],
    [KeyboardButton("🔔 后勤生活信息频道")]
]

# ✅ Load and save users
def load_users():
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# ✅ Escape Markdown characters
def escape_markdown(text):
    """Escape Markdown special characters"""
    if not text:
        return "N/A"
    return text.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]")

# ✅ Start Command (Menu & Form Button)
async def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)

    keyboard = [[InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    menu_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)

    await update.message.reply_text("📌 Please select an option:", reply_markup=menu_markup)
    await update.message.reply_text("Click below to open the form inside Telegram:", reply_markup=reply_markup)

# ✅ Handle Form Data Submission
async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            logger.info(f"🔍 Raw WebApp Data: {form_data_json}")

            form_data = json.loads(form_data_json)
            logger.info(f"✅ Parsed WebApp Data: {form_data}")

            # Extract Data & Escape Markdown
            user_id = escape_markdown(form_data.get("user_id", "N/A"))
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

            # 🔔 Logistics Request Form
            elif form_type == "logistics":
                message += (
                    f"📦 *Package Type:* `{escape_markdown(form_data.get('package_type', 'N/A'))}`\n"
                    f"📅 *Delivery Date:* `{escape_markdown(form_data.get('delivery_date', 'N/A'))}`\n"
                )

            # 🥗 Canteen Order Form
            elif form_type == "canteen":
                message += (
                    f"🍽️ *Meal Type:* `{escape_markdown(form_data.get('meal_type', 'N/A'))}`\n"
                    f"🔢 *Quantity:* `{escape_markdown(form_data.get('quantity', 'N/A'))}`\n"
                )

            # 🛒 Shopping Order Form
            elif form_type == "shop":
                message += (
                    f"🛍️ *Product Name:* `{escape_markdown(form_data.get('product_name', 'N/A'))}`\n"
                    f"🔢 *Quantity:* `{escape_markdown(form_data.get('shop_quantity', 'N/A'))}`\n"
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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))  # Handle menu selection

    application.run_polling()

if __name__ == "__main__":
    main()
