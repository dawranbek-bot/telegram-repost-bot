import telebot

TOKEN = "8874804432:AAFV_kKsEzX1xL6VQXfRlRDl3y93noRtxH4c"  # O'z bot tokeningizni kiriting
ADMIN_ID = 5757866670  # Xabarlarni qabul qiluvchi Telegram ID (Сарыбаев Дауран)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "👋 Salommmm! Botga xabar yozing, u avtomatik ravishda adminga yuboriladi.")

# Har qanday xabarni admin ID'ga yuborish
@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    bot.send_message(ADMIN_ID, f"📩 Yangi xabar:\n\n👤 {message.from_user.first_name} (@{message.from_user.username})\n🆔 {message.from_user.id}\n\n✉ {message.text}")

# Botni doimiy ishlashga tushirish
bot.polling(none_stop=True)
