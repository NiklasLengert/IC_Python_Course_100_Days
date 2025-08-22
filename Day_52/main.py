from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

# I did not want to create a new instagram account for this so I only use username and password variables without a real value
class InstaFollow:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 30)

    def login(self, username, password):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)

        decline_cookies_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"
        cookie_warning = self.driver.find_elements(By.XPATH, decline_cookies_xpath)
        if cookie_warning:
            cookie_warning[0].click()

        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))

        username_input.send_keys(username)
        password_input.send_keys(password)

        time.sleep(2)
        password_input.send_keys(Keys.RETURN)

        time.sleep(5)
        save_login_prompt = self.driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Not now')]")
        if save_login_prompt:
            save_login_prompt.click()

        time.sleep(5)
        notifications_prompt = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Not Now')]")
        if notifications_prompt:
            notifications_prompt.click()

    def find_followers(self, follower_bases):
        time.sleep(3)
        self.driver.get(f"https://www.instagram.com/{follower_bases}/followers/")

        time.sleep(3)
        modal = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))
        for x in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)

    def follow_user(self):
        all_follower_btns = self.driver.find_elements(By.CSS_SELECTOR, value="._aano button")
        time.sleep(3)

        for btn in all_follower_btns:
            try:
                btn.click()
            except Exception as e:
                print(f"Error clicking follow button: {e}")
                cancel_button = self.driver.find_element(By.XPATH, "//button[text()='Cancel']")
                cancel_button.click()
            time.sleep(2)

follower_bot = InstaFollow()
follower_bot.login("your_username", "your_password")
follower_bot.find_followers("target_user_followers")
follower_bot.follow_user()