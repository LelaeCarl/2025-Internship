'''
07 - BS4 Module - Searching the Document Tree
'''
from bs4 import BeautifulSoup
import re

# Parse the HTML
soup = BeautifulSoup(
    open("hello2.html", encoding="utf-8"),
    'lxml'
)

# 1. name parameter (search by tag name)
# 1.1 Pass a string
print("1.1 Pass a string:", soup.find_all("a"))

# 1.2 Pass a regular expression
pattern = re.compile(r"^b")
for tag in soup.find_all(pattern):
    print("1.2 Pass a regular expression:", tag.name)

# 1.3 Pass a list
print("1.3 Pass a list:", soup.find_all(['a', 'b']))

# 2. keyword parameter (search by tag attribute value)
print("2. keyword parameter:", soup.find_all(id="link2"))

# 3. text parameter (search by text content)
# 3.1 Pass a string
print("3.1 Pass a string:", soup.find_all(text="Wang Yang"))

# 3.2 Pass a regular expression
pattern = re.compile("Story")
print("3.2 Pass a regular expression:", soup.find_all(text=pattern))

# 3.3 Pass a list
# The content of the strings in the list must match exactly with the HTML text content (no spaces, otherwise the search won't find it)
print("3.3 Pass a list:", soup.find_all(text=['Wang Yang', 'Gu Xuhui', 'Dahai']))
