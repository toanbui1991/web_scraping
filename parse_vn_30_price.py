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
target_link = 'https://banggia.vndirect.com.vn/chung-khoan/vn30'
options = ChromeOptions()
options.add_argument("--lang=vi-vn")

#start browser with context manager
with Chrome(executable_path=driver_path, chrome_options=options) as driver:
    wait = WebDriverWait(driver,15)
    driver.get(target_link)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table#banggia-khop-lenh')))
    time.sleep(10)
    page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')
#get header
columns = ['Mã CK', 'TC', 'Trần', 'Sàn', 'Tông KL', 'Bên mua_Giá 3', 'Bên mua_KL3', 'Bên mua_Giá 2', 'Bên mua_KL2',
'Bên mua_Giá 1', 'Bên mua_KL1', 'Khớp lệnh_Giá', 'Khớp lệnh_KL', 'Khớp lệnh_+/-', 'Bên bán_Giá 3', 'Bên bán_KL3', 'Bên bán_Giá 2', 'Bên bán_KL2',
'Bên bán_Giá 1', 'Bên bán_KL1', 'Giá_Cao', 'Giá_TB', 'Giá_Thấp', 'Dư_Mua', 'Dư_Bán', 'ĐTNN_Mua', 'ĐTNN_Bán']
#get table content
print('length of columns: {}'.format(len(columns)))
tables = soup.select_one('table#banggia-khop-lenh')
tables = pd.read_html(str(tables)) #have to use with table tag
table_data = tables[0]
table_data.columns = columns
output_data = table_data[['Mã CK']]
output_data.to_csv('./data/vn_30_list.csv')
