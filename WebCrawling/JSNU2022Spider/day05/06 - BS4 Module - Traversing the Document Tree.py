'''
06 - BS4 Module - Traversing the Document Tree
'''
from bs4 import BeautifulSoup

soup = BeautifulSoup(
    open("hello2.html", encoding="utf-8"),
    'lxml'
)

# 1. Direct child nodes
# 1.1 contents (returns a list)
print("1.1 contents:", soup.head.contents)

# 1.2 children (returns an iterator)
# 1.2 children: <list_iterator object at 0x0000021145B43F40>
print("1.2 children:", soup.head.children)
# for child in soup.head.children:
#     print(child)

# 2. All descendant nodes
# This starts traversing and recursively from the document node
# for child in soup.descendants:
#     print(child)

# 3. Node content .string attribute
for child in soup.p.children:
    print(child.string)

# Traverse the document tree
for desc in soup.descendants:
    print("Traverse the document tree:", desc.string)
