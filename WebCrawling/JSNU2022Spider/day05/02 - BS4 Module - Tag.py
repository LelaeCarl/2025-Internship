'''
02 - BS4 Module - Tag
'''
from bs4 import BeautifulSoup

# 1. Set the string to be parsed
html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Jiangsu Normal University</title>
</head>
<body>
    <p class="title" name="jack">
        <b>The Dormouse's story</b>
    </p>
    <p class="story">
        The Story of Sun Wukong and Bai Gu Jing
        <a href="https://www.jsnu.edu.cn/wy"
            class="sister" id="link1">
            <!-- Wang Yang -->
        </a>
        <a href="https://www.jsnu.edu.cn/gxh"
            class="sister" id="link2">
            Gu Xuhui
        </a>
          <a href="https://www.jsnu.edu.cn/dh"
            class="sister" id="link3">
            Dahai
        </a>
        The Story of Monks, Taoists, and Nuns
    </p>
    <p class="story">
        ......
    </p>
</body>
</html>
'''

# 2. Parse into BS4 object
soup = BeautifulSoup(html, "lxml")

# 3. Get the title tag
print("3. Get title tag:", soup.title)

# 4. Get all <a> tags (default matches only the first one)
print("4. Get <a> tag:", soup.a)

print("4. Object type:", type(soup.a))

# 5. Get the <p> tag
print("5. Get <p> tag:", soup.p)

# 6. Get content inside <head> tag (.name retrieves the tag name)
print("6. Get content inside <head> tag:", soup.head.name)

# 7. Get the attrs property and values of <p> tag
print("7. Get attrs property and values of <p> tag:", soup.p.attrs)

# 8. Get the attributes and values of <p> tag
print("8. Get attributes and values of <p> tag:", soup.p['class'])
print("8. Get attributes and values of <p> tag:", soup.p['name'])

# 9. Delete the attribute of <p> tag
del soup.p['class']
print("9. Delete attribute of <p> tag:", soup.p)

# 10. Modify the attribute value of <p> tag
soup.p['name'] = 'zpp'
print("10. Modify attribute value of <p> tag:", soup.p)

# 11. Add a new attribute value to <p> tag
soup.p['menu'] = 'zcc'
print("11. Add new attribute value to <p> tag:", soup.p)
