def demonstrate_yield_behavior():
    """Демонстрирует поведение yield по шагам."""
    print("=" * 60)
    print("ЧТО ПРОИСХОДИТ С yield digit")
    print("=" * 60)

    def my_generator(n):
        print(f"  🟢 Генератор начал работу с n={n}")
        for digit in range(n):
            print(f"  🔄 Готовимся yield {digit}")
            yield digit
            print(f"  ↩️ Продолжаем после yield {digit}")
        print(f"  🔴 Генератор завершил работу")

    print("1. Создаем генератор (функция НЕ выполняется!):")
    gen = my_generator(3)
    print(f"   gen = {gen}")
    print(f"   type(gen) = {type(gen)}")

    print("\n2. Первый вызов next() - функция начинает выполняться:")
    value1 = next(gen)
    print(f"   Получили: {value1}")

    print("\n3. Второй вызов next() - продолжаем с места остановки:")
    value2 = next(gen)
    print(f"   Получили: {value2}")

    print("\n4. Третий вызов next():")
    value3 = next(gen)
    print(f"   Получили: {value3}")

    print("\n5. Четвертый вызов next() - генератор исчерпан:")
    try:
        value4 = next(gen)
        print(f"   Получили: {value4}")
    except StopIteration:
        print("   ❌ StopIteration - генератор закончился!")


def compare_return_vs_yield():
    """Сравнение return vs yield."""
    print("\n" + "=" * 60)
    print("RETURN vs YIELD")
    print("=" * 60)

    # Функция с return
    def function_with_return(n):
        result = []
        for digit in range(n):
            result.append(digit)
        return result  # Возвращает ВСЕ сразу

    # Функция с yield (генератор)
    def function_with_yield(n):
        for digit in range(n):
            yield digit  # Возвращает ПО ОДНОМУ

    print("1. Функция с return:")
    result = function_with_return(5)
    print(f"   result = {result}")
    print(f"   type(result) = {type(result)}")
    print("   ↳ Все значения созданы СРАЗУ и хранятся в памяти")

    print("\n2. Функция с yield:")
    generator = function_with_yield(5)
    print(f"   generator = {generator}")
    print(f"   type(generator) = {type(generator)}")
    print("   ↳ Значения создаются ПО ТРЕБОВАНИЮ")

    print("\n3. Получение значений из генератора:")
    for i, value in enumerate(generator):
        print(f"   Шаг {i + 1}: получили {value}")


def yield_memory_efficiency():
    """Демонстрация эффективности памяти генераторов."""
    print("\n" + "=" * 60)
    print("ЭФФЕКТИВНОСТЬ ПАМЯТИ")
    print("=" * 60)

    import sys

    # Создание большого списка
    def create_list(n):
        return [x for x in range(n)]

    # Создание генератора
    def create_generator(n):
        for x in range(n):
            yield x

    n = 1000

    big_list = create_list(n)
    big_generator = create_generator(n)

    print(f"Размер списка из {n} элементов:")
    print(f"   sys.getsizeof(big_list) = {sys.getsizeof(big_list)} байт")

    print(f"\nРазмер генератора для {n} элементов:")
    print(f"   sys.getsizeof(big_generator) = {sys.getsizeof(big_generator)} байт")

    print(f"\nЭкономия памяти: {sys.getsizeof(big_list) / sys.getsizeof(big_generator):.1f}x")


def yield_with_state():
    """Демонстрация сохранения состояния в генераторе."""
    print("\n" + "=" * 60)
    print("СОХРАНЕНИЕ СОСТОЯНИЯ")
    print("=" * 60)

    def stateful_generator():
        print("   🔧 Инициализация состояния")
        count = 0

        while count < 5:
            count += 1
            print(f"   📊 Состояние перед yield: count = {count}")
            yield f"Значение-{count}"
            print(f"   ⏭️ Состояние после yield: count = {count}")

    print("Генератор сохраняет локальные переменные между вызовами:")

    gen = stateful_generator()

    print("\nПолучаем значения по одному:")
    print(f"1. {next(gen)}")
    print(f"2. {next(gen)}")
    print(f"3. {next(gen)}")


def yield_expressions():
    """Демонстрация yield как выражения."""
    print("\n" + "=" * 60)
    print("YIELD КАК ВЫРАЖЕНИЕ")
    print("=" * 60)

    def echo_generator():
        print("   🎬 Генератор запущен")
        while True:
            received = yield "Готов принять данные"
            if received is None:
                break
            print(f"   📨 Получено: {received}")
            yield f"Обработано: {received.upper()}"

    print("yield может получать значения через send():")

    gen = echo_generator()

    # Первый next() для запуска генератора
    response1 = next(gen)
    print(f"1. {response1}")

    # Отправляем данные в генератор
    response2 = gen.send("hello")
    print(f"2. {response2}")

    # Получаем следующее значение
    response3 = next(gen)
    print(f"3. {response3}")


def practical_yield_examples():
    """Практические примеры использования yield."""
    print("\n" + "=" * 60)
    print("ПРАКТИЧЕСКИЕ ПРИМЕРЫ")
    print("=" * 60)

    # 1. Чтение файла по строкам
    def read_file_lines(filename):
        """Генератор для чтения файла по строкам."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    yield line_num, line.strip()
        except FileNotFoundError:
            yield 0, "Файл не найден"

    # 2. Числа Фибоначчи
    def fibonacci_generator():
        """Бесконечный генератор чисел Фибоначчи."""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    # 3. Фильтрация данных
    def filter_even_numbers(numbers):
        """Генератор четных чисел."""
        for num in numbers:
            if num % 2 == 0:
                yield num

    print("1. Генератор Фибоначчи (первые 10 чисел):")
    fib = fibonacci_generator()
    fib_numbers = [next(fib) for _ in range(10)]
    print(f"   {fib_numbers}")

    print("\n2. Фильтрация четных чисел:")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_gen = filter_even_numbers(numbers)
    even_numbers = list(even_gen)
    print(f"   Исходные: {numbers}")
    print(f"   Четные: {even_numbers}")

    print("\n3. Имитация чтения файла:")
    # Создаем тестовый файл в памяти (имитация)
    fake_file_content = ["строка 1", "строка 2", "строка 3"]

    def read_fake_file():
        for i, line in enumerate(fake_file_content, 1):
            yield i, line

    print("   Содержимое 'файла':")
    for line_num, content in read_fake_file():
        print(f"     {line_num}: {content}")


def yield_vs_list_comprehension():
    """Сравнение генератора и list comprehension."""
    print("\n" + "=" * 60)
    print("GENERATOR vs LIST COMPREHENSION")
    print("=" * 60)

    # List comprehension - создает список сразу
    squares_list = [x ** 2 for x in range(5)]
    print(f"List comprehension: {squares_list}")
    print(f"Type: {type(squares_list)}")

    # Generator expression - создает генератор
    squares_gen = (x ** 2 for x in range(5))
    print(f"\nGenerator expression: {squares_gen}")
    print(f"Type: {type(squares_gen)}")

    # Получаем значения из генератора
    print("\nЗначения из генератора:")
    for square in squares_gen:
        print(f"   {square}")

    # После итерации генератор исчерпан!
    print(f"\nПопытка повторной итерации:")
    squares_from_gen = list(squares_gen)
    print(f"   {squares_from_gen}")  # Пустой список!


def common_yield_mistakes():
    """Распространенные ошибки с yield."""
    print("\n" + "=" * 60)
    print("ЧАСТЫЕ ОШИБКИ С YIELD")
    print("=" * 60)

    print("❌ Ошибка 1: Смешивание return и yield")
    print("def bad_generator():")
    print("    yield 1")
    print("    return 2  # Это остановит генератор!")
    print("    yield 3   # Этот код никогда не выполнится")

    print("\n❌ Ошибка 2: Попытка повторного использования генератора")

    def single_use_gen():
        for i in range(3):
            yield i

    gen = single_use_gen()
    first_use = list(gen)
    second_use = list(gen)  # Пустой!

    print(f"Первое использование: {first_use}")
    print(f"Второе использование: {second_use}")

    print("\n✅ Правильно: создавать новый генератор")
    gen1 = single_use_gen()
    gen2 = single_use_gen()
    print(f"Генератор 1: {list(gen1)}")
    print(f"Генератор 2: {list(gen2)}")


if __name__ == "__main__":
    demonstrate_yield_behavior()
    compare_return_vs_yield()
    yield_memory_efficiency()
    yield_with_state()
    yield_expressions()
    practical_yield_examples()
    yield_vs_list_comprehension()
    common_yield_mistakes()

    print("\n" + "=" * 60)
    print("ЗАКЛЮЧЕНИЕ О YIELD")
    print("=" * 60)
    print("yield digit делает следующее:")
    print("🔄 Приостанавливает выполнение функции")
    print("📤 Возвращает значение digit вызывающему коду")
    print("💾 Сохраняет состояние функции (локальные переменные)")
    print("⏸️ Ждет следующего вызова next() или итерации")
    print("▶️ Продолжает выполнение с места остановки")
    print("\nПреимущества:")
    print("• Экономия памяти (ленивые вычисления)")
    print("• Эффективность при работе с большими данными")
    print("• Элегантный код для итераторов")
    print("• Возможность создания бесконечных последовательностей")