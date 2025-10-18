from bs4 import BeautifulSoup
import requests as r

# response = r.get('https://www.pwabuilder.com/')
# response = r.get('https://4pda.to/')
response = r.get('https://lms.ithillel.ua/')

# print(response)

soup = BeautifulSoup(response.text, 'html.parser')

print("Название:")
print(soup.title.text)

# print(end='\n\n\n')
# print(soup.title)
# print(soup.title.name)
# print(soup.title.text)
# print(soup.title.parent)
# print(soup, end="\n\n")
# print(soup.prettify(), end="\n\n")
# print(soup.find('div'), end="\n\n")