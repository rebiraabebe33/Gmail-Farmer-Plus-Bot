import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import random
import string

# ==========================================
# 1. BOT TOKEN 8656530199:AAFHtfUoYUdU7NCSOXIx-GZNz5kC7UC8NAk
# ==========================================
BOT_TOKEN = "8656530199:AAFHtfUoYUdU7NCSOXIx-GZNz5kC7UC8NAk"
bot = telebot.TeleBot(BOT_TOKEN)

# Main Menu (Reply Keyboard)
def main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("➕ Register a new Gmail", "📋 My accounts")
    markup.row("💰 Balance", "👥 My referrals")
    markup.row("⚙️ Settings", "❓ Help")
    return markup

# Credentials Generator (Maqaa fi Email Tasumaa Uumuu)
def generate_credentials():
    first_names = ["Moises", "John", "David", "Michael", "Alex", "James", "Robert"]
    last_names = ["Smith", "Johnson", "Brown", "Williams", "Miller", "Davis"]
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    num = random.randint(100, 999)
    email = f"{fn.lower()}{ln.lower()}{num}@gmail.com"
    chars = string.ascii_letters + string.digits
    password = "".join(random.choice(chars) for _ in range(10))
    year = random.randint(1995, 2003)
    return fn, ln, email, password, year

# Command /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Register Gmail accounts and get paid for it.\n\n"
        "For each account you will receive: from 0.15$ to 0.23$\n\n"
        "Everything is very simple. The bot provides you with data for registering a Gmail account, "
        "you copy it and go to Google. Create a Gmail account there, then return to the bot"
    )
    bot.reply_to(message, welcome_text, reply_markup=main_keyboard(), parse_mode="Markdown")

# Register a new Gmail Handler
@bot.message_handler(func=lambda message: message.text == "➕ Register a new Gmail")
def handle_register(message):
    fn, ln, email, pwd, year = generate_credentials()
    task_text = (
        "Register Gmail account using the specified data and get from 0.15$ to 0.23$\n\n"
        f"First name: {fn}\n"
        f"Last name: {ln}\n"
        f"Email: {email}\n"
        f"Password: {pwd}\n"
        f"Year of birth: {year}\n\n"
        "🔒 Be sure to use the specified data, otherwise the account will not be paid."
    )
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton("✅ Done", callback_data="done"))
    inline.add(InlineKeyboardButton("🚫 Cancel registration", callback_data="cancel_reg"))
    inline.add(InlineKeyboardButton("❓ How to create account", callback_data="how_to"))
    bot.send_message(message.chat.id, task_text, reply_markup=inline, parse_mode="Markdown")

# Balance Handler
@bot.message_handler(func=lambda message: message.text == "💰 Balance")
def handle_balance(message):
    bal_text = "Balance: 0$\nHold: 0$"
    inline = InlineKeyboardMarkup()
    inline.row(
        InlineKeyboardButton("💳 Payout", callback_data="payout"),
        InlineKeyboardButton("📜 Balance history", callback_data="history")
    )
    bot.send_message(message.chat.id, bal_text, reply_markup=inline, parse_mode="Markdown")

# My Accounts Handler
@bot.message_handler(func=lambda message: message.text == "📋 My accounts")
def handle_accounts(message):
    acc_text = (
        "uvefifeboxi316@gmail.com\n🔴 Registration is not over\nCreated: 12.08.26 at 5:38 PM\n\n"
        "useqava980@gmail.com\n🔴 Registration is not over\nCreated: 07.08.26 at 8:01 AM"
    )
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton("Next (2/30) >>", callback_data="acc_next"))
    bot.send_message(message.chat.id, acc_text, reply_markup=inline)

# Settings Handler
@bot.message_handler(func=lambda message: message.text == "⚙️ Settings")
def handle_settings(message):inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton("🔕 Disable balance notifications", callback_data="no_notif"))
    inline.row(
        InlineKeyboardButton("🔙 Back", callback_data="back_main"),
        InlineKeyboardButton("💵 Currency", callback_data="currency")
    )
    bot.send_message(message.chat.id, "Select an action from the menu list", reply_markup=inline)

# Help Handler
@bot.message_handler(func=lambda message: message.text == "❓ Help")
def handle_help(message):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton("❓ What is a hold?", callback_data="faq_hold"))
    inline.add(InlineKeyboardButton("❓ How to avoid SMS confirmation?", callback_data="faq_sms"))
    inline.add(InlineKeyboardButton("❓ Why is the account 'Unavailable'?", callback_data="faq_unavail"))
    inline.add(InlineKeyboardButton("↗️ Technical support", url="https://t.me/GmailFarmersSupport"))
    inline.add(InlineKeyboardButton("↗️ Buy accounts", url="https://t.me/accs_market_news"))
    bot.send_message(message.chat.id, "Most common questions:", reply_markup=inline)

# My Referrals Handler
@bot.message_handler(func=lambda message: message.text == "👥 My referrals")
def handle_referrals(message):
    bot_info = bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"
    ref_text = (
        "👨‍👩‍👧‍👦 Total referrals: 0\n\n"
        "In the first month:\n"
        "• 2fa 0.015$\n"
        "• 2fa 0.013$\n\n"
        f"🔗 Your referral link:\n{ref_link}"
    )
    bot.send_message(message.chat.id, ref_text, parse_mode="Markdown")

# Inline Callbacks Listener
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "payout":
        inline = InlineKeyboardMarkup()
        inline.add(InlineKeyboardButton("🪙 Crypto Bot | 3.0% | min: 1.03$", callback_data="payout_crypto"))
        inline.add(InlineKeyboardButton("💎 Tether (USDT-BEP-20) | 0% | min: 0.09$", callback_data="payout_usdt"))
        inline.add(InlineKeyboardButton("🔴 Tron (TRX) | 0% | min: 0.30$", callback_data="payout_trx"))
        inline.add(InlineKeyboardButton("🔙 Back", callback_data="back_main"))
        bot.send_message(call.message.chat.id, "Select Payment System", reply_markup=inline)
    elif call.data == "done":
        bot.answer_callback_query(call.id, "Account submitted for checking!")
    elif call.data == "cancel_reg":
        bot.edit_message_text("❌ Registration cancelled.", call.message.chat.id, call.message.message_id)

# Bot Execution
bot.infinity_polling()
