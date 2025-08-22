from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class InternetSpeedMonitor:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.down = 0
        self.up = 0
        self.wait = WebDriverWait(self.driver, 30)
    
    def check_speed(self):
        try:
            self.driver.get("https://www.speedtest.net/")
            time.sleep(3)

            try:
                terms_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
                terms_btn.click()
            except:
                pass

            go_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".start-button a")))
            go_btn.click()
            time.sleep(45)
            
            self.down = float(self.driver.find_element(By.CSS_SELECTOR, "[data-download-status-value]").text)
            self.up = float(self.driver.find_element(By.CSS_SELECTOR, "[data-upload-status-value]").text)
            
            print(f"Download: {self.down} Mbps")
            print(f"Upload: {self.up} Mbps")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.driver.quit()

checker = InternetSpeedMonitor()
checker.check_speed()