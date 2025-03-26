'''
02 - Regex Module - findall
'''

import re

# Setting up the regular expression pattern
pattern = re.compile(r"\d+")

# 1. findall() method - Find all substrings that match the pattern
fd = pattern.findall("one123two456")
print("1. Find all matching substrings:", fd)

# 1. Reverse Search - Find all matching substrings
fd = pattern.findall("one123two456")
print("1. Find all matching substrings:", fd)

# 2. findall() with specified start and end positions
fd = pattern.findall("one123two456", 6, 12)
print("2. Search result within specified range:", fd)

fd = pattern.findall("one123two456", 6, 12)
print("2. Search result within specified range:", fd)

# 3. Using a complex regex pattern
pattern = re.compile(r"\d+\.\d+")

fd = pattern.findall("5.,123.123312,'bigcat',435535,3.1415")
print("3. Find all decimal numbers:", fd)
