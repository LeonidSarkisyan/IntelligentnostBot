

def get_balance_show_message(balance: int) -> str:
    return f"""
<b>Ваш баланс: {balance} RUB</b>

<b>Пополнить баланс можно через владельца - @wordofm8uth</b>
"""


ASK_AMOUNT_MESSAGE = "Введите сумму, на которую хотите пополнить баланс:"

INCORRECT_AMOUNT_MESSAGE = "Введите число:"


def get_minimal_amount_message(MINIMAL_DEPOSIT):
    return f"Минимальная сумма баланса - {MINIMAL_DEPOSIT} RUB"
