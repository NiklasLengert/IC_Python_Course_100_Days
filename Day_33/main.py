import requests
from datetime import datetime
import smtplib
import time

def is_iss_overhead():
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    iss_longitude = float(data_iss["iss_position"]["longitude"])
    iss_latitude = float(data_iss["iss_position"]["latitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

# response = requests.get(url="https://api.kanye.rest")
# response.raise_for_status()
# data = response.json()["quote"]
# print(data)

MY_LAT = 52.50
MY_LONG = 13.41

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
    sunset = data["results"]["sunset"].split("T")[1].split(":")[0]

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True
    

while True:
    time.sleep(60)  # Check every minute
    if is_iss_overhead and is_night:
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user="your_email@gmail.com", password="your_password")
        connection.sendmail(from_addr="your_email@gmail.com", to_addrs="recipient_email@gmail.com", msg="Subject:Look Up\n\nThe ISS is above you in the sky!")
        connection.close()
