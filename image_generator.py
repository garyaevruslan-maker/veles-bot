"""
image_generator.py — каждая картинка уникальна.
- имя файла = хеш заголовка
- на картинке: дата, источник, уникальный фактоид
"""
import os
import hashlib
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from config import IMAGES_DIR

WIDTH, HEIGHT = 1080, 1080

BG = (10, 20, 20)
CARD = (15, 26, 26)
CARD_BORDER = (30, 60, 58)
TURQUOISE = (94, 230, 208)
TURQUOISE_DIM = (60, 145, 130)
ORANGE = (255, 140, 66)
TEXT_MAIN = (230, 244, 241)
TEXT_DIM = (122, 155, 150)
TEXT_FAINT = (60, 85, 82)
GRID = (16, 28, 28)

INDICATORS = {
    "news":      ("threat.detected",   TURQUOISE),
    "breakdown": ("incident.analyzed", ORANGE),
    "lifehack":  ("action.required",   TURQUOISE),
    "welcome":   ("SOC · online",      TURQUOISE),
    "stat":      ("data.tracked",      TURQUOISE),
    "law":       ("policy.update",     ORANGE),
}


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


def _hash_id(seed: str) -> str:
    return hashlib.md5(seed.encode("utf-8")).hexdigest()[:10]


def create_post_image(
    category, headline, dek, kind="news",
    fact_label=None, fact_value=None,
    filename=None,
    channel_handle="@cyberveles",
    site_url="veles-it.ru",
    source_name=None,
    seed=None,
):
    os.makedirs(IMAGES_DIR, exist_ok=True)

    if not filename:
        seed = seed or headline or "post"
        filename = f"post_{_hash_id(seed)}.png"
    path = os.path.join(IMAGES_DIR, filename)

    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    _draw_grid(draw)

    _draw_v_logo(draw, 70, 70, size=44)
    draw.text((128, 76), "Велес IT", font=_font(28, bold=True), fill=TEXT_MAIN)

    date_str = datetime.now().strftime("%d.%m.%Y")
    meta_parts = [kind.upper(), date_str]
    if source_name:
        meta_parts.append(source_name[:20])
    meta_text = "  ·  ".join(meta_parts)
    meta_w = draw.textlength(meta_text, font=_font(20))
    draw.text((WIDTH - 70 - meta_w, 84), meta_text, font=_font(20), fill=TEXT_DIM)

    draw.line([(70, 145), (WIDTH - 70, 145)], fill=TURQUOISE_DIM, width=1)

    cat_y = 200
    draw.line([(70, cat_y + 14), (105, cat_y + 14)], fill=TURQUOISE, width=2)
    draw.text((118, cat_y), category.upper(),
              font=_font(22, bold=True), fill=TURQUOISE)

    char_count = len(headline)
    if char_count <= 30:    title_size = 92
    elif char_count <= 50:  title_size = 80
    elif char_count <= 75:  title_size = 68
    elif char_count <= 100: title_size = 58
    else:                   title_size = 50

    title_font = _font(title_size, bold=True)
    title_lines = _wrap(draw, headline, title_font, WIDTH - 140)[:5]
    line_height = int(title_size * 1.15)
    y = 260
    for line in title_lines:
        draw.text((70, y), line, font=title_font, fill=TEXT_MAIN)
        y += line_height

    y += 20
    dek_font = _font(30)
    for line in _wrap(draw, dek, dek_font, WIDTH - 200)[:3]:
        draw.text((70, y), line, font=dek_font, fill=TEXT_DIM)
        y += 42

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
