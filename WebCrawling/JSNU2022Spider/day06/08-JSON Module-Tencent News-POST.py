'''
08-JSON Module - Tencent News - POST Request
'''
import json
from jsonpath_ng import parse
import requests
import pymysql

# 1. Set the URL
url = "https://i.news.qq.com/web_feed/getWebList"

# 2. Set headers
headers = {
    "authority": "i.news.qq.com",
    "method": "POST",
    "path": "/web_feed/getWebList",
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-length": "196",
    "content-type": "application/json",
    "origin": "https://xw.qq.com",
    "referer": "https://xw.qq.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}

# Set POST data payload
data = {
    "adcode": "110000",
    "base_req": {"from": "qq_web"},
    "channel_id": "news_news_wap",
    "device_id": "0_1fiJ5ErkcccaG",
    "flush_num": 0,
    "forward": "2",
    "is_local_chlid": "",
    "qimei36": "0_1fiJ5ErkcccaG",
    "uin": "test"
}

# 3. Send POST request and get JSON response
response = requests.post(url=url, headers=headers, data=json.dumps(data))

# 4. Set encoding
response.encoding = 'utf-8'

# 5. Get response content as string
html = response.text
print(html)

# 6. Parse JSON string to object
jsonObj = json.loads(html)

# 7. Use jsonpath to extract fields
idList = [match.value for match in parse('$..id').find(jsonObj)]
titleList = [match.value for match in parse('$..title').find(jsonObj)]
timeList = [match.value for match in parse('$..publish_time').find(jsonObj)]
linkList = [match.value for match in parse('$..link_info.url').find(jsonObj)]
picList = [match.value for match in parse('$..pic_info.big_img').find(jsonObj)]

# 8. MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sagemovie',
    'database': 'news',
    'charset': 'utf8mb4'
}

try:
    # Create database connection
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Create table if not exists
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS news (
        id INT AUTO_INCREMENT PRIMARY KEY,
        news_id VARCHAR(100) COMMENT 'News ID',
        title VARCHAR(500) NOT NULL COMMENT 'News Title',
        publish_time VARCHAR(50) COMMENT 'Publish Time',
        link_url TEXT COMMENT 'News Link',
        pic_url TEXT COMMENT 'Image Link'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    cursor.execute(create_table_sql)

    # Optionally clear existing data
    cursor.execute("TRUNCATE TABLE news")

    # Prepare data for batch insert
    insert_sql = """
    INSERT INTO news (news_id, title, publish_time, link_url, pic_url)
    VALUES (%s, %s, %s, %s, %s)
    """

    data_to_insert = []
    for i in range(len(titleList)):
        data_to_insert.append((
            idList[i] if idList and i < len(idList) else '',
            titleList[i] if titleList and i < len(titleList) else '',
            timeList[i] if timeList and i < len(timeList) else '',
            linkList[i] if linkList and i < len(linkList) else '',
            picList[i] if picList and i < len(picList) else ''
        ))

    # Insert data in batch
    cursor.executemany(insert_sql, data_to_insert)
    conn.commit()
    print(f"Successfully saved {len(data_to_insert)} news items to the database")

except pymysql.Error as e:
    print(f"Database error: {e}")
    if conn:
        conn.rollback()

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()

# Save JSON data to file (optional)
with open('news_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'ids': idList,
        'titles': titleList,
        'times': timeList,
        'links': linkList,
        'pics': picList
    }, f, ensure_ascii=False, indent=2)
