import json
import logging
import os
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    WebAppInfo, InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup
)
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Replace with your bot token and admin ID
BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"  # Your hosted form

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

# ✅ Form Selection Buttons
FORM_BUTTONS = [
    [InlineKeyboardButton("✈ Airport Pickup", web_app=WebAppInfo(url=f"{WEB_APP_URL}?type=airport"))],
    [InlineKeyboardButton("🏩 Hotel Booking", web_app=WebAppInfo(url=f"{WEB_APP_URL}?type=hotel"))],
    [InlineKeyboardButton("🔖 Visa Application", web_app=WebAppInfo(url=f"{WEB_APP_URL}?type=visa"))],
    [InlineKeyboardButton("🏤 House Rental", web_app=WebAppInfo(url=f"{WEB_APP_URL}?type=rental"))],
    [InlineKeyboardButton("🥗 Canteen Order", web_app=WebAppInfo(url=f"{WEB_APP_URL}?type=canteen"))],
    [InlineKeyboardButton("🔔 Logistics Request", web_app=WebAppInfo(url=f"{WEB_APP_URL}?type=logistics"))],
    [InlineKeyboardButton("🛒 Shopping Order", web_app=WebAppInfo(url=f"{WEB_APP_URL}?type=shop"))]
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

# ✅ Start Command (Menu & Form Buttons)
async def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)

    menu_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    form_markup = InlineKeyboardMarkup(FORM_BUTTONS)

    await update.message.reply_text("📌 Please select an option:", reply_markup=menu_markup)
    await update.message.reply_text("📝 Choose a form to fill:", reply_markup=form_markup)

# ✅ Handle Menu Selection
async def handle_menu(update: Update, context: CallbackContext):
    text = update.message.text
    if text in RESPONSE_DATA:
        data = RESPONSE_DATA[text]
        buttons = data.get("buttons", [])
        reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
        if "photo" in data:
            await update.message.reply_photo(photo=open(data["photo"], "rb"), caption=data["caption"], reply_markup=reply_markup)
        else:
            await update.message.reply_text(data["caption"], reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"✅ You selected: {text}")

# ✅ Handle Form Data Submission
async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            logger.info(f"🔍 Raw WebApp Data: {form_data_json}")

            form_data = json.loads(form_data_json)
            logger.info(f"✅ Parsed WebApp Data: {form_data}")

            # ✅ Get Common Data
            user_id = form_data.get("user_id", "N/A")
            username = form_data.get("username", "N/A")
            form_type = form_data.get("form_type", "N/A")

            # ✅ Construct Message with Dynamic Data
            message = f"📋 *New Form Submission*\n\n"
            message += f"🆔 *User ID:* `{user_id}`\n"
            message += f"👤 *Username:* `{username}`\n"
            message += f"📄 *Form Type:* `{form_type}`\n"

            # ✅ Append Specific Form Data
            if form_type == "canteen":
                message += f"🍽 *Meal Type:* `{form_data.get('meal_type', 'N/A')}`\n"
                message += f"📦 *Quantity:* `{form_data.get('quantity', 'N/A')}`\n"
            elif form_type == "airport":
                message += f"✈ *Arrival Date:* `{form_data.get('arrival_date', 'N/A')}`\n"
                message += f"🛫 *Flight Number:* `{form_data.get('flight_number', 'N/A')}`\n"
            elif form_type == "hotel":
                message += f"🏨 *Check-in Date:* `{form_data.get('checkin_date', 'N/A')}`\n"
                message += f"🏩 *Hotel Name:* `{form_data.get('hotel_name', 'N/A')}`\n"
            elif form_type == "visa":
                message += f"🛂 *Full Name:* `{form_data.get('full_name', 'N/A')}`\n"
                message += f"📜 *Passport Number:* `{form_data.get('passport_number', 'N/A')}`\n"
            elif form_type == "rental":
                message += f"📍 *Location:* `{form_data.get('location', 'N/A')}`\n"
                message += f"💰 *Budget:* `{form_data.get('budget', 'N/A')}`\n"
            elif form_type == "logistics":
                message += f"📦 *Package Type:* `{form_data.get('package_type', 'N/A')}`\n"
                message += f"📅 *Delivery Date:* `{form_data.get('delivery_date', 'N/A')}`\n"
            elif form_type == "shop":
                message += f"🛍 *Product:* `{form_data.get('product_name', 'N/A')}`\n"
                message += f"📦 *Quantity:* `{form_data.get('shop_quantity', 'N/A')}`\n"

            logger.info(f"📤 Sending message to {ADMIN_ID}...")
            await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="MarkdownV2")

            await update.message.reply_text("✅ Your form has been submitted successfully!")

    except Exception as e:
        logger.error(f"❌ Error processing form data: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")

# ✅ Run the Bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))

    application.run_polling()

if __name__ == "__main__":
    main()
