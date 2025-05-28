"""
Message templates for the BGMI Warrior Bot by IBR with multi-language support.
"""
from typing import Dict, Any, Optional

# Base language is English
MESSAGES = {
    "en": {
        # Welcome and help messages
        "welcome": (
            "🎮 *Yo, BGMI Warrior! Welcome to the DDoS Drop Zone!* 🎮\n\n"
            "🔥 *Gear up!* I'm your squad leader for smashing servers in BGMI!\n\n"
            "💣 *Battle Plan:*\n"
            "1️⃣ *Manual Mode:* You snipe—IP, port, duration, BOOM!\n"
            "2️⃣ *Auto Mode:* Drop IP and port, I'll frag with a random timer!\n\n"
            "✋ *Chicken Dinner Brake:* `stop all` to pull out!\n\n"
            "🔒 *Squad Rules:* Private needs `/auth`. Groups? 5 strikes/day unless you're a warlord!\n\n"
            "📡 *Intel:* `/help` for the full loot drop!\n\n"
            "*Built by Ibr, the BGMI Beast!*"
        ),
        "help": (
            "📡 *BGMI DDoS Bootcamp* 📡\n\n"
            "💥 *Snipe IPs & Ports with HTTP Canary for BGMI Domination!* 💥\n\n"
            "🎯 *Warzone Intel:* 🎯\n"
            "1️⃣ *Gear Up:* Grab *HTTP Canary* from Play Store—your scope! 📲\n"
            "2️⃣ *Lock On:* Hit *Start* (▶️) to scan the battlefield! 🌐\n"
            "3️⃣ *Drop In:* Launch BGMI, hit the lobby, wait for the timer! 🎮\n"
            "4️⃣ *Spot Enemies:* Flip to Canary, lock onto *UDP* packets! 📡\n"
            "5️⃣ *Target Locked:* Find ports *10,000-30,000* (e.g., `12345`). IP like `203.0.113.5`—grab it! ✂️\n"
            "6️⃣ *Strike Hard:*\n"
            "   - *Manual:* `<IP> <Port> <Duration>` (e.g., `203.0.113.5 14567 60`)\n"
            "   - *Auto:* `<IP> <Port>` (e.g., `203.0.113.5 14567`)\n\n"
            "🔫 *Hot Drops:*\n"
            "   - Manual: `203.0.113.5 14567 60`\n"
            "   - Auto: `203.0.113.5 14567`\n\n"
            "⚠️ *No-Fly Zones:*\n"
            "   - Blocked ports: `{blocked_ports}`—dodge 'em! 🚫\n"
            "   - Private? `/auth` for warlord status. Groups? {rate_limit}/day unless elite!\n\n"
            "💪 *Need Backup?* I've got your six—just holler!\n\n"
            "*Forged by Ibr, the BGMI War Machine!*"
        ),
        
        # Auth messages
        "auth_already_admin": "👑 *You're already a BGMI God!* No queue for legends!",
        "auth_already_authorized": (
            "🔥 *You're a BGMI Warlord!* 🔥\n\n"
            "⏰ *War Pass Expires:* `{expire_time}` ({timezone})\n"
            "Keep owning the battleground!"
        ),
        "auth_request_sent": (
            "🎮 *Warlord Request Dropped!* Stay frosty!\n\n"
            "👤 *ID:* `{user_id}`\n"
            "👑 *Tag:* @{username}\n\n"
            "Admins are scoping—warlord status incoming! 💣"
        ),
        "auth_admin_notification": (
            "🎮 *New BGMI Warlord Request!* 🎮\n\n"
            "👤 *Player:* @{username} (ID: `{user_id}`)\n"
            "💣 *Mission:* Approve or frag this wannabe!"
        ),
        "auth_approved": "👑 *You're a BGMI Warlord!* Unlimited strikes—drop 'em all! 🔥",
        "auth_rejected": "😡 *Warlord Denied!* Admin dropped you—GG no re!",
        "auth_removed": "💥 *Warlord Status Revoked!* Admin sniped you!",
        
        # Status messages
        "ping_response": (
            "🎯 *Ping!* Locked and loaded!\n"
            "⏰ *Uptime:* `{uptime}`\n"
            "🔥 *Active Strikes:* `{active_count}`\n"
            "💪 *Status:* Ready to deploy!"
        ),
        "stats": (
            "📊 *BGMI Warzone Report* 📊\n\n"
            "⏰ *Sitrep:* `{now}`\n"
            "👑 *Warlords:* `{authorized_users}`\n"
            "👤 *Total Users:* `{total_users}`\n"
            "💥 *Live Strikes:* `{active_count}`\n"
            "🔫 *Today's Kills:* `{today_actions}`\n"
            "🎯 *All-Time Kills:* `{total_actions}`\n\n"
            "{daily_actions}\n"
            "*Command the battleground!*"
        ),
        "usage": (
            "📊 *Group Strike Report!* 📊\n\n"
            "🔫 *Fired:* `{used}/{limit}`\n"
            "💣 *Ammo Left:* `{remaining}`\n\n"
            "⏰ *Reloads:* Midnight ({timezone})\n"
            "🎯 *Go Warlord:* `/auth` in private for endless frags!"
        ),
        "unlimited_usage": "🔥 *Unlimited BGMI Chaos!* Warlords like you don't reload! 💪",
        
        # Action messages
        "action_start": (
            "💥 *{mode} Mode Strike Incoming!* 💥\n\n"
            "🌍 *Target IP:* `{ip}`\n"
            "🔌 *Port:* `{port}`\n"
            "⏳ *Fuse:* `{duration}s`\n"
            "🔫 *Firepower:* `{thread_value}`\n\n"
            "🎮 *Dropping the DDoS bomb—brace yourself!*"
        ),
        "action_progress": (
            "🔥 *Strike LIVE!* `{remaining}s` to detonation!\n\n"
            "🌍 *IP:* `{ip}`\n"
            "🔌 *Port:* `{port}`\n"
            "🔫 *Firepower:* `{thread_value}`\n\n"
            "💣 *BGMI chaos in progress—hold the line!*"
        ),
        "action_complete": (
            "🏆 *Chicken Dinner Secured!* 🏆\n\n"
            "🌍 *IP:* `{ip}`\n"
            "🔌 *Port:* `{port}`\n"
            "⏱ *Strike Time:* `{duration}s`\n"
            "🔫 *Firepower:* `{thread_value}`\n\n"
            "🎮 *Server smoked—next target, warrior?*"
        ),
        "action_failed": "⚠️ *Strike Failed!* Error: `{error_msg}`",
        "action_stopped": "🛑 *Strike Aborted!* Squad's safe!",
        "no_action_to_stop": "⚠️ *No Strikes to Abort!* Zone's clear!",
        
        # Error messages
        "invalid_ip": "❌ *IP Miss!* That's not a target—scope again!\n\n*By Ibr, the BGMI Beast!*",
        "invalid_port": "❌ *Port Off-Target!* Aim 1-65535!\n\n*By Ibr, the BGMI Beast!*",
        "blocked_port": "⛔ *Port {port} is a Dead Zone!* Switch targets!\n\n*By Ibr, the BGMI Beast!*",
        "invalid_duration": "❌ *Timer Jam!* Set 1-600s—reload!\n\n*By Ibr, the BGMI Beast!*",
        "invalid_thread": "⚠️ *Thread Load Invalid!* Use value between 50-500!",
        "rate_limit_exceeded": (
            "⛔ *Ammo Depleted!* You've fired {limit} strikes today in this group!\n\n"
            "🎯 *Go Warlord:* `/auth` in private for unlimited frags!"
        ),
        "auth_required": "🚫 *Warlord Pass Needed!* Drop `/auth` to unlock!",
        "auth_required_private": "🚫 *Warlord Squad Only!* Drop `/auth` to join the fray! 🔥\n\n*Built by Ibr, the BGMI Beast!*",
        "admin_only": "🚫 *Squad Leaders Only!* Warlords get the intel!",
        "admin_private_only": "🚫 *Warlord Command Only!* Elite squad approves!",
        
        # Input format messages
        "auto_format": "⚠️ *Drop Fail!* Aim like `<ip> <port>`—lock on!\n\n*By Ibr, the BGMI Beast!*",
        "manual_format": (
            "⚠️ *Aim Off!* Lock it in:\n"
            "`<ip> <port> <duration>`\n\n"
            "*Ex:* `192.168.1.100 8080 60`—60s of chaos!\n\n"
            "*By Ibr, the BGMI Beast!*"
        ),
        "approve_format": "❌ *Command Fumble!* Drop `/approve <user_id> <duration>`!",
        "reject_format": "❌ *Target Missed!* Use `/reject <user_id>`—aim better!",
        "remove_format": "❌ *Kick Fail!* Use `/remove <user_id>`—lock on!",
        "invalid_duration_format": "❌ *Timer Glitch!* Use `Xd`, `Xh`, `Xm`, or `permanent`!",
        
        # History messages
        "history_empty": "🌌 *No Kills Yet!* Time to frag!",
        "history_title": "📜 *Your BGMI Kill Log!* 📜\n\n",
        "history_entry": "🌍 *IP:* `{ip}` | 🔌 *Port:* `{port}` | ⏳ `{duration}s` | *Mode:* `{mode}` | ⏰ `{timestamp}`\n\n",
        
        # Thread messages
        "thread_current": (
            "🔫 *Current Thread Load:* `{thread_value}`\n\n"
            "🎮 *Reload:* `/setthread <value>`—lock and load!"
        ),
        "thread_updated": "🎮 *Thread Locked at {thread_value}!* Your weapon's primed! 💥",
        
        # Mode messages
        "mode_changed": "🎮 *Switched to {mode} Mode!* Time to frag! 💣",
        
        # Active users messages
        "no_active_users": "🌌 *Dead Zone!* No squads in action!",
        "active_users_title": "🔥 *Active BGMI Warriors:* 🔥\n\n",
        "active_user_entry": (
            "👤 *Player:* {username} (ID: `{user_id}`)\n"
            "🎯 *Target:* `{ip}:{port}`\n"
            "⏳ *Remaining:* `{remaining}s`\n\n"
        ),
        
        # Broadcast messages
        "broadcast_empty": "❌ *Mic Jam!* Drop some war cries first!",
        "broadcast_preview": "🎤 *Squad Alert Preview:*\n\n`{message}`\n\nReady to hype the battleground?",
        "broadcast_processing": "📡 *Broadcasting message to all users...* 📡",
        "broadcast_complete": "🎉 *Squad Hyped!* War cries sent to {sent} users! ({failed} failed)",
        "broadcast_denied": "🚫 *Warlord Mic Only!* Grunts don't shout!",
    },
    
    # Hindi language (partial implementation - just a few examples)
    "hi": {
        "welcome": (
            "🎮 *नमस्ते, BGMI योद्धा! DDoS ड्रॉप जोन में आपका स्वागत है!* 🎮\n\n"
            "🔥 *तैयार हो जाओ!* मैं BGMI में सर्वर तोड़ने के लिए आपका स्क्वाड लीडर हूँ!\n\n"
            "💣 *युद्ध योजना:*\n"
            "1️⃣ *मैन्युअल मोड:* आप स्नाइप करें—IP, पोर्ट, अवधि, बूम!\n"
            "2️⃣ *ऑटो मोड:* IP और पोर्ट डालें, मैं रैंडम टाइमर के साथ फ्रैग करूंगा!\n\n"
            "✋ *चिकन डिनर ब्रेक:* बाहर निकलने के लिए `stop all`!\n\n"
            "🔒 *स्क्वाड नियम:* प्राइवेट को `/auth` की जरूरत है। ग्रुप्स? 5 स्ट्राइक्स/दिन जब तक आप योद्धा नहीं हैं!\n\n"
            "📡 *इंटेल:* पूरी जानकारी के लिए `/help`!\n\n"
            "*Ibr, BGMI बीस्ट द्वारा निर्मित!*"
        ),
        "help": (
            "📡 *BGMI DDoS बूटकैंप* 📡\n\n"
            "💥 *BGMI वर्चस्व के लिए HTTP Canary के साथ IP और पोर्ट स्नाइप करें!* 💥\n\n"
            "🎯 *युद्धक्षेत्र इंटेल:* 🎯\n"
            "1️⃣ *तैयारी:* Play Store से *HTTP Canary* डाउनलोड करें—आपका स्कोप! 📲\n"
            "2️⃣ *लॉक ऑन:* *Start* (▶️) दबाकर युद्धक्षेत्र स्कैन करें! 🌐\n"
            "3️⃣ *ड्रॉप इन:* BGMI लॉन्च करें, लॉबी में जाएं, टाइमर का इंतजार करें! 🎮\n"
            "4️⃣ *दुश्मन ढूंढें:* Canary पर जाएं, *UDP* पैकेट्स को लॉक करें! 📡\n"
            "5️⃣ *टारगेट लॉक:* पोर्ट *10,000-30,000* ढूंढें (उदा., `12345`)। IP जैसे `203.0.113.5`—पकड़ लें! ✂️\n"
            "6️⃣ *जोरदार हमला:*\n"
            "   - *मैन्युअल:* `<IP> <Port> <Duration>` (उदा., `203.0.113.5 14567 60`)\n"
            "   - *ऑटो:* `<IP> <Port>` (उदा., `203.0.113.5 14567`)\n\n"
            "🔫 *हॉट ड्रॉप्स:*\n"
            "   - मैन्युअल: `203.0.113.5 14567 60`\n"
            "   - ऑटो: `203.0.113.5 14567`\n\n"
            "⚠️ *नो-फ्लाई जोन:*\n"
            "   - ब्लॉक किए गए पोर्ट: `{blocked_ports}`—इनसे बचें! 🚫\n"
            "   - प्राइवेट? योद्धा स्थिति के लिए `/auth`। ग्रुप्स? {rate_limit}/दिन जब तक आप एलीट नहीं हैं!\n\n"
            "💪 *बैकअप चाहिए?* मैं आपका साथी हूँ—बस पुकारें!\n\n"
            "*Ibr, BGMI युद्ध मशीन द्वारा निर्मित!*"
        ),
    },
    "ur": {
        "welcome": (
            "🎮 *سلام، BGMI جنگجو! DDoS ڈراپ زون میں خوش آمدید!* 🎮\n\n"
            "🔥 *تیار ہو جاؤ!* میں BGMI میں سرورز توڑنے کے لیے تمہارا سکواڈ لیڈر ہوں!\n\n"
            "💣 *جنگی منصوبہ:*\n"
            "1️⃣ *مینوئل موڈ:* تم نشانہ لگاؤ—IP، پورٹ، مدت، بوم!\n"
            "2️⃣ *آٹو موڈ:* IP اور پورٹ ڈالو، میں رینڈم ٹائمر کے ساتھ فریگ کروں گا!\n\n"
            "✋ *چکن ڈنر بریک:* باہر نکلنے کے لیے `stop all`!\n\n"
            "🔒 *سکواڈ قوانین:* پرائیویٹ کو `/auth` کی ضرورت ہے۔ گروپس؟ 5 سٹرائیکس فی دن جب تک تم جنگجو نہ ہو!\n\n"
            "📡 *انٹیلی جنس:* مکمل معلومات کے لیے `/help`!\n\n"
            "*ابر، BGMI بیسٹ کے ذریعے بنایا گیا!*"
        ),
        "help": (
            "📡 *BGMI DDoS بوٹ کیمپ* 📡\n\n"
            "💥 *BGMI غلبہ کے لیے HTTP Canary کے ساتھ IPs اور پورٹس نشانہ بنائیں!* 💥\n\n"
            "🎯 *جنگی میدان کی معلومات:* 🎯\n"
            "1️⃣ *تیاری:* Play Store سے *HTTP Canary* حاصل کریں—تمہارا اسکوپ! 📲\n"
            "2️⃣ *لاک آن:* *Start* (▶️) دبائیں تاکہ جنگی میدان اسکین ہو! 🌐\n"
            "3️⃣ *ڈراپ ان:* BGMI لانچ کریں، لابی میں جائیں، ٹائمر کا انتظار کریں! 🎮\n"
            "4️⃣ *دشمنوں کا پتہ لگائیں:* Canary پر جائیں، *UDP* پیکٹس کو لاک کریں! 📡\n"
            "5️⃣ *ہدف لاک:* پورٹس *10,000-30,000* تلاش کریں (مثال، `12345`)۔ IP جیسے `203.0.113.5`—اسے پکڑو! ✂️\n"
            "6️⃣ *سخت حملہ:*\n"
            "   - *مینوئل:* `<IP> <Port> <Duration>` (مثال، `203.0.113.5 14567 60`)\n"
            "   - *آٹو:* `<IP> <Port>` (مثال، `203.0.113.5 14567`)\n\n"
            "🔫 *ہاٹ ڈراپس:*\n"
            "   - مینوئل: `203.0.113.5 14567 60`\n"
            "   - آٹو: `203.0.113.5 14567`\n\n"
            "⚠️ *نو-فلائی زونز:*\n"
            "   - بلاک شدہ پورٹس: `{blocked_ports}`—ان سے بچو! 🚫\n"
            "   - پرائیویٹ؟ جنگجو کی حیثیت کے لیے `/auth`۔ گروپس؟ {rate_limit}/دن جب تک ایلیٹ نہ ہو!\n\n"
            "💪 *بیک اپ کی ضرورت؟* میں تمہارے ساتھ ہوں—بس پکارو!\n\n"
            "*ابر، BGMI وار مشین کے ذریعے بنایا گیا!*"
        ),
    },
    "ar": {
        "welcome": (
            "🎮 *مرحبًا، محارب BGMI! مرحبًا بك في منطقة إسقاط DDoS!* 🎮\n\n"
            "🔥 *استعد!* أنا قائد فرقتك لتحطيم الخوادم في BGMI!\n\n"
            "💣 *خطة المعركة:*\n"
            "1️⃣ *الوضع اليدوي:* أنت القناص—IP، المنفذ، المدة، بوم!\n"
            "2️⃣ *الوضع التلقائي:* أسقط IP والمنفذ، سأقوم بالتدمير بمؤقت عشوائي!\n\n"
            "✋ *توقف عن العشاء الدجاجي:* `stop all` للانسحاب!\n\n"
            "🔒 *قواعد الفرقة:* الخاص يحتاج `/auth`. المجموعات؟ 5 ضربات/يوم ما لم تكن محاربًا!\n\n"
            "📡 *المعلومات:* `/help` للحصول على كامل المعلومات!\n\n"
            "*صنعه إبر، وحش BGMI!*"
        ),
        "help": (
            "📡 *معسكر تدريب DDoS لـ BGMI* 📡\n\n"
            "💥 *استهدف IPs والمنافذ باستخدام HTTP Canary للسيطرة على BGMI!* 💥\n\n"
            "🎯 *معلومات ساحة المعركة:* 🎯\n"
            "1️⃣ *التجهيز:* احصل على *HTTP Canary* من متجر Play—منظارك! 📲\n"
            "2️⃣ *التصويب:* اضغط *Start* (▶️) لمسح ساحة المعركة! 🌐\n"
            "3️⃣ *الإنزال:* شغّل BGMI، ادخل اللوبي، انتظر المؤقت! 🎮\n"
            "4️⃣ *رصد الأعداء:* انتقل إلى Canary، ركز على حزم *UDP*! 📡\n"
            "5️⃣ *الهدف مؤمن:* ابحث عن منافذ *10,000-30,000* (مثال، `12345`)، IP مثل `203.0.113.5`—احصل عليه! ✂️\n"
            "6️⃣ *الضرب بقوة:*\n"
            "   - *يدوي:* `<IP> <Port> <Duration>` (مثال، `203.0.113.5 14567 60`)\n"
            "   - *تلقائي:* `<IP> <Port>` (مثال، `203.0.113.5 14567`)\n\n"
            "🔫 *الإنزالات الساخنة:*\n"
            "   - يدوي: `203.0.113.5 14567 60`\n"
            "   - تلقائي: `203.0.113.5 14567`\n\n"
            "⚠️ *مناطق ممنوعة:* \n"
            "   - المنافذ المحظورة: `{blocked_ports}`—تجنبها! 🚫\n"
            "   - خاص؟ `/auth` للحصول على حالة المحارب. المجموعات؟ {rate_limit}/يوم ما لم تكن نخبة!\n\n"
            "💪 *تحتاج دعمًا؟* أنا معك—فقط نادِ!\n\n"
            "*صنعه إبر، آلة حرب BGMI!*"
        ),
    },
    "zh": {
        "welcome": (
            "🎮 *你好，BGMI战士！欢迎来到DDoS投放区！* 🎮\n\n"
            "🔥 *准备好！* 我是你摧毁BGMI服务器的战队领袖！\n\n"
            "💣 *作战计划：*\n"
            "1️⃣ *手动模式：* 你来狙击—IP，端口，持续时间，轰！\n"
            "2️⃣ *自动模式：* 提供IP和端口，我会用随机计时器开火！\n\n"
            "✋ *鸡肉晚餐刹车：* 输入 `stop all` 撤退！\n\n"
            "🔒 *战队规则：* 私人模式需要 `/auth`。群组？每天5次攻击，除非你是战神！\n\n"
            "📡 *情报：* 输入 `/help` 获取完整信息！\n\n"
            "*由Ibr，BGMI野兽打造！*"
        ),
        "help": (
            "📡 *BGMI DDoS训练营* 📡\n\n"
            "💥 *使用HTTP Canary狙击IP和端口，称霸BGMI！* 💥\n\n"
            "🎯 *战场情报：* 🎯\n"
            "1️⃣ *装备：* 从Play Store获取 *HTTP Canary*—你的瞄准镜！ 📲\n"
            "2️⃣ *锁定：* 点击 *Start* (▶️) 扫描战场！ 🌐\n"
            "3️⃣ *投放：* 启动BGMI，进入大厅，等待计时器！ 🎮\n"
            "4️⃣ *发现敌人：* 切换到Canary，锁定 *UDP* 数据包！ 📡\n"
            "5️⃣ *目标锁定：* 寻找端口 *10,000-30,000*（例如，`12345`）。IP如 `203.0.113.5`—抓住它！ ✂️\n"
            "6️⃣ *猛烈打击：*\n"
            "   - *手动：* `<IP> <Port> <Duration>`（例如，`203.0.113.5 14567 60`）\n"
            "   - *自动：* `<IP> <Port>`（例如，`203.0.113.5 14567`）\n\n"
            "🔫 *热门投放：*\n"
            "   - 手动：`203.0.113.5 14567 60`\n"
            "   - 自动：`203.0.113.5 14567`\n\n"
            "⚠️ *禁飞区：*\n"
            "   - 封锁端口：`{blocked_ports}`—避开它们！ 🚫\n"
            "   - 私人？使用 `/auth` 获取战神状态。群组？每天 {rate_limit} 次，除非你是精英！\n\n"
            "💪 *需要支援？* 我在你身后—随时呼叫！\n\n"
            "*由Ibr，BGMI战争机器打造！*"
        ),
    },
    
    # Add more languages as needed
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
        "hi": "Hindi",
        "ur": "Urdu",
        "ar": "Arabic",
        "zh": "Chinese",
        # Add more languages as they are implemented
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
