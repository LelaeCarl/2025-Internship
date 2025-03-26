# 01 - Requests module - POST example

import requests

# 1. Set the URL
url = "https://fanyi.baidu.com/ait/text/translate"

# 2. Set the User-Agent headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# 3. Set the form data to be submitted
form_data = {
    "query": "python"
}

# 4. Make the POST request
response = requests.post(
    url=url,
    headers=headers,
    data=form_data
)

# 5. Output the content of the response
html = response.text
print(html)

# 6. Complete URL information
'''
The translation result of 'python' is not displayed directly in the HTML.
Instead, after sending the request, the result is obtained via AJAX and injected into the HTML page.
'''
print("URL:", response.request.url)
