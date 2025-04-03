import os
import re
import requests
from lxml import etree
from time import sleep
from urllib.parse import urljoin

# Configuration parameters
BASE_DOMAIN = 'https://www.biqu04.cc'
START_URL = 'https://www.biqu04.cc/book/45850/1.html'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Referer': BASE_DOMAIN
}
SAVE_DIR = 'A Thought Through Eternity'
MAX_RETRY = 3
REQUEST_INTERVAL = 2.5  # Base request interval

# Initialize save directory
os.makedirs(SAVE_DIR, exist_ok=True)


def sanitize_title(title):
    """Clean special characters from title"""
    return re.sub(r'[\\/*?:"<>|]', '', title).strip()[:80]  # Limit title length


def parse_content(element):
    """Recursively parse content elements"""
    content = []
    for node in element.xpath('node()'):
        if isinstance(node, str):
            text = node.strip()
            if text:
                content.append(text)
        else:
            if node.tag == 'br':
                content.append('\n')
            else:
                content.extend(parse_content(node))
    return content


def fetch_page(url):
    """Page request with retry mechanism"""
    for _ in range(MAX_RETRY):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return etree.HTML(response.text)
            if response.status_code == 404:
                return 'END'
        except Exception as e:
            print(f"Request failed: {url} - {str(e)}")
        sleep(REQUEST_INTERVAL * 1.5)
    return None


def parse_chapter(html):
    """Parse chapter information"""
    try:
        # Extract title
        title = html.xpath('//div[@class="bookname"]/h1/text()')
        if not title:
            title = html.xpath('//h1/text()')
        title = title[0].strip() if title else "Unknown Chapter"

        # Extract main content
        content_element = html.xpath('//div[@id="content"]')
        if not content_element:
            content_element = html.xpath('//div[contains(@class,"content")]')

        if not content_element:
            print("Content not found")
            return None

        raw_content = parse_content(content_element[0])

        # Clean content
        cleaned = []
        for line in raw_content:
            line = re.sub(r'\s+', ' ', line)
            line = line.replace('\u3000', ' ').strip()
            if line and not line.startswith(('『', '--', 'www.', 'http')):
                cleaned.append(line)

        # Extract next chapter link
        next_links = html.xpath('//a[contains(text(),"Next Chapter")]/@href')
        if not next_links:
            next_links = html.xpath('//a[contains(text(),"Next Page")]/@href')

        if not next_links:
            return {
                'title': sanitize_title(title),
                'content': '\n'.join(cleaned),
                'next_url': None
            }

        next_url = urljoin(BASE_DOMAIN, next_links[0])

        return {
            'title': sanitize_title(title),
            'content': '\n'.join(cleaned),
            'next_url': next_url
        }
    except Exception as e:
        print(f"Parsing error: {str(e)}")
        return None


def save_chapter(title, content, index):
    """Safely save chapter content"""
    try:
        filename = f"{index:04d}_{title}.txt"
        filepath = os.path.join(SAVE_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n\n{content}")
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Save failed: {title} - {str(e)}")


def is_terminate(next_url, visited):
    """Check termination conditions"""
    if not next_url:
        print("No next chapter link found, stopping crawl")
        return True
    if next_url in visited:
        print("Duplicate link detected, stopping crawl")
        return True
    if not next_url.endswith('.html'):
        print("Non-chapter link detected, stopping crawl")
        return True
    return False


def novel_crawler():
    """Main crawler function"""
    current_url = START_URL
    chapter_index = 1
    visited_urls = set()

    while True:
        # Check termination conditions
        if is_terminate(current_url, visited_urls):
            break

        # Record visited URL
        visited_urls.add(current_url)
        print(f"Processing: Chapter {chapter_index} - {current_url}")

        # Fetch page
        html = fetch_page(current_url)
        if html == 'END':
            print("404 page detected, stopping crawl")
            break
        if html is None:
            print("Failed to fetch page, skipping")
            continue

        # Parse content
        chapter_data = parse_chapter(html)
        if not chapter_data:
            print("Failed to parse chapter, stopping crawl")
            break

        # Save content
        save_chapter(
            chapter_data['title'],
            chapter_data['content'],
            chapter_index
        )

        # Check if this is the last chapter
        if not chapter_data['next_url']:
            print("Reached the last chapter")
            break

        # Update state
        current_url = chapter_data['next_url']
        chapter_index += 1

        # Dynamic interval (1.5–3.5 seconds)
        sleep(REQUEST_INTERVAL + (hash(current_url) % 2000) / 1000)


if __name__ == '__main__':
    novel_crawler()
    print("=== Crawling task completed ===")
