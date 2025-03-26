'''
01 - Regex Module - search
'''

import re

# Setting up the regular expression pattern
pattern = re.compile(r"\d+")

# 1. search() method - Default search
sea = pattern.search("one123two456")
print("1. Default search result:", sea)

# 2. search() method - Specifying search range
sea = pattern.search("onetwo123threefour456", 10, 21)
print("2. Specified range search result:", sea)

# 3. search() method - Matching multiple numbers
sea = pattern.search("Hello 1233214543 1312312213")
print("3. Matching multiple numbers result:", sea)

# 4. Retrieving search results
print("4. Matched group:", sea.group())
print("4. Matched span:", sea.span())
