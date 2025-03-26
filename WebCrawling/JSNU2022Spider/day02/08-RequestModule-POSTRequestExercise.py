"""
08 - Requests Module - POST Request Exercise

Tasks:
1. Use requests.post() to search a novel.
2. Crawl all chapters and save to local folder.
   2.1 User inputs novel name (一念永恒).
   2.2 Search novel from provided URL.
   2.3 Get chapters' URLs from directory page.
   2.4 Crawl each chapter's content.
   2.5 Clean and save each chapter into .txt files.
3. Create a folder named after the novel.
4. Save all chapters as separate text files:
   Chapter 1 - title.txt
   Chapter 2 - title.txt
"""

import requests
import os
from bs4 import BeautifulSoup

# Global headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/134.0.0.0 Safari/537.36"
}

BASE_URL = "http://www.xbiqugu.la"

def search_novel(novel_name):
    search_url = f"{BASE_URL}/modules/article/waps.php"
    data = {"searchkey": novel_name}

    response = requests.post(search_url, data=data, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, 'html.parser')

    result = soup.find('td', class_='even').find('a')
    novel_href = result['href']
    if not novel_href.startswith('http'):
        novel_href = BASE_URL + novel_href

    print(f"Novel found at: {novel_href}")
    return novel_href

def get_chapter_links(novel_url, limit=10):
    response = requests.get(novel_url, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, 'html.parser')

    chapter_list = soup.find('div', id='list').find_all('a')
    links = []
    for chapter in chapter_list[:limit]:  # Limit to first 'limit' chapters
        href = chapter['href']
        if not href.startswith('http'):
            href = BASE_URL + href
        links.append((chapter.text.strip(), href))
    return links

def get_chapter_content(chapter_url):
    response = requests.get(chapter_url, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').text.strip()
    content_div = soup.find('div', id='content')
    [s.extract() for s in content_div(['script', 'style'])]
    content = content_div.get_text(separator="\n", strip=True).replace('\xa0', ' ')

    return title, content

def save_chapter(title, content):
    filename = f"{title}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Saved: {filename}")

def main():
    novel_name = input("Enter the novel name to crawl (e.g., 一念永恒): ").strip()

    if not os.path.exists(novel_name):
        os.makedirs(novel_name)
    os.chdir(novel_name)

    try:
        novel_url = search_novel(novel_name)
        chapters = get_chapter_links(novel_url, limit=10)  # Adjust here if needed

        print(f"Downloading first {len(chapters)} chapters.")

        for idx, (chapter_title, chapter_url) in enumerate(chapters, start=1):
            print(f"Crawling Chapter {idx}: {chapter_title}")
            title, content = get_chapter_content(chapter_url)
            save_chapter(f"Chapter {idx} - {title}", content)

        print(f"First {len(chapters)} chapters of '{novel_name}' downloaded successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
