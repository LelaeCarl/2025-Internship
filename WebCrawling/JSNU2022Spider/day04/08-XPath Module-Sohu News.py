'''
08 - XPath Module - Sohu News
Requirements:
    1. Open the Sohu News official website and scrape the news list (news title, news link)
    2. Based on the news link, scrape the news content details page
       Example: Zhou Xiaochuan: This generation of young people need to make expectations and plans for future pension
        .....
    3. On the details page, scrape the following content:
        News title, news body (publication time, publication place)
    4. Save each day's news to a text file
            Example: Zhou Xiaochuan: This generation of young people >>>.txt (The news body content is stored in the text file)
    5. Use lxml library and xpath statements to achieve the functionality
'''
import os
import re
from urllib.parse import urljoin
import lxml.etree
import requests

url = "https://www.sohu.com/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
}
response = requests.get(url=url, headers=headers)
response.encoding = "utf-8"
htmlDom = lxml.etree.HTML(response.text)
titles = htmlDom.xpath("//div[@class='list16']/ul/li/a/span/text()")
hrefs = htmlDom.xpath("//div[@class='list16']/ul/li/a/@href")

for title, href in zip(titles, hrefs):
    href = urljoin(url, href)
    response = requests.get(url=href, headers=headers)
    response.encoding = "utf-8"
    htmlDom = lxml.etree.HTML(response.text)
    time = htmlDom.xpath("//span[@id='news-time']/text()")[0]
    context = htmlDom.xpath("//article[@class='article']/p/text()")
    with open(f"{title}.txt", "w", encoding="utf-8") as file:
        file.write(f"News Title: {title}\n")
        file.write(f"Published Time: {time}\n")
        file.write("News Body:\n")
        if isinstance(context, bytes):
            context = context.decode('utf-8')
        for item in context:
            file.write(item + "\n")

    print(f"Successfully saved news: {title}")
