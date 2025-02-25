from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import os

# Get the Bot Token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Menu structure
MENU = {
    "main": [
        ("🍔 Food", "food"),
        ("🍹 Drinks", "drinks"),
        ("❓ Help", "help")
    ],
    "food": [
        ("🍕 Pizza", "pizza"),
        ("🍔 Burger", "burger"),
        ("🔙 Back", "main")
    ],
    "drinks": [
        ("🥤 Soda", "soda"),
        ("☕ Coffee", "coffee"),
        ("🔙 Back", "main")
    ]
}

async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in MENU["main"]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose a category:", reply_markup=reply_markup)

async def menu_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    menu_name = query.data

    if menu_name in MENU:
        keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in MENU[menu_name]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"You selected {menu_name}. Choose an option:", reply_markup=reply_markup)
    else:
        await query.edit_message_text(text=f"You selected {menu_name}! 🎉")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(menu_callback))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
