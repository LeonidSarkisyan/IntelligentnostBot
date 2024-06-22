

def get_balance_show_message(balance: int) -> str:
    return f"""
<b>Ваш баланс: {balance} RUB</b>

Пополнить баланс можно по карте ниже.
Если требуется перевод по СБП - напишите: @wordofm8uth"""


ASK_AMOUNT_MESSAGE = "Введите сумму, на которую хотите пополнить баланс:"

INCORRECT_AMOUNT_MESSAGE = "Введите число:"


def get_minimal_amount_message(MINIMAL_DEPOSIT):
    return f"Минимальная сумма баланса - {MINIMAL_DEPOSIT} RUB"


ASK_RECEIPT_MESSAGE = "Отправьте скрин перевода, чтобы мы могли убедиться, что вы отправили средства:"

def get_user_send_receipt_message(user_id: int, username: str):
    return f"<b>Пользователь @{username} отправил скрин, как пополнил баланс!</b>\n\n<b>ID пользователя = <code>{user_id}</code></b>"

SUCCESS_SENT_RECEIPT = "<b>Спасибо за пополнение!</b>\n\n<i>Скрин отправлен в модерацию и вскоре мы пополним Ваш баланс!</i>"