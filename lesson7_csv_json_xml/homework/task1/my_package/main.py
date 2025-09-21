# У файлі main.py імпортуй функції з модулів і продемонструй їх роботу, викликавши кожну з функцій.
# from lesson7_csv_json_xml.homework.task1_unittest_doctest.my_package import math_utils
# from lesson7_csv_json_xml.homework.task1_unittest_doctest.my_package import string_utils

from math_utils import factorial, my_gcd
from string_utils import *


def main() -> None:
    """
    Точка входу в програму. Викликає функції з модулів `math_utils` та `string_utils` і демонструє їх роботу.
    """
    print(f"Факторіал 5 = {factorial(5)}")
    print(f"НСД(505, 15) = {my_gcd(505, 15)}")

    text = "   Hello World!    "

    print(f"Без пробілів: '{trip_whitespace(text)}'")
    print(f"У верхньому регістрі: '{upper_case_string(text)}'")
    print(f"Комбіновано: '{upper_case_string(trip_whitespace(text))}'")


if __name__ == "__main__":
    main()
