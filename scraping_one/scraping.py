from bs4 import BeautifulSoup
import requests
import pandas as pd
import selenium.webdriver as webdriver
import selenium.webdriver.common.by as By
import time

web_url = "https://listado.mercadolibre.com.mx/laptops-loq?sb=all_mercadolibre#D[A:laptops%20loq]"

driver = webdriver.Safari()
driver.get(web_url)
time.sleep(5)

content = driver.page_source

soup = BeautifulSoup(content, features="html.parser")

laptops_info = []

laptops = soup.find_all("li", class_="ui-search-layout__item")
for laptop in laptops:
    title_tag = laptop.find("h3", class_="poly-component__title-wrapper")
    title = title_tag.text.strip() if title_tag else "No title"
    seller_tag = laptop.find("span", class_="poly-component__seller")
    seller = seller_tag.text.strip() if seller_tag else "No seller"
    price_tag = laptop.find("span", class_="andes-money-amount__fraction")
    price = price_tag.text.strip() if price_tag else 0
    price = price.replace(",", "")
    price = int(price) if price.isdigit() else 0
    reseñas = laptop.find("span", class_="poly-reviews__rating")
    reseñas = reseñas.text.strip() if reseñas else "0"
    reseñas = reseñas.replace("(", "").replace(")", "")
    reseñas = float(reseñas) if reseñas.replace(".", "", 1).isdigit() else 0.0

    
    laptops_info.append({
        "Title": title,
        "Seller": seller,
        "Price": price,
        "Reviews": reseñas
    })

driver.quit()

df = pd.DataFrame(laptops_info)
df.to_csv("laptops_info.csv", index=False)