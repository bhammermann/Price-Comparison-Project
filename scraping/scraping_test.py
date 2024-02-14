### FOR TESTING WITH LOCAL DATA
import time
import random
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

    # with open(url, 'r', encoding='utf-8') as file:
    #     resp = file.read()
    # s = BeautifulSoup(resp, 'html.parser')
    
    resp = requests.get(url)
    s = BeautifulSoup(resp.text, 'html.parser')
    with open('data.txt', 'w', encoding='utf-8') as file:
        file.write(resp.text)
    
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
        with open('data2.txt', 'w', encoding='utf-8') as file:
            file.write(prod.text)
        offer = s2.find(id='offer__0')
        if offer is None:
            i += 1
            print(f"Cannot find offer 0 for product {i}")
            continue
        link = offer.find('a',{'class':'offer_bt'}).get('href')

        mydict = {"name": names, "preis": prices, "image": image, "link": link}
        #mycol.insert_one(mydict)
        print(mydict)
        
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

CPU_Prices()

####### Code fürs Umleiten von den Daten in die Datei data.txt
# if html.status_code == 200:
#     html_text = html.text

#     with open('data.txt', 'w', encoding='utf-8') as file:
#         file.write(html_text)
# else:
#     print('failure')