'''
02-JSON Module - dumps
'''
import json
import chardet

# 1. Common Python data types
listStr = [1, 2, 3, 4]
tupleStr = (5, 6, 7, 8, 10)
dictStr = {"city": "Beijing", "name": "Zhang Sanfeng"}

# 2. Convert Python listStr to JSON array
print(json.dumps(listStr))
print(type(json.dumps(listStr)))

# 3. Convert Python tupleStr to JSON array
print(json.dumps(tupleStr))
print(type(json.dumps(tupleStr)))

# 4. Convert Python dictStr to JSON object
'''
1. json.dumps() uses ASCII encoding by default – affects Chinese characters
2. Set ensure_ascii=False to avoid default encoding (so Chinese displays correctly)
'''
print(json.dumps(dictStr, ensure_ascii=False))
print(type(json.dumps(dictStr)))

'''
5. chardet encoding detection module
   ensure_ascii=False sets encoding to UTF-8 instead of ASCII
   encoding='utf-8' specifies the decoding format used by bytes() function
'''
print(chardet.detect(
    bytes(json.dumps(dictStr, ensure_ascii=False),
          encoding='utf-8')
))
print(chardet.detect(bytes(json.dumps(dictStr), encoding='utf-8')))
