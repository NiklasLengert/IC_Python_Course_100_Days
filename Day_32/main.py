# import smtplib
# my_email = ""
# password = ""

# with smtplib.SMTP("smtp.gmail.com") as connection:
#     connection.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
#     connection.login(user=my_email, password=password)  # Replace with your actual password
#     connection.sendmail(from_addr=my_email,
#                         to_addrs="niklas.lengert@gematik.de",
#                         msg="Subject:Hello\n\nThis is the body of the email.")
#     connection.close()  # Close the connection


import datetime as dt
import smtplib
import os
file_path = os.path.join(os.path.dirname(__file__), "quotes.txt")
# now = dt.datetime.now()
# print(now)
# print(now.year)
# print(now.month)
# print(now.day)
# print(now.weekday())
# if now.year == 2025:
#     print("It's 2025!")

# date_of_birth = dt.datetime(year=1998, month=1, day=27)
# print(date_of_birth)

# now = dt.datetime.now()
# if now.weekday() == 0:
#     with open(file_path, "r") as file:
#         quotes = file.readlines()
#         quote = quotes[now.day % len(quotes)].strip()
#         print(quote)
    
#     with smtplib.SMTP("smtp.gmail.com") as connection:
#         connection.starttls()
#         connection.login(user="MY_EMAIL", password="MY_PASSWORD")
#         connection.sendmail(from_addr="MY_EMAIL",
#                             to_addrs="THEIR_EMAIL",
#                             msg=f"Subject:Monday Motivation\n\n{quote}")
#         connection.close()



    