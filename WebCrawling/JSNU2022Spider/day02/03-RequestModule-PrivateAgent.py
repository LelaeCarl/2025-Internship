import requests

# 1. If the proxy requires HTTP Basic Authentication, you can use the following format
proxy = {
    "http": "zs:zs123@61.158.21.39:1667"
}

# 2. Send the request
response = requests.get("https://www.baidu.com", proxies=proxy)

# 3. Output the result
response.encoding = "utf-8"
print(response.text)
