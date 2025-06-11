import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def _safe_int(key: str, default: int = 0) -> int:
    """Safely convert environment variable to int, logging warning if conversion fails."""
    try:
        return int(os.getenv(key, default))
    except ValueError:
        logger.warning(f"Invalid int for {key}, defaulting to {default}")
        return default


def _safe_float(key: str, default: float = 0.0) -> float:
    """Safely convert environment variable to float, logging warning if conversion fails."""
    try:
        return float(os.getenv(key, default))
    except ValueError:
        logger.warning(f"Invalid float for {key}, defaulting to {default}")
        return default


# Telegram API credentials
API_ID = _safe_int("API_ID")
API_HASH = os.getenv("API_HASH", "")
PHONE_NUMBER = _safe_int("PHONE_NUMBER")

# Weather API key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
if not WEATHER_API_KEY:
    logger.warning("Missing WEATHER_API_KEY")

# Geographic coordinates and timezone
LAT = _safe_float("LAT")
LON = _safe_float("LON")
TIMEZONE = os.getenv("TIMEZONE")
CITY = os.getenv("CITY")

logger.info(f"Config loaded: CITY={CITY}, TIMEZONE={TIMEZONE}, LAT={LAT}, LON={LON}")
