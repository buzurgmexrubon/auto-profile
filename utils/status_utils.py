from datetime import datetime

from loguru import logger


def get_status(dt: datetime) -> str:
    """
    Determines a concise status string based on the given datetime object.
    Assumes the datetime object has its timezone information correctly set.

    Args:
        dt (datetime): The datetime object to check.

    Returns:
        str: A short status string in Uzbek.
    """
    try:
        hour = dt.hour
        day_of_week = dt.weekday()  # Monday: 0, Sunday: 6

        # Weekend statuses (Saturday: 5, Sunday: 6)
        if day_of_week in [5, 6]:
            if 8 <= hour < 12:
                return "Dam. Tong ☕"
            elif 12 <= hour < 20:
                return "Dam. Faol 🎉"
            else:
                return "Dam. Tinchlik 🌙"

        # Weekday statuses
        if 8 <= hour < 13:
            return "Ishda 🧑‍💻"
        elif 13 <= hour < 14:
            return "Tushlik 🍔"
        elif 14 <= hour < 18:
            return "Ishda 📈"
        elif 18 <= hour < 22:
            return "Shaxsiy vaqt 🔒"
        elif 22 <= hour < 24 or 0 <= hour < 6:
            return "Tungi 💤"
        else:  # Covers 6:00 to 7:59
            return "Ertalab ☀️"
    except AttributeError as e:
        logger.error(f"Invalid datetime object provided: {e}", exc_info=True)
        return "?"
    except Exception as e:
        logger.critical(
            f"An unexpected error occurred in get_status: {e}", exc_info=True
        )
        return "?"
