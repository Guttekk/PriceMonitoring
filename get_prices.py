import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def get_page(url):
    page = requests.get(url)
    parsed_page = BeautifulSoup(page.content, "html.parser")

    return parsed_page


def get_price(url, html_element, attribute_name, attribute_value):
    parsed_page = get_page(url)
    price = parsed_page.find(html_element, {attribute_name: attribute_value}).text
    price_no_currency = price.replace("zł", "")
    price_comma_to_dot = price_no_currency.replace(",", ".")
    price_removed_dash = price_comma_to_dot.replace(".-", "")
    price_removed_non_break_space = price_removed_dash.replace(u"\xa0", "")
    price_trimmed = price_removed_non_break_space.replace(" ", "").strip()
    price_final = price_trimmed

    return price_final


df = pd.read_excel("items.xlsx")
ar = np.array([])

for index, shop_item in df.iterrows():
    try:
        cost = get_price(shop_item["URL"], shop_item["HTML_ELEMENT"], shop_item["ATTRIBUTE_NAME"], shop_item["ATTRIBUTE_VALUE"])
    except AttributeError:
        cost = "0"

    ar = np.append(ar, float(cost))


def prices_append_excel(items):
    prices_source = pd.read_excel("prices.xlsx")
    prices_source.loc[len(df)] = items
    writer = pd.ExcelWriter("prices.xlsx", engine="xlsxwriter")
    prices_source.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()


prices_append_excel(ar)


# def cena():
#     URL = "https://www.twojemeble.pl/produkt/halmar/stoly-stoliki-i-lawy-halmar/nowoczesna-lawa-do-salonu-camila,89931"
#     parsed_page = get_page(URL)
#     soup = parsed_page.find(class_="regular-price")
#
#     print(soup)
