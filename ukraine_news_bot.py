import feedparser
import asyncio
import json
import os
from telegram import Bot

BOT_TOKEN = "8308467082:AAGpbzpiDc29rPGnynGpIgLdhbUoN90ls_U"
CHANNEL_ID = -1003592617376

RSS_FEEDS = {
    "Pravda": "https://www.pravda.com.ua/rss/",
    "TSN": "https://tsn.ua/rss/full.rss",
    "Suspilne": "https://suspilne.media/rss/all.xml",
    "Ukrinform": "https://www.ukrinform.ua/rss/block-lastnews",
    "Svoboda": "https://www.radiosvoboda.org/api/zrqiteous",
    "NV": "https://nv.ua/rss/all.xml",
    "Censor": "https://censor.net/ru/rss/news",
    "UNIAN": "https://rss.unian.net/site/news_ukr.rss",
    "Ukranews": "https://ukranews.com/rss",
}

SEEN_FILE = "seen.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

async def check_news():
    bot = Bot(token=BOT_TOKEN)
    seen = load_seen()

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            link = entry.link
            if link not in seen:
                title = entry.title
                message = f"📰 <b>{source}</b>\n\n{title}\n\n🔗 {link}"
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=message,
                    parse_mode="HTML"
                )
                seen.add(link)
                await asyncio.sleep(5)

    save_seen(seen)

async def main():
    print("Bot started! Checking news every 2 minutes...")
    while True:
        await check_news()
        await asyncio.sleep(120)

if __name__ == "__main__":
    asyncio.run(main())