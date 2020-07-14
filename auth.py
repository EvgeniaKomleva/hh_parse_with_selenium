import time
import io
from selenium import webdriver
from bs4 import BeautifulSoup as soup

auth_status = 0
options = ''

myurl = 'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&logic=normal&no_magic=false&order_by=relevance&pos=full_text&search_period=1&specialization=1&text=&experience=noExperience'
#myurl = 'https://hh.ru/search/resume?text=&st=resumeSearch&logic=normal&pos=full_text&exp_period=all_time&exp_company_size=any&exp_industry=any&specialization=1&area=1&relocation=living_or_relocation&salary_from=&salary_to=&currency_code=RUR&experience=noExperience&education=none&age_from=&age_to=&gender=unknown&order_by=relevance&search_period=1&items_on_page=1'
driver = webdriver.Chrome(executable_path='C:/ProgramData/chocolatey/lib/chromedriver/tools/chromedriver.exe',
                          chrome_options=options)

driver.get(myurl)
time.sleep(1)

filename = "data/data.csv"
f = io.open(filename, "w", encoding="utf-8")
headers = "title,href,last_work_place\n"
f.write(headers)

all_resume = driver.find_elements_by_xpath('//div[@class="resume-search-item__content"]')


for resume in all_resume:
    title_conteiner = resume.find_element_by_xpath('.//div[@class="resume-search-item__header"]')
    title = title_conteiner.find_element_by_xpath('.//span[@class="bloko-section-header-3 bloko-section-header-3_lite"]').text
    href_contein = title_conteiner.find_element_by_xpath('.//span[@class="bloko-section-header-3 bloko-section-header-3_lite"]/a')
    href = href_contein.get_attribute('href')
    last_work = ''
    try:
        last_work = resume.find_element_by_xpath('.//span[@class="resume-search-item__company-name"]').text
    except:
        last_work = 'None'
    f.write(str(title).replace(',', ' ') + "," + str(href) + "," + str(last_work).replace(',', ' ') + "\n")

f.close()

# driver.close()
