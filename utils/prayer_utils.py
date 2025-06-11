import requests
import pytz
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_fixed
from loguru import logger

from config import LAT, LON, TIMEZONE

# Uzbek names for the five daily Islamic prayers
PRAYER_NAMES = {
    "Fajr": "Bomdod",
    "Dhuhr": "Peshin",
    "Asr": "Asr",
    "Maghrib": "Shom",
    "Isha": "Xufton",
}

# Short Hijri month names in Uzbek transliteration
HIJRI_SHORT = [
    "Muh",
    "Saf",
    "Rab-I",
    "Rab-II",
    "Jum-I",
    "Jum-II",
    "Raj",
    "Sha",
    "Ram",
    "Shav",
    "Zul-Q",
    "Zulh",
]


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_prayer_data() -> dict:
    """
    Fetches prayer times and Hijri date from AlAdhan API.
    Retries up to 3 times on failure with 2s wait between.
    """
    try:
        url = f"https://api.aladhan.com/v1/timings?latitude={LAT}&longitude={LON}&school=1&timezonestring{TIMEZONE}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()["data"]
    except Exception as e:
        logger.error(f"Failed to fetch prayer data: {e}")
        raise


def get_next_prayer_short(timings: dict) -> str:
    """
    Determines the next upcoming prayer and how much time remains until it.
    Returns a short Uzbek message like: "Bomdod 03:12 (qoldi: 2 soat 15 daqiqa)"
    """
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)

    try:
        for key in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
            time_str = timings.get(key)
            if not time_str:
                continue  # skip if timing missing

            # Combine current date with prayer time and localize
            prayer_time = tz.localize(
                datetime.strptime(time_str, "%H:%M").replace(
                    year=now.year, month=now.month, day=now.day
                )
            )

            if now < prayer_time:
                delta = prayer_time - now
                hours, remainder = divmod(delta.seconds, 3600)
                minutes = remainder // 60
                return f"{PRAYER_NAMES[key]} {time_str} (qoldi: {hours} soat {minutes} daqiqa)"

        return "Bugun 🕌✅"
    except Exception as e:
        logger.warning(f"Failed to calculate next prayer: {e}")
        return "?"


def get_hijri_short(hijri: dict) -> str:
    """
    Formats Hijri date to short Uzbek format.
    Example: '13 Ram 1446'
    """
    try:
        month_index = int(hijri["month"]["number"]) - 1
        month_name = HIJRI_SHORT[month_index]
        return f"{hijri['day']} {month_name} {hijri['year']}"
    except Exception as e:
        logger.warning(f"Failed to format Hijri date: {e}")
        return "?"
