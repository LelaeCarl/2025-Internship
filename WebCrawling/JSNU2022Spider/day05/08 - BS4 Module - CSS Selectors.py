'''
08 - BS4 Module - CSS Selectors
'''
from bs4 import BeautifulSoup
import re

# Parse the HTML
soup = BeautifulSoup(
    open("hello2.html", encoding="utf-8"),
    'lxml'
)

# 1. Find by tag name
print("1. Find by tag name:", soup.select("title"))
print("1. Find by tag name:", soup.select("a"))

# 2. Find by class name
print("2. Find by class name:", soup.select(".title"))

# 3. Find by ID
print("3. Find by ID:", soup.select("#link1"))

# 4. Combined search
print("4. Combined search:", soup.select("p #link1"))
print("4. Combined search:", soup.select("head > title"))

# 5. Search by attributes
print("5. Search by attributes:", soup.select("a[class='sister']"))
print("5. Search by attributes + combined search:", soup.select("p a[class='sister']"))

# 6. Get content
print("6. Get tag content:", soup.select("title"))
print("6. Get tag content:", soup.select("title")[0].get_text())
