from dotenv import load_dotenv
from telethon.sync import TelegramClient
import os

# Telegram API Credentials
# Load environment variables once
load_dotenv('../.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Specify the target channel
target_channel = "https://t.me/lobelia4cosmetics"

# Directory to save images
output_dir = "lobelia_images"
os.makedirs(output_dir, exist_ok=True)

with TelegramClient("session_name", api_id, api_hash) as client:
    # Get messages only from the @lobelia4cosmetics channel
    messages = client.get_messages(target_channel, limit=50)  # Adjust limit as needed
    for msg in messages:
        if msg.photo:  # Check if the message contains a photo
            file_path = client.download_media(msg.photo, file=output_dir)
            print(f"Downloaded: {file_path}")
