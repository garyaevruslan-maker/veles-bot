import os
from dotenv import load_dotenv

load_dotenv()

# === Telegram ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "@cyberveles")
TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")

# Режим: "auto" — постит сразу в канал, "draft" — на одобрение в личку
MODERATION_MODE = os.getenv("MODERATION_MODE", "draft")

# === Бренд ===
SITE_URL = os.getenv("SITE_URL", "https://veles-it.ru")
CHANNEL_HANDLE = "@cyberveles"
CONTACT_HANDLE = os.getenv("CONTACT_HANDLE", "@Rama_888")
AUDIT_BOT_HANDLE = os.getenv("AUDIT_BOT_HANDLE", "@VelesIT_bot")

# === AI ===
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
USE_AI = bool(ANTHROPIC_API_KEY.strip())

# === Файлы ===
SENT_FILE = "sent.json"
PENDING_FILE = "pending.json"
IMAGES_DIR = "images"

# === RSS источники ===
RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://www.darkreading.com/rss.xml",
    "https://www.securityweek.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://securelist.com/feed/",
]

# === Фильтр тем ===
KEYWORDS_INCLUDE = [
    "data breach", "leak", "leaked", "exposed",
    "ransomware", "ransom", "encrypted",
    "phishing", "spear phishing", "scam",
    "ecommerce", "e-commerce", "magento", "shopify", "woocommerce",
    "vulnerability", "exploit", "zero-day", "0day", "rce",
    "api", "payment", "checkout", "stripe",
    "skimmer", "magecart", "card data",
    "customer data", "pii", "personal data",
    "ddos", "credential", "stealer",
    "sql injection", "xss", "supply chain",
]

KEYWORDS_EXCLUDE = [
    "apt28", "apt29", "lazarus group analysis",
    "kremlin", "geopolit", "election interference",
]

# === CTA ===
CTA_VARIANTS = [
    "Покажем за 15 минут, где у вашего сайта дыры. Без презентаций, без продажи. Пиши в",
    "Если у вас интернет-магазин — атакуем его так, как сделал бы реальный злоумышленник. Первый осмотр бесплатно. Пиши в",
    "Велес IT работает в тени, чтобы ваш бизнес оставался на свету. Бесплатный аудит — пиши в",
    "Не ждите письма с требованием выкупа. Найдём дыры раньше. Пиши в",
]
