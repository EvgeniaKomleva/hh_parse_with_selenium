import script
import time

driver.get('https://hh.ru/account/login?from=employer_index_header&backurl=%2Femployer')
# This gets the element name i.e your username field.
# We’ll learn how to do this later (If you are curious)
username = driver.find_element_by_name('username')
# Now we click that ,virtually ofcourse. username.click()
# send_keys() is like typing words on the element
username.send_keys('komelva.1999@inbox.ru')
# Same goes for Password Field
password = driver.find_element_by_name('password')
password.click()
password.send_keys ('Hfpbkz115')
# click on submit button
username.submit()
sleep(300)