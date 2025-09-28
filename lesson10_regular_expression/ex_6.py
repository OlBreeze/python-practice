import re

string = " test1 test2 test3 test4 test5"

# re.split(pattern, string, [maxsplit=0]) - призначений для поділу рядка за заданим шаблоном
# Стільки поділів, скільки це можливо
result = re.split(pattern=r"\s", string=string) # У вихідному коді вказано r"t", але зважаючи на рядок string та результат, логічніше використати r"\s" (пробіл). Якщо потрібно саме r"t", то:
# result = re.split(pattern=r"t", string=string)
print(result)

# maxsplit - кількість поділів
result = re.split(pattern=r"t", string=string, maxsplit=5)
print(result)

# maxsplit - кількість поділів
result = re.split(pattern=r"t", string=string, maxsplit=10)
print(result)