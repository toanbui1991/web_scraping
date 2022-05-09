import time
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

#setting
driver_path = './chromedriver.exe'
target_link = 'https://www.youtube.com/watch?v=_wlTizkaQx8&t=132s'
options = ChromeOptions()
options.add_argument("--lang=vi-vn")