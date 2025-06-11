import os
import asyncio
from datetime import datetime
from telethon import TelegramClient, functions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
import pytz

import config
from utils.bio_utils import generate_display_fields

# Configure Loguru logger
logger.add(
    "bot.log",
    rotation="1 week",
    compression="zip",
    level="INFO",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
)

PROFILE_PIC_DIR = "profile_pics"


async def update_profile_photo(client: TelegramClient):
    """
    Updates Telegram profile photo based on current weekday (e.g., mon.jpg).
    """
    tz = pytz.timezone(config.TIMEZONE)
    now = datetime.now(tz)
    weekday = now.strftime("%a").lower()  # e.g., mon, tue, ...
    filename = f"{weekday}.jpg"
    path = os.path.join(PROFILE_PIC_DIR, filename)

    if not os.path.exists(path):
        logger.warning(f"Profile photo not found: {path}")
        return

    try:
        file = await client.upload_file(path)
        await client(functions.photos.UploadProfilePhotoRequest(file))
        logger.info(f"Profile photo updated: {filename}")
    except Exception as e:
        logger.error(f"Failed to update profile photo: {e}")


async def update_profile(client: TelegramClient):
    """
    Updates first name, last name, and bio fields of the Telegram profile.
    Retries up to 3 times if an error occurs.
    """
    tz = pytz.timezone(config.TIMEZONE)
    now = datetime.now(tz)

    for attempt in range(1, 4):
        try:
            first_name, last_name, bio = generate_display_fields()
            await client(
                functions.account.UpdateProfileRequest(
                    first_name=first_name, last_name=last_name, about=bio
                )
            )
            logger.info(f"{now.strftime('%H:%M:%S')} — Profile updated successfully.")
            break
        except Exception as e:
            logger.warning(
                f"{now.strftime('%H:%M:%S')} — Attempt {attempt}/3 failed: {e}"
            )
            await asyncio.sleep(2)
    else:
        logger.error("Profile update failed after 3 attempts.")


async def start_scheduler(client: TelegramClient):
    """
    Starts the APScheduler to periodically update profile and photo.
    """
    scheduler = AsyncIOScheduler()
    # Update profile every 1 minute
    scheduler.add_job(update_profile, "interval", minutes=1, args=[client])
    # Update profile photo at midnight (00:00)
    scheduler.add_job(update_profile_photo, "cron", hour=0, minute=0, args=[client])
    scheduler.start()

    logger.info("Scheduler started (Profile update every 1 minute).")
    await asyncio.Event().wait()  # Keep the process alive


async def main():
    """
    Initializes Telegram client and starts the scheduler.
    """
    try:
        client = TelegramClient("AutoProfileUpdater", config.API_ID, config.API_HASH)
        await client.start(phone=config.PHONE_NUMBER)
        logger.success("Successfully connected to Telegram account.")
        await start_scheduler(client)
    except Exception as e:
        logger.critical(f"Startup failed: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped by user.")
