import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton, \
    ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

BOT_TOKEN = "7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg"
ADMIN_ID = "8101143576"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

MENU = [
    [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
    [KeyboardButton("🏩 酒店预订"), KeyboardButton("🥗 食堂频道"), KeyboardButton("🛒 生活用品")],
    [KeyboardButton("🔔 后勤生活信息频道")]
]

RESPONSE_DATA = {
    "✈ 落地接机": {
        "photo": "images/接机.jpg",
        "caption": "🛬 Welcome! \n🌟 欢迎加入【后勤接机】群 🌟\n\n✅ 请核对信息，如有更改，请联系客服！",
        "buttons": [[InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=WEB_APP_URL)),
                     InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
                     InlineKeyboardButton("✈ 接机频道", url="https://t.me/+pqM959ERihBkYTc9")]]
    },
    "🔖 证照办理": {
        "photo": "images/passport.jpg",
        "caption": "📋 证照办理服务：\n\n✔️ 提供快速办理签证、护照及其他相关证件的服务。\n📞 点击客服咨询更多详情。",
        "buttons": [[InlineKeyboardButton("📝 Fill Form", web_app=WebAppInfo(url=WEB_APP_URL)),
                     InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
                     InlineKeyboardButton("🔖 证件办理频道", url="https://t.me/+sINSVji28vM4ZDJl")]]
    }
}


async def start(update: Update, context: CallbackContext):
    menu_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text("📌 Please select an option:", reply_markup=menu_markup)


async def handle_menu(update: Update, context: CallbackContext):
    text = update.message.text
    if text in RESPONSE_DATA:
        data = RESPONSE_DATA[text]
        buttons = InlineKeyboardMarkup(data["buttons"])
        await update.message.reply_photo(photo=open(data["photo"], "rb"), caption=data["caption"], reply_markup=buttons)
    else:
        await update.message.reply_text("❌ Invalid option. Please select a valid menu item.")


async def receive_form(update: Update, context: CallbackContext):
    try:
        if update.message and update.message.web_app_data:
            form_data_json = update.message.web_app_data.data
            logger.info(f"🔍 Raw WebApp Data Received: {form_data_json}")
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 Raw Data Received:\n```{form_data_json}```",
                                           parse_mode="MarkdownV2")
            form_data = json.loads(form_data_json)
            logger.info(f"✅ Parsed Data: {form_data}")

            message = f"📋 *New Form Submission*\n\n"
            message += f"🆔 *User ID:* `{form_data.get('user_id', 'N/A')}`\n"
            message += f"👤 *Name:* `{form_data.get('first_name', 'N/A')} {form_data.get('last_name', 'N/A')}`\n"
            message += f"📄 *Form Type:* `{form_data.get('form_type', 'N/A')}`\n"

            for key, value in form_data.items():
                if key not in ["user_id", "first_name", "last_name", "form_type"]:
                    message += f"🔹 *{key}:* `{value}`\n"

            await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="MarkdownV2")
            await update.message.reply_text("✅ Your form has been submitted successfully!")
    except Exception as e:
        logger.error(f"❌ Error processing form data: {e}")
        await update.message.reply_text("❌ Submission failed. Please try again.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, receive_form))
    application.run_polling()


if __name__ == "__main__":
    main()
