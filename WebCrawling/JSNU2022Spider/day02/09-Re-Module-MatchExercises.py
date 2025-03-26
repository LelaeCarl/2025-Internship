"""
09 - re module - Match exercises
"""

import re

# Compile a regular expression pattern
pattern = re.compile(r"\d+")

# 1. Matching from the start of the string (should fail, returns None)
match_result = pattern.match("onetwo123threefour456")
print("1. Match result:", match_result)

# 2. Matching from the start of the string (should succeed, matches '123')
match_result = pattern.match("123threefour445")
print("2. Match result:", match_result)

# 3. Matching from a specified starting position (index 6, should match '123')
match_result = pattern.match("onetwo123threefour456", 6)
print("3. Match from position 6:", match_result)

# 4. Matching within specified start and end positions (3 to 11, should match '123')
match_result = pattern.match("one123four456", 3, 11)
print("4. Match within positions 3-11:", match_result)

# 5. Display matched group
match_result = pattern.match("one123four456", 3, 11)
print("5. Matched group:", match_result.group())

# 6. Starting index of matched group
print("6. Start position of match:", match_result.start())

# 7. Ending index of matched group
print("7. End position of match:", match_result.end())

# 8. Span of matched group (tuple of start and end positions)
print("8. Span of match (start, end):", match_result.span())

# Reset the pattern to include groups and ignore case
# ([a-z]+) : Group of lowercase letters
# re.I     : Ignore case (uppercase/lowercase)
pattern = re.compile(r"([a-z]+) ([a-z]+)", re.I)

# 10. Perform matching with the new pattern
match_result = pattern.match("Hello World Where Python")
print("10. Matching result:", match_result)

# 11. Retrieve specific matched groups
# group(0): Entire match
# group(1): First subgroup match
# group(2): Second subgroup match
print("11. Matched subgroup 2:", match_result.group(2))

# 12. Retrieve span (start, end) of entire matched content
print("12. Span of entire match:", match_result.span())

# 13. Retrieve the first and second subgroup matches separately
print("13. First subgroup match:", match_result.group(1))
print("13. Second subgroup match:", match_result.group(2))

# 14. Retrieve all matched groups as a tuple
print("14. All matched groups:", match_result.groups())
print("14. First group:", match_result.groups()[0])
print("14. Second group:", match_result.groups()[1])

# 15. Retrieve span of entire matched content and individual subgroups
print("15. Span of entire matched content:", match_result.span(0))
print("15. Span of first subgroup:", match_result.span(1))
print("15. Span of second subgroup:", match_result.span(2))
