import telebot

TOKEN = "6442203249:AAH0GJh68n6YlE8kNOncCMp-wcdbRcru1hc"  # O'z bot tokeningizni kiriting
ADMIN_ID = 7490075648  # Xabarlarni qabul qiluvchi Telegram ID (Сарыбаев Дауран)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "👋 Salommmm! sizga nima kerak.")

# Har qanday xabarni admin ID'ga yuborish
@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    bot.send_message(ADMIN_ID, f"📩 Yangi xabar:\n\n👤 {message.from_user.first_name} (@{message.from_user.username})\n🆔 {message.from_user.id}\n\n✉ {message.text}")

# Botni doimiy ishlashga tushirish
bot.polling(none_stop=True)
