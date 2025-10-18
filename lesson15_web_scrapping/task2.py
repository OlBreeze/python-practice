from bs4 import BeautifulSoup
import requests as r

# response = r.get('https://sinoptik.ua/')
# response = r.get('https://www.pwabuilder.com/')
response = r.get('https://4pda.to/')
# response = r.get('https://lms.ithillel.ua/')


print(response)

soup = BeautifulSoup(response.text, 'html.parser')

# print(end='\n\n\n')
# print(soup.title)
# print(soup.title.name)
# print(soup.title.text)
# print(soup.title.parent)
# print(soup, end="\n\n")
# print(soup.prettify(), end="\n\n")
# print(soup.find('div'), end="\n\n")

print("Назва:")
print(soup.title.text)

divs = soup.find_all('div')[:10]
print(len(divs))
for i, div in enumerate(divs, 1):
    print(f"DIV #{i}:")
    print(div.prettify())