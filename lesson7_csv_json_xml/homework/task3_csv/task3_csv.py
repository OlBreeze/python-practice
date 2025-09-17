# Завдання 3: Робота з CSV файлами
# Напиши програму, яка: Читає дані з CSV-файлу. Виводить середню оцінку студентів.
# Додає нового студента до файлу.

import csv
from typing import List, Dict, Optional
import os


def create_csv_file(filename: str = "students.csv") -> None:
    """
    Створює новий CSV файл з заголовками, якщо файл не існує.
    """
    if not os.path.exists(filename):
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["name", "age", "score"])
        print(f"Створено файл {filename} з заголовками")


def write_to_csv(name: str, age: int, score: float, filename: str = "students.csv") -> None:
    """
    Записує дані студента до CSV файлу (перезаписує весь файл).
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "age", "score"])
        writer.writerow([name, age, score])
    print(f"Записано в {filename}")


def add_student_to_csv(name: str, age: int, score: float, filename: str = "students.csv") -> None:
    """
    Додає нового студента до існуючого CSV файлу.

    Args:
        name (str): Ім'я студента
        age (int): Вік студента
        score (float): Оцінка студента
        filename (str): Ім'я файлу. За замовчуванням "students.csv"
    """
    if not os.path.exists(filename):
        create_csv_file(filename)

    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, age, score])
    print(f"Додано студента {name} до {filename}")


def read_csv(filename: str = "students.csv") -> List[Dict[str, str]]:
    """
    Читає дані з CSV файлу та повертає список студентів.

    Args:
        filename (str): Ім'я файлу для читання. За замовчуванням "students.csv"

    Returns:
        List[Dict[str, str]]: Список словників з даними студентів
    """
    students_data: List[Dict[str, str]] = []

    try:
        with open(filename, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                students_data.append(row)
                # print(f"Зчитано з файлу:\nІм'я: {row['name']}, "
                #       f"Вік: {row['age']}, Оцінка: {row['score']}")
        return students_data
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено")
        return []


def calculate_average_score(filename: str = "students.csv") -> Optional[float]:
    """
    Обчислює середню оцінку всіх студентів у файлі.

    Args:
        filename (str): Ім'я файлу. За замовчуванням "students.csv"

    Returns:
        Optional[float]: Середня оцінка або None, якщо файл порожній або не існує
    """
    scores: List[float] = []
    error = -0.0
    try:
        with open(filename, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    score = float(row['score'])
                    scores.append(score)
                except (ValueError, KeyError) as e:
                    print(f"Помилка при обробці рядка: {row}. Помилка: {e}")
                    continue

            if scores:
                return sum(scores) / len(scores)
            else:
                return error

    except FileNotFoundError:
        print(f"Файл {filename} не знайдено")
        return error


def display_all_students(filename: str = "students.csv") -> None:
    """
    Виводить інформацію про всіх студентів.
    """
    students = read_csv(filename)
    if students:
        print("\n----> Студенти: <----")
        print(f"{'Ім\'я':<15} {'Вік':<5} {'Оцінка':<8}")
        print("-" * 30)
        for student in students:
            print(f"{student['name']:<15} {student['age']:<5} {student['score']:<8}")
        print("-" * 30)


def main() -> None:
    """
    Головна функція для демонстрації роботи з CSV файлами.
    """
    filename = "students.csv"

    # Створюємо файл з заголовками, якщо його немає
    create_csv_file(filename)

    # Додаємо кількох студентів
    students_to_add = [
        ("Іван Петров", 20, 85.5),
        ("Марія Сидорова", 19, 92.0),
        ("Олександр Коваль", 21, 78.3),
        ("Анна Шевченко", 20, 88.7)
    ]

    for name, age, score in students_to_add:
        add_student_to_csv(name, age, score, filename)

    # Виводимо всіх студентів
    display_all_students(filename)

    # Обчислюємо та виводимо середню оцінку
    av = calculate_average_score(filename)
    print(f"Середня оцінка студентів: {av:.2f}")


if __name__ == "__main__":
    main()
