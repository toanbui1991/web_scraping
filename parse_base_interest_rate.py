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
target_link = 'https://portal.vietcombank.com.vn/Personal/lai-suat/Pages/lai-suat.aspx?devicechannel=default'
options = ChromeOptions()
options.add_argument("--lang=vi-vn")

#start browser with context manager
with Chrome(executable_path=driver_path, chrome_options=options) as driver:
    wait = WebDriverWait(driver,15)
    driver.get(target_link)
    target_table = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table#danhsachlaisuat')))
    page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')
target_table = soup.select_one('table#danhsachlaisuat')
# print('target_table: {}'.format(target_table))
#have to turn html to str for read_html. pd.read_html(io) with io: string, pth object, file like object
#read_html() method return a list of pandas dataframe
table_list = pd.read_html(str(target_table))
table_data = table_list[0]
clean_table = table_data[np.logical_not(table_data['Kỳ hạn'].isin(['Tiết kiệm', 'Không kỳ hạn', 'Tiền gửi có kỳ hạn']))]
#using string method rstrip('char') and series astype('float') method
clean_table['VND'] = clean_table['VND'].str.rstrip('%').astype('float')
clean_table['EUR'] = clean_table['EUR'].str.rstrip('%').astype('float')
clean_table['USD'] = clean_table['USD'].str.rstrip('%').astype('float')

#convert series to list so that we eaiser to index and get element
annual_rate = list(clean_table['VND'][clean_table['Kỳ hạn'] == '12 tháng'])
annual_rate = float(annual_rate[0])
unit_price = 100 / annual_rate
print('annual_rate: {}'.format(annual_rate))
print('unit price of captical: {}'.format(unit_price))