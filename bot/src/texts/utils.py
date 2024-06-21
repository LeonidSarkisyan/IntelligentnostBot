
def get_price_message(name: str, cost: int, description: str) -> str:
    return f"""
<b>Услуга: {name}</b>

<b>Стоимость: {cost} RUB</b>

<b>Описание услуги:</b>

{description}

<i>Деньги с вашего баланса будут забронированы и будут возвращены в случае отказа предоставления услуги или отменой с помощью /cancel</i>
"""


def get_sure_message(balance: int, cost: int) -> str:
    return (f"<b>Ваш баланс: {balance} RUB</b>\n\n"
            f"<b>Подтвердите покупку услуги ({cost} RUB):</b>")


def get_enough_money_message(count_need_money: int) -> str:
    return (f"Недостаточно средств ({count_need_money} RUB). Пополните баланс.")
