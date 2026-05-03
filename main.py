import sys
import time
from datetime import datetime
from sources import fetch_news, load_sent, save_sent
from filter import filter_and_diversify
from generator import build_daily_pack, build_welcome_post
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
        filename=post["img_filename"],
    )
    publish(post, img_path)


def run_once():
    print("→ Fetching news...")
    raw = fetch_news()
    print(f"  raw: {len(raw)}")

    picked = filter_and_diversify(raw, n=3)
    print(f"  picked: {len(picked)} ({[p['category'] for p in picked]})")

    if len(picked) < 2:
        print("Мало релевантного. Выходим.")
        return

    is_friday = datetime.now().weekday() == 4
    posts = build_daily_pack(picked, is_friday=is_friday)

    sent = load_sent()
    for i, post in enumerate(posts):
        _render_and_publish(post)
        print(f"  post {i+1} ({post['kind']}): sent")
        time.sleep(2)

    save_sent(sent + [p["link"] for p in picked])
    print("✓ Done")


def run_welcome():
    """Публикует приветственный пост. Запускать один раз при старте канала."""
    print("→ Publishing welcome post...")
    post = build_welcome_post()
    _render_and_publish(post)
    print("✓ Welcome posted. Pin it in channel manually.")


def run_moderation_loop():
    """Цикл проверки нажатий ✅/❌. Держать запущенным параллельно с run_once."""
    print("→ Moderation loop started. Ctrl+C to stop.")
    while True:
        try:
            poll_and_handle_callbacks()
        except Exception as e:
            print(f"[loop] err: {e}")
        time.sleep(5)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    if cmd == "welcome":
        run_welcome()
    elif cmd == "moderate":
        run_moderation_loop()
    else:
        run_once()
