"""
🌟 Message Templates for BGMI Warrior Bot by IBR 🌟
✨ Enhanced with beautiful UI, animations, and premium styling ✨
"""
from typing import Dict, Any, Optional

# Message Templates
MESSAGES = {
    "en": {
        "welcome": (
            "╔═══════════════════════════════════╗\n"
            "║    🌟 BGMI WARRIOR BOT 🌟          ║\n"
            "║         💎 PREMIUM EDITION 💎      ║\n"
            "╚═══════════════════════════════════╝\n\n"
            "🎭 **Welcome, Elite Warrior!** 🎭\n\n"
            "🚀 **QUANTUM BATTLE MODES** 🚀\n"
            "🎯 **Precision Mode:** Manual Control\n"
            "🤖 **AI Mode:** Smart Auto Strike\n"
            "⚡ **Blitz Mode:** Fast Attack\n"
            "🌊 **Tsunami Mode:** Heavy Strike\n\n"
            "🎨 **New Features:**\n"
            "• 🌈 **Rainbow UI** with animations\n"
            "• 🗣️ **Voice Commands** (Premium)\n"
            "• 📊 **Real-time Analytics**\n"
            "• 🎪 **Interactive Mini-Games**\n"
            "• 🏆 **Achievement System**\n\n"
            "💫 **Emergency Stop:** Type `🛑 STOP ALL 🛑`\n\n"
            "🎪 **Type `/menu` for Interactive Dashboard!**\n\n"
            "🔮 *Crafted by IBR Technologies* 🔮"
        ),
        
        "help": (
            "╔══════════════════════════════════════╗\n"
            "║     🌟 BGMI Command Center 🌟        ║\n"
            "║         💎 Elite Guide 💎            ║\n"
            "╚══════════════════════════════════════╝\n\n"
            "🎯 **Master the Battlefield** 🎯\n\n"
            "🔧 **Setup Guide** 🔧\n"
            "📱 Download **HTTP Canary** from Play Store\n"
            "🎮 Launch BGMI and enter lobby\n"
            "🔍 Scan UDP packets (10K-30K ports)\n"
            "🎯 Target IP format: `203.0.113.5`\n\n"
            "🚀 **Enhanced Battle Modes** 🚀\n\n"
            "🎯 **Manual Attack:** `IP PORT DURATION`\n"
            "   Example: `203.0.113.5 14567 60`\n\n"
            "🤖 **AI Auto Mode:** `IP PORT`\n"
            "   Example: `203.0.113.5 14567`\n\n"
            "⚡ **Blitz Mode:** `blitz IP PORT`\n"
            "   Example: `blitz 203.0.113.5 14567`\n\n"
            "🌊 **Tsunami Mode:** `tsunami IP PORT1,PORT2,PORT3`\n"
            "   Example: `tsunami 203.0.113.5 14567,14568,14569`\n\n"
            "⚠️ **Blocked Zones:** `{blocked_ports}`\n"
            "🔒 Private chats: `/auth` required\n"
            "👥 Groups: {rate_limit}/day limit\n\n"
            "🌟 **Need help? I'm your AI companion!** 🌟\n\n"
            "*Built by IBR, King of BGMI!*"
        ),
        
        "auth_already_admin": "👑 *You're already a BGMI God!* No queue for legends!",
        "auth_request_sent": (
            "🎮 *Warrior request sent!* Stay frosty!\n\n"
            "👤 *ID:* `{user_id}`\n"
            "👑 *Tag:* @{username}\n\n"
            "Admins are watching—warrior status incoming! 💣"
        ),
        "auth_approved": "👑 *You're a BGMI Warlord!* Unlimited strikes—drop 'em all! 🔥",
        "auth_rejected": "😡 *Warlord Denied!* Admin dropped you—GG no re!",
        "ping_response": (
            "🎯 *Ping!* Locked & loaded!\n"
            "⏰ *Uptime:* `{uptime}`\n"
            "🔥 *Active strikes:* `{active_count}`\n"
            "💪 *Status:* Ready for deployment!"
        ),
        "action_start": (
            "💥 *{mode} Mode Strike Incoming!* 💥\n\n"
            "🌍 *Target IP:* `{ip}`\n"
            "🔌 *Port:* `{port}`\n"
            "⏳ *Fuse:* `{duration}s`\n"
            "🔫 *Firepower:* `{thread_value}`\n\n"
            "🎮 *DDoS bomb dropping—brace for impact!*"
        ),
        "language_changed": "🌐 *Language changed!* Now speaking {language}! 🎉",
        "ai_command_understood": "🤖 *AI command understood!* 🎯 Target: `{target}` 🚀 Initiating strike...",
    },
    
    # Hindi Language Messages - Full Translation
    "hi": {
        "welcome": (
            "╔═══════════════════════════════════╗\n"
            "║    🌟 BGMI WARRIOR BOT 🌟          ║\n"
            "║         💎 हिंदी संस्करण 💎         ║\n"
            "╚═══════════════════════════════════╝\n\n"
            "🎭 **स्वागत है, योद्धा!** 🎭\n\n"
            "🚀 **युद्ध मोड** 🚀\n"
            "🎯 **सटीक मोड:** मैनुअल कंट्रोल\n"
            "🤖 **AI मोड:** स्मार्ट ऑटो स्ट्राइक\n"
            "⚡ **ब्लिट्ज मोड:** तेज़ हमला\n"
            "🌊 **सुनामी मोड:** भारी हमला\n\n"
            "🎨 **नई सुविधाएं:**\n"
            "• 🌈 **इंद्रधनुष UI** एनिमेशन के साथ\n"
            "• 🗣️ **वॉयस कमांड** (प्रीमियम)\n"
            "• 📊 **रियल-टाइम एनालिटिक्स**\n"
            "• 🎪 **इंटरेक्टिव मिनी-गेम्स**\n"
            "• 🏆 **उपलब्धि सिस्टम**\n\n"
            "💫 **आपातकालीन स्टॉप:** `🛑 STOP ALL 🛑` टाइप करें\n\n"
            "🎪 **इंटरेक्टिव डैशबोर्ड के लिए `/menu` टाइप करें!**\n\n"
            "🔮 *IBR Technologies द्वारा बनाया गया* 🔮"
        ),
        
        "help": (
            "╔══════════════════════════════════════╗\n"
            "║     🌟 BGMI कमांड सेंटर 🌟           ║\n"
            "║         💎 हिंदी गाइड 💎             ║\n"
            "╚══════════════════════════════════════╝\n\n"
            "🎯 **युद्धक्षेत्र में महारत हासिल करें** 🎯\n\n"
            "🔧 **सेटअप गाइड** 🔧\n"
            "📱 Play Store से **HTTP Canary** डाउनलोड करें\n"
            "🎮 BGMI लॉन्च करें और लॉबी में प्रवेश करें\n"
            "🔍 UDP पैकेट स्कैन करें (10K-30K पोर्ट्स)\n"
            "🎯 टारगेट IP फॉर्मेट: `203.0.113.5`\n\n"
            "🚀 **बेहतर युद्ध मोड** 🚀\n\n"
            "🎯 **सटीक हमला:** `IP PORT DURATION`\n"
            "   उदाहरण: `203.0.113.5 14567 60`\n\n"
            "🤖 **AI ऑटो मोड:** `IP PORT`\n"
            "   उदाहरण: `203.0.113.5 14567`\n\n"
            "⚡ **ब्लिट्ज मोड:** `blitz IP PORT`\n"
            "   उदाहरण: `blitz 203.0.113.5 14567`\n\n"
            "🌊 **सुनामी मोड:** `tsunami IP PORT1,PORT2,PORT3`\n"
            "   उदाहरण: `tsunami 203.0.113.5 14567,14568,14569`\n\n"
            "⚠️ **प्रतिबंधित क्षेत्र:** `{blocked_ports}`\n"
            "🔒 प्राइवेट चैट: `/auth` आवश्यक\n"
            "👥 ग्रुप्स: {rate_limit}/दिन सीमा\n\n"
            "🌟 **मदद चाहिए? मैं आपका AI साथी हूं!** 🌟\n\n"
            "*IBR द्वारा बनाया गया, BGMI का राजा!*"
        ),
        
        "auth_already_admin": "👑 *आप पहले से ही BGMI गॉड हैं!* दिग्गजों के लिए कोई कतार नहीं!",
        "auth_request_sent": (
            "🎮 *योद्धा अनुरोध भेजा गया!* धैर्य रखें!\n\n"
            "👤 *ID:* `{user_id}`\n"
            "👑 *टैग:* @{username}\n\n"
            "एडमिन देख रहे हैं—योद्धा स्टेटस आ रहा है! 💣"
        ),
        "auth_approved": "👑 *आप BGMI योद्धा हैं!* असीमित हमले—सब गिरा दो! 🔥",
        "auth_rejected": "😡 *योद्धा मना!* एडमिन ने आपको गिरा दिया—GG no re!",
        "ping_response": (
            "🎯 *पिंग!* लॉक्ड एंड लोडेड!\n"
            "⏰ *अपटाइम:* `{uptime}`\n"
            "🔥 *सक्रिय हमले:* `{active_count}`\n"
            "💪 *स्थिति:* तैनाती के लिए तैयार!"
        ),
        "action_start": (
            "💥 *{mode} मोड हमला आ रहा है!* 💥\n\n"
            "🌍 *टारगेट IP:* `{ip}`\n"
            "🔌 *पोर्ट:* `{port}`\n"
            "⏳ *फ्यूज:* `{duration}s`\n"
            "🔫 *फायरपावर:* `{thread_value}`\n\n"
            "🎮 *DDoS बम गिराया जा रहा है—तैयार हो जाइए!*"
        ),
        "language_changed": "🌐 *भाषा बदल गई!* अब {language} में बात करते हैं! 🎉",
        "ai_command_understood": "🤖 *AI कमांड समझ गया!* 🎯 टारगेट: `{target}` 🚀 हमला शुरू...",
    },
    
    # Roman Urdu Language Support
    "ur": {
        "welcome": (
            "╔═══════════════════════════════════╗\n"
            "║    🌟 BGMI WARRIOR BOT 🌟          ║\n"
            "║         💎 Urdu Version 💎         ║\n"
            "╚═══════════════════════════════════╝\n\n"
            "🎭 **Khush Aamdeed, Jangju!** 🎭\n\n"
            "🚀 **Jung Ke Modes** 🚀\n"
            "🎯 **Manual Mode:** Khud Control\n"
            "🤖 **AI Mode:** Smart Auto Strike\n"
            "⚡ **Blitz Mode:** Tez Hamla\n"
            "🌊 **Tsunami Mode:** Bara Hamla\n\n"
            "🎨 **Nayi Features:**\n"
            "• 🌈 **Rainbow UI** animations ke saath\n"
            "• 🗣️ **Voice Commands** (Premium)\n"
            "• 📊 **Real-time Analytics**\n"
            "• 🎪 **Interactive Mini-Games**\n"
            "• 🏆 **Achievement System**\n\n"
            "💫 **Emergency Stop:** `🛑 STOP ALL 🛑` type karen\n\n"
            "🎪 **Interactive Dashboard ke liye `/menu` type karen!**\n\n"
            "🔮 *IBR Technologies ne banaya hai* 🔮"
        ),
        
        "help": (
            "╔══════════════════════════════════════╗\n"
            "║     🌟 BGMI Command Center 🌟        ║\n"
            "║         💎 Urdu Guide 💎             ║\n"
            "╚══════════════════════════════════════╝\n\n"
            "🎯 **Battlefield mein Mahir Baniye** 🎯\n\n"
            "🔧 **Setup Guide** 🔧\n"
            "📱 Play Store se **HTTP Canary** download karen\n"
            "🎮 BGMI launch karen aur lobby mein jayen\n"
            "🔍 UDP packets scan karen (10K-30K ports)\n"
            "🎯 Target IP format: `203.0.113.5`\n\n"
            "🚀 **Behtareen Jung Modes** 🚀\n\n"
            "🎯 **Manual Attack:** `IP PORT DURATION`\n"
            "   Misal: `203.0.113.5 14567 60`\n\n"
            "🤖 **AI Auto Mode:** `IP PORT`\n"
            "   Misal: `203.0.113.5 14567`\n\n"
            "⚡ **Blitz Mode:** `blitz IP PORT`\n"
            "   Misal: `blitz 203.0.113.5 14567`\n\n"
            "🌊 **Tsunami Mode:** `tsunami IP PORT1,PORT2,PORT3`\n"
            "   Misal: `tsunami 203.0.113.5 14567,14568,14569`\n\n"
            "⚠️ **Blocked Zones:** `{blocked_ports}`\n"
            "🔒 Private chats: `/auth` zaroori\n"
            "👥 Groups: {rate_limit}/din limit\n\n"
            "🌟 **Madad chahiye? Main apka AI dost hun!** 🌟\n\n"
            "*IBR ne banaya hai, BGMI ka badshah!*"
        ),
        
        "auth_already_admin": "👑 *Ap pehle se hi BGMI God hain!* Legends ke liye queue nahi!",
        "auth_request_sent": (
            "🎮 *Warrior request bhej diya!* Sabr rakhen!\n\n"
            "👤 *ID:* `{user_id}`\n"
            "👑 *Tag:* @{username}\n\n"
            "Admins dekh rahe hain—warrior status aa raha hai! 💣"
        ),
        "auth_approved": "👑 *Ap BGMI Warrior hain!* Unlimited attacks—sab gira do! 🔥",
        "auth_rejected": "😡 *Warrior denied!* Admin ne ap ko drop kiya—GG no re!",
        "ping_response": (
            "🎯 *Ping!* Tayar hai!\n"
            "⏰ *Uptime:* `{uptime}`\n"
            "🔥 *Active attacks:* `{active_count}`\n"
            "💪 *Status:* Deployment ke liye ready!"
        ),
        "action_start": (
            "💥 *{mode} Mode attack aa raha hai!* 💥\n\n"
            "🌍 *Target IP:* `{ip}`\n"
            "🔌 *Port:* `{port}`\n"
            "⏳ *Timer:* `{duration}s`\n"
            "🔫 *Power:* `{thread_value}`\n\n"
            "🎮 *DDoS bomb drop kar rahe hain—tayyar ho jaiye!*"
        ),
        "language_changed": "🌐 *Zuban badal gayi!* Ab {language} mein baat karte hain! 🎉",
        "ai_command_understood": "🤖 *AI samjh gaya!* 🎯 Target: `{target}` 🚀 Attack shuru...",
    },
    
    # Chinese Language Support  
    "zh": {
        "welcome": (
            "╔═══════════════════════════════════╗\n"
            "║    🌟 BGMI WARRIOR BOT 🌟          ║\n"
            "║         💎 中文版本 💎             ║\n"
            "╚═══════════════════════════════════╝\n\n"
            "🎭 **欢迎，精英战士！** 🎭\n\n"
            "🚀 **量子战斗模式** 🚀\n"
            "🎯 **精确模式:** 手动控制\n"
            "🤖 **AI模式:** 智能自动攻击\n"
            "⚡ **闪电模式:** 快速攻击\n"
            "🌊 **海啸模式:** 大规模攻击\n\n"
            "🎨 **新功能:**\n"
            "• 🌈 **彩虹UI** 带动画效果\n"
            "• 🗣️ **语音命令** (高级版)\n"
            "• 📊 **实时分析仪表板**\n"
            "• 🎪 **互动迷你游戏**\n"
            "• 🏆 **成就系统**\n\n"
            "💫 **紧急停止:** 输入 `🛑 STOP ALL 🛑`\n\n"
            "🎪 **互动仪表板请输入 `/menu`!**\n\n"
            "🔮 *由IBR科技精心打造* 🔮"
        ),
        
        "help": (
            "╔══════════════════════════════════════╗\n"
            "║     🌟 BGMI指挥中心 🌟               ║\n"
            "║         💎 中文指南 💎               ║\n"
            "╚══════════════════════════════════════╝\n\n"
            "🎯 **掌握战场** 🎯\n\n"
            "🔧 **设置指南** 🔧\n"
            "📱 从Play Store下载 **HTTP Canary**\n"
            "🎮 启动BGMI并进入大厅\n"
            "🔍 扫描UDP数据包 (10K-30K端口)\n"
            "🎯 目标IP格式: `203.0.113.5`\n\n"
            "🚀 **增强战斗模式** 🚀\n\n"
            "🎯 **精确攻击:** `IP 端口 持续时间`\n"
            "   示例: `203.0.113.5 14567 60`\n\n"
            "🤖 **AI自动模式:** `IP 端口`\n"
            "   示例: `203.0.113.5 14567`\n\n"
            "⚡ **闪电模式:** `blitz IP 端口`\n"
            "   示例: `blitz 203.0.113.5 14567`\n\n"
            "🌊 **海啸模式:** `tsunami IP 端口1,端口2,端口3`\n"
            "   示例: `tsunami 203.0.113.5 14567,14568,14569`\n\n"
            "⚠️ **限制区域:** `{blocked_ports}`\n"
            "🔒 私人聊天: 需要 `/auth`\n"
            "👥 群组: {rate_limit}/天 限制\n\n"
            "🌟 **需要帮助？我是你的AI伙伴！** 🌟\n\n"
            "*IBR制作，BGMI之王！*"
        ),
        
        "auth_already_admin": "👑 *您已经是BGMI之神！* 传奇无需排队！",
        "auth_request_sent": (
            "🎮 *战士申请已发送！* 请保持冷静！\n\n"
            "👤 *ID:* `{user_id}`\n"
            "👑 *标签:* @{username}\n\n"
            "管理员正在审核—战士身份即将到来! 💣"
        ),
        "auth_approved": "👑 *您是BGMI战士！* 无限攻击—全部击落! 🔥",
        "auth_rejected": "😡 *战士被拒绝！* 管理员击落了您—GG no re!",
        "ping_response": (
            "🎯 *Ping!* 准备就绪!\n"
            "⏰ *运行时间:* `{uptime}`\n"
            "🔥 *活跃攻击:* `{active_count}`\n"
            "💪 *状态:* 准备部署!"
        ),
        "action_start": (
            "💥 *{mode}模式攻击来袭！* 💥\n\n"
            "🌍 *目标IP:* `{ip}`\n"
            "🔌 *端口:* `{port}`\n"
            "⏳ *引信:* `{duration}s`\n"
            "🔫 *火力:* `{thread_value}`\n\n"
            "🎮 *DDoS炸弹投放中—准备冲击！*"
        ),
        "language_changed": "🌐 *语言已更改！* 现在用{language}交流! 🎉",
        "ai_command_understood": "🤖 *AI理解了！* 🎯 目标: `{target}` 🚀 开始攻击...",
    }
}

def get_message(key: str, lang: str = "en", **kwargs) -> str:
    """
    Get a message template by key and language with formatting.
    
    Args:
        key: Message key
        lang: Language code (defaults to "en")
        **kwargs: Format arguments
    
    Returns:
        Formatted message string
    """
    # Fall back to English if language not available
    if lang not in MESSAGES:
        lang = "en"
        
    # Get message template
    message_template = MESSAGES.get(lang, MESSAGES["en"]).get(key)
    
    # Fall back to English if message not available in selected language
    if message_template is None:
        message_template = MESSAGES["en"].get(key, f"Missing message: {key}")
        
    # Format message with provided arguments
    if kwargs:
        try:
            return message_template.format(**kwargs)
        except KeyError as e:
            # Log or handle missing format argument
            return f"Error formatting message {key}: {e}"
    
    return message_template

def get_available_languages() -> Dict[str, str]:
    """
    Get list of available languages.
    
    Returns:
        Dictionary of language codes and names
    """
    return {
        "en": "English",
        "hi": "हिंदी",
        "ur": "Roman Urdu", 
        "zh": "中文"
    }

def get_user_language(user_id: int, database=None, default: str = "en") -> str:
    """
    Get user's preferred language.
    
    Args:
        user_id: Telegram user ID
        database: Optional database instance for fetching language preference
        default: Default language if not set
    
    Returns:
        Language code
    """
    if database:
        # This needs to be run in an async context
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're already in an async context
                language = loop.create_task(database.get_user_language(user_id, default))
                return language.result()
            else:
                # We need to run this in a new event loop
                return asyncio.run(database.get_user_language(user_id, default))
        except:
            # Fall back to default language if there's any issue
            return default
    return default
