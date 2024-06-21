

def get_added_money_message(balance: int, added_money: int) -> str:
    return (f"<b>Ваш баланс пополнен на {added_money} RUB!</b> 💸💸💸\n\n"
            f"<b>Текущий баланс: {balance + added_money} RUB</b>")


def get_back_money_message(balance: int, added_money: int) -> str:
    return (f"<b>На ваш баланс было возвращено {added_money} RUB</b> 💸↩️\n\n"
            f"<b>Текущий баланс: {balance + added_money} RUB</b>")
