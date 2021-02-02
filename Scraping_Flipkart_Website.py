from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pandas as pd
import xlwt
import pymongo

dbConn = pymongo.MongoClient("mongodb://localhost:27017/")  # opening a connection to Mongo
db = dbConn['WebScrapingDB']  # connecting to the database called crawlerDB

products = []
ratings = []
prices = []
flipkart_url = "https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as" \
               "-show=off&as=off"
uClient = uReq(flipkart_url)  # requesting the webpage from the internet
flipkartPage = uClient.read()  # reading the webpage
flipkart_html = bs(flipkartPage, "html.parser")  # parsing the webpage as HTML
name = flipkart_html.find_all('div', {'class': '_4rR01T'})
rating = flipkart_html.find_all('div', {'class': '_3LWZlK'})
price = flipkart_html.find_all('div', {'class': '_30jeq3 _1_WHN1'})

indexval = 0
for i in range(len(name)):
    products.append(name[indexval].text)
    ratings.append(rating[indexval].text)
    prices.append(price[indexval].text)
    indexval += 1

#df = pd.DataFrame({'Product Name': products, 'Ratings': ratings, 'Price in Rs': prices})
#df.to_excel('products.xls', index=False, encoding='utf-8')
mydata = {'Product Name': products, 'Ratings': ratings, 'Price in Rs': prices}
Flipkart_Laptop = db.Flipkart_Laptop
Flipkart_Laptop.insert_one(mydata)
# closing the connection to the web server
uClient.close()
