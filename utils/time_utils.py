from datetime import datetime
from loguru import logger

# Uzbek short weekday names (starting from Monday)
WEEKDAYS_SHORT = ["Du", "Se", "Chor", "Pay", "Jum", "Sha", "Yak"]

# Uzbek short month names (1-based index)
MONTHS_SHORT = [
    "Yan",
    "Fev",
    "Mar",
    "Apr",
    "May",
    "Iyn",
    "Iyul",
    "Avg",
    "Sen",
    "Okt",
    "Noy",
    "Dek",
]


def format_short_date(dt: datetime) -> str:
    """
    Returns a short Uzbek-formatted date string.
    Example: 'Chor 11 Iyn'
    """
    try:
        weekday = WEEKDAYS_SHORT[dt.weekday()]
        month = MONTHS_SHORT[dt.month - 1]
        return f"{weekday} {dt.day} {month}"
    except (IndexError, AttributeError) as e:
        logger.error(f"Error formatting date: {e}")
        return "??? ?? ???"


def format_time(dt: datetime) -> str:
    """
    Returns time in HH:MM format (24-hour).
    Example: '09:45'
    """
    try:
        return dt.strftime("%H:%M")
    except Exception as e:
        logger.error(f"Error formatting time: {e}")
        return "??:??"
