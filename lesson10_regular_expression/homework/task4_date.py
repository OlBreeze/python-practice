# Завдання 4. Форматування дати
# Напишіть функцію, яка перетворює дати з формату DD/MM/YYYY у формат YYYY-MM-DD.
import re
from typing import Optional
from datetime import datetime


# 1v
def reformat_date(date_str: str) -> Optional[str]:
    """
    Перетворює дату з формату DD/MM/YYYY у формат YYYY-MM-DD.
    """

    pattern = r'^(\d{2})/(\d{2})/(\d{4})$'
    match = re.match(pattern, date_str)
    if match:
        day, month, year = match.groups()
        return f"{year}-{month}-{day}"
    return None


print(reformat_date("27/09/2025"))  # '2025-09-27'
print(reformat_date("31/02/2025"))  # '2025-09-27' // нет такой даты
print(reformat_date("7/9/2025"))  # None (некоректний формат)
print(reformat_date("27-09-2025"))  # None (некоректний роздільник)


# v2
def reformat_date2(date_str: str) -> Optional[str]:
    """
    Перетворює дату з формату DD/MM/YYYY у формат YYYY-MM-DD з перевіркою валідності.
    """
    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None


print()
print(reformat_date2("27/09/2025"))  # '2025-09-27'
print(reformat_date2("31/02/2025"))  # None нет такой даты
print(reformat_date2("7/9/2025"))  # 2025-09-07
print(reformat_date2("27-09-2025"))  # None (некоректний роздільник)
