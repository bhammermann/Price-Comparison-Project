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
#mycol = mydb.GPU

#data to be sent to MongoDB (example for one entry) --> should be replaced with data from scraping
#mydict = {"name": "Ryzen5 3600", "preis": "149€"}

###example for more than one entry
# mydict = {"name": "product0", "preis": "product0.price"},
# {"name": "product1", "preis": "product1.price"},
# {"name": "product2", "preis": "product2.price"}

#mycol.insert_one(mydict)
#if you want to enter more than one entry: mycol.insert(mydict)


####### Code um die HTML-Soup von der URL: https://geizhals.de/?cat=gra16_512 zu laden

# with open('data.txt', 'r', encoding='utf-8') as file:
#     n = file.read()

# s = BeautifulSoup(n, 'html.parser')

def scrape_prices(url, category):
    myclient = MongoClient(os.getenv('MONGO_URI'))
    mydb = myclient.Prices
    mycol = getattr(mydb, category)

    resp = requests.get(url)
    s = BeautifulSoup(resp.text, 'html.parser')

    results = s.find(id='product0')
    data = results.find_all('span', class_='notrans')

    names = data[0].text
    prices = data[2].text

    mydict = {"name": names, "preis": prices}
    mycol.insert_one(mydict)

def GPU_Prices():
    scrape_prices('https://geizhals.de/?cat=gra16_512', 'GPU')

def CPU_Prices():
    scrape_prices('https://geizhals.de/?cat=cpuamdam4', 'CPU')

def Main_Prices():
    scrape_prices('https://geizhals.de/?cat=mbam5', 'Mainboard')

def PSU_Prices():
    scrape_prices('https://geizhals.de/?cat=gehps', 'PSU')

def RAM_Prices():
    scrape_prices('https://geizhals.de/?cat=ramddr3', 'RAM')

def Case_Prices():
    scrape_prices('https://geizhals.de/?cat=gehatx', 'Case')


# print(html.text)

# with open('data.txt', 'r', encoding='utf-8') as file:
#     n = file.read()

# s = BeautifulSoup(n, 'html.parser')

# results = s.find(id='product0')

# prices = results.find_all('span', class_='notrans')

# print(data[0])


####### Code fürs Umleiten von den Daten in die Datei data.txt
# if html.status_code == 200:
#     html_text = html.text

#     with open('data.txt', 'w', encoding='utf-8') as file:
#         file.write(html_text)
# else:
#     print('failure')