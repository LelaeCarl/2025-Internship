'''
01-JSON Module - loads
'''
import json

# 1. Define JSON data type (string object) - list
strList = '[1,2,3,4]'

# 2. Define JSON data type (string object) - object
strDict = '{"city":"Beijing", "name":"Zhang Sanfeng"}'

# 3. Convert strList to list: convert JSON string list to Python type
print(json.loads(strList))
print(type(json.loads(strList)))

# 4. Convert strDict to dictionary: convert JSON string object to Python type
print(json.loads(strDict))
print(type(json.loads(strDict)))
