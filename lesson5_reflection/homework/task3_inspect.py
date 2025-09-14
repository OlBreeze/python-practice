# Завдання 3: Інспекція модулів
# Напишіть програму, яка приймає на вхід назву модуля (рядок) та виводить список усіх класів, функцій та їхніх сигнатур у модулі.
# Використовуйте модуль inspect.
import importlib
import inspect


def analyze_module(module_name: str) -> None:
    """
    Функція, яка приймає на вхід назву модуля (рядок) та виводить список усіх класів, функцій та їхніх сигнатур у модулі.
    :param module_name: Назва модуля (рядок), наприклад: "math"
    """
    print(f"\n<----- МОДУЛЬ {module_name} ----->")
    try:
        # Динамічне імпортування модуля за назвою
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Модуль '{module_name}' не знайдено.")
        return

    # ---- Класи ----
    classes = inspect.getmembers(module, predicate=inspect.isclass)

    print("\nКласи:")
    if classes:
        for name, cls in classes:
            # Перевіряємо, чи клас справді належить цьому модулю (а не імпортований з іншого)
            if cls.__module__ == module_name:
                print(f"- {name}")
        if not any(cls.__module__ == module_name for _, cls in classes):
            print("- <немає класів у модулі>")
    else:
        print("- <немає класів у модулі>")

    # ---- Функції ----
    functions = inspect.getmembers(module, predicate=inspect.isfunction)
    builtins = inspect.getmembers(module, predicate=inspect.isbuiltin)  # Встроен функций, реализов на C

    all_functions = functions + builtins

    print("Функції:")
    if all_functions:
        for name, func in all_functions:
            try:
                sig = inspect.signature(func)
                print(f"- {name}{sig}")
            except (ValueError, TypeError):
                # Деякі функції можуть не мати сигнатур (наприклад, з C-реалізації)
                print(f"- {name}(...)")
    else:
        print("- <немає функцій>")


# --------------------------------------------------------
analyze_module("math")
analyze_module("random")
analyze_module("json")
analyze_module("nonexistent_module")  # перевірка помилки
