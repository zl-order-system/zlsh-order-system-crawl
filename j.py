from function import *
 
url = "https://staging.order-system.octoberserver.net/system/api/meal"    # 到時候設置github token
token = "5b72819dc9e3c7edb3b634b2c6f27b941caa07df95209451"
d = getCompleteData(0)
headers = {
    "Authorization" : "Bearer " + token,
    "Content-Type" : "application/json",
    "Cache-Control" : "no-cache",
    "Accept" : "*/*"
}
req = requests.put(url, data=d.encode('utf-8'), headers=headers)
print(req.status_code)
print(req.text)