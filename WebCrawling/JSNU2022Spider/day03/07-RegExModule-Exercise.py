r'''
07 - Regex Module - Exercise
Requirement:
    1. Use re module to match all Chinese + tag symbols + \s
    2. Scrape all titles and links from the Hua Qiangu novel directory page.
    3. Using hrefList and titleList to scrape chapter content using findall, search, etc.
    4. Save files under the folder 'HuaQiangu'.
'''

import os
import re
import requests
from bs4 import BeautifulSoup

# Creating directory to save files
if not os.path.exists('HuaQiangu'):
    os.makedirs('HuaQiangu')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

def scrape_novel_directory(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')

    titleList = []
    hrefList = []

    for a_tag in soup.find_all('a', href=True):
        title = a_tag.get_text().strip()
        href = a_tag['href'].strip()
        if title and href.startswith('http'):
            titleList.append(title)
            hrefList.append(href)
        elif title and not href.startswith('http'):
            hrefList.append(f'https://www.xyeduoku.com{href}')
            titleList.append(title)

    return titleList, hrefList


def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'[\r\n\t]+', '\n', text)  # Normalize new lines
    text = re.sub(r'[\s]+', ' ', text)  # Remove excessive whitespace
    return text.strip()


def scrape_chapter_content(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    pattern = r'<div[^>]*id=["\']content["\'][^>]*>(.*?)</div>'
    match = re.search(pattern, response.text, re.DOTALL)

    if match:
        cleaned_text = clean_text(match.group(1))
        return cleaned_text
    return None


def save_chapter(title, content):
    filename = f'HuaQiangu/{title}.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f'Saved: {filename}')


if __name__ == '__main__':
    base_url = 'https://www.xyeduoku.com/88590/11031998.html'
    titles, links = scrape_novel_directory(base_url)

    for title, link in zip(titles, links):
        content = scrape_chapter_content(link)
        if content:
            save_chapter(title, content)
