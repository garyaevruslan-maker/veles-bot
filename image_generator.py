"""
image_generator.py — генерация постовых картинок в фирстиле Велес IT.
Палитра снята со скриншота сайта veles-it.ru:
  - фон #0A1414
  - карточка #0F1A1A
  - бирюза #5EE6D0 (главный акцент)
  - оранжевый #FF8C42 (alert / breakdown)
  - текст #E6F4F1 / #7A9B96
"""
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from config import IMAGES_DIR

WIDTH, HEIGHT = 1080, 1080

# === Брендовая палитра Велес IT ===
BG = (10, 20, 20)              # #0A1414
CARD = (15, 26, 26)            # #0F1A1A
CARD_BORDER = (30, 60, 58)
TURQUOISE = (94, 230, 208)     # #5EE6D0
TURQUOISE_DIM = (60, 145, 130)
ORANGE = (255, 140, 66)        # #FF8C42
TEXT_MAIN = (230, 244, 241)    # #E6F4F1
TEXT_DIM = (122, 155, 150)     # #7A9B96
TEXT_FAINT = (60, 85, 82)
GRID = (16, 28, 28)

# Контекстные индикаторы по типу поста
INDICATORS = {
    "news":      ("threat.detected",   TURQUOISE),
    "breakdown": ("incident.analyzed", ORANGE),
    "lifehack":  ("action.required",   TURQUOISE),
    "welcome":   ("SOC · online",      TURQUOISE),
    "stat":      ("data.tracked",      TURQUOISE),
    "law":       ("policy.update",     TURQUOISE),
}


def generate_image_prompt(topic: str) -> str:
    return (
        f"Premium B2B cybersecurity poster, very dark teal background (#0A1414), "
        f"turquoise accent (#5EE6D0), faint geometric grid, monitoring dashboard aesthetic. "
        f"Editorial typography, spacious composition. NO hooded hacker, NO matrix code. "
        f"Theme: {topic}. Square 1080x1080."
    )


def _font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _wrap(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _draw_v_logo(draw, x, y, size=44):
    """Логотип V — стилизованный щит, как на сайте."""
    points_outer = [
        (x, y),
        (x + size, y),
        (x + size, y + size * 0.55),
        (x + size / 2, y + size),
        (x, y + size * 0.55),
    ]
    draw.polygon(points_outer, outline=TURQUOISE, fill=None, width=2)
    pad = size * 0.22
    inner = [
        (x + pad, y + pad),
        (x + size - pad, y + pad),
        (x + size / 2, y + size - pad * 1.2),
    ]
    draw.polygon(inner, fill=TURQUOISE)


def _draw_grid(draw):
    step = 60
    for x in range(0, WIDTH, step):
        draw.line([(x, 0), (x, HEIGHT)], fill=GRID, width=1)
    for y in range(0, HEIGHT, step):
        draw.line([(0, y), (WIDTH, y)], fill=GRID, width=1)


def create_post_image(
    category: str,
    headline: str,
    dek: str,
    kind: str = "news",
    fact_label: str = None,
    fact_value: str = None,
    filename: str = "post.png",
    channel_handle: str = "@cyberveles",
    site_url: str = "veles-it.ru",
) -> str:
    """Создаёт картинку поста в фирстиле Велес IT. Возвращает путь."""
    os.makedirs(IMAGES_DIR, exist_ok=True)
    path = os.path.join(IMAGES_DIR, filename)

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    _draw_grid(draw)

    # ШАПКА
    _draw_v_logo(draw, 70, 70, size=44)
    draw.text((128, 76), "Велес IT", font=_font(28, bold=True), fill=TEXT_MAIN)

    date_str = datetime.now().strftime("%d.%m.%Y")
    meta_text = f"{kind.upper()}  ·  {date_str}"
    meta_w = draw.textlength(meta_text, font=_font(20))
    draw.text((WIDTH - 70 - meta_w, 84), meta_text, font=_font(20), fill=TEXT_DIM)

    draw.line([(70, 145), (WIDTH - 70, 145)], fill=TURQUOISE_DIM, width=1)

    # РУБРИКА
    cat_y = 200
    draw.line([(70, cat_y + 14), (105, cat_y + 14)], fill=TURQUOISE, width=2)
    draw.text((118, cat_y), category.upper(),
              font=_font(22, bold=True), fill=TURQUOISE)

    # ЗАГОЛОВОК (адаптивный размер под длину)
    char_count = len(headline)
    if char_count <= 30:   title_size = 92
    elif char_count <= 50: title_size = 80
    elif char_count <= 75: title_size = 68
    else:                  title_size = 58

    title_font = _font(title_size, bold=True)
    title_lines = _wrap(draw, headline, title_font, WIDTH - 140)[:5]
    line_height = int(title_size * 1.15)
    y = 260
    for line in title_lines:
        draw.text((70, y), line, font=title_font, fill=TEXT_MAIN)
        y += line_height

    # ДЕК
    y += 20
    dek_font = _font(30)
    for line in _wrap(draw, dek, dek_font, WIDTH - 200)[:3]:
        draw.text((70, y), line, font=dek_font, fill=TEXT_DIM)
        y += 42

    # ФАКТОИД
    if fact_label and fact_value:
        box_y = HEIGHT - 320
        box_h = 150
        draw.rounded_rectangle(
            [70, box_y, WIDTH - 70, box_y + box_h],
            radius=18, fill=CARD, outline=CARD_BORDER, width=1
        )
        value_size = 64 if len(fact_value) <= 8 else 52 if len(fact_value) <= 12 else 44
        draw.text((100, box_y + 18), fact_value,
                  font=_font(value_size, bold=True), fill=TURQUOISE)
        draw.text((100, box_y + 95), fact_label.lower(),
                  font=_font(22), fill=TEXT_DIM)

        indicator_text, indicator_color = INDICATORS.get(kind, INDICATORS["news"])
        ind_w = draw.textlength(indicator_text, font=_font(20))
        ind_x = WIDTH - 100 - ind_w - 22
        ind_y = box_y + 30
        draw.ellipse([ind_x, ind_y, ind_x + 12, ind_y + 12], fill=indicator_color)
        draw.text((ind_x + 22, ind_y - 4), indicator_text,
                  font=_font(20), fill=TEXT_DIM)

    # ПОДВАЛ
    footer_y = HEIGHT - 90
    draw.line([(70, footer_y), (WIDTH - 70, footer_y)], fill=TEXT_FAINT, width=1)
    draw.text((70, footer_y + 25), channel_handle,
              font=_font(22), fill=TEXT_DIM)
    cta_text = f"{site_url}  →"
    cta_w = draw.textlength(cta_text, font=_font(22, bold=True))
    draw.text((WIDTH - 70 - cta_w, footer_y + 25), cta_text,
              font=_font(22, bold=True), fill=TURQUOISE)

    img.save(path, "PNG", optimize=True)
    return path


# Совместимость со старым API generator.py
def create_placeholder_image(title, subtitle, filename, kind="news",
                              fact_label="минут на бесплатный аудит",
                              fact_value="15"):
    category_map = {
        "news": "Новость", "breakdown": "Разбор", "lifehack": "Лайфхак",
        "welcome": "Знакомство", "stat": "Цифра дня", "law": "Закон",
    }
    return create_post_image(
        category=category_map.get(kind, "Новость"),
        headline=title, dek=subtitle, kind=kind,
        fact_label=fact_label, fact_value=fact_value,
        filename=filename,
    )
