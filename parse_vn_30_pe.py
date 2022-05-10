import time, sys
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

    #parse  first page
    target_link = 'https://finance.vietstock.vn/doanh-nghiep-a-z/?page=1'
    driver.get(target_link)
    table_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#az-container')))
    time.sleep(5)
    page_source = driver.page_source
    #parse rendered page_source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    title =  soup.select_one('h1.title.style-scope.ytd-video-primary-info-renderer yt-formatted-string')
    comments = soup.select('div.style-scope.ytd-comment-renderer#body')
    page_source = driver.page_source

    #parse rendered page_source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    table_html =soup.select_one('table.table.table-striped.table-bordered.table-hover.table-middle.pos-relative.m-b')
    tables = pd.read_html(str(table_html))
    table = tables[0]
    print('the shape of table: {}'.format(table.shape))
    #find link for each stock code
    #use beautifulsoup element methods like: get_text() and get('attr')
    links = table_html.select('a.title-link')
    links = [l.get('href') for l in links]
    print('the length of links: {}'.format(len(links)))
    table['link'] = links
    table.to_csv('./data/stocks_page_1.csv')
    
    #continue to parse other pages
    #prepare for the loop
    page_number = 1
    continue_flag = True
    while continue_flag:
        try:
            #move to the next links
            next_button = driver.find_element(By.CSS_SELECTOR, 'button#btn-page-next')
            driver.execute_script("arguments[0].click();", next_button)
            page_number += 1 #move the next page and increase page_number
            time.sleep(5)
            table_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#az-container')))
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            table_html =soup.select_one('table.table.table-striped.table-bordered.table-hover.table-middle.pos-relative.m-b')
            tables = pd.read_html(str(table_html))
            table = tables[0]
            print('the shape of table: {}'.format(table.shape))
            #find link for each stock code
            #use beautifulsoup element methods like: get_text() and get('attr')
            links = table_html.select('a.title-link')
            links = [l.get('href') for l in links]
            print('the length of links: {}'.format(len(links)))
            table['link'] = links
            table.to_csv('./data/stocks_page_{}.csv'.format(page_number))
            if page_number == 161:
                print('parsing completed!')
                sys.exit(0)


        except Exception as e:
            print('Exception: {}'.format(e))
            continue_flag = False

#try to combine parsed data together
# data = pd.read_csv('')