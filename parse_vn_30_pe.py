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
email = 'buixuantoan1991@live.com'
password = 'Buixuantoan@916263'
driver_path = './chromedriver.exe'
target_link = 'https://vietstock.vn/'
options = ChromeOptions()
options.add_argument("--lang=vi-vn")

with Chrome(executable_path=driver_path, chrome_options=options) as driver:
    wait = WebDriverWait(driver,15)
    driver.get(target_link)
    login_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'li > a.title-link.btnlogin')))
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(5)
    # driver.find_element_by_css_selector('li > a.title-link.btnlogin').click()
    # time.sleep(20)
    form = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'form#form1')))
    email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#txtEmailLogin')))
    email_input.send_keys(email)
    password_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#txtPassword')))
    password_input.send_keys(password)
    login_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button#btnLoginAccount')))
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(5)
    target_link = 'https://finance.vietstock.vn/doanh-nghiep-a-z/?page=1'
    driver.get(target_link)
    table_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#az-container')))
    time.sleep(5)
    page_source = driver.page_source
    #parse rendered page_source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    title =  soup.select_one('h1.title.style-scope.ytd-video-primary-info-renderer yt-formatted-string')
    comments = soup.select('div.style-scope.ytd-comment-renderer#body')
    table = table_container.find_element(by=By.CSS_SELECTOR, value='table')
    tables = pd.read_html(str(table.page_source))
    table = tables[0]
    print('table: ')
    print(table)
    page_source = driver.page_source