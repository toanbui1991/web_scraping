import pandas as pd
import numpy as np
import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
vn_30_path = './data/vn_30_list.csv'
vn_30_data = pd.read_csv(vn_30_path)
vn_30_data.drop(columns=["Unnamed: 0"], inplace=True)
stock_dict_path = './data/stocks_dict.csv'
stock_data = pd.read_csv(stock_dict_path)
stock_data.drop(columns=['Unnamed: 0'], inplace=True)
#get links from stocks_data
vn_30_data = pd.merge(left=vn_30_data, right=stock_data, on=['Mã CK'], how='left')
#index=False if do not have named index, which is most of the case
vn_30_data.to_csv('./data/vn_30_with_links.csv', index=False) 

#setting for parsing vn30
driver_path = './chromedriver.exe'
options = ChromeOptions()
options.add_argument("--lang=ko-KR")
stocks = list(vn_30_data["Mã CK"])
links = list(vn_30_data["Link"])
with Chrome(executable_path=driver_path, chrome_options=options) as driver:
    wait = WebDriverWait(driver,15)
    
    for stock, link in zip(stocks, links):
        print('{}: {}'.format(stock, link))
        driver.get(link)
        time.sleep(5)
