import telebot
from telebot import types

# কনফিগারেশন
API_TOKEN = '8530900754:AAH-xyYJ1etm88QW2A_O3CabD5heC0-1Asc'
ADMIN_ID = 5716499834 
# প্রাইভেট চ্যানেলের আইডি বের করতে বটকে আগে অ্যাডমিন করুন, তারপর চ্যানেলে /id লিখে মেসেজ দিন। 
# সাময়িকভাবে নিচের ডামি আইডিগুলো থাকল।
CHANNELS = ['-1002271830209', '-1002302307565'] 
CHANNEL_LINKS = ['https://t.me/+YJGx3ZCvX1g5Yzlh', 'https://t.me/+YlNW7n3rYsE4M2Mx']

bot = telebot.TeleBot(API_TOKEN)

# জয়েন চেক করার ফাংশন
def is_subscribed(user_id):
    for chat_id in CHANNELS:
        try:
            member = bot.get_chat_member(chat_id, user_id)
            if member.status == 'left':
                return False
        except Exception:
            return False
    return True

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🎬 Watch Demo", callback_data="show_demo"),
            types.InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium"),
            types.InlineKeyboardButton("💬 Support", url="https://t.me/your_username")
        )
        bot.send_message(message.chat.id, f"স্বাগতম {message.from_user.first_name}! 🔥\nআমাদের প্রিমিয়াম ডেমো এবং সার্ভিস পেতে নিচের বাটনগুলো দেখুন।", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        for i, link in enumerate(CHANNEL_LINKS):
            markup.add(types.InlineKeyboardButton(f"Join Channel {i+1} 📢", url=link))
        markup.add(types.InlineKeyboardButton("Joined ✅", callback_data="check_sub"))
        bot.send_message(message.chat.id, "⚠️ আপনি আমাদের চ্যানেলগুলোতে জয়েন নেই!\nবটটি ব্যবহার করতে নিচের চ্যানেলগুলোতে জয়েন করে 'Joined ✅' বাটনে ক্লিক করুন।", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "check_sub":
        if is_subscribed(call.from_user.id):
            bot.answer_callback_query(call.id, "ধন্যবাদ! এখন আপনি বট ব্যবহার করতে পারবেন।")
            welcome(call.message)
        else:
            bot.answer_callback_query(call.id, "⚠️ আপনি এখনও সব চ্যানেলে জয়েন করেননি!", show_alert=True)
    
    elif call.data == "buy_premium":
        text = "💎 **Premium Plans** 💎\n\n✅ Monthly: 5$\n✅ Lifetime: 10$\n\n💳 **Payment Methods:**\n- Binance (USDT)\n- Bkash/Nagad\n- Telegram Stars\n\nপেমেন্ট করতে সরাসরি অ্যাডমিনকে মেসেজ দিন।"
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

bot.infinity_polling()
