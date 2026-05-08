"""
main.py — точка входа.

Команды:
  python main.py           — постит один пост (slot=0 по умолчанию)
  python main.py slot 0    — пост утреннего слота (10:00)
  python main.py slot 1    — пост дневного слота (14:00)
  python main.py slot 2    — пост вечернего слота (18:00, лайфхак/разбор)
  python main.py welcome   — приветственный пост
  python main.py moderate  — цикл одобрения для draft-режима
"""
import sys
import os
from datetime import datetime
from sources import fetch_news, load_sent, save_sent
from filter import filter_and_diversify
from generator import build_single_post, build_welcome_post, build_daily_pack
from image_generator import create_post_image
from telegram_sender import publish, poll_and_handle_callbacks


def _render_and_publish(post):
    img_path = create_post_image(
        category=post["img_category"],
        headline=post["img_headline"],
        dek=post["img_dek"],
        kind=post["kind"],
        fact_label=post["img_fact_label"],
        fact_value=post["img_fact_value"],
        filename=post.get("img_filename"),
        source_name=post.get("img_source"),
        seed=post.get("img_seed"),
    )
    publish(post, img_path)


def run_single_slot(slot: int):
    """Постит ОДИН пост для конкретного слота (0/1/2)."""
    print(f"→ Slot {slot} run...")
    raw = fetch_news()
    print(f"  raw: {len(raw)}")

    picked = filter_and_diversify(raw, n=5)
    print(f"  picked: {len(picked)} ({[p['category'] for p in picked]})")

    if not picked:
        print("Нет релевантных новостей. Выходим.")
        return

    post = build_single_post(picked, slot_index=slot)
    _render_and_publish(post)
    print(f"  posted: {post['kind']}")

    # Помечаем как использованную ТОЛЬКО ту новость, что взяли
    if slot < len(picked):
        sent = load_sent()
        save_sent(sent + [picked[slot % len(picked)]["link"]])

    print("✓ Done")


def run_welcome():
    print("→ Publishing welcome...")
    post = build_welcome_post()
    _render_and_publish(post)
    print("✓ Welcome posted. Pin it manually.")


def run_daily_pack():
    """Старая логика — 3 поста разом. Оставлена для совместимости."""
    print("→ Daily pack run...")
    raw = fetch_news()
    picked = filter_and_diversify(raw, n=3)
    if len(picked) < 2:
        print("Мало релевантного.")
        return
    is_friday = datetime.now().weekday() == 4
    posts = build_daily_pack(picked, is_friday=is_friday)
    sent = load_sent()
    for i, post in enumerate(posts):
        _render_and_publish(post)
        print(f"  post {i+1}: ok")
    save_sent(sent + [p["link"] for p in picked])
    print("✓ Done")


def run_moderation_loop():
    import time
    print("→ Moderation loop")
    while True:
        try:
            poll_and_handle_callbacks()
        except Exception as e:
            print(f"[loop] {e}")
        time.sleep(5)


if __name__ == "__main__":
    args = sys.argv[1:]

    # Поддержка GitHub Actions: команда может быть передана как одно слово
    # Например: "slot 0" → ["slot", "0"]
    cmd = args[0] if args else "run"

    if cmd == "welcome":
        run_welcome()
    elif cmd == "moderate":
        run_moderation_loop()
    elif cmd == "slot":
        slot = int(args[1]) if len(args) > 1 else 0
        run_single_slot(slot)
    elif cmd in ("slot0", "slot_0"):
        run_single_slot(0)
    elif cmd in ("slot1", "slot_1"):
        run_single_slot(1)
    elif cmd in ("slot2", "slot_2"):
        run_single_slot(2)
    elif cmd == "pack":
        run_daily_pack()
    else:
        # По умолчанию — один пост в утреннем слоте
        run_single_slot(0)
