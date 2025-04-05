'''
04-JSON Module - jsonPath - Lagou.com
'''
import json, jsonpath, chardet
import requests

# 1. Set URL
url = "https://www.lagou.com/lbs/getAllCitySearchLabels.json"

# 2. Set user-agent headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

# 3. Send request and get JSON response
response = requests.get(url=url, headers=headers)

# 4. Set correct encoding
response.encoding = 'utf-8'

# 5. Get response content as text
html = response.text

# 6. Convert JSON string to JSON object
jsonObj = json.loads(html)

# 7. Use jsonpath to extract all "name" nodes
cityList = jsonpath.jsonpath(jsonObj, '$..name')

# 8. Convert JSON data to string (disable ASCII escaping)
content = json.dumps(cityList, ensure_ascii=False)
print(content)

# 9. Write to file
fp = open('city.json', 'w')
fp.write(content)
fp.close()
