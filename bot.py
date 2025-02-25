from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Get the Bot Token from environment variable (for security)
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = "https://example.com/form"  # Replace with your actual form URL

# Menu structure (formatted as grid layout)
MENU = [
    [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
    [KeyboardButton("🏩 酒店预订"), KeyboardButton("🥗 食堂频道"), KeyboardButton("🛒 生活用品")],
    [KeyboardButton("🔔 后勤生活信息频道")]
]


# Response data mapping user selections to images and buttons
RESPONSE_DATA = {
    "✈ 落地接机": {
        "photo": "images/接机.jpg",
        "caption": "🌟 欢迎加入【后勤接机】群 🌟\n\n✅ 请核对信息，如有更改，请联系客服！",
        "buttons": [["🧑🏻‍💻 在线客服", "https://t.me/HQBGSKF"], ["✈ 接机频道", "https://t.me/+pqM959ERihBkYTc9"]]
    },
    "🔖 证照办理": {
        "photo": "images/passport.jpg",
        "caption": "📋 证照办理服务：\n\n✔️ 提供快速办理签证、护照及其他相关证件的服务。\n📞 点击客服咨询更多详情。",
        "buttons": [["🧑🏻‍💻 在线客服", "https://t.me/HQBGSKF"], ["🔖 证件办理频道", "https://t.me/+sINSVji28vM4ZDJl"]]
    },
    "🏤 房产凭租": {
        "photo": "images/resized-image.jpg",
        "caption": "🏤 房产租赁信息：\n\n✔️ 提供房产出租和购房服务，涵盖各类房型。\n🔍 点击下方按钮了解更多。",
        "buttons": [["🧑🏻‍💻 在线客服", "https://t.me/HQBGSKF"], ["🏤 房产信息频道", "https://t.me/+8i7xQLV_UiY2NTY1"]]
    },
    "🏩 酒店预订": {
        "photo": "images/sofietel.jpg",
        "caption": "🏨高端酒店预订代办服务| 索菲特 & 瑰丽酒店 |🏨\n\n✨ 奢华体验，优惠价格，预订更省心！ ✨\n\n📞 联系我们，轻松享受高端住宿！",
        "buttons": [["🧑🏻‍💻 在线客服", "https://t.me/HQBGSKF"], ["🏩 酒店详情频道", "https://t.me/+M5Q_hf4xyG00YzRl"]]
    },
    "🥗 食堂频道": {
        "photo": "images/食堂.jpg",
            "caption": "🏨高端酒店预订代办服务| 索菲特 & 瑰丽酒店 |🏨\n\n✨ 奢华体验，优惠价格，预订更省心！ ✨\n\n📞 联系我们，轻松享受高端住宿！",
            "buttons": [["🧑🏻‍💻 在线客服", "https://t.me/DINGCHUANG001"], ["🏩 酒店详情频道", "https://t.me/+M0su9kfTZHk2ODU1"]]
    },
    "🛒 生活用品": {
        "photo": "images/生活用品.jpg",
            "caption": "🏨高端酒店预订代办服务| 索菲特 & 瑰丽酒店 |🏨\n\n✨ 奢华体验，优惠价格，预订更省心！ ✨\n\n📞 联系我们，轻松享受高端住宿！",
            "buttons": [["🧑🏻‍💻 在线客服", "https://t.me/HQBGSKF"], ["🏩 酒店详情频道", "https://t.me/+M5Q_hf4xyG00YzRl"]]
    },
    "🔔 后勤生活信息频道": {
        "photo": "images/logistic.png",
        "caption": "📌 主要提供各种后勤管理和生活服务，确保用户能够方便、高效地获取信息和帮助。",
        "buttons": [["🔔 详细了解", "https://t.me/+QQ56RVTKshQxMDU1"]]
    }
}

async def start(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text("📌 请选择一个选项:", reply_markup=reply_markup)

async def handle_menu(update: Update, context: CallbackContext):
    text = update.message.text
    if text in RESPONSE_DATA:
        data = RESPONSE_DATA[text]
        buttons = [[InlineKeyboardButton(btn[0], url=btn[1])] for btn in data.get("buttons", [])]
        reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
        if "photo" in data:
            await update.message.reply_photo(photo=open(data["photo"], "rb"), caption=data["caption"], reply_markup=reply_markup)
        else:
            await update.message.reply_text(data["caption"], reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"✅ 你选择了: {text}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    
    application.run_polling()

if __name__ == "__main__":
    main()
