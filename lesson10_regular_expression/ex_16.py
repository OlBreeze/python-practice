import re

string = "sa dfas?df, asd;fa:s!df"
# Шаблон r'[,,;?:!\s]' розділяє рядок за будь-яким символом, вказаним у квадратних дужках.
result = re.split(r'[,,;?:!\s]', string)
result = re.split(r'[,,;?:!\s]'," ", string)
print(result)