from telethon import TelegramClient, events
import asyncio
import time

api_id = 37228454
api_hash = "82b00418c470d6f0b31603ec40a0900d"

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

queue = asyncio.Queue()

DELAY = 25  # 25 sekund

processed = set()


# ================== QUEUE WORKER ==================
async def worker():
    while True:
        item = await queue.get()

        try:
            chat_id = item["chat_id"]
            msg = item["message"]

            caption = (msg.message or "") + "\n\n@jetkeriwshi_xabar"

            if msg.media:
                await client.send_file(
                    target_channel,
                    msg.media,
                    caption=caption
                )
            else:
                await client.send_message(
                    target_channel,
                    caption
                )

            print("📤 Yuborildi")
            await asyncio.sleep(DELAY)

        except Exception as e:
            print("❌ Xato:", e)

        queue.task_done()


# ================== HANDLER ==================
@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        key = f"{event.chat_id}_{event.id}"

        if key in processed:
            return

        processed.add(key)

        await queue.put({
            "chat_id": event.chat_id,
            "message": event.message
        })

        print("➕ Queue ga qo‘shildi")

    except Exception as e:
        print("❌ Handler xato:", e)


# ================== START ==================
async def main():
    await client.start()
    print("🤖 Bot ishga tushdi")

    asyncio.create_task(worker())  # worker start

    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
