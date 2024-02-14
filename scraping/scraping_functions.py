###THIS SHOULD BE RUN ON A SERVER
import random
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
        print(f"Handling product {i}")
        results = s.find(id=f'product{i}')
        if results is None:
            print(f"Product {i} not found")
            i += 1
            continue
        further = results.find('a',{'class':'productlist__link'}).get('href')
        imgs = results.find_all('img')
        data = results.find_all('span', class_='notrans')

        names = data[0].text
        prices = data[2].text
        image = imgs[0].get("src")
        product_link = (f'https://geizhals.de/{further}')
        
        time.sleep(120+random.randint(-10,10))
        
        #get link from product site
        prod = requests.get(product_link)
        s2 = BeautifulSoup(prod.text, 'html.parser')
        offer = s2.find(id='offer__0')
        if offer is None:
            i += 1
            print(f"Cannot find offer 0 for product {i}")
            continue
        link = offer.find('a',{'class':'offer_bt'}).get('href')
        
        mydict = {"name": names, "preis": prices, "image": image, "link": link}
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


###execute the functions one by one every ten minutes (60 minutes until all 6 functions have been executed)
functions = [GPU_Prices, CPU_Prices, Main_Prices, PSU_Prices, RAM_Prices, Case_Prices]

while True:
    for func in functions:
        func()
        print(time.time(), ": Scraped ", func.__name__)
        time.sleep(180+random.randint(-10,10))

####### Code fürs Umleiten von den Daten in die Datei data.txt
# if html.status_code == 200:
#     html_text = html.text

#     with open('data.txt', 'w', encoding='utf-8') as file:
#         file.write(html_text)
# else:
#     print('failure')
