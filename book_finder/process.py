from bs4 import BeautifulSoup
import requests
import sqlite3

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class Scrape():
    image = []
    title = []
    prices = []
    rating = []
    ref_url = []
    products = [] # 0:title  1:price  2:rating  3:ref_url  4:image
    
    def __init__(self, key):
        self.word = key
        self.clearList()
        self.products.clear()
        self.scrapeAmazon()
        self.scrapeFlipkart()
        self.scrapeSapna()
    
    def __del__(self):
        print("destructor---------")


    def clearList(self):
        self.title.clear()
        self.prices.clear()
        self.rating.clear()
        self.ref_url.clear()
        self.image.clear()

# scraping for amazon

    def scrapeAmazon(self):
        url = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + self.word
        resp = requests.get(url, headers=headers)
        bs = BeautifulSoup(resp.content, features="lxml")
        self.clearList()
        
        for x in bs.find('div', {'class': 's-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16'}):
            for product_title in bs.find_all({'a'}, {'class': 'a-link-normal a-text-normal'}):
                product_title = product_title.get_text().strip()
                self.title.append(product_title)

            for product_price in bs.find_all('span', {'class': 'a-price' , 'class': 'a-price-whole'}):
                product_price = product_price.get_text().strip('.')
                self.prices.append(product_price)
            
            for product_rating in bs.find_all('div', {'class': 'a-row a-size-small'}):
                product_rating = product_rating.get_text().strip('\n')
                self.rating.append(product_rating)
                
            for product_link in bs.find_all({'a'},{'class':'a-link-normal s-no-outline'}):
                self.ref_url.append('https://www.amazon.in' + product_link.get('href'))

            for product_img in bs.find_all({'img'},{'class':'s-image'}):
                self.image.append(product_img.get('src'))
            
        for i in range(2):
            temp = []
            temp.append(self.title[i])
            temp.append(int(self.prices[i].replace(",","")))
            temp.append(self.rating[i])
            temp.append(self.ref_url[i])
            temp.append(self.image[i])

            self.products.append(temp)

#------------------------------------------------------------------------------------------------------------------------------
# scraping for flipkart

    def scrapeFlipkart(self):
        url = 'https://www.flipkart.com/search?q=' + self.word + '&marketplace=FLIPKART&otracker=start&as-show=on&as=off'
        resp = requests.get(url, headers=headers)
        bs = BeautifulSoup(resp.text, features="lxml")
        self.clearList()
        
        for productName in bs.find_all('a', {'class': 's1Q9rs'}):
            productName = productName.get_text().strip()
            self.title.append(productName)

        for product_price in bs.find_all('div', {'class': '_30jeq3'}):
            product_price = product_price.get_text()
            self.prices.append(product_price[1:])

        for product_rating in bs.find_all('div', {'class': 'gUuXy- _2D5lwg'}):
            product_rating = product_rating.get_text()
            self.rating.append(product_rating)

        for product_link in bs.find_all( {'a'}, {'class': '_2rpwqI'}):
            self.ref_url.append('http://www.flipkart.in/' + product_link.get('href'))

        for product_img in bs.find_all( {'img'}, {'class': '_396cs4 _3exPp9'}):
            self.image.append(product_img.get('src'))
        
        for i in range(2):
            temp = []
            temp.append(self.title[i])
            temp.append(int(self.prices[i].replace(",","")))
            temp.append(self.rating[i])
            temp.append(self.ref_url[i])
            temp.append(self.image[i])

            self.products.append(temp)

#------------------------------------------------------------------------------------------------------------------------------
# scraping for sapna

    def scrapeSapna(self):
        url = 'https://www.sapnaonline.com/search?keyword=' + self.word
        resp = requests.get(url, headers=headers)
        bs = BeautifulSoup(resp.text, features="lxml")
        self.clearList()
        
        for product_title in bs.find_all('h2', {'class': 'ProductCard__AboutText-sc-10n3822-2 kOZyab link'}):
            product_title = product_title.get_text().strip()
            self.title.append(product_title)

        for product_price in bs.find_all('h3', {'class': 'ProductCard__PrcieText-sc-10n3822-7 hnbQgS'}):
            product_price = product_price.get_text()
            self.prices.append(product_price[1:])

        for product_rating in bs.find_all('div', {'class': 'sc-Axmtr ProductCard__ReviewText-sc-10n3822-6 frtHvE'}):
            product_rating = product_rating.get_text()
            self.rating.append(product_rating)

        for product_link in bs.find_all('a'):
            self.ref_url.append(product_link.get('href'))

        for product_img in bs.find_all('img', {'class': 'bookImage'}):
            self.image.append(product_img.get('src'))

        for i in range(2):
            temp = []
            temp.append(self.title[i])
            temp.append(int(self.prices[i].replace(",","")))
            temp.append(self.rating[i])
            temp.append('https://www.sapnaonline.com' + self.ref_url[10+i])
            temp.append(self.image[i])

            self.products.append(temp)
    

    def getSortedByPrice(self):
        self.products.sort(key = lambda x:x[1])
    
    def getSortedByRating(self):
        self.products.sort(key = lambda x:x[2], reverse=True)
