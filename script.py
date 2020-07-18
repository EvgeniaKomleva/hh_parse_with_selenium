import time
import io
import csv
import json
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.chrome.options import Options


def multiply_request(urls, key_words, auth_status):
    for url in urls:
        base(url, key_words, auth_status)


def click_on_resume(driver, key_words, resume, window_before, j):
    resume_button = resume.find_element_by_xpath(
        './/span[@class="bloko-section-header-3 bloko-section-header-3_lite"]/a')

    resume_button.click()
    driver.implicitly_wait(50)
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)  # чтобы перейти в другую вкладку
    match_count = get_key_words(driver, key_words, resume)
    all_job = get_all_job(driver)
    citizenship = add_citizenship(driver)
    driver.implicitly_wait(150)
    driver.close()
    driver.switch_to.window(window_before)
    driver.implicitly_wait(50)
    return match_count, all_job, citizenship


def get_all_job(driver):
    jobs_with_description = driver.find_element_by_xpath(
        './/div[@class="bloko-column bloko-column_xs-4 bloko-column_s-6 bloko-column_m-7 bloko-column_l-10"]')
    jobs = jobs_with_description.find_elements_by_xpath('.//div[@class="resume-block__sub-title"]')
    last_jobs = []
    for last_job in jobs:
        last_jobs.append(last_job.text)
    return last_jobs


def get_key_words(driver, key_words, resume):
    expiriance = driver.find_element_by_xpath('.//div[@class="bloko-tag-list"]').text
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


def auth():
    options = Options()
    user_name = 'komle'  # впишите ваше имя компьютера
    profile_path = r'C:\Users\{}\AppData\Local\Google\Chrome\User Data'.format(user_name)
    options.add_argument("user-data-dir={}".format(profile_path))
    return options


def base(myurl, key_words, auth_status):
    options = ''
    if auth_status == 1:
        options = auth()
    driver = webdriver.Chrome(executable_path='C:/ProgramData/chocolatey/lib/chromedriver/tools/chromedriver.exe',
                              chrome_options=options)

    driver.get(myurl)
    time.sleep(1)

    all_resume = driver.find_elements_by_xpath('//div[@class="resume-search-item__content"]')
    window_before = driver.window_handles[0]
    filename = "data/data.csv"
    f = io.open(filename, "w", encoding="utf-8")
    headers = "title,href,last_work_place,match_count,all_jobs, citizenship\n"
    f.write(headers)

    last_page = 0
    try:
        buttons = driver.find_element_by_xpath('//*[@id="HH-React-Root"]/div/div/div/div[2]/div[2]/div/div[3]/div').text
        #print(len(buttons))
        last_page = str(buttons)[len(buttons) - 8:-6].replace('...', '')
        #print(last_page)
    except:
        last_page = 1
    i = 0
    j = 0
    while i < int(last_page):

        i = i + 1  # номер текущей страницы парсинга
        for resume in all_resume:
            j = j + 1  # Номер текущего резюме
            title_conteiner = resume.find_element_by_xpath('.//div[@class="resume-search-item__header"]')
            title = title_conteiner.find_element_by_xpath(
                './/span[@class="bloko-section-header-3 bloko-section-header-3_lite"]').text
            href_contein = title_conteiner.find_element_by_xpath(
                './/span[@class="bloko-section-header-3 bloko-section-header-3_lite"]/a')
            href = href_contein.get_attribute('href')

            match_count, all_job, citizenship = click_on_resume(driver, key_words, resume, window_before, j)
            last_work = ''

            try:
                last_work = resume.find_element_by_xpath('.//span[@class="resume-search-item__company-name"]').text
            except:
                last_work = 'None'

            f.write(str(title).replace(',', ' ') + "," + str(href) + "," + str(last_work).replace(',', ' ') + "," + str(
                match_count) + "," + str(all_job) + "," + str(citizenship) + "\n")

        # блок перехода на следующую страницу
        try:
            page = driver.find_element_by_xpath(
                '//a[@data-qa="pager-next"]')  # Для перехода на след страницу (кроме последней!)
            page.click()
            driver.implicitly_wait(5)
            window_before = driver.window_handles[0]
        except:
            print('last page done')

        all_resume = driver.find_elements_by_xpath('//div[@class="resume-search-item__content"]')

        if len(all_resume) == 0:
            print('AAAAAAAAAAAAAAAAA')
            print(i)

    f.close()
    transform_to_json(driver)
    print(last_page)


def transform_to_json(driver):
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
    driver.close()


if __name__ == '__main__':
    key_words = ['HTML5', 'CSS3']
    url1 = ''
    url2 = ''
    # urls = [url1, url2]
    auth_status = 0
    myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&experience=noExperience&items_on_page=100&label=only_with_salary&logic=normal&no_magic=false&order_by=relevance&pos=full_text&salary_from=25000&salary_to=40000&search_period=1&text=&specialization=1.9'
    urls = [myurl]
    multiply_request(urls, key_words, auth_status)
