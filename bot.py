from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

TOKEN = "8874804432:AAFV_kKsEzX1xL6VQXfRlRDl3y93noRtxH4"

ADMIN_ID = 7490075648

MESSAGE = 1


courses = {
    "google": {
        "name": "GOOGLE PROJECT MANAGEMENT",
        "image": "1.jpg",
        "price": "50 min swm"
    },
    "microsoft": {
        "name": "Microsoft Project Management: Build Job-Ready Skills",
        "image": "2.jpg",
        "price": "70 min swm"
    },
    "ibm": {
        "name": "IBM IT Support",
        "image": "3.jpg",
        "price": "100 min swm"
    },
    "meta": {
        "name": "META FRONT-END DEVELOPER",
        "image": "4.jpg",
        "price": "100 min swm"
    },
    "aws": {
        "name": "AWS GENERATIV AI",
        "image": "5.jpg",
        "price": "30 min swm"
    }
}


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎓 Sertifikat olish", callback_data="certificate")]
    ])


def certificate_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("GOOGLE PROJECT MANAGEMENT", callback_data="google")],
        [InlineKeyboardButton("Microsoft Project Management: Build Job-Ready Skills", callback_data="microsoft")],
        [InlineKeyboardButton("IBM IT Support", callback_data="ibm")],
        [InlineKeyboardButton("META FRONT-END DEVELOPER", callback_data="meta")],
        [InlineKeyboardButton("AWS GENERATIV AI", callback_data="aws")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
    ])


def course_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 Adminga murojaat", callback_data="contact_admin")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="certificate")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Kerakli bo'limni tanlang.",
        reply_markup=main_menu()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "back_main":
        await query.edit_message_text(
            "Kerakli bo'limni tanlang.",
            reply_markup=main_menu()
        )
        return

    if data == "certificate":
        await query.edit_message_text(
            "Sertifikatni tanlang:",
            reply_markup=certificate_menu()
        )
        return

    if data in courses:

        context.user_data["course"] = data

        course = courses[data]

        await query.message.delete()

        with open(course["image"], "rb") as photo:
            await context.bot.send_photo(
                chat_id=query.message.chat.id,
                photo=photo,
                caption=f"{course['name']}\n\nNarxi: {course['price']}",
                reply_markup=course_menu()
            )

        return

    if data == "contact_admin":

        await query.message.reply_text(
            "Xabaringizni yozing:"
        )

        return MESSAGE


async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    course = context.user_data.get("course", "")

    user = update.effective_user

    msg = f"""
📩 Yangi murojaat

Kurs:
{courses[course]['name']}

Foydalanuvchi:
{user.full_name}

Username:
@{user.username}

ID:
{user.id}

Xabar:
{text}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=msg
    )

    await update.message.reply_text(
        "✅ Xabaringiz adminga yuborildi."
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END


app = Application.builder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(buttons, pattern="contact_admin")
    ],
    states={
        MESSAGE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message)
        ]
    },
    fallbacks=[
        CommandHandler("cancel", cancel)
    ],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(conv)

print("Bot ishga tushdi...")

app.run_polling()
