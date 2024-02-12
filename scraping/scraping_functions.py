###THIS SHOULD BE RUN ON A SERVER

import requests
import time
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

#if you want to enter more than one entry: mycol.insert(mydict)


####### Code um die HTML-Soup von Geizhals zu laden

def scrape_prices(url, category):
    mydb = myclient.Prices
    mycol = getattr(mydb, category)

    resp = requests.get(url)
    s = BeautifulSoup(resp.text, 'html.parser')

    i = 0
    
    while i < 5:
        results = s.find(id=f'product{i}')
        imgs = results.find_all('img')
        data = results.find_all('span', class_='notrans')

        names = data[0].text
        prices = data[2].text
        image = imgs[0].get("src")

        mydict = {"name": names, "preis": prices, "image": image}
        mycol.insert_one(mydict)
        
        i += 1

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


###execute the functions one by one every ten minutes (60 minutes until all 6 functions have been executed)
functions = [GPU_Prices, CPU_Prices, Main_Prices, PSU_Prices, RAM_Prices, Case_Prices]

while True:
    for func in functions:
        func()
        print(time.time(), ": Scraped ", func.__name__)
        time.sleep(600)

####### Code fürs Umleiten von den Daten in die Datei data.txt
# if html.status_code == 200:
#     html_text = html.text

#     with open('data.txt', 'w', encoding='utf-8') as file:
#         file.write(html_text)
# else:
#     print('failure')
