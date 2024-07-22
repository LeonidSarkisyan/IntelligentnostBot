from src.config import LEGIT_PRICE

LEGIT_DESCRIPTION = f"""
Для проверки айтема на аутентичность, необходимо ознакомиться с правильной подачей (кнопка снизу).

У любого первого пользователя имеется первая бесплатная проверка за отзыв.
Далее {LEGIT_PRICE}₽ за проверку.
Мы можем отказать в проверке без объяснения причины.
"""


LEGIT_GUIDE_MESSAGE = "Перед legit check, ознакомьтесь с инструкцией"

ASK_PHOTOS_MESSAGE = "Скиньте фотографии вещи, в соответствии с инструкцией, а затем нажмите \"Готово\""

INCORRECT_PHOTOS_MESSAGE = "Скиньте именно фотографию!"

ONE_MORE_PHOTO_MESSAGE = "Скиньте хотя бы 1 фотографию"

ASK_TEXT_MESSAGE = "Напишите сообщения, если есть какие-то пожелания и т.п."

THANKS_REPORT_MESSAGE = """
<b>Спасибо за обращение!</b>

Мы уже начинаем проверку вашей вещи."""


NO_SURE_MESSAGE_LEGIT = "<b>Вы отменили покупку услуги: \"Legit Check\"</b>"


def get_new_report_legit_message(username: str, text: str) -> str:
    msg = ""

    msg += f"<b>Новая заявка на legit check от @{username}! 👁✅</b>\n\n"

    if text == "Без текста":
        msg += "Пользователь оставил заявку без текста."
    else:
        msg += f"Текст от пользователя: {text}"

    return msg


ASK_SOLVE_MESSAGE = "Примите решение по легиту для пользователя:"

DECISION_SENT_TO_USER_MESSAGE = "Решение было отправлено пользователю  ✅"

ORIGINAL_MESSAGE = """
Специалист подтверждает оригинальность вещи, на которую вы оставили заявку  ✅

С уважением Intelligent Chek 
Просим оставить отзыв: <a href="https://vk.com/wall673463594_38">ВК</a>"""

NOT_ORIGINAL_MESSAGE = """
Специалист опровергает оригинальность вещи, на которую вы оставили заявку  ❌

С уважением Intelligent Chek 
Просим оставить отзыв: <a href="https://vk.com/wall673463594_38">ВК</a>"""


def get_deny_legit_message(msg: str) -> str:
    head_message = ("<b>Ваш запрос на legit check был отклонён  🚫\n\n</b>"
                    "<b>Причина:</b>\n\n"
                    f"<i>{msg}</i>")
    return head_message
