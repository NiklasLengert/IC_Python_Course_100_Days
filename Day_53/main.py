from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import re
import time

URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSc9ZreeKtZY2HhaMFoQoi56eSlvXhRfkIvN-yaXUcFbS9DCCw/viewform?usp=dialog"

class ZillowScraper:
    def __init__(self):
        self.soup = None

    def get_data(self):
        self.soup = BeautifulSoup(requests.get(URL).text, "html.parser")

    def filter_prices(self):
        price_elements = self.soup.find_all("span", {"data-test": "property-card-price"})
        prices = []
        for price in price_elements:
            price_text = price.get_text()
            numbers = re.findall(r'[\d,]+\.?\d*', price_text)
            if numbers:
                clean_price = int(float(numbers[0].replace(',', '')))
                prices.append(clean_price)
        
        print(prices)
        return prices

    def filter_addresses(self):
        address_elements = self.soup.find_all("address", {"data-test": "property-card-addr"})
        addresses = [address.get_text().strip() for address in address_elements]
        filtered_addresses = [address for address in addresses]
        print(addresses)
        return filtered_addresses
    
    def filter_links(self):
        link_elements = self.soup.find_all("a", {"data-test": "property-card-link"})
        links = [link.get("href") for link in link_elements]
        filtered_links = [link for link in links if "zillow.com" in link]
        print(filtered_links)
        return filtered_links

class Googleform_Writer:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def write_to_google_form(self, price_list, address_list, link_list, counter):
        self.driver.get(GOOGLE_FORM_LINK)
        for i in range(counter):
            self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input").click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input").send_keys(str(price_list[i]))
            self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input").click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input").send_keys(address_list[i])
            self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input").click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input").send_keys(link_list[i])
            self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span").click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a").click()
            time.sleep(2)

    def close_browser(self):
        self.driver.quit()

zbot = ZillowScraper()
gbot = Googleform_Writer()
zbot.get_data()
prices = zbot.filter_prices()
addresses = zbot.filter_addresses()
links = zbot.filter_links()

gbot.write_to_google_form(prices, addresses, links, len(prices))
gbot.close_browser()
