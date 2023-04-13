import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

make_list = ["samsung", "lg", "tcl", "hisense",
             "toshiba", "philips", "sony", "panasonic"]
size_pattern = r"[\d]{2}\"|[\d]{2}\s(inch)"
price_pattern = r"£[0-9\,]+\.[0-9]{2}"

ebay_text = []


def prepare_data(products):
    site = []
    make = []
    conditionZ = []
    priceZ = []
    for product in products:
        make.append(product[0])
        site.append(product[4])
        conditionZ.append(product[3])
        priceZ.append(product[2])
        dict = {"Make": make,
                "Site": site,
                "Condition": conditionZ,
                "Price": priceZ,
                }
        df = pd.DataFrame(dict)
        df.to_csv('AmazonTVData.csv')

    print(make)


def make_match(web_text):
    new_tv_list = []
    for each in web_text:
        tv_list = []
        for make in make_list:
            if make in each[0]:
                tv_list.append(make)
                match_m = re.search(size_pattern, each[0])
                if match_m:
                    tv_list.append(match_m.group())
                else:
                    tv_list.append("")
                match_price = re.search(price_pattern, each[1])
                if match_price:
                    tv_list.append(match_price.group())
                else:
                    tv_list.append("")

                tv_list.append(each[2])
                tv_list.append("Amazon")
                new_tv_list.append(tv_list)
    return new_tv_list


# Set headers to mimic a web browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

for page in range(1, 2):

    # URL of the Amazon page you want to scrape
    amazon_url = f'https://www.amazon.co.uk/s?k=65+inch+tv&page={page}&crid=3Q9RHHJ0DH71W&qid=1681383218&sprefix=65+inch%2Caps%2C494&ref=sr_pg_1'

    # Make a request to the Amazon page and get its HTML content
    amazon_response = requests.get(amazon_url, headers=headers)

    # Create an empty list to store products
    products = []

    # Check if the requests were successful
    if amazon_response.status_code == 200:

        # Parse the HTML content using BeautifulSoup
        amazon_soup = BeautifulSoup(amazon_response.content, 'html.parser')

        # Extract the information you need from the Amazon page
        amazon_products = amazon_soup.find_all(
            'div', {'class': 's-result-item'})
        for product in amazon_products:
            try:
                name = product.find('h2').text.strip().lower()
                if '65 inch' not in name:
                    continue
                price = product.find('span', {'class': 'a-price'}).text.strip()
                condition = 'new'

                products.append([name, price, condition])
                # Do something with the extracted information
                # print(f"Amazon: {name}, {price}, {condition}")
            except AttributeError:
                name = ""

        print(make_match(products))
        prepare_data(make_match(products))

    else:
        print("Error making requests to Amazon")
