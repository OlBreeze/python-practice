from bs4 import BeautifulSoup
import re

result = ''

with open('index.html', encoding='UTF-8') as f:
    data = f.read()
    soup = BeautifulSoup(data, 'lxml')
    print(type(soup.html.text))
    result = soup.html.text

print("Result is:", result)

phone_numbers1 = []
phone_numbers1 += re.findall(r'\d{3}-\d{3}-\d{2}-\d{2}', result)
print("phone_numbers1 are:", phone_numbers1)

phone_numbers2 = []
phone_numbers2 += re.findall(r'\(\d{3}\)\d{7}', result)
print("phone_numbers2 are:", phone_numbers2)

emails = []
emails += re.findall(r'\d+(\w+@\w+\.\w+)', result)
print("emails are:", emails)