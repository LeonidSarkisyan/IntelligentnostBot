from src.models.find import FindForm


FIND_DESCRIPTION = """
Для поиска определенного айтема, вам необходимо указать следующие параметры по порядку:

<b>1. Название вещи </b>
<b>2. Размер, Цвет </b>
<b>3. Состояние вещи </b>
<b>4. Под заказ или на руках </b>

Мы постараемся найти вам вещь по самой низкой цене на рынке. Данные вещи которые мы найдем, обязательно будут проходить Legit Chek.
"""


START_FIND_MESSAGE = """
Если захотите отменить поиск - /cancel

<b>Напишите название модели:</b>
"""

ASK_SIZE_MESSAGE = "<b>Напишите нужный размер:</b>"

ASK_LINK_MESSAGE = """
<b>Скиньте ссылки на похожую модель через пробел (если есть):</b>
"""

NOT_CORRECT_LINKS_MESSAGE = """
Скиньте сообщение, которое содержит только ссылки через пробел.
"""

ASK_PHOTOS_MESSAGE = """
<b>Скиньте фотографии модели (если есть):</b>

После того как вы скинете фотки, нажмите на кнопку <b>"Готово"</b>.
"""

ASK_CONDITION_MESSAGE = """
<b>Выберите состояние вещи:</b>
"""

INCORRECT_CONDITION_MESSAGE = """
Выберите тип состояния вещи с помощью кнопок ниже.
"""

ASK_LOCATION_MESSAGE = """
<b>Где заказывать?</b>
"""

INCORRECT_LOCATION_MESSAGE = """
Выберите локацию с помощью кнопок ниже.
"""

SURE_MESSAGE = "<b>Подтвердите покупку услуги (250 RUB):</b>"

NO_SURE_MESSAGE = "<b>Вы отменили покупку услуги: \"Поиск вещи\"</b>"

THANKS_REPORT_MESSAGE = """
<b>Спасибо за обращение!</b>

Мы уже начинаем поиск нужной вам вещи.
"""


def get_new_report_find_message(username: str, f: FindForm) -> str:
    msg = ""

    msg += f"""
    <b>Новая заявка на поиск вещи от @{username}! 🔎</b>
    
<b>Название:</b> {f.name}

<b>Размер:</b> {f.size}
"""

    if len(f.links) > 0:
        msg += "\n<b>Ссылки: </b>\n\n"

        for link in f.links:
            msg += f"{link}\n"
    else:
        msg += """
<b>Ссылок нет.</b>
        """

    msg += f"""
<b>Состояние:</b> {f.condition.value}

<b>Локация:</b> {f.location.value}
    """

    return msg


ASK_SEND_LINKS_MESSAGE = "Нажмите на кнопку, чтобы скинуть ссылки пользователю."

SEND_LINKS_MESSAGE = "Скиньте ссылки:"

SUCCESS_SENT_MESSAGE = "Ссылки отправлены пользователю  ✅"

SEND_REASON_DENY_MESSAGE = "Напишите причину, почему вы отказали пользователю в услуге:"

REASON_DENY_SENT_MESSAGE = "Причина отравлена пользователю  ✅"


def get_sent_links_message(msg: str) -> str:
    head_message = "Поиск завершён! Результат: \n\n"
    return head_message + msg


def get_deny_find_message(msg: str) -> str:
    head_message = ("<b>Ваш запрос на поиск вещи был отклонён  🚫\n\n</b>"
                    "<b>Причина:</b>\n\n"
                    f"<i>{msg}</i>")
    return head_message
