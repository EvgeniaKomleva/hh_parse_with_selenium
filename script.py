import time
import io
import csv
import json
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup as soup  # grab page
import os
from selenium.webdriver.chrome.options import Options

auth_status = 0
options = ''
if auth_status == 1:
    options = Options()
    user_name = 'komle'  # впишите ваше имя компьютера
    profile_path = r'C:\Users\{}\AppData\Local\Google\Chrome\User Data'.format(user_name)
    options.add_argument("user-data-dir={}".format(profile_path))

myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&specialization=1&text=&experience=noExperience'
# myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&experience=noExperience&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&text='
driver = webdriver.Chrome(executable_path='C:/ProgramData/chocolatey/lib/chromedriver/tools/chromedriver.exe',
                          chrome_options=options)
# myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&experience=noExperience&label=only_with_salary&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&text=&salary_from=25000&salary_to=40000'
# AUTH!!!!!!!!!!!!!!!!!!!!!!!!

# driver.get('https://hh.ru/account/login?from=employer_index_header&backurl=%2Femployer')
# username = driver.find_element_by_name('username')
# username.send_keys('razilyakomleva@mail.ru')
# password = driver.find_element_by_name('password')
# password.click()
# password.send_keys('test')
# username.submit()

# sleep(300)
# time.sleep(300)
driver.get(myurl)
time.sleep(1)

page_soup = soup(driver.page_source, "html.parser")
resume = page_soup.findAll("div", {"data-qa": "resume-serp__resume"})  # получаем блок с резюме

filename = "data/data.csv"
f = io.open(filename, "w", encoding="utf-8")
headers = "title,href,last_work_place\n"
f.write(headers)

buttons = page_soup.findAll("span", {"class": "pager-item-not-in-short-range"})
last_page = buttons[-1].text
print(last_page)  # получаем количество страниц для парсинга

i = 0
j = 0

while i < int(last_page):
    i = i + 1  # номер текущей страницы парсинга
    # print(i)
    # page_soup = soup(driver.page_source, "html.parser")  # получаем резюме с текущей страницы
    # resume = page_soup.findAll("div", {"data-qa": "resume-serp__resume"})

    for res in resume:
        j = j + 1
        title = res.find("span", {"class": "bloko-section-header-3 bloko-section-header-3_lite"}).text
        href = res.find("a").get('href')
        last_work_Container = res.select('span.resume-search-item__company-name')
        last_work = 'null'
        for work in last_work_Container:
            last_work_text = work.get_text(strip=True)
            last_work = last_work_text
        f.write(str(title).replace(',', ' ') + "," + str(href) + "," + str(last_work).replace(',', ' ') + "\n")

    # if i < int(last_page)-1:
    #     page = driver.find_element_by_xpath('//a[@data-qa="pager-next"]')  # Для перехода на след страницу (кроме последней!)
    #     driver.implicitly_wait(5)
    #     page.click()
    # блок перехода на следующую страницу
    k = 0
    try:
        k = k + 1
        page = driver.find_element_by_xpath(
            '//a[@data-qa="pager-next"]')  # Для перехода на след страницу (кроме последней!)
        driver.implicitly_wait(5)
        page.click()
        driver.implicitly_wait(5)
        # print("OK")
    except:
        print(i)

    driver.implicitly_wait(5)
    page_soup = soup(driver.page_source, "html.parser")  # получаем резюме с текущей страницы
    resume = page_soup.findAll("div", {"data-qa": "resume-serp__resume"})
    if (len(resume) == 0):
        print('AAAAAAAAAAAAAAAAA')
        resume = page_soup.findAll("div", {"data-qa": "resume-serp__results-search"})
        print(i, resume)
    # print(resume)                             resume-serp__results-search resume-serp__results-search
    driver.implicitly_wait(5)

print(k, j, i, last_page)

# для последней страницы
for res in resume:
    j = j + 1
    title = res.find("span", {"class": "bloko-section-header-3 bloko-section-header-3_lite"}).text
    href = res.find("a").get('href')
    last_work_Container = res.select('span.resume-search-item__company-name')
    last_work = 'null'
    for work in last_work_Container:
        last_work_text = work.get_text(strip=True)
        last_work = last_work_text
    f.write(str(title).replace(',', ' ') + "," + str(href) + "," + str(last_work).replace(',', ' ') + "\n")

f.close()

# делаем json (А зачем?)
csvfile = open('data/data.csv', 'r', encoding="utf-8")
jsonfile = open('data/data.json', 'w', encoding="utf-8")
jsonfile.write('[' + '\n')
fieldnames = ("title", "href", "last_work_place")
reader = csv.DictReader(csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write(',' + '\n')
jsonfile.write(']' + '\n')
# driver.close()
