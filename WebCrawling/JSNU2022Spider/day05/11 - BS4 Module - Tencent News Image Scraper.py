'''
11 - BS4 Module - Tencent News Image Scraper
Requirements:
    1. Scrape images and content from the page
    2. Create a folder named "Tencent News"
    3. Scrape images from the specified page
    4. Use the content of the <h1> tag as part of the image filename
       Example: "Tilt-shift takes you to see spring｜Enjoy spring flowers and fun spring outings in the mountains and fields!.png"
    Target URL:
    https://news.qq.com/rain/a/20250327A06T1O00
'''
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 1. Set headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 2. Target URL
url = 'https://news.qq.com/rain/a/20250327A06T1O00'

# 3. Send request
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

# 4. Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 5. Create folder
folder_name = 'Tencent News'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# 6. Get article title
title = soup.find('h1').text.strip() if soup.find('h1') else 'No Title'
# Clean invalid characters from filename
invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
for char in invalid_chars:
    title = title.replace(char, '')

# 7. Find all image tags
images = soup.find_all('img')
image_urls = []

for img in images:
    img_url = img.get('src') or img.get('data-src')
    if img_url and 'http' not in img_url:
        img_url = urljoin(url, img_url)
    if img_url and 'http' in img_url:
        image_urls.append(img_url)

# 8. Download images
for i, img_url in enumerate(image_urls):
    try:
        img_data = requests.get(img_url, headers=headers).content
        # Generate filename
        if i == 0:
            file_name = f"{title}.png"
        else:
            file_name = f"{title}_{i}.png"

        file_path = os.path.join(folder_name, file_name)

        with open(file_path, 'wb') as f:
            f.write(img_data)
            print(f"Downloaded successfully: {file_name}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

print("Image download complete!")
