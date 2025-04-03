'''
01 - BS4 Module - Example Test
'''
from bs4 import BeautifulSoup

# 1. Set the string to be parsed
html = '''
 <div>
        <ul>
            <li class="item-0">
                <a href="link1.html">first item</a>
            </li>
            <li class="item-1">
                <a href="link2.html">second item</a>
            </li>
            <li class="zpp-item">
                <a href="link3.html">third item</a>
            </li>
            <li class="item-1">
                <a href="link4.html">fourth item</a>
            </li>
            <li class="item-0">
                <a href="link5.html">fifth item</a>
            </li>
        </ul>
 </div>
'''
print("HTML:", type(html))

# 2. Parse using BeautifulSoup, default to using 'lxml' library
soup = BeautifulSoup(html, features="lxml")
print("2.1 Type of bs4 object:", type(soup))
print("2.2 bs4 object:", soup)

# 3. Output object content
print("3.1 Output object content:", soup.prettify())

print("3.2 Type of object content:", type(soup.prettify()))
