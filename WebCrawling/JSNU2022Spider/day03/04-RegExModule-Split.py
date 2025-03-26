'''
04 - Regex Module - split
'''

import re

# Setting up the regular expression pattern
pattern = re.compile(r"[\,\;\s]+")

# Splitting the string based on the specified pattern
sp = pattern.split("a,b,;;;;;; c# dd ?? ?? ?")
print("Result of split method:", sp)
