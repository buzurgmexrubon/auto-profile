# 🧠 AutoProfile

**AutoProfile** automatically updates your Telegram profile (first name, last name, and bio) every minute based on:

- 🕌 Upcoming prayer time
- 🗓️ Hijri and Gregorian date
- 🌤️ Local weather
- 🔄 Time-based status and profile photo

---

## 📸 Example Output

- **First name**: `Buzruk | Tong | 04:38`
- **Last name**: `Chor 11 Iyn | 15 Zul-Q 1446`
- **Bio**:
  `Bomdod 04:08 (qoldi: 0 soat 15 daqiqa)`
  `T: +21°C, Biroz bulutli`

---

## 📽️ Quickstart Video Guide

Watch the setup video

![AutoProfile demo](assets/demo.gif)

---

## 📁 Requirements

- Python 3.8+
- Telegram account
- [API credentials](https://my.telegram.org/)
- [OpenWeather API key](https://openweathermap.org/)
- `.env` configuration (see below)

---

## 🛠️ Environment Variables

Create a `.env` file based on `.env.example`:

```env
API_ID=your_telegram_api_id             # Required, from my.telegram.org
API_HASH=your_telegram_api_hash         # Required
PHONE_NUMBER=your_phone_number          # Required, in international format

WEATHER_API_KEY=openweather_api_key     # Required, from openweathermap.org
LAT=41.311081                           # Required, your city’s latitude
LON=69.240562                           # Required, your city’s longitude
TIMEZONE=Asia/Tashkent                  # Required, your local timezone (IANA)
CITY=Tashkent                           # Required, your city name in English
```

---

## 🐳 Docker (Recommended)

```bash
git clone https://github.com/buzurgmexrubon/autoprofile.git
cd autoprofile
cp .env.example .env   # Fill in the required values
```

Build and run:

```bash
docker build -t autoprofile .
docker run --env-file=.env -v /etc/localtime:/etc/localtime:ro autoprofile
```

If you're using **Windows**, map your timezone manually:

```bash
docker run --env-file=.env -v C:/path/to/timezone:/etc/timezone:ro autoprofile
```

---

## 🐍 Python (Alternative)

### Linux/macOS

```bash
git clone https://github.com/buzurgmexrubon/autoprofile.git
cd autoprofile
cp .env.example .env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Windows

```cmd
git clone https://github.com/buzurgmexrubon/autoprofile.git
cd autoprofile
copy .env.example .env
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python main.py
```

---

## 🧾 Systemd Service (Linux only)

To run as a background service on boot:

1. Copy the `.service` file:

   ```bash
   sudo cp autoprofile.service /etc/systemd/system/
   ```

2. Reload and start:

   ```bash
   sudo systemctl daemon-reexec
   sudo systemctl enable autoprofile
   sudo systemctl start autoprofile
   ```

Make sure `.env` file is placed and readable from the working directory inside the `.service` file.

---

## 🤝 Contributing

We welcome contributions!
Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting a pull request or issue.

---

## 📝 License

MIT License © 2025
