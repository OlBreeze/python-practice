from task1_simple_types import calculate_discount
from task2_list_tuple import filter_adults
from task3_union_optional import parse_input
from task4_generics import get_first
from task5_callable import apply_operation, double, square

# 1
print("---------- task1 calculate_discount-----------")
print(calculate_discount(100, 20))
print(calculate_discount(100, 75))
print(calculate_discount(100, 50))
print(calculate_discount(50, 110))

# 2
print("---------- task2 filter_adults-----------")
people = [("Андрій", 25), ("Олег", 16), ("Марія", 19), ("Ірина", 15)]
print(filter_adults(people))

# 3
print("---------- task3 parse_input-----------")
print(parse_input(42))
print(parse_input("100"))
print(parse_input("hello"))

# 4
print("---------- task4 get_first-----------")
print(get_first([1, 2, 3]))
print(get_first(["a", "b", "c"]))
print(get_first([]))

# 5
print("---------- task5 apply_operation-----------")
print(apply_operation(5, square))
print(apply_operation(5, double))

# RESULT
# PS C:\WorkspacePython\project_python> mypy lesson9_type_hints/homework/homework.py
# Success: no issues found in 1 source file
# PS C:\WorkspacePython\project_python>
