import json
import os
import feedparser
from bs4 import BeautifulSoup
from config import RSS_FEEDS, SENT_FILE


def load_sent():
    if not os.path.exists(SENT_FILE):
        return []
    try:
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_sent(sent_list):
    sent_list = sent_list[-500:]
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(sent_list, f, ensure_ascii=False, indent=2)


def _clean(html_text: str) -> str:
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text(" ", strip=True)[:800]


def fetch_news(limit_per_feed=20):
    sent = set(load_sent())
    items = []

    for feed_url in RSS_FEEDS:
        try:
            parsed = feedparser.parse(feed_url)
            for entry in parsed.entries[:limit_per_feed]:
                link = entry.get("link", "").strip()
                if not link or link in sent:
                    continue
                items.append({
                    "title": entry.get("title", "").strip(),
                    "summary": _clean(entry.get("summary") or entry.get("description", "")),
                    "link": link,
                    "source": parsed.feed.get("title", "Source"),
                })
        except Exception as e:
            print(f"[sources] err {feed_url}: {e}")

    return items
