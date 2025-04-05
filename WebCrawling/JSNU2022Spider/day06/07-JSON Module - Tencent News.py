import requests
from bs4 import BeautifulSoup
import pymysql
from datetime import datetime
import time
import random
from urllib.parse import urljoin

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '846938042',
    'database': 'news',
    'charset': 'utf8mb4'
}

# User agent list
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0'
]

# Entry point URLs for Tencent News
NEWS_URLS = [
    'https://news.qq.com/',
    'https://new.qq.com/',
    'https://www.qq.com/'
]


def get_random_headers():
    """Get random HTTP headers"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.qq.com/',
        'DNT': '1',
        'Connection': 'keep-alive'
    }


def create_database_and_table():
    """Create database and table if they do not exist"""
    temp_config = DB_CONFIG.copy()
    db_name = temp_config.pop('database')

    try:
        conn = pymysql.connect(**temp_config)
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        print(f"Database {db_name} created/verified")

        cursor.execute(f"USE {db_name};")

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS tengxunnews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            publish_time DATETIME,
            link_info VARCHAR(512),
            pic_info VARCHAR(512),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY (link_info(255))  -- Prevent duplicate insertions
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table 'tengxunnews' created/verified")

    except pymysql.Error as e:
        print(f"Database operation failed: {e}")
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def fetch_tencent_news():
    """Scrape Tencent news data"""
    session = requests.Session()
    news_list = []

    for base_url in NEWS_URLS:
        try:
            print(f"\nScraping: {base_url}")
            headers = get_random_headers()
            response = session.get(base_url, headers=headers, timeout=15)
            time.sleep(random.uniform(1, 3))

            print(f"Status: {response.status_code}, Content length: {len(response.text)}")

            if response.status_code != 200:
                print(f"Request failed, status: {response.status_code}")
                continue

            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            with open(f'tencent_news_{time.strftime("%Y%m%d%H%M%S")}.html', 'w', encoding='utf-8') as f:
                f.write(response.text)

            selectors = [
                'a[href*="qq.com"]',
                'div.content > a',
                'article > a',
                'li > a',
                'h3 > a'
            ]

            for selector in selectors:
                items = soup.select(selector)
                if items:
                    print(f"Using selector '{selector}', found {len(items)} items")
                    for item in items:
                        try:
                            title = item.get_text().strip()
                            if not title or len(title) < 5:
                                continue

                            link = item.get('href', '').strip()
                            if not link or link.startswith('javascript:'):
                                continue

                            link = urljoin(base_url, link)
                            if not any(x in link for x in ['qq.com', 'news.qq.com', 'new.qq.com']):
                                continue

                            if any(n['link_info'] == link for n in news_list):
                                continue

                            print(f"Found news: {title[:30]}...")
                            detail_info = fetch_news_detail(link, session)

                            news_item = {
                                'title': title[:255],
                                'link_info': link[:512],
                                'publish_time': detail_info['publish_time'],
                                'pic_info': detail_info['pic_info'][:512] if detail_info['pic_info'] else None
                            }
                            news_list.append(news_item)

                            if len(news_list) >= 50:
                                return news_list

                            time.sleep(random.uniform(0.5, 1.5))

                        except Exception as e:
                            print(f"Error processing item: {e}")
                    break

        except Exception as e:
            print(f"Error scraping {base_url}: {e}")
            continue

    return news_list


def fetch_news_detail(url, session):
    """Fetch detail information of a news item"""
    print(f"Fetching detail: {url[:60]}...")
    detail_info = {'publish_time': None, 'pic_info': None}

    try:
        headers = get_random_headers()
        response = session.get(url, headers=headers, timeout=15)
        time.sleep(random.uniform(1, 2))

        if response.status_code != 200:
            print(f"Detail request failed, status: {response.status_code}")
            return detail_info

        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try to parse publish time
        time_selectors = [
            'span.article-time',
            'span.time',
            'div.pubtime',
            'div.time',
            'meta[property="article:published_time"]'
        ]

        for selector in time_selectors:
            element = soup.select_one(selector)
            if element:
                time_str = element.get_text().strip() if selector != 'meta[property="article:published_time"]' else element.get('content', '')
                if time_str:
                    time_formats = [
                        '%Y年%m月%d日 %H:%M',
                        '%Y-%m-%d %H:%M:%S',
                        '%Y/%m/%d %H:%M',
                        '%Y-%m-%dT%H:%M:%S%z',
                        '%Y-%m-%d %H:%M'
                    ]
                    for fmt in time_formats:
                        try:
                            publish_time = datetime.strptime(time_str, fmt)
                            detail_info['publish_time'] = publish_time.strftime('%Y-%m-%d %H:%M:%S')
                            break
                        except ValueError:
                            continue
                break

        # Try to extract image info
        img_selectors = [
            'div.content img',
            'div.article-content img',
            'img[src*="http"]',
            'meta[property="og:image"]'
        ]

        for selector in img_selectors:
            element = soup.select_one(selector)
            if element:
                img_src = element.get('src') if selector != 'meta[property="og:image"]' else element.get('content')
                if img_src:
                    if img_src.startswith('//'):
                        img_src = 'https:' + img_src
                    elif img_src.startswith('/'):
                        img_src = urljoin(url, img_src)
                    detail_info['pic_info'] = img_src
                    break

        return detail_info

    except Exception as e:
        print(f"Error fetching detail: {e}")
        return detail_info


def save_to_database(news_list):
    """Save news list to database"""
    if not news_list:
        print("No data to save.")
        return

    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        insert_sql = """
        INSERT IGNORE INTO tengxunnews 
        (title, publish_time, link_info, pic_info)
        VALUES (%s, %s, %s, %s)
        """

        success_count = 0
        for news in news_list:
            try:
                cursor.execute(insert_sql, (
                    news['title'],
                    news['publish_time'],
                    news['link_info'],
                    news['pic_info']
                ))
                success_count += 1
            except pymysql.Error as e:
                print(f"Insert failed: {e}, data: {news['title'][:20]}...")

        conn.commit()
        print(f"Successfully inserted {success_count}/{len(news_list)} items")

    except pymysql.Error as e:
        print(f"Database connection failed: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def main():
    """Main function"""
    print("Tencent News Crawler started...")
    start_time = time.time()

    try:
        create_database_and_table()

        print("\nStarting to scrape Tencent news...")
        news_list = fetch_tencent_news()
        print(f"\nTotal news items fetched: {len(news_list)}")

        if news_list:
            save_to_database(news_list)
        else:
            print("No news data retrieved.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        print(f"\nFinished in {time.time() - start_time:.2f} seconds")


if __name__ == '__main__':
    main()
