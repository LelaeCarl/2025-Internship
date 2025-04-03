'''
05 - BS4 Module - Comment
'''
from bs4 import BeautifulSoup

# 1. Parse HTML into a BS4 object
soup = BeautifulSoup(
    open("hello2.html", encoding="utf-8"),
    'lxml'
)

# 2. Get the text content of the <a> tag
# Normally, comment content is ignored, but removing spaces around it will display the comment content
print("2. Get the text content of the <a> tag:", soup.a.string)

# 3. Type of the text content of the tag
# If it contains comment symbols, it will be of type Comment
print("3. Type of the text content of the tag:", type(soup.a.string))
