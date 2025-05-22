from dotenv import load_dotenv
from telethon import TelegramClient, events
import requests
import os

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
source_channel = os.getenv('SOURCE_CHANNEL')
target_channel = os.getenv('TARGET_CHANNEL')
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

client = TelegramClient('session_name', api_id, api_hash)

MAX_DISCORD_LENGTH = 2000

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message_text = event.message.message  # Get the text from the message

    # Send to target Telegram channel
    await client.send_message(target_channel, message_text)

    # Send to Discord via webhook
    if message_text:
        chunks = [message_text[i:i+MAX_DISCORD_LENGTH] for i in range(0, len(message_text), MAX_DISCORD_LENGTH)]
        for chunk in chunks:
            data = { "content": chunk }
            try:
                response = requests.post(webhook_url, json=data)
                response.raise_for_status()
                print(f"Sent chunk to Discord: {chunk[:50]}...")
            except requests.exceptions.RequestException as e:
                print(f"Error sending to Discord: {e}")

async def main():
    await client.start()
    print("Listening for messages...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())

