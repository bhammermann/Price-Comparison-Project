import requests
from bs4 import BeautifulSoup


# url = 'https://geizhals.de/?cat=gra16_512'
# html = requests.get(url)
# print(html.text)

with open('data.txt', 'r', encoding='utf-8') as file:
    n = file.read()

s = BeautifulSoup(n, 'html.parser')

results = s.find(id='product0')

prices = results.find_all('span', class_='notrans')

print(prices[2])


####### Code fürs Umleiten von den Daten in die Datei data.txt
# if html.status_code == 200:
#     html_text = html.text

#     with open('data.txt', 'w', encoding='utf-8') as file:
#         file.write(html_text)
# else:
#     print('failure')