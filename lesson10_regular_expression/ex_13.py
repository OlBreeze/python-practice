import re

string = 'test123@gmail.com, test123@mail.ru, test123@ukr.net'

# Шукає @, за якою слідує один або більше символів слова (\w+)
result = re.findall(pattern=r'@\w+', string=string)
print(result)

# Шукає @, за якою слідують символи слова, крапка (\.), і знову символи слова
result = re.findall(pattern=r'@\w+\.\w+', string=string)
print(result)

# Шукає @, за якою слідують символи слова, крапка, і знову символи слова (але тепер використовує групу захоплення)
# Тут, ймовірно, мається на увазі r'@\w+\.(\w+)' для захоплення лише доменної зони
# Проте, на картинці:
result = re.findall(pattern=r'@\w+\.(\w+)', string=string)
print(result)