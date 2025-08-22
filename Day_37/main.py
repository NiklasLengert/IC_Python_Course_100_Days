import requests
from datetime import datetime

pixela_endpoint = "https://pixe.la/v1/users"
pixela_graphs_endpoint = "https://pixe.la/v1/users/niklas/graphs"
pixel_create_endpoint = "https://pixe.la/v1/users/niklas/graphs/graph1"

user_params = {
    "username": "niklas",
    "token": "xxxxxxxxxxxxxxxxxxxdddddxxxxxxx",
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

response = requests.post(url=pixela_endpoint, json=user_params)
print(response.text)

param = {
    "id": "graph1",
    "name": "Coding Graph",
    "unit": "hours",
    "type": "float",
    "color": "shibafu",
    "timezone": "Asia/Tokyo"
}
headers = {
    "X-USER-TOKEN": "xxxxxxxxxxxxxxxxxxxdddddxxxxxxx"
}

response1 = requests.post(url=pixela_graphs_endpoint, json=param, headers=headers)
print(response1.text)

pixel_params = {
    "date": datetime.today.strftime("%Y%m%d"),
    "quantity": 5.5
}

pixel_headers = {
    "X-USER-TOKEN": "xxxxxxxxxxxxxxxxxxxdddddxxxxxxx"
}

response2 = requests.post(url=pixel_create_endpoint, json=pixel_params, headers=pixel_headers)
print(response2.text)