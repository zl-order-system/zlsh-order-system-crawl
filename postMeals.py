import json
import os
import requests

# 打開json
with open('API/meals/latest.json', 'r') as file:
    latestData = json.load(file)

# 發送資料給後端
url = os.environ["meals_request_url"]    # 到時候設置github token
token = os.environ["meals_request_token"]
print(url, token)
headers = {
    "Authorization" : "Bearer " + token,
    "Content-Type" : "application/json",
    "Cache-Control" : "no-cache",
    "Accept" : "*/*"
}
req = requests.put(url, data=latestData.encode("utf-8"), headers=headers)
print(req.status_code)
print(req.text)