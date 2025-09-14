# 2. Ітератор для генерації унікальних ідентифікаторів
# Створіть ітератор, який генерує унікальні ідентифікатори
# (наприклад, на основі UUID або хеш-функції).
# hashed = hashlib.sha256(raw.encode()).hexdigest()
# Ідентифікатори повинні генеруватися один за одним при кожній ітерації, і бути унікальними.

import uuid
from typing import Iterator, Set

def unique_uuid_generator() -> Iterator[str]:
    """
    Генерує нескінченний потік унікальних UUID4 у вигляді рядків.

    Для гарантії унікальності всі згенеровані UUID зберігаються у множині.!!!!
    Якщо трапляється колізія (дуже малоймовірно), UUID генерується повторно.

    :return: Ітератор рядків, кожен з яких є унікальним UUID4.
    """
    generated: Set[str] = set()
    while True:
        uid: str = str(uuid.uuid4())
        if uid not in generated:
            generated.add(uid)
            yield uid
