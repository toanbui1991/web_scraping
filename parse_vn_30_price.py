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
    target_table = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table.banggia.fixed-header')))
    page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')
tables = soup.select_one('table#danhsachlaisuat')
for table in tables:
    print('table: ')
    table