import requests
import sys
from configparser import ConfigParser
import os

if (os.path.exists("data/data.json")):
    os.remove("data/data.json")
    #print("Remuve")
file = str(sys.argv[1]) #'java.ini'
print(file)
file1 = file
config = ConfigParser()
f = open(file, 'r', encoding='cp1251')
config.read_file(f)

area = config['parametrs']['area'] #str(input("Enter area number(null - all areas, 1 - Moscow, 2- St. Piterburg, 2019 -MO, more areas-+ https://api.hh.ru/areas): "))
specialization = config['parametrs']['specialization'] # str(input("Enter specialization number (1 - IT, 17- sales, more-https://api.hh.ru/specializations): "))
search_period = config['parametrs']['search_period'] # str(input("Enter search period (1- day,3- 3 days,7,30 - mounth,365): "))
# order_by = str(input("Order by (relevance, publication_time, salary_desc, salary_asc): "))
search_text = config['parametrs']['search_text'].encode('cp1251').decode('utf-8')
auth_status = config['parametrs']['auth_status']  # int(input("Do you whant login? (1-yes, null -no): "))
#print(auth_status)
#url1 = ["https://hh.ru/search/resume?area="+area+"&clusters=true&exp_company_size=any&exp_industry=any&exp_period=all_time&logic=normal&no_magic=False&order_by=relevance&search_period="+search_period+"&pos=full_text%2Cworkplace_position&text="+search_text+"&specialization="+specialization]
url = "https://hh.ru/search/resume?area="+area+"&clusters=true&exp_company_size=any&exp_industry=any&exp_period=all_time&logic=normal&no_magic=False&order_by=relevance&pos=full_text%2Cworkplace_position&text="+search_text+"&specialization="+specialization+"&search_period="+search_period+"&items_on_page=100"
print(url)