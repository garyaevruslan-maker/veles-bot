import json
import os
import time
import requests
from config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, TELEGRAM_ADMIN_ID,
    MODERATION_MODE, PENDING_FILE
)

API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def _send_text(chat_id, text, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    r = requests.post(f"{API}/sendMessage", data=data, timeout=30)
    return r.json() if r.ok else None


def _send_photo(chat_id, image_path, caption, reply_markup=None):
    if len(caption) > 1024:
        with open(image_path, "rb") as f:
            requests.post(
                f"{API}/sendPhoto",
                data={"chat_id": chat_id},
                files={"photo": f},
                timeout=60,
            )
        return _send_text(chat_id, caption, reply_markup)

    with open(image_path, "rb") as f:
        data = {"chat_id": chat_id, "caption": caption, "parse_mode": "HTML"}
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)
        r = requests.post(f"{API}/sendPhoto", data=data, files={"photo": f}, timeout=60)
    if r.ok:
        return r.json()
    print(f"[telegram] sendPhoto failed: {r.text}")
    return _send_text(chat_id, caption, reply_markup)


def _load_pending():
    if not os.path.exists(PENDING_FILE):
        return {}
    with open(PENDING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_pending(data):
    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def publish(post: dict, image_path: str):
    """Публикует или шлёт админу на одобрение в зависимости от режима."""
    if MODERATION_MODE == "auto":
        return _send_photo(TELEGRAM_CHANNEL_ID, image_path, post["text"])

    pending = _load_pending()
    post_id = str(int(time.time() * 1000))
    pending[post_id] = {
        "text": post["text"],
        "image_path": image_path,
        "kind": post["kind"],
    }
    _save_pending(pending)

    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ Опубликовать", "callback_data": f"publish:{post_id}"},
            {"text": "❌ Отклонить", "callback_data": f"reject:{post_id}"},
        ]]
    }
    return _send_photo(TELEGRAM_ADMIN_ID, image_path, post["text"], keyboard)


def poll_and_handle_callbacks():
    """Поллинг кнопок ✅/❌ от админа."""
    offset_file = ".tg_offset"
    offset = 0
    if os.path.exists(offset_file):
        with open(offset_file) as f:
            offset = int(f.read().strip() or 0)

    r = requests.get(f"{API}/getUpdates", params={"offset": offset, "timeout": 5})
    if not r.ok:
        return

    updates = r.json().get("result", [])
    for upd in updates:
        offset = upd["update_id"] + 1
        cq = upd.get("callback_query")
        if not cq:
            continue

        data = cq.get("data", "")
        if ":" not in data:
            continue
        action, post_id = data.split(":", 1)

        pending = _load_pending()
        post = pending.get(post_id)
        if not post:
            requests.post(f"{API}/answerCallbackQuery",
                          data={"callback_query_id": cq["id"], "text": "Уже обработано"})
            continue

        if action == "publish":
            _send_photo(TELEGRAM_CHANNEL_ID, post["image_path"], post["text"])
            requests.post(f"{API}/answerCallbackQuery",
                          data={"callback_query_id": cq["id"], "text": "✅ Опубликовано"})
        else:
            requests.post(f"{API}/answerCallbackQuery",
                          data={"callback_query_id": cq["id"], "text": "❌ Отклонено"})

        del pending[post_id]
        _save_pending(pending)

    with open(offset_file, "w") as f:
        f.write(str(offset))
