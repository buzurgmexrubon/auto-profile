from datetime import datetime
import pytz
from loguru import logger

import config
from utils.weather_utils import get_weather_short
from utils.prayer_utils import fetch_prayer_data, get_next_prayer_short, get_hijri_short
from utils.time_utils import format_short_date, format_time
from utils.status_utils import get_status


def generate_display_fields():
    """
    Returns formatted strings for:
    - first_name: includes user name, status, and time
    - last_name: includes weekday/date and Hijri date
    - bio: includes next prayer and weather

    All data is localized to the configured timezone.
    """
    tz = pytz.timezone(config.TIMEZONE)
    now = datetime.now(tz)

    # Format current time and date
    dt = format_time(now)
    date = format_short_date(now)
    status = get_status(now)

    # Initialize fallback values
    prayer = "Namoz: ?"
    hijri = "Hijri: ???"
    weather = "T: ?°C, ?"

    try:
        # Fetch prayer and Hijri date info
        prayer_data = fetch_prayer_data()
        prayer = get_next_prayer_short(prayer_data.get("timings", {}))
        hijri = get_hijri_short(prayer_data.get("date", {}).get("hijri", {}))
    except Exception as e:
        logger.warning(f"Failed to fetch or parse prayer data: {e}")

    try:
        weather = get_weather_short()
    except Exception as e:
        logger.warning(f"Failed to fetch or format weather data: {e}")

    # Assemble the final fields
    first_name = f"{config.NAME} | {status} | {dt}"
    last_name = f"{date} | {hijri}"
    bio = f"{prayer}\n{weather}"

    return first_name, last_name, bio
