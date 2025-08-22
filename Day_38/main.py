import requests
from datetime import datetime
import os

APP_ID = os.getenv("NUTRITIONIX_APP_ID", "your_app_id")
API_KEY = os.getenv("NUTRITIONIX_API_KEY", "your_api_key")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "my_google_sheet_endpoint"

exercise_text = input("Tell me which exercises you did: ")

header = {
    "x-app-id": APP_ID,
    "x-api-key": API_KEY,
}

bearer_header = {
    "Authorization": f"Bearer {os.getenv('BEARER_TOKEN')}"
}

params = {
    "query": exercise_text,
    "GENDER": "male",
    "AGE": 25,
    "HEIGHT": 175,
    "WEIGHT": 70,
}

response = requests.post(
    exercise_endpoint,
    json=params,
    headers=header
)

result = response.json()
print(result)


today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%H")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        headers=bearer_header
    )

    print(sheet_response.text)