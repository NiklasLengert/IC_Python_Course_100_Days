from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import smtplib
import os

load_dotenv()

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Accept-Encoding": "gzip, deflate, br"
}

practice_url = "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

response = requests.get(live_url, headers=header)
soup = BeautifulSoup(response.content, "html.parser")
print(soup.prettify())
price = soup.find(class_="a-offscreen").get_text()
price_without_currency = price.replace("$", "")
print(f"The price of the Instant Pot is: {price_without_currency}")

price_float = float(price_without_currency)
print(f"The price of the Instant Pot as a float is: {price_float}")


# Send an email with the price
title = soup.find(id="productTitle").get_text().strip()
print(f"The title of the Instant Pot is: {title}")

BUY_PRICE = 100.00

SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if price_float < BUY_PRICE:
    message = f"Subject: {title} is now {price}\n"

    with smtplib.SMTP(SMTP_ADDRESS, 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)