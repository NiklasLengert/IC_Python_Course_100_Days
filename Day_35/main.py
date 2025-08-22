import requests

def get_weather(city: str) -> dict:
    api_key = "my_api_key"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "City not found"}
    
def display_weather(weather_data: dict) -> None:
    if "error" in weather_data:
        print(weather_data["error"])
    else:
        city = weather_data["name"]
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        print(f"Weather in {city}: {temperature}°C, {description}")

# Send a sms to myself
# from twilio.rest import Client

# account_sid = 'my_account_sid'
# auth_token = 'my_auth_token'
# client = Client(account_sid, auth_token)
# message = client.messages.create(
#     body="Hello! This is a test message from my Python script.",
#     from_='my_twilio_number',
#     to='my_personal_number'
# )
# print(f"Message sent: {message.sid}")