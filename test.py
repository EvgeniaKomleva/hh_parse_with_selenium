import time
import io
import csv
import json
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup as soup
import os
from selenium.webdriver.chrome.options import Options

auth_status = 0
options = ''
myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&experience=noExperience&label=only_with_salary&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&specialization=1&text=&salary_from=25000&salary_to=40000'
#myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&specialization=1&text=&experience=noExperience'
driver = webdriver.Chrome(executable_path='C:/ProgramData/chocolatey/lib/chromedriver/tools/chromedriver.exe',
                          chrome_options=options)

driver.get(myurl)
time.sleep(1)
buttons = driver.find_element_by_xpath('div[@data-qa="pager-block"]')
print(buttons)
