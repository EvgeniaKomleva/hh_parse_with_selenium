from selenium import webdriver
import os

driver = webdriver.Chrome()
html_file = os.getcwd() + "//" + "index.html"
driver.get("file:///" + html_file)
some_text = driver.find_element_by_xpath('/html/body/h2')
print(some_text.text)