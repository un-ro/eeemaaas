import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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

    f = open("data.json", "w")
    f.write(json_formatted_str)
    f.close()


def updater():
    # Selenium WebDriver
    options = Options()
    options.binary_location = GOOGLE_CHROME_PATH
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))
    options.headless = True
    browser = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH,options=options)
    browser.get('https://www.tokopedia.com/emas/harga-hari-ini/')
    browser.implicitly_wait(10)


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
