import time
import io
import csv
import json
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup as soup  # grab page
import os

os.remove("data/data.json")
myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&specialization=1&text=&experience=noExperience'

driver = webdriver.Chrome('C:/ProgramData/chocolatey/lib/chromedriver/tools/chromedriver.exe')
driver.get(myurl)
time.sleep(1)

# parse html
page_soup = soup(driver.page_source, "html.parser")

# grab reviews
resume = page_soup.findAll("div", {"class": "resume-search-item__content"})
# make the csv file

filename = "data/data.csv"
f = io.open(filename, "w", encoding="utf-8")

# headers of csv file
headers = "title,href,last_work_place\n"
buttons = page_soup.findAll("span", {"class": "pager-item-not-in-short-range"})

last_page = buttons[-1].text

f.write(headers)

i = 0
while i < int(last_page):
    i = i + 1
    for res in resume:
        title_Container = res.findAll("span", {"class": "bloko-section-header-3 bloko-section-header-3_lite"})
        title = title_Container[0].text
        href = res.find("a").get('href')
        # last_work_Container = res.find("span", {"class": "resume-search-item__company-name"})
        # last_work = last_work_Container.get_text()
        last_work_Container = res.select('span.resume-search-item__company-name')
        # print(headlines)
        last_work = 'null'
        for work in last_work_Container:
            last_work_text = work.get_text(strip=True)
            last_work = last_work_text
        f.write(str(title).replace(',', ' ') + "," + str(href) + "," + str(last_work).replace(',', ' ') + "\n")
        #f.write()
        #f.write("{ title : " + title + ", href: " + href + ", last_work_place :" + last_work + "}"+"\n")


#f.write("]")
f.close()
csvfile = open('data/data.csv', 'r', encoding="utf-8")
jsonfile = open('data/data.json', 'w', encoding="utf-8")
jsonfile.write('['+'\n')
fieldnames = ("title","href","last_work_place")
reader = csv.DictReader(csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write(','+'\n')
jsonfile.write(']'+'\n')
#driver.close()
