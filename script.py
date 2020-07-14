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
if auth_status == 1:
    options = Options()
    user_name = 'komle'  # впишите ваше имя компьютера
    profile_path = r'C:\Users\{}\AppData\Local\Google\Chrome\User Data'.format(user_name)
    options.add_argument("user-data-dir={}".format(profile_path))
myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&experience=noExperience&label=only_with_salary&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&specialization=1&text=&salary_from=25000&salary_to=40000'
#myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&specialization=1&text=&experience=noExperience'
driver = webdriver.Chrome(executable_path='C:/ProgramData/chocolatey/lib/chromedriver/tools/chromedriver.exe',
                          chrome_options=options)

driver.get(myurl)
time.sleep(1)

page_soup = soup(driver.page_source, "html.parser")
#resume = page_soup.findAll("div", {"data-qa": "resume-serp__resume"})  # получаем блок с резюме
all_resume = driver.find_elements_by_xpath('//div[@class="resume-search-item__content"]')

filename = "data/data.csv"
f = io.open(filename, "w", encoding="utf-8")
headers = "title,href,last_work_place\n"
f.write(headers)

buttons = page_soup.findAll("span", {"class": "pager-item-not-in-short-range"})
last_page = 3#buttons[-1].text
print(last_page)  # получаем количество страниц для парсинга

i = 0
j = 0

while i < int(last_page):
    i = i + 1  # номер текущей страницы парсинга

    for resume in all_resume:
        title_conteiner = resume.find_element_by_xpath('.//div[@class="resume-search-item__header"]')
        title = title_conteiner.find_element_by_xpath(
            './/span[@class="bloko-section-header-3 bloko-section-header-3_lite"]').text
        href_contein = title_conteiner.find_element_by_xpath(
            './/span[@class="bloko-section-header-3 bloko-section-header-3_lite"]/a')
        href = href_contein.get_attribute('href')
        last_work = ''
        try:
            last_work = resume.find_element_by_xpath('.//span[@class="resume-search-item__company-name"]').text
        except:
            last_work = 'None'
        f.write(str(title).replace(',', ' ') + "," + str(href) + "," + str(last_work).replace(',', ' ') + "\n")

    # if i < int(last_page)-1:
    #     page = driver.find_element_by_xpath('//a[@data-qa="pager-next"]')  # Для перехода на след страницу (кроме последней!)
    #     driver.implicitly_wait(5)
    #     page.click()
    # блок перехода на следующую страницу
    k = 0
    try:
        k = k + 1
        page = driver.find_element_by_xpath('//a[@data-qa="pager-next"]')  # Для перехода на след страницу (кроме последней!)
        driver.implicitly_wait(5)
        page.click()
        driver.implicitly_wait(5)
        # print("OK")
    except:
        print('cant parse{}'.format(i))

    driver.implicitly_wait(5)
    page_soup = soup(driver.page_source, "html.parser")  # получаем резюме с текущей страницы
    #resume = page_soup.findAll("div", {"data-qa": "resume-serp__resume"})
    all_resume = driver.find_elements_by_xpath('//div[@class="resume-search-item__content"]')

    if (len(all_resume) == 0):
        print('AAAAAAAAAAAAAAAAA')
        #resume = driver.find_elements_by_xpath('//div[@data-qa="resume-serp__results-search"]')
        #resume = page_soup.findAll("div", {"data-qa": "resume_search_result"})

        #page_soup = soup(resume.page_source, "html.parser")
        print(i)
    # print(resume)                             resume-serp__results-search resume-serp__results-search
    driver.implicitly_wait(5)

print(k, j, i, last_page)

# для последней страницы
# for resume in all_resume:
#     title_conteiner = resume.find_element_by_xpath('.//div[@class="resume-search-item__header"]')
#     title = title_conteiner.find_element_by_xpath('.//span[@class="bloko-section-header-3 bloko-section-header-3_lite"]').text
#     href_contein = title_conteiner.find_element_by_xpath('.//span[@class="bloko-section-header-3 bloko-section-header-3_lite"]/a')
#     href = href_contein.get_attribute('href')
#     last_work = ''
#     try:
#         last_work = resume.find_element_by_xpath('.//span[@class="resume-search-item__company-name"]').text
#     except:
#         last_work = 'None'
#     f.write(str(title).replace(',', ' ') + "," + str(href) + "," + str(last_work).replace(',', ' ') + "\n")

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
