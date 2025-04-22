# 01- Collaborative Filtering Recommendation Algorithm
'''
...
'''

import pandas as pd
# Import Jaccard similarity score: Jaccard similarity
from sklearn.metrics  import jaccard_score
# Calculate Jaccard similarity between all rows
from sklearn.metrics.pairwise import pairwise_distances

# 1. Prepare dataset
# 1.1 Construct user and item information list
users = ['User1','User2','User3','User4','User5']
items = ['Item A','Item B','Item C','Item D','Item E']

# 1.2 Construct raw data (purchase records)
# datasets = [
#     ['buy',None,'buy','buy',None],
#     ['buy',None,None,'buy','buy'],
#     ['buy','None','buy',None,None],
#     [None,'buy',None,'buy','buy'],
#     ['buy','buy','buy',None,'buy']
# ]

# 1.3 Encode dataset
datasets = [
    [1,0,1,1,0],
    [1,0,0,1,1],
    [1,0,1,0,0],
    [0,1,0,1,1],
    [1,1,1,0,1]
]

# 2. Create DataFrame
df = pd.DataFrame(datasets,columns=items,index=users)

# 3. Calculate similarity between Item A and Item B
print(jaccard_score(df['Item A'],df['Item B']))

# 4. Calculate pairwise Jaccard similarities
# 4.1 Calculate user similarity
user_similar = 1 - pairwise_distances(df.values,
                                      metric='jaccard')
# 4.2 Convert user similarity array to DataFrame
user_similar = pd.DataFrame(user_similar,
                            columns=users,
                            index=users)
print("User similarity matrix:\n",user_similar)

# 4.3 Calculate item similarity
item_similar = 1 - pairwise_distances(df.values.T,
                                      metric='jaccard')
item_similar = pd.DataFrame(item_similar,
                            columns=items,
                            index=items)
print("Item similarity matrix:\n",item_similar)
