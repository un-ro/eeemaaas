import json
import os
from datetime import datetime
from selenium import webdriver


def packaging(price):
    last_check = datetime.today().strftime('%d-%m-%Y')
    buy_price = price[0]
    sale_price = price[1]

    # Pea
    weights = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 25.0, 50.0, 100.0]

    buy_price_list = {}
    sale_price_list = {}

    for w in weights:
        buy_price_list[str(w)] = w * int(buy_price)
        sale_price_list[str(w)] = w * int(sale_price)

    # Include cleaner data to JSON
    data = {
        "last_update": last_check,
        "buy_price": buy_price,
        "sale_price": sale_price,
        "list_buy": buy_price_list,
        "list_sale": sale_price_list
    }

    data_json = json.loads(str(data).replace("\'", "\""))
    json_formatted_str = json.dumps(data_json, indent=4)

    print(json_formatted_str)


def updater():
    # Selenium WebDriver
    webdriver.ChromeOptions.add_argument("--headless")
    webdriver.ChromeOptions.add_argument("--disable-dev-shm-usage")
    webdriver.ChromeOptions.add_argument("--no-sandbox")
    webdriver.ChromeOptions.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    browser.get('https://www.tokopedia.com/emas/harga-hari-ini/')

    # Scrape price using XPATH
    prices = browser.find_elements_by_xpath('//*[@class="main-price"]')

    price = []

    # Cleaning data
    for value in prices:
        data = value.text
        data = data[2:]
        data = data.replace(".", "")
        price.append(data)

    browser.close()  # Close the browser
    browser.quit()
    return price


if __name__ == '__main__':
    packaging(updater())
