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

key_words = ['HTML', 'CSS']
auth_status = 0
options = ''
#myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&experience=noExperience&label=only_with_salary&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&specialization=1&text=&salary_from=25000&salary_to=40000'
myurl = 'https://hh.ru/resume/f21f626b0005469c550048714c365a495a366a?hhtmFrom=resume_search_result'
driver = webdriver.Chrome(executable_path='C:/ProgramData/chocolatey/lib/chromedriver/tools/chromedriver.exe',
                          chrome_options=options)

driver.get(myurl)
time.sleep(1)
expiriance = driver.find_element_by_xpath('.//div[@class="bloko-tag-list"]').text
skill_list = str(expiriance).split('\n')
match_count = 0
for skil in skill_list:
    for key in key_words:
        if (skil == key):
            match_count = match_count + 1
print(match_count)
#print(expiriance)
driver.close()
