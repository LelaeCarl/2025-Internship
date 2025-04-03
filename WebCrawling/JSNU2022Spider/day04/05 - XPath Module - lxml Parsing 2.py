'''
05 - XPath Module - lxml Parsing 2
'''
from lxml import etree

# 1. Parse HTML into a DOM document
html = etree.parse("hello.html")
print("1.1 html content:", html)
print("1.2 html type:", type(html))

# 2. Serialize the HTML document
htmlStr = etree.tostring(html, pretty_print=True)
print("2.1 htmlStr type:", type(htmlStr))

# 3. Convert the serialized HTML into a string
print("3.1 Convert htmlStr to string:", str(htmlStr, encoding="utf-8"))
