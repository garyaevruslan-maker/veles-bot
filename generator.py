"""
generator.py — два режима тона: редакционный и продающий.
- editorial (60%): мало продажи, факты, контекст, цифры
- promo (40%): полный CTA блок в финале
"""
import random
from ai_writer import rewrite_in_veles_tone, cta, get_category_label
from config import CHANNEL_HANDLE, CONTACT_HANDLE, AUDIT_BOT_HANDLE


# === Мини-CTA для редакционного режима (одна строка вместо абзаца) ===
SOFT_CTA_VARIANTS = [
    f"<i>P.S. Если у вас сайт с клиентами — {CONTACT_HANDLE} смотрит за 15 минут что у вас открыто. Бесплатно.</i>",
    f"<i>Если хотите проверить свой сайт по тем же местам, где взломали этот — {CONTACT_HANDLE}.</i>",
    f"<i>{CONTACT_HANDLE} — бесплатный экспресс-осмотр сайта. Без презентаций.</i>",
    f"<i>Хотите узнать, открыты ли такие двери у вас? {CONTACT_HANDLE}.</i>",
]


def soft_cta() -> str:
    return random.choice(SOFT_CTA_VARIANTS)


def build_news_post_editorial(news_item: dict) -> dict:
    """Редакционный пост: больше контекста, минимум продажи."""
    rw = rewrite_in_veles_tone(news_item)
    source = news_item.get("source", "Источник")

    text = (
        f"{rw['emoji']} <b>{rw['hook']}</b>\n\n"
        f"{rw['lead']}\n\n"
        f"{rw['details']}\n\n"
        f"{rw['context']}\n\n"
        f"<b>📉 На что это влияет в реальном бизнесе:</b>\n"
        f"{rw['consequences']}\n\n"
        f"<a href=\"{rw['source_link']}\">Подробнее в источнике →</a>\n\n"
        f"———\n\n"
        f"{soft_cta()}\n\n"
        f"{CHANNEL_HANDLE}"
    )
    return {
        "text": text,
        "img_category": get_category_label(rw["category"]),
        "img_headline": rw["hook"],
        "img_dek": rw.get("lead_short", rw["lead"][:120]),
        "img_filename": None,
        "img_fact_label": rw.get("fact_label", "минут на бесплатный аудит"),
        "img_fact_value": rw.get("fact_value", "15"),
        "img_seed": news_item["link"],
        "img_source": source,
        "kind": "news",
    }


def build_news_post_promo(news_item: dict) -> dict:
    """Продающий пост: с полным CTA в финале."""
    rw = rewrite_in_veles_tone(news_item)
    source = news_item.get("source", "Источник")

    text = (
        f"{rw['emoji']} <b>{rw['hook']}</b>\n\n"
        f"{rw['lead']}\n\n"
        f"{rw['details']}\n\n"
        f"{rw['context']}\n\n"
        f"<b>📉 Чем это грозит вам как владельцу бизнеса:</b>\n"
        f"{rw['consequences']}\n\n"
        f"———\n\n"
        f"<b>🎯 Что с этим делать</b>\n\n"
        f"{rw['solution']} <a href=\"{rw['source_link']}\">Источник</a>.\n\n"
        f"{cta()} {CONTACT_HANDLE}\n\n"
        f"{CHANNEL_HANDLE}"
    )
    return {
        "text": text,
        "img_category": get_category_label(rw["category"]),
        "img_headline": rw["hook"],
        "img_dek": rw.get("lead_short", rw["lead"][:120]),
        "img_filename": None,
        "img_fact_label": rw.get("fact_label", "минут на бесплатный аудит"),
        "img_fact_value": rw.get("fact_value", "15"),
        "img_seed": news_item["link"],
        "img_source": source,
        "kind": "news",
    }


def build_news_post(news_item: dict, force_mode: str = None) -> dict:
    """
    Главная функция. Выбирает режим:
    - force_mode='editorial' / 'promo' для явного выбора
    - иначе: 60% editorial, 40% promo
    """
    if force_mode == "editorial":
        return build_news_post_editorial(news_item)
    if force_mode == "promo":
        return build_news_post_promo(news_item)
    if random.random() < 0.6:
        return build_news_post_editorial(news_item)
    return build_news_post_promo(news_item)


def build_breakdown_post(news_item: dict) -> dict:
    rw = rewrite_in_veles_tone(news_item)
    source = news_item.get("source", "Источник")

    text = (
        f"🔍 <b>Разбор: {rw['hook']}</b>\n\n"
        f"{rw['lead']}\n\n"
        f"<b>Как именно вошли:</b>\n\n"
        f"🟢 {rw['attack_step_1']}\n"
        f"🟢 {rw['attack_step_2']}\n"
        f"🟢 {rw['attack_step_3']}\n\n"
        f"{rw['context']}\n\n"
        f"<b>📉 Что это означало бы для интернет-магазина средней руки:</b>\n"
        f"{rw['consequences']}\n\n"
        f"———\n\n"
        f"<b>🎯 Как это ловит пентест</b>\n\n"
        f"{rw['solution']}\n\n"
        f"{cta()} {CONTACT_HANDLE}\n\n"
        f"{CHANNEL_HANDLE}"
    )
    return {
        "text": text,
        "img_category": "Разбор",
        "img_headline": rw["hook"],
        "img_dek": "Анатомия атаки. Шаг за шагом.",
        "img_filename": None,
        "img_fact_label": rw.get("fact_label", "минут на бесплатный аудит"),
        "img_fact_value": rw.get("fact_value", "15"),
        "img_seed": news_item["link"] + "_breakdown",
        "img_source": source,
        "kind": "breakdown",
    }


def build_lifehack_post() -> dict:
    text = (
        f"⏱ <b>5 минут — и вы знаете о своей безопасности больше, чем 90% бизнесов</b>\n\n"
        f"Большинство владельцев интернет-магазинов узнают о взломе от банка, "
        f"клиентов или СМИ. Не от своей IT-команды. Чтобы это поменять, "
        f"не нужен безопасник в штате — нужно 5 минут и три проверки.\n\n"
        f"<b>Прямо сейчас:</b>\n\n"
        f"🟢 Откройте <b>haveibeenpwned.com</b> и проверьте корпоративную почту. "
        f"Если она светится в утечках — пароли сотрудников уже в базах даркнета. "
        f"Любой может попробовать их на вашей админке.\n\n"
        f"🟢 Зайдите в админку сайта и откройте список пользователей. Найдите "
        f"учётки, которых не помните: «test», «admin2», старые аккаунты разработчиков. "
        f"Это самые частые точки входа.\n\n"
        f"🟢 Проверьте двухфакторку у трёх ключевых людей: владельца, главного "
        f"разработчика, маркетолога с доступом к рассылкам. Если хоть у одного "
        f"нет — это и есть ваша главная уязвимость.\n\n"
        f"Если по любому из пунктов нашлась проблема — у вас уже есть, с чем работать. "
        f"Если всё чисто — вы в топ-10% рунет-бизнесов по гигиене.\n\n"
        f"———\n\n"
        f"<b>🎯 Дальше — глубже</b>\n\n"
        f"Это поверхностный осмотр. Реальные дыры обычно лежат на уровне кода, "
        f"конфигов и сторонних интеграций — туда без пентеста не заглянешь.\n\n"
        f"{cta()} {CONTACT_HANDLE}\n\n"
        f"{CHANNEL_HANDLE}"
    )
    return {
        "text": text,
        "img_category": "Лайфхак",
        "img_headline": "5 минут — и вы впереди 90% бизнесов",
        "img_dek": "Три проверки, которые покажут, кто и как может зайти в ваш сайт",
        "img_filename": "lifehack.png",
        "img_fact_label": "минут на проверку",
        "img_fact_value": "5",
        "img_seed": "lifehack_5min",
        "img_source": None,
        "kind": "lifehack",
    }


def build_welcome_post() -> dict:
    text = (
        f"🛡 <b>Это канал Велес IT. Мы взламываем компании раньше, "
        f"чем это делают другие.</b>\n\n"
        f"Велес IT — команда пентестеров. Мы имитируем настоящие хакерские "
        f"атаки на сайты, инфраструктуру и сотрудников, чтобы наши клиенты "
        f"узнавали о своих дырах раньше, чем о них узнают злоумышленники.\n\n"
        f"Этот канал — не про настройку файрволов и не про чтение CVE. "
        f"Этот канал — для владельцев бизнеса, e-commerce директоров, "
        f"основателей SaaS и всех, у кого есть сайт, клиенты и данные, "
        f"которые страшно потерять.\n\n"
        f"<b>Что вы здесь будете читать:</b>\n\n"
        f"🟢 <b>Утечки и атаки</b> — что произошло вчера, без воды и "
        f"технических лекций.\n"
        f"🟢 <b>Разборы реальных взломов</b> — как именно вошли, что украли, "
        f"как этого можно было избежать.\n"
        f"🟢 <b>Лайфхаки на 5 минут</b> — что проверить в своём бизнесе сегодня.\n"
        f"🟢 <b>Тренды и закон</b> — 152-ФЗ, штрафы, новые виды атак.\n\n"
        f"Тон у нас простой: без галстуков, без «комплексных решений», без "
        f"«хакера в капюшоне». Только факты, цифры и язык, который понимает "
        f"предприниматель.\n\n"
        f"———\n\n"
        f"<b>Что мы делаем за деньги:</b>\n\n"
        f"🟢 <b>Пентест внешнего периметра</b>\n"
        f"🟢 <b>Red Team</b> — полная симуляция атаки\n"
        f"🟢 <b>Защита от DDoS и защищённый хостинг</b>\n"
        f"🟢 <b>Сопровождение по 152-ФЗ</b>\n\n"
        f"<b>Что мы делаем бесплатно:</b>\n\n"
        f"🟢 <b>Экспресс-аудит сайта за 15 минут.</b> Смотрим снаружи, "
        f"показываем 1-2 конкретные зоны риска. Без презентаций.\n\n"
        f"———\n\n"
        f"<b>Как получить бесплатный аудит:</b>\n\n"
        f"🤖 Быстрый старт — напишите боту {AUDIT_BOT_HANDLE}, "
        f"оставьте адрес сайта, и мы возьмём его в работу.\n"
        f"💬 Хотите обсудить лично — пишите напрямую {CONTACT_HANDLE}.\n\n"
        f"<i>Работаем в тени, чтобы ваш бизнес оставался на свету.</i>\n\n"
        f"🌐 veles-it.ru\n"
        f"🤖 {AUDIT_BOT_HANDLE} — бот для заявок на аудит\n"
        f"💬 {CONTACT_HANDLE} — связь напрямую\n\n"
        f"{CHANNEL_HANDLE}"
    )
    return {
        "text": text,
        "img_category": "Знакомство",
        "img_headline": "Взламываем раньше, чем это сделают другие",
        "img_dek": "Канал Велес IT — кибербезопасность языком предпринимателя",
        "img_filename": "welcome.png",
        "img_fact_label": "минут на бесплатный аудит вашего сайта",
        "img_fact_value": "15",
        "img_seed": "welcome",
        "img_source": None,
        "kind": "welcome",
    }


def build_single_post(news_items, slot_index=0):
    """
    Возвращает ОДИН пост для конкретного слота времени (режим 2 поста в день).
    slot 0 = 10:00 (editorial новость)
    slot 1 = 18:00 (чередуется: пн/ср/пт — promo-новость, вт/чт — лайфхак, сб/вс — разбор)
    """
    if not news_items:
        raise ValueError("Нет новостей")

    from datetime import datetime
    item = news_items[slot_index % len(news_items)]

    if slot_index == 0:
        # Утро — всегда новость в редакционном тоне
        return build_news_post(item, force_mode="editorial")

    # Вечерний слот — чередуем формат по дню недели
    weekday = datetime.now().weekday()  # 0=пн ... 6=вс
    if weekday in (1, 3):
        # вт, чт — лайфхак (польза)
        return build_lifehack_post()
    elif weekday in (5, 6):
        # сб, вс — разбор взлома
        return build_breakdown_post(item)
    else:
        # пн, ср, пт — продающая новость
        return build_news_post(item, force_mode="promo")


# Совместимость со старым API
def build_daily_pack(news_items, is_friday=False):
    if len(news_items) < 2:
        raise ValueError("Минимум 2 новости")
    posts = [
        build_news_post(news_items[0], force_mode="editorial"),
        build_news_post(news_items[1], force_mode="promo"),
    ]
    if is_friday and len(news_items) >= 3:
        posts.append(build_breakdown_post(news_items[2]))
    else:
        posts.append(build_lifehack_post())
    return posts
