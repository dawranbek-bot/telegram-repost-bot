from telethon import TelegramClient, events
import asyncio
import time

api_id = 37228454
api_hash = "82b00418c470d6f0b31603ec40a0900d"  # <-- bu yerga api_hash qo'ying

source_channels = [
    "@ShimbayNukusTaxi1",
    "@moynaq_nokis2",
    "@nukus_kungrad47",
    "@kungrad_nukus001",
    "@taxtanukustaxigruppa",
    "@Qaraozeknukustaxi247",
    "@tortkulnukus",
    "@QANLIKOL_NOKIS_NUKUS_QANLIKOL",
    "@Kegeyli_Nukus_01",
    "@Shomanay_nukus",
    "@shimbaynokis3"
]

target_channel = "@jetkeriwshi_xabar"

client = TelegramClient("session", api_id, api_hash)

processed_groups = set()
processed_messages = set()

# ⏱ 5 minut limit
last_send_time = 0
DELAY = 300  # 5 minut

def can_send():
    global last_send_time
    return time.time() - last_send_time >= DELAY

def update_timer():
    global last_send_time
    last_send_time = time.time()


@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    global last_send_time

    try:
        # ===== ALBUM POST =====
        if event.message.grouped_id:

            if not can_send():
                print("⏳ Tanaffus: 5 minut kutish kerak (album)")
                return

            group_id = event.message.grouped_id

            if group_id in processed_groups:
                return

            processed_groups.add(group_id)

            await asyncio.sleep(2)

            messages = await client.get_messages(
                event.chat_id,
                limit=20
            )

            album = [
                msg for msg in messages
                if msg.grouped_id == group_id
            ]

            album.reverse()

            files = []
            caption = ""

            for msg in album:
                if msg.media:
                    files.append(msg.media)

                if msg.message:
                    caption = msg.message

            caption += "\n\n@jetkeriwshi_xabar - Bidziń jetkeriwshi xabar kanalǵa aǵza bolıń ✅"

            await client.send_file(
                target_channel,
                files,
                caption=caption
            )

            update_timer()

            print("📤 Album yuborildi")
            return

        # ===== ODDIY POST =====

        key = f"{event.chat_id}_{event.id}"

        if key in processed_messages:
            return

        processed_messages.add(key)

        if not can_send():
            print("⏳ Tanaffus: 5 minut kutish kerak (oddiy post)")
            return

        caption = (
            (event.message.message or "")
            + "\n\n@jetkeriwshi_xabar - jetkeriwshi xabar kanalǵa aǵza bolıń ✅"
        )

        if event.message.media:

            await client.send_file(
                target_channel,
                file=event.message.media,
                caption=caption
            )

        else:

            await client.send_message(
                target_channel,
                caption
            )

        update_timer()

        print("📤 Post yuborildi")

    except Exception as e:
        print("❌ Xato:", e)


print("🤖 Bot ishga tushdi...")
client.start()

with client:
    client.run_until_disconnected()
