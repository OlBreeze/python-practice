import re

string = 'name: Admin, birthday: 01-12-2000, certificate: 01-06-2022'

# Без групи захоплення: повертає повний збіг (дату)
result = re.findall(pattern=r'\d{2}-\d{2}-\d{4}', string=string)
print(result)

# З групою захоплення навколо року: повертає лише вміст групи захоплення (рік)
result = re.findall(pattern=r'\d{2}-\d{2}-(\d{4})', string=string)
print(result)