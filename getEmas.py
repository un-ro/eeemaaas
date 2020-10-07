import sqlite3
from datetime import datetime
from sqlite3 import Error
from selenium.webdriver import Chrome


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def checking(price):
    tanggal = datetime.today().strftime('%d-%m-%Y')
    buy_price = price[0]
    sale_price = price[1]

    sql = 'INSERT INTO emas VALUES ( {}, {}, {})'.format(str(tanggal), str(buy_price), str(sale_price))
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()
    return cur.lastrowid


def updater():
    browser = Chrome()
    browser.get('https://www.tokopedia.com/emas/harga-hari-ini/')
    buy_price = browser.find_elements_by_xpath('//*[@class="main-price"]')
    price = []
    for i in buy_price:
        price.append(i.text)
    buy_price = price[0]
    sale_price = price[1]

    buy_price = buy_price[2:]
    sale_price = sale_price[2:]

    buy_price = buy_price.replace(".", "")
    sale_price = sale_price.replace(".", "")

    price.clear()

    price.append(int(buy_price))
    price.append(int(sale_price))

    browser.close()
    return price


if __name__ == '__main__':
    conn = create_connection('mydatabase.db')
    checking(updater())