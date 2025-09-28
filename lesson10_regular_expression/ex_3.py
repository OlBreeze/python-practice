import re

string = "Test1 Test2 Test3 Test4 Test5"

# re.search(pattern, string) - схожий на метод match(), але шукає не тільки на початку рядка,
# повертає лише перший знайдений збіг
result = re.search(pattern=r"Test3", string=string)
print(result.group())
print(result.group(0))

# IndexError: no such group
# print(result.group(1))
# Цей рядок закоментовано, оскільки він викликає помилку IndexError: no such group,
# адже не було використано жодних груп захоплення (дужок) у шаблоні r"Test3"