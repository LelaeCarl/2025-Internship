'''
01 - XPath Module - Syntax
'''
from lxml import etree

# Convert
htmlDom = etree.parse("book.xml")

# 1. Get the first child element of the bookstore element
result = htmlDom.xpath("/bookstore/book[1]")
print("1. First child element of bookstore:", result[0].text)

# 2. Get the last child element of the bookstore element
result = htmlDom.xpath("/bookstore/book[last()]")
print("2. Last child element of bookstore:", result[0].text)

# 3. Get the second last child element of the bookstore element
result = htmlDom.xpath("/bookstore/book[last()-1]")
print("3. Second last child element of bookstore:", result[0].text)

# 4. Get the first two child elements of the bookstore element
result = htmlDom.xpath("/bookstore/book[position()<3]")
print("4. First two child elements of bookstore:", result)

# 5. Get the title element with a lang attribute
result = htmlDom.xpath("//title[@lang]")
print("5. Title element(s) with lang attribute:", result)

# 6. Get the title element with lang attribute value equal to 'en'
result = htmlDom.xpath("//title[@lang='en']")
print("6. Title element(s) with lang='en':", result)

# 7. Get all book elements in bookstore where price is greater than 35.00
result = htmlDom.xpath("/bookstore/book[price>35.00]/title")
print("7. Title elements of book elements with price > 35.00 in bookstore:", result)

# 8. Get all book elements in bookstore where price is less than 35.00
result = htmlDom.xpath("/bookstore/book[price<=35.00]/title")
print("8. Title elements of book elements with price <= 35.00 in bookstore:", result)
