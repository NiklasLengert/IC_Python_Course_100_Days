from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# driver = webdriver.Chrome(chrome_options)
# # driver.get("https://en.wikipedia.org/wiki/Main_Page")
# driver.get("https://secure-retreat-92358.herokuapp.com/")

# # article_count = driver.find_element(By.XPATH, value="//*[@id='articlecount']/ul/li[2]/a[1]")
# # # article_count.click()
# input_first_name = driver.find_element(By.NAME, value="fName")
# input_first_name.click()
# input_first_name.send_keys("Niklas")

# # all_portals = driver.find_element(By.LINK_TEXT, value="Content portals")
# # # all_portals.click()
# input_last_name = driver.find_element(By.NAME, value="lName")
# input_last_name.click()
# input_last_name.send_keys("Lengert")

# # search_bar = driver.find_element(By.NAME, value="search")
# # search_bar.send_keys("Python", Keys.ENTER)
# input_mail = driver.find_element(By.NAME, value="email")
# input_mail.click()
# input_mail.send_keys("xxx@gmail.com")

# sign_up = driver.find_element(By.CSS_SELECTOR, value="form button")
# sign_up.click()

# from selenium.common.exceptions import NoSuchElementException
# from time import sleep, time

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=chrome_options)

# driver.get("https://ozh.github.io/cookieclicker/")
# sleep(3)


# print("Looking for language selection...")
# try:
#     language_button = driver.find_element(by=By.ID, value="langSelect-EN")
#     print("Found language button, clicking...")
#     language_button.click()
#     sleep(3)
# except NoSuchElementException:
#     print("Language selection not found")

# sleep(2)
# cookie = driver.find_element(by=By.ID, value="bigCookie")

# item_ids = [f"product{i}" for i in range(18)]

# wait_time = 5
# timeout = time() + wait_time
# five_min = time() + 60 * 5

# while True:
#     cookie.click()

#     if time() > timeout:
#         try:
#             cookies_element = driver.find_element(by=By.ID, value="cookies")
#             cookie_text = cookies_element.text
#             cookie_count = int(cookie_text.split()[0].replace(",", ""))

#             products = driver.find_elements(by=By.CSS_SELECTOR, value="div[id^='product']")

#             best_item = None
#             for product in reversed(products):
#                 if "enabled" in product.get_attribute("class"):
#                     best_item = product
#                     break

#             if best_item:
#                 best_item.click()
#                 print(f"Bought item: {best_item.get_attribute('id')}")

#         except (NoSuchElementException, ValueError):
#             print("Couldn't find cookie count or items")

#         timeout = time() + wait_time

#     if time() > five_min:
#         try:
#             cookies_element = driver.find_element(by=By.ID, value="cookies")
#             print(f"Final result: {cookies_element.text}")
#         except NoSuchElementException:
#             print("Couldn't get final cookie count")
#         break