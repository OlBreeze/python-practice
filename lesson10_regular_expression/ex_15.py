import re

phones = ['8884320688', '888888-888', '88888#8888']

for value in phones:
    if re.match(pattern=r'[8-9]{1}[0-9]{9}', string=value) and len(value) == 10:
        print('yes')
    else:
        print('no')