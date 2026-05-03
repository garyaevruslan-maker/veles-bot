from config import KEYWORDS_INCLUDE, KEYWORDS_EXCLUDE


def is_relevant(item) -> bool:
    blob = f"{item['title']} {item['summary']}".lower()
    if any(bad in blob for bad in KEYWORDS_EXCLUDE):
        return False
    return any(kw in blob for kw in KEYWORDS_INCLUDE)


def detect_category(item) -> str:
    blob = f"{item['title']} {item['summary']}".lower()
    if any(w in blob for w in ["ransomware", "ransom", "encrypted"]):
        return "ransomware"
    if any(w in blob for w in ["data breach", "leak", "leaked", "exposed", "pii"]):
        return "leak"
    if any(w in blob for w in ["phishing", "spear", "scam"]):
        return "phishing"
    if any(w in blob for w in ["ddos"]):
        return "ddos"
    if any(w in blob for w in ["magecart", "skimmer", "card data", "checkout"]):
        return "ecommerce"
    if any(w in blob for w in ["zero-day", "0day", "rce", "exploit"]):
        return "vulnerability"
    if any(w in blob for w in ["api", "supply chain"]):
        return "api"
    return "general"


def filter_and_diversify(items, n=3):
    relevant = [i for i in items if is_relevant(i)]
    for it in relevant:
        it["category"] = detect_category(it)

    seen = set()
    picked = []
    for it in relevant:
        if it["category"] in seen:
            continue
        picked.append(it)
        seen.add(it["category"])
        if len(picked) == n:
            return picked

    for it in relevant:
        if it not in picked:
            picked.append(it)
            if len(picked) == n:
                break
    return picked
