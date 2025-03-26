'''
07 - Requests Module - GET Request Exercise
Task:
1. Crawl "Hua Qian Gu" from BiQuGe - Chapter 3
2. Use the requests module to perform the crawling
3. Use functions for modular code:
   - get_html(): Get the response content
   - clean_info(html): Clean the HTML content
   - save_data(title, content): Save the cleaned content
'''

import requests
from bs4 import BeautifulSoup


def get_html():
    url = "https://www.biqvkk.cc/30_30295/11093038.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/134.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.encoding = "gb2312"
    html = response.text
    clean_info(html)


def clean_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Extract the title
    title = soup.find('h1').get_text().strip()

    # Extract ONLY the content text
    content_div = soup.find('div', id='content')
    if content_div:
        # Remove unwanted scripts or ads inside content if present
        [s.extract() for s in content_div(['script', 'style'])]
        content = content_div.get_text(separator='\n', strip=True)
    else:
        content = "Content not found."

    save_data(title, content)


def save_data(title, content):
    with open(f"{title}.txt", "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Saved successfully as {title}.txt")


if __name__ == "__main__":
    get_html()
