'''
04 - BS4 Module - BeautifulSoup
'''
from bs4 import BeautifulSoup

# 1. Parse HTML into a BS4 object
soup = BeautifulSoup(
    open("hello2.html", encoding="utf-8"),
    'lxml'
)

# 2. Get the name of the BS4 object
print("2. Get the name of the BS4 object:", soup.name)

# 3. Get the tag name of the BS4 object
print("3. Get the tag name of the BS4 object:", type(soup.name))

# 4. Get the attributes of the document object
print("4. Get the attributes of the document object:", soup.attrs)
