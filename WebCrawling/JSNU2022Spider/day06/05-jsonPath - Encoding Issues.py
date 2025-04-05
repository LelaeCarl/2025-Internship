'''
05-jsonPath - Encoding Issues
Any encoding on any platform can be converted to and from Unicode
'''

# Define a UTF-8 encoded string
utf8Str = "Hello Earth"

# 1. Convert UTF-8 to Unicode encoding (bytes)
unicodeStr = utf8Str.encode("utf-8")
print(unicodeStr)

# 2. Convert Unicode (bytes) back to UTF-8 string
utf8Str = unicodeStr.decode("utf-8")
print(utf8Str)

# 3. Attempt to decode Unicode bytes using GBK (may cause error if characters don't match encoding)
try:
    gbkStr = unicodeStr.decode("gbk")
    print(gbkStr)

    # 4. Convert GBK-encoded string back to Unicode (bytes)
    unicodeStr = gbkStr.encode("gbk")
    print(unicodeStr)
except UnicodeDecodeError as e:
    print("Encoding error:", e)
