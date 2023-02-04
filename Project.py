from pprint import pprint
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint

def scrape_amazon_data(pages):
    product_list = []
    for page in range(1, pages + 1):
        url = f"https://www.amazon.in/s?k=bags&page={page}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        print(f"*********{page}***********")
        count = 0
        products = soup.find_all("div", class_="s-result-item")
        for product in products:
            product_data = {}
            try:
                product_data["url"] = product.find("a", class_="a-link-normal").get("href")
            except:
                continue
            try:
                product_data["name"] = product.find("span", class_="a-size-medium a-color-base a-text-normal").text
            except:
                continue
            try:
                product_data["price"] = product.find("span", class_="a-offscreen").text
            except:
                continue
            try:
                product_data["rating"] = product.find("span", class_="a-icon-alt").text
            except:
                continue
            try:
                product_data["reviews"] = product.find("span", class_="a-size-base s-underline-text").text
            except:
                continue
            product_list.append(product_data)
    return(product_list)


def scrape_product_details(product_list):
    details_list = []
    for product in product_list[:200]:
        url = "http://www.amazon.in" + product["url"]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        #Here the soup is not getting the response it should be getting due to which further operation dose not happen
        description = soup.find("div", id="productDescription").text
        asin = soup.find("td", class_="a-color-secondary a-size-base").text
        manufacturer = soup.find("td", class_="a-color-secondary a-size-base").text
        details_data = {}
        details_data["url"] = url
        details_data["description"] = description
        details_data["asin"] = asin
        details_data["manufacturer"] = manufacturer
        details_list.append(details_data)
    return details_list

data = scrape_amazon_data(20)
details = scrape_product_details(data)
df = pd.DataFrame(details)
df.to_csv("amazon_product_details.csv", index=False)