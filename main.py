import json
from datetime import datetime

def format_transaction_history(transactions):
    formatted_transactions = []
    last_five_transactions = transactions[-5:]  # Выбираем только последние 5 операций
    for transaction in last_five_transactions[::-1]:  # Обращаем список для вывода в порядке от последней к первой
        transaction_date = datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S.%f")
        description = transaction["description"]
        from_account = transaction.get("from", "")
        to_account = transaction.get("to", "")
        amount = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]

        masked_from_account = mask_account_number(from_account)
        masked_to_account = mask_account_number(to_account)

        formatted_date = transaction_date.strftime("%d.%m.%Y")
        formatted_amount = f"{amount} {currency}"  # Обновленное форматирование

        formatted_transaction = (
            f"{formatted_date} {description}\n"
            f"{masked_from_account} -> {masked_to_account}\n"
            f"{formatted_amount}\n"
        )
        formatted_transactions.append(formatted_transaction)

    return "\n\n".join(formatted_transactions)

def mask_account_number(account_number):
    if len(account_number) >= 8:
        masked_number = account_number[-4:].rjust(len(account_number), "*")
        return f"**{masked_number}"
    return account_number

# Загрузка данных из operations.json
with open("operations.json", "r", encoding="utf-8") as file:
    transactions = json.load(file)

formatted_history = format_transaction_history(transactions)
print(formatted_history)
