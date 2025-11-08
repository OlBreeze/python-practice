Вот красиво оформленный и структурированный **Markdown-файл** с твоим материалом 👇
(подходит для вставки в GitHub README или документацию проекта)

---

# 🧪 Результати тестування Django форми `TaskForm`

```
============================= 5 passed in 0.16s ==============================
```

## 🔍 Що сталося

Один тест виконався **5 разів з різними параметрами**:

```python
@pytest.mark.parametrize("title,description,is_valid", [
    ("Valid Title", "Valid Description", True),     # Тест 1 [20%]
    ("T", "D", True),                               # Тест 2 [40%]
    ("T" * 200, "D" * 1000, True),                  # Тест 3 [60%]
    ("", "Valid Description", False),               # Тест 4 [80%]
    ("Valid Title", "", False),                     # Тест 5 [100%]
])
```

---

### 🧩 Один тест → 5 виконань з різними параметрами

| №   | Статус   | Опис                         | Очікування        |
| --- | -------- | ---------------------------- | ----------------- |
| 1️⃣ | ✅ [20%]  | Валідні дані                 | Форма ОК          |
| 2️⃣ | ✅ [40%]  | Мінімум (1 символ)           | Форма ОК          |
| 3️⃣ | ✅ [60%]  | Максимум (200/1000 символів) | Форма ОК          |
| 4️⃣ | ✅ [80%]  | Пустий `title`               | ❌ Форма невалідна |
| 5️⃣ | ✅ [100%] | Пустий `description`         | ❌ Форма невалідна |

---

## 💡 Порада для кращої читабельності

Додайте `ids` до параметризації — тоді pytest буде показувати красиві короткі назви тестів:

```python
@pytest.mark.parametrize("title,description,is_valid", [
    ("Valid Title", "Valid Description", True),
    ("T", "D", True),
    ("T" * 200, "D" * 1000, True),
    ("", "Valid Description", False),
    ("Valid Title", "", False),
], ids=["valid", "min_length", "max_length", "no_title", "no_description"])
```

### Результат:

```
test_form[valid] PASSED [20%]
test_form[min_length] PASSED [40%]
test_form[max_length] PASSED [60%]
test_form[no_title] PASSED [80%]
test_form[no_description] PASSED [100%]
```

---

# 📊 Розбір кожного тесту

### 🧠 Тест 1: `[Valid Title-Valid Description-True]` ✅

> Валідні дані → форма очікувано валідна.

---

### 🧠 Тест 2: `[T-D-True]` ✅

> Мінімальна довжина — теж прийнятна.

---

### 🧠 Тест 3: `[TTT...DDD...-True]` ✅

> Максимальна довжина (200 / 1000) — валідно.
> ⚠️ Назва довга, бо pytest показує фактичні значення.

---

### 🧠 Тест 4: `[-Valid Description-False]` ✅

> Пустий `title` → форма **невалідна**, як очікувалось.

---

### 🧠 Тест 5: `[Valid Title--False]` ✅

> Пустий `description` → форма **невалідна**, як очікувалось.

---

# 🧱 Переваги параметризації

### Без параметризації (❌ багато дублювання)

```python
def test_form_valid_title_and_description(): ...
def test_form_valid_min_length(): ...
def test_form_valid_max_length(): ...
def test_form_invalid_empty_title(): ...
def test_form_invalid_empty_description(): ...
```

### З параметризацією (✅ коротко й зрозуміло)

```python
@pytest.mark.parametrize("title,description,is_valid", [
    ("Valid Title", "Valid Description", True),
    ("T", "D", True),
    ("T" * 200, "D" * 1000, True),
    ("", "Valid Description", False),
    ("Valid Title", "", False),
])
def test_task_form_field_combinations_functional(title, description, is_valid):
    data = {'title': title, 'description': description, 'due_date': date.today() + timedelta(days=1)}
    form = TaskForm(data=data)
    assert form.is_valid() == is_valid
```

✅ Менше коду
✅ Легше додавати нові тести
✅ Чітко видно всі сценарії

---

# ✨ Покращення: читабельні тести

```python
import pytest
from datetime import date, timedelta
from main.forms import TaskForm
```

## Варіант 1 — з `ids`

```python
@pytest.mark.django_db
@pytest.mark.parametrize("title,description,is_valid", [
    ("Valid Title", "Valid Description", True),
    ("T", "D", True),
    ("T" * 200, "D" * 1000, True),
    ("", "Valid Description", False),
    ("Valid Title", "", False),
], ids=[
    "valid_data",
    "min_length",
    "max_length",
    "empty_title",
    "empty_description"
])
def test_task_form_field_combinations_with_ids(title, description, is_valid):
    data = {'title': title, 'description': description, 'due_date': date.today() + timedelta(days=1)}
    form = TaskForm(data=data)
    assert form.is_valid() == is_valid
```

## Варіант 2 — з `pytest.param`

```python
@pytest.mark.django_db
@pytest.mark.parametrize("title,description,is_valid", [
    pytest.param("Valid Title", "Valid Description", True, id="valid_data"),
    pytest.param("T", "D", True, id="min_length"),
    pytest.param("T" * 200, "D" * 1000, True, id="max_length"),
    pytest.param("", "Valid Description", False, id="empty_title"),
    pytest.param("Valid Title", "", False, id="empty_description"),
    pytest.param("  ", "Valid Description", False, id="whitespace_title", marks=pytest.mark.skip("TODO: додати валідацію пробілів")),
])
def test_task_form_field_combinations_advanced(title, description, is_valid):
    data = {'title': title, 'description': description, 'due_date': date.today() + timedelta(days=1)}
    form = TaskForm(data=data)
    assert form.is_valid() == is_valid
```

---

# 🧮 Додаткові приклади

### Комбінації пустих полів

```python
@pytest.mark.parametrize("title", ["", "   ", None])
@pytest.mark.parametrize("description", ["", "   ", None])
def test_empty_fields_combinations(title, description):
    data = {'title': title, 'description': description, 'due_date': date.today() + timedelta(days=1)}
    form = TaskForm(data=data)
    assert not form.is_valid()
```

Створює **9 тестів (3×3 комбінації)**.

---

### Тестування дат

```python
@pytest.mark.parametrize("due_date,expected_valid", [
    (date.today() - timedelta(days=7), False),
    (date.today() - timedelta(days=1), False),
    (date.today(), True),
    (date.today() + timedelta(days=1), True),
    (date.today() + timedelta(days=30), True),
    (date.today() + timedelta(days=365), True),
])
def test_due_date_validation(due_date, expected_valid):
    data = {'title': 'Test', 'description': 'Description', 'due_date': due_date}
    form = TaskForm(data=data)
    assert form.is_valid() == expected_valid
```

---

# 📊 Підсумок

Ви протестували:

✅ Валідні дані
✅ Мінімальну довжину (edge case)
✅ Максимальну довжину (edge case)
✅ Пустий title
✅ Пустий description

🧠 Це називається **boundary testing** — тестування межових значень.

---

# 🚀 Що можна додати

* 🔍 Тести на пробіли: `"   "`
* 🔍 Тести на `None`
* 🔍 Тести на надто довгі значення
* 🔍 Тести на спецсимволи
* 🔍 Тести на SQL Injection
* 🔍 Тести на XSS

---

# ⚙️ Корисні команди Pytest

```bash
# Запустити тільки параметризовані тести
pytest -k "field_combinations" -v

# Запустити конкретний тест
pytest main/tests/test_forms.py::test_task_form_field_combinations_functional -v

# Показати локальні змінні при помилці
pytest --showlocals

# Зупинити після першої помилки
pytest -x

# Показати найповільніші тести
pytest --durations=10
```

---

