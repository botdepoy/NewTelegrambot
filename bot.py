import json
import logging
import os
import time
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    WebAppInfo, KeyboardButton, ReplyKeyboardMarkup, InputMediaPhoto
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    CallbackContext, CallbackQueryHandler
)

# Replace with your actual bot token
BOT_TOKEN = "7472767533:AAFDewMWR-lN1BMEPffa0AwjAvffUMUXHyg"
ADMIN_ID = "1799744741"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Main menu options
MENU = [
    [KeyboardButton("✈️ 交通服务"), KeyboardButton("📜 证照办理"), KeyboardButton("🌍 翻译与商务对接")],
    [KeyboardButton("🏛️ 企业落地支持"), KeyboardButton("🏨 酒店与租凭"), KeyboardButton("🚀 综合增值服务")],
    [KeyboardButton("👩‍💻 人工客服")]
]

# Data for response messages
RESPONSE_DATA = {
    "✈️ 交通服务": {
        "photo": "images/IMG_0106.JPG",
        "caption": "🚖 **交通服务 | Transportation Services**\n\n"
                   "✨ 提供专业出行方案，助您畅行无忧！ ✨\n"
                   "🚗 机场接送 – 准时接送，轻松出行 🛫\n"
                   "🚘 专车服务 – 商务用车 / 高端专车 / VIP接待 💼\n"
                   "🧑‍✈️ 司机租赁 – 经验丰富，安全可靠 🏆\n"
                   "✅ 安全 | 🚀 高效 | 💎 舒适\n\n"
                   "无论是商务出行还是尊享专车，我们都为您提供最佳方案！ 🌍✨",
        "buttons": [
            [InlineKeyboardButton("🚗 专车服务", callback_data="car_service"),
             InlineKeyboardButton("✈ 机场接送", callback_data="airport_service")],
            [InlineKeyboardButton("🔙 返回", callback_data="✈️ 交通服务")]
        ]
    },
    "car_service": {
        "photo": "images/IMG_0105.JPG",
        "caption": "🚗 **专车服务**\n\n"
                   "🔹 高端商务用车 🚘\n"
                   "🔹 VIP接待 🏆\n"
                   "🔹 舒适 & 便捷\n"
                   "💎 尊享您的出行体验！",
        "buttons": [[InlineKeyboardButton("🔙 返回", callback_data="✈️ 交通服务")]]
    },
    "airport_service": {
        "photo": "images/接机.jpg",
        "caption": "✈ **机场接送**\n\n"
                   "🚕 准时接送，轻松出行\n"
                   "🚖 商务 & 休闲出行皆宜\n"
                   "🌟 24小时服务",
        "buttons": [[InlineKeyboardButton("🔙 返回", callback_data="✈️ 交通服务")]]
    }
}


# Handle button clicks and edit message instead of sending a new one
async def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    key = query.data
    if key in RESPONSE_DATA:
        data = RESPONSE_DATA[key]
        keyboard = InlineKeyboardMarkup(data["buttons"])

        # Ensure the image file exists
        if os.path.exists(data["photo"]):
            with open(data["photo"], "rb") as photo:
                # Edit existing message instead of sending a new one
                await query.message.edit_media(
                    media=InputMediaPhoto(photo, caption=data["caption"]),
                    reply_markup=keyboard
                )
        else:
            # If image is missing, just edit text
            await query.message.edit_caption(
                caption=data["caption"],
                reply_markup=keyboard
            )


# Start Command
async def start(update: Update, context: CallbackContext):
    menu_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text("📌 请选择服务:", reply_markup=menu_markup)


# Handle Menu Selection
async def handle_menu(update: Update, context: CallbackContext):
    text = update.message.text
    if text in RESPONSE_DATA:
        data = RESPONSE_DATA[text]
        keyboard = InlineKeyboardMarkup(data["buttons"])

        # Ensure the image file exists
        if os.path.exists(data["photo"]):
            with open(data["photo"], "rb") as photo:
                await update.message.reply_photo(photo=photo, caption=data["caption"], reply_markup=keyboard)
        else:
            await update.message.reply_text("🚨 图片不存在，请联系管理员!", reply_markup=keyboard)
    else:
        await update.message.reply_text("❌ 无效的选项，请选择正确的菜单项。")


# Main Function
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    # Start Polling
    application.run_polling()


if __name__ == "__main__":
    main()
