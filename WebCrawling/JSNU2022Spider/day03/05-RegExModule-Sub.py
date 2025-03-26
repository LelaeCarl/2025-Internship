'''
05 - Regex Module - sub
'''

import re

# Setting up the regular expression pattern
pattern = re.compile(r"(\w+) (\w+)")

st = "Hello 123 World 456"

# 1. Finding matching results
fd = pattern.findall(st)
print("1. findall result:", fd)

# 2. Replacing using a replacement string
stb = pattern.sub("Python Java", st)
print("2. sub result:", stb)

# 3. Using group reference for substitution
stb2 = pattern.sub(r"\2 \1", st)
print("3. Group reference substitution:", stb2)

# 4. Using a replacement function
# m is the match object, group(0) is the matched string

def func(m):
    return "Hi " + m.group(0)

# Setting up string
pp = "Hello 123,Hello 456"

# Match operation
mt = pattern.match(pp)
print(mt)
print(mt.group(0))

# Using the function for substitution
print(pattern.sub(func, "Python 123,Java 456,PHP"))

# Specifying the number of replacements
print(pattern.sub(func, "Python 123,Java 456", 1))
