### FOR TESTING WITH LOCAL DATA


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

#if you want to enter more than one entry: mycol.insert(mydict)


####### Code um die HTML-Soup von der URL: https://geizhals.de/?cat=gra16_512 zu laden

# with open('data.txt', 'r', encoding='utf-8') as file:
#     n = file.read()

# s = BeautifulSoup(n, 'html.parser')

def scrape_prices(url, category):
    mydb = myclient.Prices
    mycol = getattr(mydb, category)

    with open(url, 'r', encoding='utf-8') as file:
        resp = file.read()
    s = BeautifulSoup(resp, 'html.parser')

    i = 0
    
    while i < 5:
        results = s.find(id=f'product{i}')
        data = results.find_all('span', class_='notrans')

        names = data[0].text
        prices = data[2].text

        mydict = {"name": names, "preis": prices}
        mycol.insert_one(mydict)
        
        i += 1

def GPU_Prices():
    scrape_prices('/home/bjorn/FOM/Price-Comparison-Project/scraping/data.txt', 'GPU')

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

#GPU_Prices()

####### Code fürs Umleiten von den Daten in die Datei data.txt
# if html.status_code == 200:
#     html_text = html.text

#     with open('data.txt', 'w', encoding='utf-8') as file:
#         file.write(html_text)
# else:
#     print('failure')