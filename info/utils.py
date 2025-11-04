import requests
import feedparser


def get_weather():
    try:
        r = requests.get("https://wttr.in/Moscow?format=j1", timeout=5)
        data = r.json()
        temp = data["current_condition"][0]["temp_C"]
        desc = data["current_condition"][0]["weatherDesc"][0]["value"]
        return f"{temp}°C, {desc}"
    except Exception:
        return "Не удалось загрузить погоду"


def get_rss_news():
    try:
        feed = feedparser.parse("https://lenta.ru/rss")
        return feed.entries[:5]
    except Exception:
        return []
