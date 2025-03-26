'''
01 - Focused Web Crawler
'''

import urllib.request

# 1. Set the URL (Uniform Resource Locator)
url = "https://www.google.com/"

# 2. Use urllib module to crawl the web page information
response = urllib.request.urlopen(url=url)

# 3. Get the response object
print("Response object:", response)

# 4. Get the response code
print("Response code:", response.getcode())

# 5. Get the requested URL
print("URL:", response.geturl())

# 6. Get the response headers
print("Headers:", response.info())
