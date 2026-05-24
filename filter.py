"""
filter.py — жёсткий фильтр и точная категоризация.

Логика отбора:
1. ОБЯЗАТЕЛЬНО есть IT-контекст (сайт, сервер, плагин, и т.д.) — иначе выкидываем
2. ОБЯЗАТЕЛЬНО есть угроза/инцидент (взлом, утечка, и т.д.) — иначе выкидываем
3. Категоризация по приоритету: ecommerce > ransomware > leak > phishing > ...
4. Diversity: берём из разных категорий
"""
from config import KEYWORDS_INCLUDE, KEYWORDS_EXCLUDE


# Whitelist: новость должна содержать ХОТЯ БЫ ОДНО из этих слов (IT-контекст)
IT_CONTEXT_TERMS = [
    # English IT-контекст
    "website", "site", "server", "plugin", "patch", "vulnerability",
    "exploit", "cve", "malware", "backdoor", "api", "endpoint",
    "domain", "browser", "firefox", "chrome", "edge", "safari",
    "windows", "linux", "android", "ios", "mac", "docker",
    "wordpress", "drupal", "magento", "shopify", "woocommerce",
    "bitrix", "1c", "joomla", "opencart",
    "cisco", "fortinet", "palo alto", "vpn", "firewall",
    "saas", "cloud", "aws", "azure", "kubernetes",
    # Русский IT-контекст
    "сайт", "сервер", "плагин", "патч", "уязвимост", "эксплоит",
    "вредонос", "бэкдор", "малвар", "стилер", "троян",
    "домен", "браузер", "хром", "файрфокс", "сафари",
    "виндовс", "линукс", "андроид", "ай-ос",
    "битрикс", "вордпресс", "опенкарт",
    "облак", "впн", "файрвол",
    "база данных", "база клиент", "персональных данн", "персональные данн",
    "учётн", "учетн", "пароль", "доступ", "админк",
    "интернет-магазин", "магазин",
    "фишинг", "фишинговая", "фишинговую", "кампания", "почта", "email",
    # Бренды и платформы
    "google", "microsoft", "apple", "telegram", "whatsapp",
    "github", "gitlab", "bitbucket",
]

# Whitelist: должна быть угроза или инцидент
THREAT_TERMS = [
    # English
    "breach", "leak", "leaked", "exposed", "stolen", "stolen",
    "ransomware", "encrypt", "phishing", "scam", "fraud",
    "vulnerability", "exploit", "zero-day", "0-day", "rce",
    "skimmer", "magecart", "stealer", "backdoor", "malware",
    "compromised", "hacked", "attacked", "breached", "ddos",
    "credential", "infected", "ransom",
    # Русский — корни и формы
    "утечк", "утек", "утёк", "слил", "слита", "слиты",
    "украден", "украл", "крадёт", "крадет",
    "вскрыт", "взлом", "взломан", "взломал", "взломали",
    "шифровальщик", "вымогатель", "вымогател",
    "фишинг", "поддельн", "мошенн", "обман",
    "уязвимост", "эксплоит", "атак", "ддос",
    "скомпрометир", "заражен", "заражён",
    "выкуп", "хакер", "взлом", "пробив",
]

# Blacklist: новость про эти темы НЕ берём, даже если она содержит IT-слова
HARD_BLACKLIST = [
    # Политика и геополитика
    "kremlin", "putin", "trump", "biden", "election interference",
    "кремл", "путин", "трамп", "выбор", "санкци",
    # Регуляторика без техники (запреты сайтов, цензура)
    "роскомнадзор заблокировал", "роскомнадзор заблокировал",
    "запрет сайта", "разблокировал", "разблокирова",
    "мосгорсуд", "верховный суд", "конституционный суд",
    "ЯПлакалъ", "анекдот",
    # Военные APT (это для безопасников, не для бизнеса)
    "apt28", "apt29", "lazarus group", "fancy bear",
    "ракет", "военн", "кибервойн",
    # Криптовалюты и трейдинг
    "bitcoin price", "ethereum price", "крипт",
    "kraken", "binance", "coinbase",
    # Прочее
    "hacker arrest", "арест хакер", "приговор",
    # Новости про защиту/исправления (не про инциденты)
    "fixed vulnerabilit", "patched", "исправил", "исправлены проблем",
    "released patch", "выпустила патч", "обновила безопасност",
    # Промышленность / АСУ ТП — НЕ наша ЦА (мы для e-com и SaaS)
    "asu tp", "асу тп", "scada", "ics/ot", "ot/ics",
    "киберфизическ", "cyber-physical", "industrial control",
    "промышленн", "нефтегаз", "энергетическ", "электростанц",
    "manufactur", "производственн", "конвейер",
    # Государственные и оборонные
    "government agency", "госорган", "министерств", "оборонн",
    "defense", "military system",
]


def _contains_any(text: str, terms: list) -> bool:
    text_lower = text.lower()
    return any(term in text_lower for term in terms)


def is_relevant(item) -> bool:
    """Жёсткая проверка: нужно совпадение с IT-контекстом И с угрозой, и не должно быть в блок-листе."""
    blob = f"{item.get('title', '')} {item.get('summary', '')}"

    # 1. Блок-лист — сразу выкидываем
    if _contains_any(blob, HARD_BLACKLIST):
        return False
    if _contains_any(blob, KEYWORDS_EXCLUDE):
        return False

    # 2. Должен быть IT-контекст
    if not _contains_any(blob, IT_CONTEXT_TERMS):
        return False

    # 3. Должна быть угроза/инцидент
    if not _contains_any(blob, THREAT_TERMS):
        return False

    # 4. Текст должен быть преимущественно на русском.
    # Без Claude API английские новости не переводятся — отсекаем их.
    if not _is_mostly_russian(blob):
        return False

    return True


def _is_mostly_russian(text: str, min_ratio: float = 0.3) -> bool:
    """
    Проверяет, что доля кириллицы достаточная.
    Английские новости (The Hacker News и т.п.) сюда не пройдут.
    min_ratio=0.3 — минимум 30% букв должны быть кириллицей.
    """
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    cyrillic = [c for c in letters if "\u0400" <= c <= "\u04FF"]
    ratio = len(cyrillic) / len(letters)
    return ratio >= min_ratio


def detect_category(item) -> str:
    """
    Определяем категорию по приоритету (от более специфичной к общей).
    """
    blob = f"{item.get('title', '')} {item.get('summary', '')}".lower()

    # E-commerce (самая важная для нашей ЦА)
    if any(w in blob for w in ["magecart", "skimmer", "card data", "checkout",
                                "shopify", "magento", "woocommerce", "shopify",
                                "bitrix", "битрикс", "интернет-магазин", "магазин"]):
        return "ecommerce"

    # Ransomware
    if any(w in blob for w in ["ransomware", "ransom", "encrypt", "шифровальщик",
                                "вымогатель", "вымогател"]):
        return "ransomware"

    # Утечки
    if any(w in blob for w in ["data breach", "leak", "leaked", "exposed", "pii",
                                "утечк", "слил", "слита", "украден"]):
        return "leak"

    # Phishing
    if any(w in blob for w in ["phishing", "spear", "scam", "fraud",
                                "фишинг", "поддельн", "мошенн"]):
        return "phishing"

    # DDoS
    if any(w in blob for w in ["ddos", "ддос"]):
        return "ddos"

    # Уязвимости и эксплойты в плагинах/CMS
    if any(w in blob for w in ["zero-day", "0-day", "rce", "exploit",
                                "эксплоит", "уязвимост"]):
        return "vulnerability"

    # API
    if any(w in blob for w in ["api leak", "api exposed", "api endpoint", "api"]):
        return "api"

    # Браузер
    if any(w in blob for w in ["firefox", "chrome", "safari", "edge", "браузер"]):
        return "browser"

    # Мобильные угрозы
    if any(w in blob for w in ["android", "ios", "mobile app", "андроид", "ай-ос"]):
        return "mobile"

    return "general"


def filter_and_diversify(items, n=5):
    """
    Берём n релевантных новостей из разных категорий.
    """
    relevant = [i for i in items if is_relevant(i)]
    for it in relevant:
        it["category"] = detect_category(it)

    # Сначала — по одной из каждой категории
    seen_categories = set()
    picked = []
    for it in relevant:
        if it["category"] in seen_categories:
            continue
        picked.append(it)
        seen_categories.add(it["category"])
        if len(picked) == n:
            return picked

    # Если не набрали — добиваем
    for it in relevant:
        if it not in picked:
            picked.append(it)
            if len(picked) == n:
                break
    return picked
