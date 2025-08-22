from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from time import sleep
import os

facebook_email = os.getenv("FB_EMAIL")
facebook_password = os.getenv("FB_PASSWORD")

browser = webdriver.Chrome()

browser.get("http://www.tinder.com")

sleep(2)
signin_btn = browser.find_element(By.XPATH, value='//*[text()="Log in"]')
signin_btn.click()

sleep(2)
facebook_btn = browser.find_element(By.XPATH, value='//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button')
facebook_btn.click()

sleep(2)
main_window = browser.window_handles[0]
facebook_window = browser.window_handles[1]
browser.switch_to.window(facebook_window)
print(browser.title)

email_field = browser.find_element(By.XPATH, value='//*[@id="email"]')
pass_field = browser.find_element(By.XPATH, value='//*[@id="pass"]')
email_field.send_keys(facebook_email)
pass_field.send_keys(facebook_password)
pass_field.send_keys(Keys.ENTER)

browser.switch_to.window(main_window)
print(browser.title)

sleep(5)

location_btn = browser.find_element(By.XPATH, value='//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
location_btn.click()

notify_btn = browser.find_element(By.XPATH, value='//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
notify_btn.click()

cookie_btn = browser.find_element(By.XPATH, value='//*[@id="content"]/div/div[2]/div/div/div[1]/button')
cookie_btn.click()

swipe_count = 0
while swipe_count < 100:
    sleep(1)

    try:
        print("called")
        heart_btn = browser.find_element(By.XPATH, value=
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        heart_btn.click()

    except ElementClickInterceptedException:
        try:
            popup_close = browser.find_element(By.CSS_SELECTOR, value=".itsAMatch a")
            popup_close.click()

        except NoSuchElementException:
            sleep(2)
    
    swipe_count += 1

browser.quit()