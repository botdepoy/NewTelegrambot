from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Get the Bot Token from environment variable (for security)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Menu structure (formatted as grid layout)
MENU = [
    [KeyboardButton("🍜 外卖"), KeyboardButton("💱 换汇"), KeyboardButton("♻️ 闲置"), KeyboardButton("📌 求职")],
    [KeyboardButton("🚖 滴滴"), KeyboardButton("📄 签证"), KeyboardButton("🛍️ 代购"), KeyboardButton("🧧 红包")],
    [KeyboardButton("💰 充值"), KeyboardButton("💳 收款"), KeyboardButton("🔄 转账"), KeyboardButton("🐱 我的")]
]

async def start(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text("📌 请选择一个选项:", reply_markup=reply_markup)

async def handle_menu(update: Update, context: CallbackContext):
    text = update.message.text
    await update.message.reply_text(f"✅ 你选择了: {text}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    
    application.run_polling()

if __name__ == "__main__":
    main()
