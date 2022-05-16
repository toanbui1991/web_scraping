import time
import pandas as pd
import numpy as np
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

#setting
driver_path = './chromedriver.exe'
target_link = 'https://finance.vietstock.vn/BID-ngan-hang-tmcp-dau-tu-va-phat-trien-viet-nam.htm'
options = ChromeOptions()
options.add_argument("--lang=vi-vn")

data = pd.read_csv('./data/stocks_dict.csv')
hose_data = data[data["Sàn"] == 'HOSE']
stocks = list(hose_data["Mã CK"])
links = list(hose_data["Link"])
columns = ["NN mua", "% NN sở hữu", "Cổ tức TM", "T/S cổ tức", "Beta", "EPS", "P/E", "F P/E", "BVPS", "P/B", 'stock']
data = []
with Chrome(executable_path=driver_path, chrome_options=options) as driver:
    wait = WebDriverWait(driver,15)
    for stock, link in zip(stocks, links):
        driver.get(link)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.col-xs-12.col-sm-5.col-md-4.col-c.bg-50')))
        time.sleep(5)
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        col_one = soup.select_one('div.col-xs-12.col-sm-5.col-md-4.col-c.bg-50')
        values = col_one.select('b.pull-right')
        values = [value.get_text() for value in values]

        col_two = soup.select_one('div.col-xs-12.col-sm-4.col-md-4.col-c-last')
        values_two = col_two.select('b.pull-right')
        values_two = [value.get_text() for value in values_two]

        values = values + values_two
        values.append(stock)
        print('values: {}'.format(values))
        data.append(values)
    data = pd.DataFrame(data, columns=columns)
    data.to_csv('./data/hose_data_key_index.csv', index=False)

        