'''
03 - BS4 Module - NavigableString
'''
from bs4 import BeautifulSoup

# 1. Parse HTML into a BS4 object
soup = BeautifulSoup(
    open("hello2.html", encoding="utf-8"),
    'lxml'
)

# 2. How to get the text content of a tag
print("2. Get content of the tag:", soup.title.string)

# 3. View the type of text content object
print("3. Type of text content object:", type(soup.title.string))
