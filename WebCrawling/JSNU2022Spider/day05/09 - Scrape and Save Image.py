'''
09 - Scrape and Save Image
'''
import urllib.request as req, os

# 1. Set the URL
url = "chrome-extension://bnjoienjhhclcabnkbhhfndecoipmcdg/background/keniu/main/favicon.png"

# 2. Directly scrape and read the data (image data is retrieved as bytes)
img = req.urlopen(url=url).read()

# 3. Write the image to the current folder
fileImg = open("Liu Yifei.png", "wb")
fileImg.write(img)
