import datetime
import time
import io
import csv
import json
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import get_url
import sys
from configparser import ConfigParser
import os

def get_contact_hr(driver):
    name = driver.find_element_by_xpath('//div[@class="resume-header-name"]').text
    
    return name


def multiply_request(urls, key_words, auth_status, user_name, are_you_hr):
    for url in urls:
        base(url, key_words, auth_status, user_name, are_you_hr)


def click_on_resume(driver, key_words, resume, window_before, j):
    resume_button = resume.find_element_by_xpath(
        './/span[@class="bloko-section-header-3 bloko-section-header-3_lite"]/a')
    try:
        resume_button.click()
        driver.implicitly_wait(5)
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)  # чтобы перейти в другую вкладку
        match_count = get_key_words(driver, key_words, resume)
        all_job = get_all_job(driver)
        citizenship = add_citizenship(driver)
        driver.implicitly_wait(5)
        driver.close()
        driver.switch_to.window(window_before)
        driver.implicitly_wait(5)
    except:
        match_count, all_job, citizenship = 0, 0, 0
        print("Not clickable")
    return match_count, all_job, citizenship


def get_all_job(driver):
    jobs_with_description = driver.find_element_by_xpath(
        './/div[@class="bloko-column bloko-column_xs-4 bloko-column_s-6 bloko-column_m-7 bloko-column_l-10"]')
    jobs = jobs_with_description.find_elements_by_xpath('.//div[@class="resume-block__sub-title"]')
    last_jobs = ''
    for last_job in jobs:
        last_jobs = last_jobs + ' ' + last_job.text
    return last_jobs


def get_key_words(driver, key_words, resume):
    try:
        expiriance = driver.find_element_by_xpath('.//div[@class="bloko-tag-list"]').text
    except:
        expiriance = ''
    skill_list = str(expiriance).split('\n')
    match_count = 0
    for skill in skill_list:
        for key in key_words:
            if skill == key:
                match_count = match_count + 1
    return match_count


def add_citizenship(driver):
    citizenship_contein = driver.find_element_by_xpath('//div[@data-qa="resume-block-additional"]')
    citizenship = citizenship_contein.find_element_by_xpath('.//div[@class="resume-block-container"]/p[1]').text
    return citizenship[13:]


def auth(user_name):
    options = Options()
    #user_name = 'komle'  # впишите ваше имя компьютера
    profile_path = r'C:\Users\{}\AppData\Local\Google\Chrome\User Data'.format(user_name)
    options.add_argument("user-data-dir={}".format(profile_path))
    return options


def base(myurl, key_words, auth_status, user_name, are_you_hr):
    options = ''
    if auth_status == 1:
        options = auth(user_name)
    driver = webdriver.Chrome(executable_path='C:/ProgramData/chocolatey/lib/chromedriver/tools/chromedriver.exe',
                              chrome_options=options)

    driver.get(myurl)
    time.sleep(1)

    all_resume = driver.find_elements_by_xpath('//div[@class="resume-search-item__content-wrapper"]')
    print(len(all_resume))
    window_before = driver.window_handles[0]
    filename = "data/data.csv"
    f = io.open(filename, "w", encoding="utf-8")
    headers = "title,href,last_work_place,match_count,all_jobs,citizenship\n"
    f.write(headers)

    last_page = 0
    try:
        buttons = driver.find_element_by_xpath('//*[@id="HH-React-Root"]/div/div/div/div[2]/div[2]/div/div[3]/div').text
        #print(len(buttons))
        last_page = str(buttons)[len(buttons) - 8:-6].replace('...', '')
        #print(last_page)
    except:
        last_page = 1

    print(last_page)
    i = 0
    j = 0
    while i < int(last_page):

        i = i + 1  # номер текущей страницы парсинга
        for resume in all_resume:
            j = j + 1  # Номер текущего резюме
            #title_conteiner = resume.find_element_by_xpath('.//div[@class="resume-search-item__header"]')
            title = resume.find_element_by_class_name('resume-search-item__name').text
            #title = title_conteiner.find_element_by_xpath(
            #    './/span[@class="bloko-section-header-3 bloko-section-header-3_lite"]').text
            #href_contein = title_conteiner.find_element_by_xpath(
            #    './/span[@class="bloko-section-header-3 bloko-section-header-3_lite"]/a')
            href = resume.find_element_by_class_name('resume-search-item__name').get_attribute('href')
            if are_you_hr == 1:
                get
            match_count, all_job, citizenship = click_on_resume(driver, key_words, resume, window_before, j)
            last_work = ''

            try:
                last_work = resume.find_element_by_class_name('resume-search-item__company-name').text
            except:
                last_work = 'None'

            f.write(str(title).replace(',', ' ') + "," + str(href) + "," + str(last_work).replace(',', ' ') + "," + str(
                match_count) + "," + str(all_job).replace(',', ' ') + "," + str(citizenship).replace(',', ' ') + "\n")

        # блок перехода на следующую страницу
        try:
            page = driver.find_element_by_xpath(
                '//a[@data-qa="pager-next"]')  # Для перехода на след страницу (кроме последней!)
            page.click()
            driver.implicitly_wait(5)
            window_before = driver.window_handles[0]
        except:
            print('last page done')
        all_resume_contein = driver.find_element_by_xpath('//div[@data-qa="resume-serp__results-search"]')
        all_resume = all_resume_contein.find_elements_by_xpath('.//div[@data-qa="resume-serp__resume"]')
        print(len(all_resume))

    f.close()
    transform_to_json(driver)
    print(last_page)


def transform_to_json(driver):
    # делаем json
    csvfile = open('data/data.csv', 'r', encoding="utf-8")
    jsonfile = open('data/data.json', 'w', encoding="utf-8")
    jsonfile.write('[' + '\n')
    fieldnames = ("title", "href", "last_work_place", "match_count","all_jobs", "citizenship")
    reader = csv.DictReader(csvfile, fieldnames)
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write(',' + '\n')
    jsonfile.write(']' + '\n')
    #driver.close()


if __name__ == '__main__':
    start_time = datetime.now()
    file = str(sys.argv[1])  # 'java.ini'
    file_name = file[:-4]
    config = ConfigParser()
    config.read(file)
    auth_status = config['parametrs']['auth_status']  # int(input("Do you want login? (1-yes, null -no): "))
    user_name = config['parametrs']['user_name']
    key_words = config['parametrs']['key_word']#['HTML5', 'HTML', 'CSS3'] # нужно из конфига!!!!!!!!!!!!!!!
    intersted_company = 'RASA'
    are_you_hr = config['parametrs']['are_you_hr']
    url1 = ''
    url2 = ''
    # urls = [url1, url2]
    #auth_status = 0
    myurl = get_url.url#'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&items_on_page=20&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&specialization=1.327&text=&experience=between3And6'
    #myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&items_on_page=20&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&text=&specialization=1.327'
    #myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&experience=noExperience&items_on_page=100&label=only_with_salary&logic=normal&no_magic=false&order_by=relevance&pos=full_text&salary_from=25000&salary_to=40000&search_period=1&text=&specialization=1.9'
    urls = [myurl]
    multiply_request(urls, key_words, auth_status, user_name, are_you_hr)
    print(datetime.now() - start_time)
# фильтр на несовпадающих по ключевым словам кондидатов(в трансформ дата) -- OK
# фильтр на дубли(повторяющиеся резюме) -- OK
# фильтр компаний -- ОК
# html ФИО