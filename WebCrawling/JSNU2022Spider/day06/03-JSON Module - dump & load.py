'''
03-JSON Module - dump & load
'''
import json

'''
1. dump
'''
# 1.1 List of dictionaries
# listStr = [{'city': 'Beijing', 'name': 'Zhang Sanfeng'}]
# json.dump(listStr, open('listStr.json', 'w'),
#           ensure_ascii=False)

# 1.2 Dictionary with a list
# dictStr = {'city': ['Beijing', 'Nanjing'], 'name': 'Zhang Sanfeng'}
# json.dump(dictStr, open('dictStr.json', 'w'),
#           ensure_ascii=False)

'''
2. load
'''
# 2.1 Load listStr.json
# strList = json.load(open("listStr.json"))
# print(strList)
# print(type(strList))

# 2.2 Load dictStr.json
# dictStr = json.load(open("dictStr.json"))
# print(dictStr)
# print(type(dictStr))
