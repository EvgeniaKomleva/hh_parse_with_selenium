import time
import io
import csv
import json
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup as soup  # grab page
import os

#os.remove("data/data.json")
myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&specialization=1&text=&experience=noExperience'

driver = webdriver.Chrome('C:/ProgramData/chocolatey/lib/chromedriver/tools/chromedriver.exe')
#driver.get(myurl)
#AUTH!!!!!!!!!!!!!!!!!!!!!!!!

# driver.get('https://hh.ru/account/login?from=employer_index_header&backurl=%2Femployer')
# username = driver.find_element_by_name('username')
# username.send_keys('razilyakomleva@mail.ru')
# password = driver.find_element_by_name('password')
# password.click()
# password.send_keys('Hfpbkz115')
# username.submit()

#sleep(300)
#time.sleep(300)
driver.get(myurl)
#driver.Navigate().GoToUrl(myurl)
time.sleep(1)
# parse html
page_soup = soup(driver.page_source, "html.parser")

# grab reviews
resume = page_soup.findAll("div", {"data-qa": "resume-serp__resume"})
#print(len(resume))
#print(resume[0])
# make the csv file

filename = "data/data.csv"
f = io.open(filename, "w", encoding="utf-8")

# headers of csv file
headers = "title,href,last_work_place\n"
buttons = page_soup.findAll("span", {"class": "pager-item-not-in-short-range"})
print(len(buttons))
last_page = buttons[-1].text
some_button = page_soup.findAll("span", {"class" : "bloko-form-spacer"})
#last_button = some_button[4]
# #some_button.findAll("a", {"class" : "bloko-button"})
#last_button = page_soup.find_element_by_class_name('bloko-button')
#print(some_button[4])
print("_"*100)
#print(button)
#print(len(botton))
#print(last_button)
f.write(headers)
i = 0
j =0
while i < int(last_page)-1:
    i = i + 1
    #'//*[@id="HH-React-Root"]/div/div/div/div[2]/div[2]/div/div[3]/div/span[3]/a'
    #'//*[@id="HH-React-Root"]/div/div/div/div[2]/div[2]/div/div[3]/div/span[3]'
    #driver.find_element_by_xpath('//*[@id="HH-React-Root"]/div/div/div/div[2]/div[2]/div/div[3]/div/span[3]/a').click()

    page_soup = soup(driver.page_source, "html.parser")
    # grab reviews
    resume = page_soup.findAll("div", {"data-qa": "resume-serp__resume"})
    # if (i < 10):
    #
    #     page = last_button.click()
    # if (i == 40):
    #     page = ''#driver.find_element_by_xpath('//*[@id="HH-React-Root"]/div/div/div/div[2]/div[2]/div/div[3]/div/span[1]/span[4]/a').click()
    #
    for res in resume:
        j =j+1
        title = res.find("span", {"class": "bloko-section-header-3 bloko-section-header-3_lite"}).text
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

    #page = driver.find_element_by_xpath('//*[@id="HH-React-Root"]/div/div/div/div[2]/div[2]/div/div[3]/div/span[2]')
    page = driver.find_element_by_xpath('//a[@data-qa="pager-next"]')#Для перехода на след страницу
    driver.implicitly_wait(5)
    page.click()
    #time.sleep(3)
    #driver.save_screenshot("hh.png")
    #page_soup = soup(driver.page_source, "html.parser")
    #resume = page_soup.findAll("div", {"data-qa": "resume-serp__resume"})


print(j, i, last_page)

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
