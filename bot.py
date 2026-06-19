import json
import requests

from datetime import time
from zoneinfo import ZoneInfo

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


BOT_TOKEN = "8874804432:AAFV_kKsEzX1xL6VQXfRlRDl3y93noRtxH4"
API_KEY = "eda2b5e469e24488923110846261906"


FILE = "obuna.json"


districts = {

    "📍 Chimboy": "Chimbay, Uzbekistan",
    "📍 Nukus": "Nukus, Uzbekistan",
    "📍 Taxiatosh": "Takhiatash, Uzbekistan",
    "📍 Qo‘ng‘irot": "Kungrad, Uzbekistan",
    "📍 Xo‘jayli": "Khojeli, Uzbekistan",
    "📍 Beruniy": "Beruniy, Uzbekistan",
    "📍 Amudaryo": "Amudarya, Uzbekistan",
    "📍 To‘rtko‘l": "Turtkul, Uzbekistan",
    "📍 Ellikqal’a": "Ellikkala, Uzbekistan",
    "📍 Mo‘ynoq": "Muynak, Uzbekistan",
    "📍 Kegeyli": "Kegeyli, Uzbekistan",
    "📍 Shumanay": "Shumanay, Uzbekistan",
    "📍 Qorao‘zak": "Qaraozek, Uzbekistan",
    "📍 Qanliko‘l": "Kanlikul, Uzbekistan",
    "📍 Taxtako‘pir": "Takhtakupyr, Uzbekistan"

}



def load_users():

    try:

        with open(
            FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return {}




def save_users(data):

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )





def weather(city):


    url = (

        "https://api.weatherapi.com/v1/forecast.json?"

        f"key={API_KEY}"

        f"&q={city}"

        "&days=10"

        "&aqi=no"

        "&alerts=no"

    )


    response = requests.get(
        url,
        timeout=15
    )


    data = response.json()



    if "error" in data:

        return "❌ Ob-havo topilmadi"



    current = data["current"]



    text = (

        f"🌤 {data['location']['name']}\n\n"


        f"📅 Bugun  🌡 {current['temp_c']}°C\n\n"


        f"Havo turi: ☁ {current['condition']['text']}\n"

        f"Shamol: 💨 {current['wind_kph']} km/soat\n"

        f"Namlik: 💧 {current['humidity']}%\n\n"


        "📆 10 kunlik prognoz:\n\n"

    )



    for i, day in enumerate(
        data["forecast"]["forecastday"]
    ):


        text += (

            f"{i+1}-kun  "

            f"{day['day']['mintemp_c']}°C"

            " - "

            f"{day['day']['maxtemp_c']}°C\n"

        )



    return text





async def start(
    update:Update,
    context:ContextTypes.DEFAULT_TYPE
):


    keyboard = []


    for item in districts:

        keyboard.append(
            [item]
        )


    keyboard.append(
        ["❌ Obunani bekor qilish"]
    )


    markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )



    await update.message.reply_text(

        "🌤 Qoraqalpog‘iston ob-havo boti\n\n"

        "Tumanni tanlang:",

        reply_markup=markup

    )







async def message_handler(
    update:Update,
    context:ContextTypes.DEFAULT_TYPE
):


    user_id = str(
        update.effective_user.id
    )


    text = update.message.text



    users = load_users()



    if text == "❌ Obunani bekor qilish":


        if user_id in users:

            del users[user_id]

            save_users(users)


            await update.message.reply_text(

                "✅ Obuna bekor qilindi"

            )

        else:

            await update.message.reply_text(

                "Siz obuna bo‘lmagansiz"

            )


        return




    if text in districts:


        users[user_id] = text

        save_users(users)



        result = weather(
            districts[text]
        )



        await update.message.reply_text(

            "✅ Obuna qilindi\n\n"

            "Xabar kelish vaqtlari:\n"

            "08:00\n"

            "13:00\n"

            "16:18\n\n"

            + result

        )


    else:


        await update.message.reply_text(

            "Tumanni tugma orqali tanlang"

        )







async def send_weather(
    context:ContextTypes.DEFAULT_TYPE
):


    users = load_users()



    for user_id, district in users.items():


        try:


            text = weather(

                districts[district]

            )



            await context.bot.send_message(

                chat_id=int(user_id),

                text=text

            )


        except Exception as e:

            print(e)







def main():


    app = Application.builder().token(
        BOT_TOKEN
    ).build()



    app.add_handler(

        CommandHandler(
            "start",
            start
        )

    )



    app.add_handler(

        MessageHandler(
            filters.TEXT,
            message_handler
        )

    )



    job = app.job_queue



    tashkent = ZoneInfo(
        "Asia/Tashkent"
    )



    job.run_daily(

        send_weather,

        time(
            8,
            0,
            tzinfo=tashkent
        )

    )


    job.run_daily(

        send_weather,

        time(
            13,
            0,
            tzinfo=tashkent
        )

    )


    job.run_daily(

        send_weather,

        time(
            16,
            51,
            tzinfo=tashkent
        )

    )



    print(
        "BOT ISHGA TUSHDI"
    )


    app.run_polling()






if __name__ == "__main__":

    main()
