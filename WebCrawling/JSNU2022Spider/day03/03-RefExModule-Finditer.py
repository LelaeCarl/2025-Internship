'''
03 - Regex Module - finditer
'''

import re

# Setting up the regular expression pattern
pattern = re.compile(r"\d+")

# 1. finditer() method - Find all numbers
ft = pattern.finditer("one123two456three789")
print("1. Find all numbers:")
for it in ft:
    print(f"{it.group()}, {it.span()}")

# 2. Specifying search range
ft2 = pattern.finditer("one123two456three789", 6, 20)
print("2. Find numbers within specified range:")
for it2 in ft2:
    print(f"{it2.group()}, {it2.span()}")
