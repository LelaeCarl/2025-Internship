'''
03 - urllib Module - Exercise

Requirements:
    1. Crawl the "荒山尸骨" (Desolate Mountain Corpse Bones) chapter of the novel "花千骨" (The Journey of Flower) from BiQuGe.
    2. Clean the chapter data, keeping only the chapter title and main text.
    3. Save the cleaned data into a .txt file:
        - The file name should be "荒山尸骨.txt"
        - The file should contain only the main text content.
    4. Important Notes:
        4.1 Replace the <p> tags in the main text with an empty string "".
        4.2 Replace the <div></div> tags in the main text with an empty string "".
        4.3 Replace the </p> tags in the main text with a newline character "\n".

'''

import urllib.request
import re

# 1. Target URL of the chapter (Replace with the correct URL if needed)
url = "https://www.xyeduku.com/88590/11031836.html"

# 2. Send request and get the HTML content
response = urllib.request.urlopen(url)
html = response.read().decode('utf-8')

# 3. Extract the chapter title
title = re.findall(r'<h1>(.*?)</h1>', html)[0]

# 4. Extract the main content inside <div id="content">
content = re.findall(r'<div id="content">(.*?)</div>', html, re.S)[0]

# 5. Clean the content based on the rules
content = content.replace('<p>', '')
content = content.replace('</p>', '\n')
content = content.replace('<div>', '')
content = content.replace('</div>', '')

# Optional: Remove any other leftover HTML tags
content = re.sub(r'<.*?>', '', content)

# 6. Save the cleaned content to a text file
with open('荒山尸骨.txt', 'w', encoding='utf-8') as f:
    f.write(title + '\n\n')
    f.write(content)

print("Chapter saved successfully as 荒山尸骨.txt")
