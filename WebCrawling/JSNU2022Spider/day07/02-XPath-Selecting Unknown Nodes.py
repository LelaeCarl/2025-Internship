'''
02 - XPath - Selecting Unknown Nodes
'''
from lxml import etree

htmlDom = etree.parse("book.xml")

# 1. Select all child elements of the bookstore element
result = htmlDom.xpath("/bookstore/*")
print("1. All child elements of bookstore:", result)

# 2. Select all elements in the document
result = htmlDom.xpath("//*")
print("2. All elements in the document:", result)

# 3. Select all elements that have attributes under title
result = htmlDom.xpath("//title[@*]")
print("3. All title elements with attributes:", result)
for dom in result:
    print(dom.text)
