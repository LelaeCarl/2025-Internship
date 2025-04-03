'''
06 - XPath Module - Practical Test
'''
from lxml import etree

html = etree.parse("hello.html")

# 1. Get all <li> tags
result = html.xpath("//li")
print("1. All <li> tags:", result)

# 2. Get all class attributes under <li> tags
result = html.xpath("//li/@class")
print("2. All class attributes under <li> tags:", result)

# (Duplicate numbering in original) 2. Get class attributes under <li> tags
result = html.xpath("//li/@class")
print("2. All class attributes under <li> tags:", result)

# 3. Get <li> tags where <a> has href='link1.html'
result = html.xpath("//li/a[@href='link1.html']")
print("3. <li> tags with <a> href='link1.html':", result)

# 4. Get all <span> tags under <li> tags
result = html.xpath("//li//span")
print("4. All <span> tags under <li> tags:", result)
