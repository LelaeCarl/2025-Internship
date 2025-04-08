import re
import json
import requests
import pymysql


url = "https://www.shanghairanking.cn/api/pub/v1/bcur?bcur_type=11&year=2024"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}


response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
html = response.text

# 正则提取
name_list = re.findall(r'"univNameCn":"(.*?)"', html)
en_list = re.findall(r'"univNameEn":"(.*?)"', html)
tag_list = re.findall(r'"univTags":\[(.*?)\]', html)
category_list = re.findall(r'"univCategory":"(.*?)"', html)
province_list = re.findall(r'"province":"(.*?)"', html)
score_list = re.findall(r'"score":([\d\.]+)', html)
rank_list = re.findall(r'"ranking":(\d+)', html)


universities = []
for i in range(len(name_list)):
    universities.append({
        "name": name_list[i],
        "en": en_list[i] if i < len(en_list) else "",
        "tag": tag_list[i] if i < len(tag_list) else "",
        "category": category_list[i] if i < len(category_list) else "",
        "province": province_list[i] if i < len(province_list) else "",
        "score": float(score_list[i]) if i < len(score_list) else 0,
        "rank": int(rank_list[i]) if i < len(rank_list) else 0
    })

# 保存到 JSON 文件
with open('name.json', 'w', encoding='utf-8') as f:
    json.dump(universities, f, ensure_ascii=False, indent=4)

print("The data has been successfully saved to name.json")

# 连接 MySQL 并创建数据库
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "sagemovie",
    "charset": "utf8mb4"
}

conn = pymysql.connect(**db_config)
cursor = conn.cursor()


cursor.execute("CREATE DATABASE IF NOT EXISTS caipiao DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
cursor.close()
conn.close()
db_config["database"] = "caipiao"
conn = pymysql.connect(**db_config)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS univ (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        en VARCHAR(255),
        tag VARCHAR(255),
        category VARCHAR(255),
        province VARCHAR(255),
        score FLOAT,
        `rank` INT
    )
''')

for univ in universities:
    cursor.execute('''
        INSERT INTO univ (name, en, tag, category, province, score, `rank`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (univ['name'], univ['en'], univ['tag'], univ['category'], univ['province'], univ['score'], univ['rank']))


conn.commit()
cursor.close()
conn.close()

print("The data has been successfully stored in the MySQL database!")
