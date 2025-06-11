from datetime import datetime
import pytz
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from loguru import logger

from config import WEATHER_API_KEY, CITY, TIMEZONE

# Mapping of English weather descriptions to Uzbek
WEATHER_DESCRIPTIONS = {
    "clear sky": "Quyoshli",
    "few clouds": "Biroz bulutli",
    "scattered clouds": "Bulutli",
    "broken clouds": "Bulutli",
    "overcast clouds": "Qorong‘i",
    "light rain": "Yengil yomgʻir",
    "moderate rain": "Oʻrtacha yomgʻir",
    "heavy intensity rain": "Kuchli yomgʻir",
    "very heavy rain": "Juda kuchli yomgʻir",
    "light snow": "Yengil qor",
    "snow": "Qor",
    "mist": "Tuman",
    "haze": "Tutun",
    "thunderstorm": "Momaqaldiroq",
    "drizzle": "Mayda yomgʻir",
}

# Simple in-memory cache to avoid excessive API calls
_cache = {"data": None, "timestamp": 0}
CACHE_TTL_SECONDS = 60 * 5  # Cache lifetime: 5 minutes


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_weather_data():
    """
    Fetches current weather data from OpenWeatherMap API.
    Retries up to 3 times with 2 seconds wait between attempts.
    """
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=en"
    )

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        logger.debug("Weather data fetched successfully from API.")
        return response.json()
    except requests.RequestException as e:
        logger.warning(f"Weather API request failed: {e}")
        raise


def get_weather_short() -> str:
    """
    Returns a short weather summary.
    Example: 'T: +23°C, Quyoshli'
    If data cannot be retrieved or parsed, returns fallback value.
    """
    tz = pytz.timezone(TIMEZONE)
    now_ts = datetime.now(tz).timestamp()

    # Use cached data if it's still valid
    if _cache["data"] and now_ts - _cache["timestamp"] < CACHE_TTL_SECONDS:
        data = _cache["data"]
    else:
        try:
            data = fetch_weather_data()
            _cache["data"] = data
            _cache["timestamp"] = now_ts
        except Exception as e:
            logger.error(f"Failed to fetch or cache weather data: {e}")
            return "T: ?°C, ?"

    try:
        desc_en = data["weather"][0]["description"].lower()
        desc = WEATHER_DESCRIPTIONS.get(desc_en, desc_en.capitalize())
        temp = round(data["main"]["temp"])
        return f"T: +{temp}°C, {desc}"
    except (KeyError, TypeError, IndexError) as e:
        logger.error(f"Failed to parse weather data: {e}")
        return "T: ?°C, ?"
