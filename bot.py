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
            [InlineKeyboardButton("🚗 专车服务", callback_data="🚗 专车服务"),
             InlineKeyboardButton("✈️ 机场接送", callback_data="✈️ 机场接送")]
            ]
    },
                                "🚗 专车服务": {
                                    "photo": "images/Web_Photo_Editor.jpg",
                                    "caption": "",
                                    "buttons": [
                                                [InlineKeyboardButton("人工客服", url="https://t.me/LUODISWKF")],
                                                [InlineKeyboardButton("🔙 返回", callback_data="✈️ 交通服务")]
                                    ]            
                                },
                                "✈️ 机场接送": {
                                    "photo": "images/接机.jpg",
                                    "caption": "✈ **机场接送**\n\n"
                                               "🚕 准时接送，轻松出行\n"
                                               "🚖 商务 & 休闲出行皆宜\n"
                                               "🌟 24小时服务",
                                    "buttons":[
                                                 [InlineKeyboardButton("机场接机", callback_data="机场接机"),
                                                InlineKeyboardButton("机场送机", callback_data="机场送机")],
                                                [InlineKeyboardButton("🔙 返回", callback_data="✈️ 交通服务")]
                                    ]
                                },


    "📜 证照办理": {
            "photo": "images/visa.jpg",
            "caption": "📜 证件办理服务** | **Document Processing Services \n\n"
                        "✨ **快速 & 高效，轻松办理您的证件！** ✨\n  "
                        
                        "🛂 **落地商务签** – 办理便捷，轻松落地 🌍\n  "
                        "🛫 **旅游签证** – 畅游世界，轻松出行 ✈️ \n "
                        "📆 **长期商务签** – 长期驻留，无忧续签 🏢\n " 
                        "🔄 **签证续签** – 快速续签，避免逾期 ⏳\n  "
                        "🆕 **护照更换** – 助您顺利更新新护照 📑\n  "
                        "🚗 **驾驶证办理** – 驾驶资格，轻松搞定 ✅ \n "
                        "✅ 手续简便 | ⚡ 快速办理 | 🔒 安全可靠 \n\n "
                        
                       " **让您的出行更无忧，我们为您提供全方位证件支持！** 🌍✨",
            "buttons": [
                [InlineKeyboardButton("🛫 商务签证", callback_data="🛫 商务签证"),
                 InlineKeyboardButton("🌍 旅游签证", callback_data="🌍 旅游签证"),
                InlineKeyboardButton("📑 护照服务", callback_data="📑 护照服务")],
                 [InlineKeyboardButton("📆 续签服务", callback_data="📆 续签服务"),
                InlineKeyboardButton("🚗 驾驶证办理", callback_data="🚗 驾驶证办理")]
            ]
        },
                                "🛫 商务签证": {
                                        "photo": "images/商务签证.png",
                                        "caption": "📜 **商务签证简介 & 服务** | **Business Visa Services**   \n\n "                                  
                                                "✨ **专业办理，助力全球商务拓展！** ✨ \n "
                                                
                                                "📌 **商务签证** 适用于前往他国进行商务洽谈、会议、市场考察及商业合作，确保您的出行 **高效 & 合规**。\n\n  "
                                                
                                                "✅ **商务签证类型**：\n  "
                                                "🔹 **落地商务签** 🏢✈️ – 到达后快速办理，适用于短期商务活动  \n"
                                                "🔹 **半年商务签** 📆🌍 – 适用于中期商务出差 & 合作项目 \n "
                                                "🔹 **一年商务签** 🔄✅ – 适用于长期商务驻留 & 跨国业务拓展 \n\n "
                                                
                                                "💼 **服务内容**： \n "
                                                "🔹 签证申请 & 指导 📄  \n"
                                                "🔹 资料准备 & 审核 ✅ \n "
                                                "🔹 面签辅导 & 预约 🎯 \n "
                                                "🔹 加急办理 & 续签 🔄 \n "
                                                
                                                "📞 **立即联系我们，让您的商务之旅更加顺畅！** 🚀✨",
                                        "buttons": [         [InlineKeyboardButton("落地商务签", callback_data="落地商务签"),
                                                             InlineKeyboardButton("半年商务签", callback_data="半年商务签"),
                                                             InlineKeyboardButton("一年商务签", callback_data="一年商务签")],
                                                            [InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]
                                                   ]
                                    },
                                    "🌍 旅游签证": {
                                        "photo": "images/travel.png",
                                        "caption": "📜 旅游签证服务 | Tourist Visa \n\n"
                                                    
                                                    "🌍 轻松办理，畅游世界！ ✈️\n"
                                                    
                                                    "✅ 落地旅游签 – 适用于短期旅行，快速办理 🛫\n\n"
                                                    
                                                    "💼 服务内容：\n"
                                                    "🔹 签证申请 & 指导 📄\n"
                                                    "🔹 资料准备 & 审核 ✅\n"
                                                    "🔹 加急办理 & 续签 🔄\n"
                                                    
                                                    "📞 联系我们，开启您的旅行之旅！ 🚀✨\n\n",
                                        "buttons": [[InlineKeyboardButton("落地旅游签", callback_data="落地旅游签")],[InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]]
                                    },
                                     "📆 续签服务": {
                                        "photo": "images/183320304_291537002602003_2178100990049262973_n.jpg",
                                        "caption": "📜 **续签服务** | **Visa Renewal**  \n\n"
            
                                                    "🔄 **签证到期？轻松续签，无忧出行！**\n " 
                                                    
                                                    "✅ **签证到期续签** – 快速办理，避免逾期 📆 \n "
                                                    "⭐ **进阶续签** – 提供更优解决方案 🌟  \n\n"
                                                    
                                                    "📞 **联系我们，确保您的签证无缝衔接！** 🚀",
                                        "buttons": [[InlineKeyboardButton("签证到期续签", callback_data="签证到期续签")],[InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]]
                                    },
                                    "📑 护照服务": {
                                        "photo": "images/20221128212817498.jpg",
                                        "caption": "📜 **护照服务** | **Passport Services**  \n\n"
                                                "🔄 **护照到期？快速更换，畅行无忧！**  \n"
                                                
                                                "✅ **护照到期更换** – 高效办理，避免影响出行 📆  \n"
                                                "⭐ **进阶服务** – 提供更优更新方案 🌟 \n\n "
                                                
                                                "📞 **联系我们，轻松换新护照！** 🚀",
                                         "buttons": [[InlineKeyboardButton("护照到期更换", callback_data="护照到期更换")],[InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]]
                                    },
                                    "🚗 驾驶证办理": {
                                        "photo": "images/接机.jpg",
                                        "caption": "🚗 **驾驶证办理** | **Driver's License Services** \n\n "
                                                    
                                                    "✅ **驾驶证办理** – 快速申请，轻松上路 🏁  \n"
                                                    "🔄 **驾驶证更换** – 到期换证，续航无忧 📆  \n"
                                                    
                                                    "📞 **联系我们，轻松获取合法驾照！** 🚀",
                                        "buttons": [[InlineKeyboardButton("驾驶证办理", callback_data="驾驶证办理"),
                                                    InlineKeyboardButton("驾驶证更换", callback_data="驾驶证更换")],
                                                    [InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]
                                                   ]
                                    },

    


 "🌍 翻译与商务对接": {
        "photo": "images/翻译与商务.jpg",
        "caption": "🗣️ 翻译与商务对接 | Translation & Business Coordination \n\n"

                    "📌 语言翻译 – 提供专业翻译，助力高效沟通 🌍\n"
                    "📌 商务对接 – 搭建桥梁，促进国际合作 🤝\n"
                    
                    "📞 联系我们，让沟通更顺畅！ 🚀\n",
        "buttons": [
            [InlineKeyboardButton("语言翻译", callback_data="语言翻译"),
             InlineKeyboardButton("商务对接", callback_data="商务对接")]
        ]
    },
                                "语言翻译": {
                                    "photo": "mages/translator.jpg",
                                    "caption": "🗣️ **语言翻译** | **Language Translation** \n\n "
                                                "✅ **现场翻译** – 实时沟通，无障碍交流 🌍 \n "
                                                "📑 **商务会议翻译** – 专业精准，助力商务洽谈 💼\n  "
                                                "🎧 **专业同声传译** – 高效流畅，国际标准 🔊 \n\n "
                                                "📞 **联系我们，提供专业翻译服务！** 🚀",
                                    "buttons": [[InlineKeyboardButton("现场翻译", callback_data="现场翻译"),
                                                InlineKeyboardButton("商务会议翻译", callback_data="商务会议翻译")],
                                                [InlineKeyboardButton("专业同声传译", callback_data="专业同声传译")],
                                                [InlineKeyboardButton("🔙 返回", callback_data="🌍 翻译与商务对接")]
                                               ]
                                },
                                "商务对接": {
                                    "photo": "images/商务对接.jpg",
                                    "caption": "🤝 **商务对接** | **Business Coordination** \n\n "
                                               " ✅ **企业洽谈安排** – 助力高效商务合作 💼 \n "
                                               " ✅ **商务会议组织** – 精准策划，提升会议效率 🏢 \n "
                                               " ✅ **VIP私人助理** – 专业服务，尊享商务体验 🌟 \n\n "
                                                
                                               " 📞 **联系我们，让商务沟通更顺畅！** 🚀",
                                    "buttons": [[InlineKeyboardButton("企业洽谈安排", callback_data="企业洽谈安排"),
                                                InlineKeyboardButton("商务会议组织", callback_data="商务会议组织")],
                                                [InlineKeyboardButton("VIP-私人助理", callback_data="VIP-私人助理")],
                                                [InlineKeyboardButton("🔙 返回", callback_data="🌍 翻译与商务对接")]
                                               ]
                                },    






"🏛️ 企业落地支持": {
            "photo": "images/黄黑白蓝色商务企业招聘微信公众号封面 (1).png",
            "caption": "🏢 **企业落地支持** | **Business Establishment Support** \n\n "
                        "📌 **一站式服务，助力企业快速落地！** 🚀  \n"
                        
                        "✅ **公司注册** 🏢📑 – 高效办理，轻松落地 \n "
                        "✅ **公司注册** 🏢📑 – 高效办理，轻松落地  \n"
                        "✅ **政府审批** 🏛️✅ – 专业指导，顺利通过  \n"
                        "✅ **人才招聘** 👥🎯 – 精准匹配，助力团队建设  \n"
                        "✅ **财税法律** 💰⚖️ – 合规运营，安全无忧 \n\n" 
                        
                        "📞 **联系我们，让您的企业发展更顺畅！** 🌍✨",
            "buttons": [
                [InlineKeyboardButton("🛫 商务签证", callback_data="🛫 商务签证"),
                 InlineKeyboardButton("🌍 旅游签证", callback_data="🌍 旅游签证"),
                InlineKeyboardButton("📑 护照服务", callback_data="📑 护照服务")],
                 [InlineKeyboardButton("📆 续签服务", callback_data="📆 续签服务"),
                InlineKeyboardButton("🚗 驾驶证办理", callback_data="🚗 驾驶证办理")]
            ]
        },
                                "🛫 商务签证": {
                                        "photo": "images/商务签证.png",
                                        "caption": "📜 **商务签证简介 & 服务** | **Business Visa Services**   \n\n "                                  
                                                "✨ **专业办理，助力全球商务拓展！** ✨ \n "
                                                
                                                "📌 **商务签证** 适用于前往他国进行商务洽谈、会议、市场考察及商业合作，确保您的出行 **高效 & 合规**。\n\n  "
                                                
                                                "✅ **商务签证类型**：\n  "
                                                "🔹 **落地商务签** 🏢✈️ – 到达后快速办理，适用于短期商务活动  \n"
                                                "🔹 **半年商务签** 📆🌍 – 适用于中期商务出差 & 合作项目 \n "
                                                "🔹 **一年商务签** 🔄✅ – 适用于长期商务驻留 & 跨国业务拓展 \n\n "
                                                
                                                "💼 **服务内容**： \n "
                                                "🔹 签证申请 & 指导 📄  \n"
                                                "🔹 资料准备 & 审核 ✅ \n "
                                                "🔹 面签辅导 & 预约 🎯 \n "
                                                "🔹 加急办理 & 续签 🔄 \n "
                                                
                                                "📞 **立即联系我们，让您的商务之旅更加顺畅！** 🚀✨",
                                        "buttons": [         [InlineKeyboardButton("落地商务签", callback_data="落地商务签"),
                                                             InlineKeyboardButton("半年商务签", callback_data="半年商务签"),
                                                             InlineKeyboardButton("一年商务签", callback_data="一年商务签")],
                                                            [InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]
                                                   ]
                                    },
                                    "🌍 旅游签证": {
                                        "photo": "images/travel.png",
                                        "caption": "📜 旅游签证服务 | Tourist Visa \n\n"
                                                    
                                                    "🌍 轻松办理，畅游世界！ ✈️\n"
                                                    
                                                    "✅ 落地旅游签 – 适用于短期旅行，快速办理 🛫\n\n"
                                                    
                                                    "💼 服务内容：\n"
                                                    "🔹 签证申请 & 指导 📄\n"
                                                    "🔹 资料准备 & 审核 ✅\n"
                                                    "🔹 加急办理 & 续签 🔄\n"
                                                    
                                                    "📞 联系我们，开启您的旅行之旅！ 🚀✨\n\n",
                                        "buttons": [[InlineKeyboardButton("落地旅游签", callback_data="落地旅游签")],[InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]]
                                    },
                                     "📆 续签服务": {
                                        "photo": "images/183320304_291537002602003_2178100990049262973_n.jpg",
                                        "caption": "📜 **续签服务** | **Visa Renewal**  \n\n"
            
                                                    "🔄 **签证到期？轻松续签，无忧出行！**\n " 
                                                    
                                                    "✅ **签证到期续签** – 快速办理，避免逾期 📆 \n "
                                                    "⭐ **进阶续签** – 提供更优解决方案 🌟  \n\n"
                                                    
                                                    "📞 **联系我们，确保您的签证无缝衔接！** 🚀",
                                        "buttons": [[InlineKeyboardButton("签证到期续签", callback_data="签证到期续签")],[InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]]
                                    },
                                    "📑 护照服务": {
                                        "photo": "images/20221128212817498.jpg",
                                        "caption": "📜 **护照服务** | **Passport Services**  \n\n"
                                                "🔄 **护照到期？快速更换，畅行无忧！**  \n"
                                                
                                                "✅ **护照到期更换** – 高效办理，避免影响出行 📆  \n"
                                                "⭐ **进阶服务** – 提供更优更新方案 🌟 \n\n "
                                                
                                                "📞 **联系我们，轻松换新护照！** 🚀",
                                         "buttons": [[InlineKeyboardButton("护照到期更换", callback_data="护照到期更换")],[InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]]
                                    },
                                    "🚗 驾驶证办理": {
                                        "photo": "images/接机.jpg",
                                        "caption": "🚗 **驾驶证办理** | **Driver's License Services** \n\n "
                                                    
                                                    "✅ **驾驶证办理** – 快速申请，轻松上路 🏁  \n"
                                                    "🔄 **驾驶证更换** – 到期换证，续航无忧 📆  \n"
                                                    
                                                    "📞 **联系我们，轻松获取合法驾照！** 🚀",
                                        "buttons": [[InlineKeyboardButton("驾驶证办理", callback_data="驾驶证办理"),
                                                    InlineKeyboardButton("驾驶证更换", callback_data="驾驶证更换")],
                                                    [InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]
                                                   ]
                                    },
   
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
