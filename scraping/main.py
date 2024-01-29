import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bs4 import BeautifulSoup

load_dotenv()


#check connetion to MongoDB
try:
    myclient = MongoClient(os.getenv('MONGO_URI'))
    print("Connected!")
except:
    print("Could not connect to MongoDB")

#set Database & Collection   
mydb = myclient.Prices
mycol = mydb.CPU

#data to be sent to MongoDB (example for one entry) --> should be replaced with data from scraping
mydict = {"name": "Ryzen5 3600", "preis": "149€"}

###example for more than one entry
# mydict = {"name": "product0", "preis": "product0.price"},
# {"name": "product1", "preis": "product1.price"},
# {"name": "product2", "preis": "product2.price"}

mycol.insert_one(mydict)
#if you want to enter more than one entry: mycol.insert(mydict)


####### Code um die HTML-Soup von der URL: https://geizhals.de/?cat=gra16_512 zu laden
# url = 'https://geizhals.de/?cat=gra16_512'
# html = requests.get(url)
# print(html.text)

# with open('data.txt', 'r', encoding='utf-8') as file:
#     n = file.read()

# s = BeautifulSoup(n, 'html.parser')

# results = s.find(id='product0')

# prices = results.find_all('span', class_='notrans')

# print(prices[2])


####### Code fürs Umleiten von den Daten in die Datei data.txt
# if html.status_code == 200:
#     html_text = html.text

#     with open('data.txt', 'w', encoding='utf-8') as file:
#         file.write(html_text)
# else:
#     print('failure')