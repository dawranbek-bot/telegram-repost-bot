```python
from telethon import TelegramClient, events, Button

api_id = 37228454
api_hash = "82b00418c470d6f0b31603ec40a0900d"

BOT_TOKEN = "8874804432:AAFV_kKsEzX1xL6VQXfRlRDl3y93noRtxH4"

client = TelegramClient("taxi_bot", api_id, api_hash)

channels = {
    "shimbay1": "@ShimbayNukusTaxi1",
    "moynaq": "@moynaq_nokis2",
    "kungrad1": "@nukus_kungrad47",
    "kungrad2": "@kungrad_nukus001",
    "taxatakopir": "@taxtanukustaxigruppa",
    "qaraozek": "@Qaraozeknukustaxi247",
    "tortkul": "@tortkulnukus",
    "qanlikol": "@QANLIKOL_NOKIS_NUKUS_QANLIKOL",
    "kegeyli": "@Kegeyli_Nukus_01",
    "shomanay": "@Shomanay_nukus",
    "shimbay2": "@shimbaynokis3"
}

main_buttons = [
    [Button.inline("🚕 TAKSILARNI TANGLANG", b"menu")]
]

menu_buttons = [
    [Button.inline("SHIMBAY-NUKUS", b"shimbay1")],
    [Button.inline("MOYNAQ-NUKUS", b"moynaq")],
    [Button.inline("KUNGRAD-NUKUS", b"kungrad1")],
    [Button.inline("KUNGRAD-NUKUS2", b"kungrad2")],
    [Button.inline("TAXATAKOPIR-NUKUS", b"taxatakopir")],
    [Button.inline("QARAOZEK-NUKUS", b"qaraozek")],
    [Button.inline("TORTKUL-NUKUS", b"tortkul")],
    [Button.inline("QANLIKOL-NUKUS", b"qanlikol")],
    [Button.inline("KEGEYLI-NUKUS", b"kegeyli")],
    [Button.inline("SHOMANAY-NUKUS", b"shomanay")],
    [Button.inline("SHIMBAY-NUKUS2", b"shimbay2")],
    [Button.inline("⬅️ ORQAGA", b"back")]
]


@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond(
        "Salom 👋\n\nBu yerdan hamma viloyatlarga taksilar bor.\n\nTaksilarni tanlang:",
        buttons=main_buttons
    )


@client.on(events.CallbackQuery)
async def callback(event):

    data = event.data.decode()

    if data == "menu":
        await event.edit(
            "Kerakli yo'nalishni tanlang:",
            buttons=menu_buttons
        )
        return

    if data == "back":
        await event.edit(
            "Salom 👋\n\nBu yerdan hamma viloyatlarga taksilar bor.\n\nTaksilarni tanlang:",
            buttons=main_buttons
        )
        return

    if data in channels:

        channel = channels[data]

        try:
            messages = await client.get_messages(
                channel,
                limit=2
            )

            await event.respond(
                f"📢 {channel} kanalidagi oxirgi 2 ta xabar:"
            )

            for msg in reversed(messages):

                if msg.media:

                    await client.send_file(
                        event.chat_id,
                        msg.media,
                        caption=msg.text or ""
                    )

                else:

                    await client.send_message(
                        event.chat_id,
                        msg.text or "Matnsiz xabar"
                    )

        except Exception as e:
            await event.respond(f"Xato: {e}")


client.start(bot_token=BOT_TOKEN)
print("Bot ishga tushdi...")
client.run_until_disconnected()
```
