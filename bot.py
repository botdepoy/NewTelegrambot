import json
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Replace with your bot token and admin ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
WEB_APP_BASE_URL = "https://botdepoy.github.io/NewTelegrambot/form.html?type="  # Base URL for hosted forms

# ✅ Enable Logging (For Debugging)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Store Users and Broadcast Messages
USER_DB = "users.json"
MESSAGE_DB = "messages.json"

# ✅ Inline Buttons for Form Selection
FORM_BUTTONS = [
    [InlineKeyboardButton("✈ Airport Pickup", web_app=WebAppInfo(url=f"{WEB_APP_BASE_URL}airport"))],
    [InlineKeyboardButton("🏨 Hotel Booking", web_app=WebAppInfo(url=f"{WEB_APP_BASE_URL}hotel"))],
    [InlineKeyboardButton("🔖 Visa Application", web_app=WebAppInfo(url=f"{WEB_APP_BASE_URL}visa"))],
    [InlineKeyboardButton("🏤 House Rental", web_app=WebAppInfo(url=f"{WEB_APP_BASE_URL}rental"))],
    [InlineKeyboardButton("🍽 Canteen Order", web_app=WebAppInfo(url=f"{WEB_APP_BASE_URL}canteen"))],
    [InlineKeyboardButton("🛍 Shopping Order", web_app=WebAppInfo(url=f"{WEB_APP_BASE_URL}shop"))]
]
FORM_SELECTION_MARKUP = InlineKeyboardMarkup(FORM_BUTTONS)

# ✅ Main Menu Structure (Reply Keyboard)
MENU = [
    [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
    [KeyboardButton("🏩 酒店预订"), KeyboardButton("🥗 食堂频道"), KeyboardButton("🛒 生活用品")],
    [KeyboardButton("🔔 后勤生活信息频道")]
]
MENU_MARKUP = ReplyKeyboardMarkup(MENU, resize_keyboard=True)

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

# ✅ Start Command (Menu & Form Button)
async def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)

    await update.message.reply_text("📌 Please select an option:", reply_markup=MENU_MARKUP)
    await update.message.reply_text("📝 Select a form to fill:", reply_markup=FORM_SELECTION_MARKUP)

# ✅ Handle Menu Selection
async def handle_menu(update: Update, context: CallbackContext):
    text = update.message.text
    await update.message.reply_text(f"✅ You selected: {text}")

# ✅ Handle Form Data Submission
async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            logger.info(f"🔍 Raw WebApp Data: {form_data_json}")

            form_data = json.loads(form_data_json)
            logger.info(f"✅ Parsed WebApp Data: {form_data}")

            user_id = form_data.get("user_id", "N/A")
            username = "@" + form_data.get("username", "N/A")
            form_type = form_data.get("form_type", "N/A")

            message = f"📋 *New Form Submission*\n\n🆔 *User ID:* `{user_id}`\n👤 *Username:* `{username}`\n📄 *Form Type:* `{form_type}`\n"

            if form_type == "airport":
                message += (
                    f"📅 *Arrival Date:* `{form_data.get('arrival_date', 'N/A')}`\n"
                    f"✈ *Flight Number:* `{form_data.get('flight_number', 'N/A')}`\n"
                )
            elif form_type == "hotel":
                message += (
                    f"🏨 *Hotel Name:* `{form_data.get('hotel_name', 'N/A')}`\n"
                    f"📅 *Check-in Date:* `{form_data.get('checkin_date', 'N/A')}`\n"
                )
            elif form_type == "visa":
                message += (
                    f"🆔 *Full Name:* `{form_data.get('full_name', 'N/A')}`\n"
                    f"🛂 *Passport Number:* `{form_data.get('passport_number', 'N/A')}`\n"
                )
            elif form_type == "rental":
                message += (
                    f"📍 *Location:* `{form_data.get('location', 'N/A')}`\n"
                    f"💰 *Budget:* `{form_data.get('budget', 'N/A')}`\n"
                )
            elif form_type == "canteen":
                message += (
                    f"🍽️ *Meal Type:* `{form_data.get('meal_type', 'N/A')}`\n"
                    f"🔢 *Quantity:* `{form_data.get('quantity', 'N/A')}`\n"
                )
            elif form_type == "shop":
                message += (
                    f"🛍️ *Product Name:* `{form_data.get('product_name', 'N/A')}`\n"
                    f"🔢 *Quantity:* `{form_data.get('shop_quantity', 'N/A')}`\n"
                )

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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    application.run_polling()

if __name__ == "__main__":
    main()
