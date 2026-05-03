"""
generator.py — посты 1200-1500 символов в формате @cyberveles.
70% контента, 30% — Велес IT в финале.
"""
from ai_writer import rewrite_in_veles_tone, cta, get_category_label
from config import CHANNEL_HANDLE, CONTACT_HANDLE


def build_news_post(news_item: dict) -> dict:
    rw = rewrite_in_veles_tone(news_item)
    text = (
        f"{rw['emoji']} <b>{rw['hook']}</b>\n\n"
        f"{rw['lead']}\n\n"
        f"{rw['details']}\n\n"
        f"{rw['context']}\n\n"
        f"📉 <b>Чем это грозит вам как владельцу бизнеса:</b>\n"
        f"{rw['consequences']}\n\n"
        f"———\n\n"
        f"🎯 <b>Что с этим делать</b>\n\n"
        f"{rw['solution']} <a href=\"{rw['source_link']}\">Источник</a>.\n\n"
        f"{cta()} {CONTACT_HANDLE}\n\n"
        f"{CHANNEL_HANDLE}"
    )
    return {
        "text": text,
        "img_category": get_category_label(rw["category"]),
        "img_headline": rw["hook"],
        "img_dek": rw["lead_short"],
        "img_filename": f"news_{rw['category']}.png",
        "img_fact_label": rw["fact_label"],
        "img_fact_value": rw["fact_value"],
        "kind": "news",
    }


def build_breakdown_post(news_item: dict) -> dict:
    rw = rewrite_in_veles_tone(news_item)
    text = (
        f"🔍 <b>Разбор взлома: {rw['hook']}</b>\n\n"
        f"{rw['lead']}\n\n"
        f"<b>Как именно вошли:</b>\n\n"
        f"🟢 {rw['attack_step_1']}\n"
        f"🟢 {rw['attack_step_2']}\n"
        f"🟢 {rw['attack_step_3']}\n\n"
        f"{rw['context']}\n\n"
        f"📉 <b>Что было бы, если бы это случилось у вас:</b>\n"
        f"{rw['consequences']}\n\n"
        f"———\n\n"
        f"🎯 <b>Как это ловит пентест</b>\n\n"
        f"{rw['solution']}\n\n"
        f"{cta()} {CONTACT_HANDLE}\n\n"
        f"{CHANNEL_HANDLE}"
    )
    return {
        "text": text,
        "img_category": "Разбор",
        "img_headline": rw["hook"],
        "img_dek": "Анатомия атаки. Шаг за шагом.",
        "img_filename": f"breakdown_{rw['category']}.png",
        "img_fact_label": rw["fact_label"],
        "img_fact_value": rw["fact_value"],
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
        f"🎯 <b>Дальше — глубже</b>\n\n"
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
        "kind": "lifehack",
    }


def build_welcome_post() -> dict:
    """Закреп для канала. Запускается один раз вручную: python main.py welcome"""
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
        f"технических лекций. Только то, что важно вам как владельцу.\n"
        f"🟢 <b>Разборы реальных взломов</b> — как именно вошли, что украли, "
        f"как этого можно было избежать.\n"
        f"🟢 <b>Лайфхаки на 5 минут</b> — что проверить в своём бизнесе сегодня, "
        f"чтобы не стать следующим кейсом.\n"
        f"🟢 <b>Тренды и закон</b> — 152-ФЗ, штрафы, новые виды атак на "
        f"e-commerce и финтех.\n\n"
        f"Тон у нас простой: без галстуков, без «комплексных решений», без "
        f"«хакера в капюшоне». Только факты, цифры и язык, который понимает "
        f"предприниматель.\n\n"
        f"———\n\n"
        f"<b>Что мы делаем за деньги:</b>\n\n"
        f"🟢 <b>Пентест внешнего периметра</b> — атакуем ваш сайт так, как это "
        f"сделал бы реальный злоумышленник\n"
        f"🟢 <b>Red Team</b> — полная симуляция атаки на компанию, включая "
        f"сотрудников и инфраструктуру\n"
        f"🟢 <b>Защита от DDoS и защищённый хостинг</b>\n"
        f"🟢 <b>Сопровождение по 152-ФЗ</b> и закрытие требований ФСТЭК\n\n"
        f"<b>Что мы делаем бесплатно:</b>\n\n"
        f"🟢 <b>Экспресс-аудит сайта за 15 минут.</b> Смотрим снаружи, "
        f"показываем 1-2 конкретные зоны риска. Без презентаций, без "
        f"продажных звонков.\n\n"
        f"———\n\n"
        f"Если у вас есть сайт с клиентами — напишите в {CONTACT_HANDLE}. "
        f"Посмотрим. Если найдём что-то серьёзное — будете знать раньше, "
        f"чем кто-либо другой.\n\n"
        f"<i>Работаем в тени, чтобы ваш бизнес оставался на свету.</i>\n\n"
        f"🌐 veles-it.ru\n"
        f"📨 {CONTACT_HANDLE} — для бесплатного аудита\n\n"
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
        "kind": "welcome",
    }


def build_daily_pack(news_items, is_friday=False):
    if len(news_items) < 2:
        raise ValueError("Минимум 2 новости")
    posts = [
        build_news_post(news_items[0]),
        build_news_post(news_items[1]),
    ]
    if is_friday and len(news_items) >= 3:
        posts.append(build_breakdown_post(news_items[2]))
    else:
        posts.append(build_lifehack_post())
    return posts
