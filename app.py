# Gregoire Layet
# 18/11/2020 11:04


#import
import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

URL = "https://www.amazon.fr/s?k="

def app(recherche,maxPage):
    recherche = "+".join(recherche.split())

    driver = webdriver.Firefox()
    driver.get(f"{URL}{recherche}")
    
    
    data = []
    for i in range(1,maxPage+1):
        driver.get(f"{URL}{recherche}&page={i}")
        page = driver.page_source
        data += getAllElementOfPage(page,recherche,i)
    
    mostDiscount = {
        "title":"",
        "discount":0,
        "link":""
    }

    for element in data:
        if "old_price" in element:
            current_price = float(".".join(element["new_price"].split(",")[0:1]))
            old_price = float(".".join(element["old_price"].split(",")[0:1]))
            discount = (old_price-current_price)*100/old_price
            discount = round(discount,2)

            if mostDiscount["discount"] < discount:
                mostDiscount["title"] = element["title"]
                mostDiscount["discount"] = discount
                mostDiscount["link"] = element["link"]
                mostDiscount["page"] = element["page"]

    print(json.dumps(mostDiscount,indent=4))
    driver.quit()
    os.system(f'start chrome "{mostDiscount["link"]}"')



def getAllElementOfPage(page, keywords,nbrPage):
    soup = BeautifulSoup(page, "html.parser")
    allDivs = soup.find_all('div', attrs={'data-component-type':"s-search-result"})

    data = []

    for div in allDivs:
        divData = {}

        divData["title"] = div.select('span.a-size-base-plus.a-color-base.a-text-normal')[0].get_text()
        divData["link"] = f"amazon.fr{div.select('a.a-link-normal.a-text-normal')[0]['href']}"
        divData["page"] = nbrPage


        if div.select('span.a-price.a-text-price'):
            divData["old_price"] = "".join(div.select('span.a-price.a-text-price > span.a-offscreen')[0].get_text().split("€")[0].split("\u00a0"))
        if div.select('span.a-price'):
            divData["new_price"] = "".join(div.select('span.a-price-whole')[0].get_text().split("€")[0].split("\u00a0"))

        a = 0
        for keyword in keywords.split("+"):
            if keyword.lower() not in divData["title"].lower().split():
                a +=1

        if a == 0:
            data.append(divData)

    return data

if __name__ == "__main__":
    print("que voulez vous rechercher ?")
    command = input("")
    app(command,10)
