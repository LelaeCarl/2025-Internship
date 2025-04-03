'''
10 - BS4 Module - Baidu Tieba
Requirements:
    1. Open the Liu Yifei Tieba
    2. Find the src of Liu Yifei's images
    3. Open the image through the src value
    4. Scrape the images and store them in the "Liu Yifei" folder
    5. Process using BeautifulSoup
    Download images with custom names, such as Liu Yifei01.png, Liu Yifei02.png...
    Note: The scraped content may contain comment symbols, so you need to address this issue before processing with BeautifulSoup
'''

import os
import requests
import time
from bs4 import BeautifulSoup

# Create folder to save images
folder_name = "Liu Yifei"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://tieba.baidu.com/"
}

# 1. Request Liu Yifei Tieba
base_url = "https://tieba.baidu.com/f?kw=%E5%88%98%E4%BA%A6%E8%8F%B2&ie=utf-8&tab=album"
try:
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()  # Check if the request was successful
    response.encoding = "utf-8"

    # Print part of HTML (for debugging)
    # print(response.text[:1000])  # Uncomment to see if the HTML is returned correctly

    # 2. Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all images (try different selectors)
    img_tags = soup.find_all("img", class_="BDE_Image")  # Old selector
    if not img_tags:
        img_tags = soup.find_all("img")  # Find all images (may include ads)

    if not img_tags:
        print("No images found, possibly due to page structure change or login required.")
    else:
        print(f"Found {len(img_tags)} images.")
        for i, img in enumerate(img_tags[:10], start=1):  # Only download the first 10 images for testing
            try:
                img_url = img.get("src")
                if not img_url:  # Some images may use data-src
                    img_url = img.get("data-src")

                if img_url:
                    print(f"Downloading image {i}: {img_url}")
                    img_data = requests.get(img_url, headers=headers).content

                    # Save the image
                    filename = f"Liu Yifei{i:02d}.jpg"  # Change to .jpg (some are in jpeg format)
                    filepath = os.path.join(folder_name, filename)

                    with open(filepath, "wb") as f:
                        f.write(img_data)
                    print(f"Saved successfully: {filepath}")

                    time.sleep(1)  # Avoid being blocked for sending requests too fast
                else:
                    print(f"Image {i} does not have a valid link.")
            except Exception as e:
                print(f"Failed to download image {i}: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

print("Scraping finished!")
