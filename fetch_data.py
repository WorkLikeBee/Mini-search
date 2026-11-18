import requests
import json

API_ENDPOINT = "https://api.stackexchange.com/2.3/questions"

params = {
    "page": 1,
    "pagesize": 100,
    "order": "desc",
    "sort": "votes",
    "filter": "withbody",
    "site": "stackoverflow"
}

response = requests.get(API_ENDPOINT, params = params)
data = response.json()

with open("raw_sample.json", "w", encoding="utf-8") as f:
    json.dump(data, f)
# print(response.status_code)
# print(data.get("error_name"), data.get("error_message"))
