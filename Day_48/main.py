from selenium import webdriver
from selenium.webdriver.common.by import By


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)

# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://www.python.org/")

# search_bar = driver.find_element(By.NAME, "q")
# print(search_bar.tag_name)

# driver.quit()


# driver = webdriver.Chrome()
# driver.get("https://python.org")

# python_event_dic = {}

# dates = driver.find_elements(By.CSS_SELECTOR, value=".event-widget time")
# for date in dates:
#     print(date.text)

# events = driver.find_elements(By.CSS_SELECTOR, value=".event-widget li a")
# for event in events:
#     print(event.text)

# for n in range(len(events)):
#     python_event_dic[n] = {
#         "time": dates[n].text,
#         "name": events[n].text
#     }

# print(python_event_dic)

# driver.quit()

