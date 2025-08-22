import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yesterday's closing stock price.
def check_stock_movement():
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": "YOUR_ALPHAVANTAGE_API_KEY"
    }

    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    response.raise_for_status()
    stock_data = response.json()

    daily_data = stock_data["Time Series (Daily)"]

    data_list = list(daily_data.items())
    yesterday_data = data_list[0]
    day_before_yesterday_data = data_list[1]

    yesterday_closing_price = float(yesterday_data[1]["4. close"])
    day_before_yesterday_close = float(day_before_yesterday_data[1]["4. close"])

    price_difference = abs(yesterday_closing_price - day_before_yesterday_close)
    percentage_difference = (price_difference / day_before_yesterday_close) * 100

    price_increased = yesterday_closing_price > day_before_yesterday_close
    movement_symbol = "🔺" if price_increased else "🔻"

    if percentage_difference >= 5:
        print(f"{STOCK}: {movement_symbol}{percentage_difference:.2f}%")
        get_news()
        return True
    else:
        print(f"{STOCK}: No significant movement ({movement_symbol}{percentage_difference:.2f}%)")
        return False



## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator
def get_news():
    news_params = {
        "q": COMPANY_NAME,
        "apiKey": "YOUR_NEWSAPI_KEY"
    }

    response = requests.get(NEWS_ENDPOINT, params=news_params)
    response.raise_for_status()
    news_data = response.json()

    articles = news_data["articles"][:3]
    for article in articles:
        title = article["title"]
        description = article["description"]
        send_sms(title, description)
    

## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.
def send_sms(title, description):
    from twilio.rest import Client

    # Your Account SID and Auth Token from twilio.com/console
    account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"{title}\n{description}",
        from_='YOUR_TWILIO_PHONE_NUMBER',
        to='YOUR_PHONE_NUMBER'
    )

    print(f"SMS sent: {message.sid}")


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

