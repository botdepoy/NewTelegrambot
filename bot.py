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
import json
from telegram.constants import ParseMode

def save_user_id(chat_id):
    try:
        with open("user_list.json", "r") as file:
            users = json.load(file)
    except:
        users = []

    found = False
    for user in users:
        if user["chat_id"] == chat_id:
            found = True
            break

    if not found:
        users.append({"chat_id": chat_id, "last_message_id": None})
        with open("user_list.json", "w") as file:
            json.dump(users, file)

# Replace with your actual bot token
BOT_TOKEN = "7896688608:AAGfcyafEuKiWWcMceHMjbVZp9oWB3666Yo"
ADMIN_ID = "7474650525"
WEB_APP_URL = "https://botdepoy.github.io/NewTelegrambot/form.html"

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Main menu options
MENU = [
    [KeyboardButton("✈️ 交通服务"), KeyboardButton("📜 证照办理"), KeyboardButton("🌍 翻译对接")],
    [KeyboardButton("🏛️ 企业落地"), KeyboardButton("🏨 酒店|租凭"), KeyboardButton("🚀 生活物资")],
    [KeyboardButton("👩‍💻 人工客服")]
]

# Data for response messages
RESPONSE_DATA = {
    "✈️ 交通服务": {
        "photo": "images/IMG_0106.JPG",
        "caption": "<b>🚖 交通服务 </b>\n\n"
                   "✨ 提供专业出行方案，助您畅行无忧！\n"
                   "🚗 机场准时接送，轻松出行 🛫\n"
                   "🚘 商务用车 / 高端专车 / VIP接待 \n"
                   "🧑‍✈️ 司机租赁 – 经验丰富，安全可靠 \n"
                   "✅ 安全 | 🚀 高效 | 💎 舒适\n\n"
                   "🌍无论是商务出行还是尊享专车,为您提供最佳方案!✨",
        "buttons": [
            [InlineKeyboardButton("🚗 专车服务", callback_data="🚗 专车服务"),
             InlineKeyboardButton("✈️ 机场接送", callback_data="✈️ 机场接送")]
            ]
    },
                                "🚗 专车服务": {
                                    "photo": "images/Web_Photo_Editor.jpg",
                                    "caption": "<b>🚘 高端商务车租赁服务</b>\n\n"
                                                
                                                "━━━━━━━━━━━━━━━\n"
                                                "<b>🚗 车型：丰田埃尔法 | 丰田 Granvia </b> \n"
                                                "⭐ 类型：高端商务 MPV \n "
                                                "🛋️ 特点：空间大，舒适乘坐  \n"
                                                "🎯 用途：接待｜出游｜婚礼｜接送机 \n\n"
                                                
                                                "💰 租金：\n"
                                                "・自驾：$200/天  \n"
                                                "・带司机：$300/天\n\n"
                                                "━━━━━━━━━━━━━━━\n"
                                                
                                                "<b>🚐 车型：大众 Multivan</b>  \n"
                                                "⭐ 类型：7座多功能商务车  \n"
                                                "🛋️ 特点：空间灵活，乘坐舒适  \n"
                                                "🎯 用途：商务｜家庭｜婚礼｜机场\n\n"
                                                
                                                "💰 租金：\n"
                                                "・自驾：$100/天  \n"
                                                "・带司机：$200/天\n"
                                                "━━━━━━━━━━━━━━━\n\n"

                                                "<b>🔹司机（中-英-柬）</b>: $100/天\n"
                                                "<b>🔹司机（英-柬） </b> : $60/天\n"
                                                "<b>🔹司机保镖带枪 </b>  : 120$/天\n"

                                                ,
                                    "buttons": [
                                                [InlineKeyboardButton(text="交通服务流程",url="https://t.me/HWLDSWFW_bot/Myapp")
                                                ,InlineKeyboardButton(text="💬 联系客服",url="https://t.me/LUODISWKF")],
                                                [InlineKeyboardButton("🔙 返回", callback_data="✈️ 交通服务")]
                                    ]            
                                },
                                "✈️ 机场接送": {
                                    "photo": "images/接机.jpg",
                                    "caption": "<b>✈️ 接送机 VIP 服务</b>\n\n"
                                                "━━━━━━━━━━━━━━\n"
                                                "<b>🚖 接机服务</b>\n"
                                                "📝 信息：时间｜地点｜联系方式\n"
                                                "📌 到达现场举牌等候\n\n"
                                                
                                                "━━━━━━━━━━━━━━\n"
                                                "<b>🚗 送机服务</b>\n"  
                                                "📝 信息：时间｜地点｜联系方式\n" 
                                                "📌 专人送达入口位置\n\n"  
                                                "━━━━━━━━━━━━━━\n"
                                                "💎 费用：$350（含VIP绿色通道）\n"
                                                ,
                                    "buttons": [
                                                [InlineKeyboardButton(text="机场接送流程",url="https://t.me/HWLDSWFW_bot/FlightService")
                                                ,InlineKeyboardButton(text="💬 联系客服",url="https://t.me/LUODISWKF")],
                                                [InlineKeyboardButton("🔙 返回", callback_data="✈️ 交通服务")]
                                    ]            
                                },


    "📜 证照办理": {
            "photo": "images/visa.jpg",
            "caption": "<b>🛂【证件办理服务】</b>\n" 
                        "快速办理签证、护照、劳工证、驾驶证等。\n\n"
                        "━━━━━━━━━━━━━━\n"
                        "<b>📌 入境签证</b>\n"  
                        "🔹 单次旅游签：85$\n"  
                        "🔹 单次商务签：105$\n"  
                        "📝 所需资料：护照首页 + 白底照片 + 入境机场/时间\n"  
                        "🕐 办理时间：1工作日\n"  
                        "⚠️ 逾期罚款：10$/天\n"  
                        "➕ 带关服务：+45$\n\n"
                        
                        "━━━━━━━━━━━━━━\n"
                        
                        "<b>🔁 续签服务</b>\n"  
                        "🔹 旅游签续签（1个月）：65$\n"  
                        "🔹 商务签续签（1个月~1年）：65$ - 300$\n"  
                        "📝 所需：护照原件（1年加劳工证照片）\n"  
                        "🕐 正常7工作日｜加急：+90$\n\n"
                        
                        "━━━━━━━━━━━━━━\n"
                        
                        "<b>📑 劳工证</b>\n"  
                        "🔹 当年劳工证：205$\n"  
                        "📝 护照页+签证页+二维码页\n"  
                        "🕐 正常7天｜加急：+70$\n"  
                        "⚠️ 逾期未续罚款：80$/年\n\n"
                        
                        "━━━━━━━━━━━━━━\n"
                        
                        "<b>🚗 驾照服务</b>\n"  
                        "🔹 换证：中国→柬：350$\n  "
                        "🔹 续签：柬→柬：70$\n"
                        "⚠️本人到场，当天出证）\n"

                        
                        "━━━━━━━━━━━━━━"
                        ,
            "buttons": [
                [InlineKeyboardButton(text="🛂 入境签证",url="https://t.me/HWLDSWFW_bot/passport"),
                InlineKeyboardButton(text="🔁 续签",url="https://t.me/HWLDSWFW_bot/xuqian")],
                [InlineKeyboardButton(text="🧾 劳工证",url="https://t.me/HWLDSWFW_bot/laogongzheng"),
                InlineKeyboardButton(text="🚗 驾驶证",url="https://t.me/HWLDSWFW_bot/jiashizheng")]
                ,[InlineKeyboardButton("💬人工客服", url="https://t.me/LUODISWKF")]
            ]
        },
                                # "🛫 商务签证": {
                                #         "photo": "images/商务签证.png",
                                #         "caption": "📜 **商务签证简介 & 服务** | **Business Visa Services**   \n\n "                                  
                                #                 "✨ **专业办理，助力全球商务拓展！** ✨ \n "
                                                
                                #                 "📌 **商务签证** 适用于前往他国进行商务洽谈、会议、市场考察及商业合作，确保您的出行 **高效 & 合规**。\n\n  "
                                                
                                #                 "✅ **商务签证类型**：\n  "
                                #                 "🔹 **落地商务签** 🏢✈️ – 到达后快速办理，适用于短期商务活动  \n"
                                #                 "🔹 **半年商务签** 📆🌍 – 适用于中期商务出差 & 合作项目 \n "
                                #                 "🔹 **一年商务签** 🔄✅ – 适用于长期商务驻留 & 跨国业务拓展 \n\n "
                                                
                                #                 "💼 **服务内容**： \n "
                                #                 "🔹 签证申请 & 指导 📄  \n"
                                #                 "🔹 资料准备 & 审核 ✅ \n "
                                #                 "🔹 面签辅导 & 预约 🎯 \n "
                                #                 "🔹 加急办理 & 续签 🔄 \n "
                                                
                                #                 "📞 **立即联系我们，让您的商务之旅更加顺畅！** 🚀✨",
                                #         "buttons": [         [InlineKeyboardButton("落地商务签", callback_data="落地商务签"),
                                #                              InlineKeyboardButton("半年商务签", callback_data="半年商务签"),
                                #                              InlineKeyboardButton("一年商务签", callback_data="一年商务签")],
                                #                             [InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]
                                #                    ]
                                #     },
                                #     "🌍 旅游签证": {
                                #         "photo": "images/travel.png",
                                #         "caption": "📜 旅游签证服务 | Tourist Visa \n\n"
                                                    
                                #                     "🌍 轻松办理，畅游世界！ ✈️\n"
                                                    
                                #                     "✅ 落地旅游签 – 适用于短期旅行，快速办理 🛫\n\n"
                                                    
                                #                     "💼 服务内容：\n"
                                #                     "🔹 签证申请 & 指导 📄\n"
                                #                     "🔹 资料准备 & 审核 ✅\n"
                                #                     "🔹 加急办理 & 续签 🔄\n"
                                                    
                                #                     "📞 联系我们，开启您的旅行之旅！ 🚀✨\n\n",
                                #         "buttons": [[InlineKeyboardButton("落地旅游签", callback_data="落地旅游签")],[InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]]
                                #     },
                                #      "📆 续签服务": {
                                #         "photo": "images/183320304_291537002602003_2178100990049262973_n.jpg",
                                #         "caption": "📜 **续签服务** | **Visa Renewal**  \n\n"
            
                                #                     "🔄 **签证到期？轻松续签，无忧出行！**\n " 
                                                    
                                #                     "✅ **签证到期续签** – 快速办理，避免逾期 📆 \n "
                                #                     "⭐ **进阶续签** – 提供更优解决方案 🌟  \n\n"
                                                    
                                #                     "📞 **联系我们，确保您的签证无缝衔接！** 🚀",
                                #         "buttons": [[InlineKeyboardButton("签证到期续签", callback_data="签证到期续签")],[InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]]
                                #     },
                                #     "📑 护照服务": {
                                #         "photo": "images/20221128212817498.jpg",
                                #         "caption": "📜 **护照服务** | **Passport Services**  \n\n"
                                #                 "🔄 **护照到期？快速更换，畅行无忧！**  \n"
                                                
                                #                 "✅ **护照到期更换** – 高效办理，避免影响出行 📆  \n"
                                #                 "⭐ **进阶服务** – 提供更优更新方案 🌟 \n\n "
                                                
                                #                 "📞 **联系我们，轻松换新护照！** 🚀",
                                #          "buttons": [[InlineKeyboardButton("护照到期更换", callback_data="护照到期更换")],[InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]]
                                #     },
                                #     "🚗 驾驶证办理": {
                                #         "photo": "images/接机.jpg",
                                #         "caption": "🚗 **驾驶证办理** | **Driver's License Services** \n\n "
                                                    
                                #                     "✅ **驾驶证办理** – 快速申请，轻松上路 🏁  \n"
                                #                     "🔄 **驾驶证更换** – 到期换证，续航无忧 📆  \n"
                                                    
                                #                     "📞 **联系我们，轻松获取合法驾照！** 🚀",
                                #         "buttons": [[InlineKeyboardButton("驾驶证办理", callback_data="驾驶证办理"),
                                #                     InlineKeyboardButton("驾驶证更换", callback_data="驾驶证更换")],
                                #                     [InlineKeyboardButton("🔙 返回", callback_data="📜 证照办理")]
                                #                    ]
                                #     },

    


 "🌍 翻译对接": {
        "photo": "images/翻译与商务.jpg",
        "caption": "🎙️ 语言翻译服务\n"
                    "🔹 现场翻译｜实时沟通\n\n"
                    "🔹 商务翻译｜术语精准\n"
                    "🔹 同声传译｜国际水准\n"
                    "🏅 等级：⭐⭐⭐ / ⭐⭐⭐⭐ VIP\n\n"
                    
                    "━━━━━━━━━━━━━━\n"
                    
                    "🤝 商务对接服务\n"
                    "🔹 洽谈安排｜高效连接\n"
                    "🔹 会议组织｜全程策划\n"
                    "🔹 VIP助理｜专属服务\n"
                    "🏅 等级：⭐⭐⭐ VIP\n"
,
        "buttons": [
            [InlineKeyboardButton(text="🎙️语言翻译",url="https://t.me/LUODISWKF?text=您好，我想了解语言翻译服务"),
            InlineKeyboardButton(text="🤝商务对接",url="https://t.me/LUODISWKF?text=您好，我想了解商务对接服务")
]
        ]
    },
                                # "语言翻译": {
                                #     "photo": "mages/translator.jpg",
                                #     "caption": "🗣️ **语言翻译** | **Language Translation** \n\n "
                                #                 "✅ **现场翻译** – 实时沟通，无障碍交流 🌍 \n "
                                #                 "📑 **商务会议翻译** – 专业精准，助力商务洽谈 💼\n  "
                                #                 "🎧 **专业同声传译** – 高效流畅，国际标准 🔊 \n\n "
                                #                 "📞 **联系我们，提供专业翻译服务！** 🚀",
                                #     "buttons": [[InlineKeyboardButton("现场翻译", callback_data="现场翻译"),
                                #                 InlineKeyboardButton("商务会议翻译", callback_data="商务会议翻译")],
                                #                 [InlineKeyboardButton("专业同声传译", callback_data="专业同声传译")],
                                #                 [InlineKeyboardButton("🔙 返回", callback_data="🌍 翻译与商务对接")]
                                #                ]
                                # },
                                # "商务对接": {
                                #     "photo": "images/商务对接.jpg",
                                #     "caption": "🤝 **商务对接** | **Business Coordination** \n\n "
                                #                " ✅ **企业洽谈安排** – 助力高效商务合作 💼 \n "
                                #                " ✅ **商务会议组织** – 精准策划，提升会议效率 🏢 \n "
                                #                " ✅ **VIP私人助理** – 专业服务，尊享商务体验 🌟 \n\n "
                                                
                                #                " 📞 **联系我们，让商务沟通更顺畅！** 🚀",
                                #     "buttons": [[InlineKeyboardButton("企业洽谈安排", callback_data="企业洽谈安排"),
                                #                 InlineKeyboardButton("商务会议组织", callback_data="商务会议组织")],
                                #                 [InlineKeyboardButton("VIP-私人助理", callback_data="VIP-私人助理")],
                                #                 [InlineKeyboardButton("🔙 返回", callback_data="🌍 翻译与商务对接")]
                                #                ]
                                # },    






"🏛️ 企业落地": {
            "photo": "images/黄黑白蓝色商务企业招聘微信公众号封面 (1).png",
            "caption": "<b>🏢【企业落地支持】</b>\n"
                      "一站式服务，助力企业快速落地 🚀\n\n"
                      "━━━━━━━━━━━━━━\n"
                      "📌 公司注册\n"
                      "• 🧾 公司注册\n"
                      "• 🧮 企业税务办理\n\n"
                      "━━━━━━━━━━━━━━\n"
                      "📌 政府审批\n"
                      "• 🏛 企业经营审批\n"
                      "• 🪪 许可证办理\n\n"
                      "━━━━━━━━━━━━━━\n"
                      "📌 人才招聘\n"
                      "• 👥 本地招聘\n"
                      "• 🎯 高端人才猎头\n\n"
                      "━━━━━━━━━━━━━━\n"
                      "📌 财税法律\n"
                      "• 💰 税务咨询\n"
                      "• ⚖️ 法律咨询\n",
            "buttons": [
                            [InlineKeyboardButton(text="✈️商务签",url="https://t.me/LUODISWKF?text=你好，我想咨询关于【商务签证】的服务。"),
                            InlineKeyboardButton(text="🌍旅游签",url="https://t.me/LUODISWKF?text=你好，我想咨询关于【旅游签证】的服务。"),
                            InlineKeyboardButton(text="📄护照服务",url="https://t.me/LUODISWKF?text=你好，我想咨询关于【护照服务】的服务。")],
                            [InlineKeyboardButton(text="📅续签服务",url="https://t.me/LUODISWKF?text=你好，我想咨询关于【续签服务】的服务。"),
                            InlineKeyboardButton(text="🚗驾驶证办理",url="https://t.me/LUODISWKF?text=你好，我想咨询关于【驾驶证办理】的服务。")
                        ]
            ]

        },
                                
   


"🏨 酒店|租凭": {
            "photo": "images/sofietel.jpg",
            "caption": "<b>🏨 【住宿与租赁服务】</b>\n\n"
                  "📌 高端酒店| 长，短租房屋 | 商务办公空间\n"
                  "🕰 无论短期考察还是长期定居，均可提供优质选择\n"
                  "💼 舒适 · 高效 · 快速对接 ✅\n",
            "buttons": [
                            [InlineKeyboardButton(text="🏨 酒店预定",callback_data="🏨 酒店预定"),
                            InlineKeyboardButton(text="🏨 公寓预定",callback_data="🏨 公寓预定"),
                        ]
            ]

        },
                         "🏨 酒店预定": {
                                    "photo": "images/Web_Photo_Editor.jpg",
                                    "caption": "📍 索菲特 Sofitel\n"
                                                "• 🛏 标准：双床房 ｜ 大床房 \n"
                                                "• 🌟 行政：Club套房 \n"
                                                "• 👑 高端：尊贵 ｜ 歌剧 ｜ 奢华体验\n"
                                                "• 🛎️ 礼遇：早餐｜酒会｜延迟退房\n\n\n"
                                                "━━━━━━━━━━━━━━━━━━━━━\n" 
                                                "📍 瑰丽 Rosewood\n"
                                                "• 🛏 行政：大床/双床房 ｜ 城景/河景\n"
                                                "• 🌟 尊贵：河景房 ｜尊贵大床 \n"
                                                "• 👑 套房：湄公河 ｜庄园 ｜瑰丽 \n"
                                                "• 🛎️ 礼遇：按摩｜观光｜饮品｜熨烫服"

                                                ,
                                    "buttons": [
                                                [InlineKeyboardButton(text="索菲特",url="https://t.me/HWLDSWFW_bot/myappcondorental")
                                                ,InlineKeyboardButton(text="瑰丽",url="https://t.me/HWLDSWFW_bot/HouseRental")],
                                                [InlineKeyboardButton(text="💬 联系客服",url="https://t.me/LUODISWKF")],
                                                [InlineKeyboardButton("🔙 返回", callback_data="🏨 酒店|租凭")]
                                    ]            
                                },
                                "🏨 公寓预定": {
                                    "photo": "images/接机.jpg",
                                    "caption": "<b>🏡 公寓房型速览</b>\n\n"
                                                "━━━━━━━━━━━━━━\n"
                                                "<b>🛋 两室一厅 </b>\n"
                                                "🛏 2卧 + 客厅\n"
                                                "🍳 厨房 + 1-2卫\n"
                                                "🪑 家具家电齐全\n"
                                                "🌤 部分带阳台\n"
                                                "✨ 🏊泳池｜🏋️健身房｜🌐Wi-Fi\n\n"
                                                
                                                "━━━━━━━━━━━━━━\n"
                                                "<b>🏠 三室一厅 </b>\n"  
                                                "🛏 3卧 + 大客厅\n" 
                                                "🍳 厨房 + 2-3卫\n"
                                                "❄️ 独立空调\n"  
                                                "🌤 双阳台\n"
                                                "✨ 🏊泳池｜🏋️健身房｜🧸儿童区｜🌐Wi-Fi\n"
                                                "━━━━━━━━━━━━━━\n" ,
                                    "buttons": [
                                                [InlineKeyboardButton(text="SKY-31 ",url="https://t.me/HWLDSWFW_bot/Sky31"),
                                                 InlineKeyboardButton(text="TK-Star ",url="https://t.me/HWLDSWFW_bot/tkstar")],
                                                [InlineKeyboardButton(text="💬 联系客服",url="https://t.me/LUODISWKF")],                    
                                                [InlineKeyboardButton("🔙 返回", callback_data="🏨 酒店|租凭")]
                                    ]            
                                },
    "🚀 生活物资": {
        "photo": "images/生活.jpg",
        "caption": "<b>🧺 新员工生活物品套装</b>\n\n"
                   "🛒 一站配齐，不用东奔西跑！\n\n"
                   "📦 套装内容:\n"
                   "🛏 卧室用品：四件套、枕芯\n"
                   "🚿 浴室用品：浴巾|毛巾|牙膏|牙刷|漱口杯\n"
                   "🧼 个人清洁：沐浴露、洗发水、肥皂\n"
                   "🏠 家庭必备：纸巾、蚊香液、蚊香器\n",
        "buttons": [
            [InlineKeyboardButton(text="💬 联系客服",url="https://t.me/LUODISWKF")]
        ]

    },

    "👩‍💻 人工客服": {
        "photo": "images/客服.jpg",
        "caption": "<b>落地商务客服</b>\n\n",
        "buttons": [
            [InlineKeyboardButton(text="💬 快速联系客服",url="https://t.me/LUODISWKF")]
        ]

    },

}

# Contact handler (replaces command `/contact`)
async def contact_handler(update: Update, context: CallbackContext):
    data = RESPONSE_DATA["👩‍💻 人工客服"]
    keyboard = InlineKeyboardMarkup(data["buttons"])
    if os.path.exists(data["photo"]):
        with open(data["photo"], "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=data["caption"], reply_markup=keyboard, parse_mode="HTML")
    else:
        await update.message.reply_text("客服图片未找到。", reply_markup=keyboard)

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
                    media=InputMediaPhoto(photo, caption=data["caption"], parse_mode="HTML"),  # ✅ Add parse_mode
                    reply_markup=keyboard
                )
        else:
            # If image is missing, just edit text
            await query.message.edit_caption(
                caption=data["caption"],
                reply_markup=keyboard,
                parse_mode="HTML"  # ✅ Add this line
            )



# Start Command
async def start(update: Update, context: CallbackContext):
    menu_markup = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text("📌 请选择服务:", reply_markup=menu_markup)
    save_user_id(update.message.chat_id)

   
# Handle Menu Selection
async def handle_menu(update: Update, context: CallbackContext):
    save_user_id(update.message.chat_id)
    text = update.message.text
    if text in RESPONSE_DATA:
        data = RESPONSE_DATA[text]
        keyboard = InlineKeyboardMarkup(data["buttons"])

        # Ensure the image file exists
        if os.path.exists(data["photo"]):
            with open(data["photo"], "rb") as photo:
                await update.message.reply_photo(
                        photo=photo,
                        caption=data["caption"],
                        reply_markup=keyboard,
                        parse_mode="HTML"  # ✅ Add this line
                    )

        else:
            await update.message.reply_text("🚨 图片不存在，请联系管理员!", reply_markup=keyboard)
    else:
        await update.message.reply_text("❌ 无效的选项，请选择正确的菜单项。")


async def broadcast(update: Update, context: CallbackContext):
    if str(update.message.chat_id) != ADMIN_ID:
        return await update.message.reply_text("❌ 没有权限")

    text = "<b>📢 系统公告</b>\n\n欢迎体验我们的新服务！"
    image_url = "images/IMG_0103.JPG"
    button_text = "点击查看"
    button_url = "https://t.me/yourbot"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(button_text, url=button_url)]
    ])

    try:
        with open("user_list.json", "r") as f:
            users = json.load(f)
    except:
        return await update.message.reply_text("⚠️ 用户数据读取失败")

    for user in users:
        try:
            msg = await context.bot.send_photo(
                chat_id=user["chat_id"],
                photo=image_url,
                caption=text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard
            )
            user["last_message_id"] = msg.message_id
        except Exception as e:
            print(f"Failed to send to {user['chat_id']}: {e}")

    with open("user_list.json", "w") as f:
        json.dump(users, f)

    await update.message.reply_text("✅ 广播发送成功")

async def update_broadcast(update: Update, context: CallbackContext):
    if str(update.message.chat_id) != ADMIN_ID:
        return await update.message.reply_text("❌ 没有权限")

    new_text = "<b>🛠️ 更新通知</b>\n我们已对公告内容进行了调整。"
    new_image = "https://yourdomain.com/updated_image.jpg"
    button_text = "查看更新"
    button_url = "https://t.me/yourbot?start=update"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(button_text, url=button_url)]
    ])

    try:
        with open("user_list.json", "r") as f:
            users = json.load(f)
    except:
        return await update.message.reply_text("⚠️ 用户数据读取失败")

    for user in users:
        if user["last_message_id"]:
            try:
                await context.bot.edit_message_media(
                    chat_id=user["chat_id"],
                    message_id=user["last_message_id"],
                    media=InputMediaPhoto(media=new_image, caption=new_text, parse_mode=ParseMode.HTML),
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Failed to update for {user['chat_id']}: {e}")

    await update.message.reply_text("✅ 广播已更新")

async def delete_broadcast(update: Update, context: CallbackContext):
    if str(update.message.chat_id) != ADMIN_ID:
        return await update.message.reply_text("❌ 没有权限")

    try:
        with open("user_list.json", "r") as f:
            users = json.load(f)
    except:
        return await update.message.reply_text("⚠️ 用户数据读取失败")

    for user in users:
        if user["last_message_id"]:
            try:
                await context.bot.edit_message_caption(
                    chat_id=user["chat_id"],
                    message_id=user["last_message_id"],
                    caption="🚫 此公告已删除。",
                    reply_markup=None
                )
            except Exception as e:
                print(f"Delete failed for {user['chat_id']}: {e}")

    await update.message.reply_text("✅ 广播已删除")


# Main Function
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(CommandHandler("contact", contact_handler))  # fixed line
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("update", update_broadcast))
    application.add_handler(CommandHandler("delete", delete_broadcast))



    # Start Polling
    application.run_polling()


if __name__ == "__main__":
    main()
