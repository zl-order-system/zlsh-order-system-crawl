from function import *
import os
import requests

# 遠端爬取最新pdf
latestData = getCompleteData(0)
print(latestData)

# 確保目錄存在
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
target_folder_path = os.path.join(current_directory, "API", "meals")
os.makedirs(target_folder_path, exist_ok=True)

# 寫入新資料
file_path = os.path.join(target_folder_path, "latest.json")
with open(file_path, 'w') as file:
    file.write(latestData)
# 發送資料給後端
url = os.environ["meals_request_url"]    # 到時候設置github token
token = os.environ["meals_request_token"]
print(url, token)
headers = {
    "Authorization" : "Bearer " + token,
    "Content-Type": "application/json"
}
req = requests.put(url, data=latestData, headers=headers)
print(req.status_code)