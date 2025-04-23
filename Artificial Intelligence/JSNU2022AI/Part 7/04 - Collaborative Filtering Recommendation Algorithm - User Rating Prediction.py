# 04 - Collaborative Filtering Recommendation Algorithm - User Rating Prediction
# (Dense Rating Matrix, Sparse Rating Matrix)

import pandas as pd
import numpy as np

# 1. Set dataset
users = ['User1','User2','User3','User4','User5']
items = ['Item A','Item B','Item C','Item D','Item E']

# Construct dataset
datasets = [
    [5,3,4,4,None],
    [3,1,2,3,3],
    [4,3,4,3,5],
    [3,3,1,5,4],
    [1,5,5,2,1]
]

# 2. Generate DataFrame
df = pd.DataFrame(data=datasets,
                  columns=items,
                  index=users)

# 3. Directly calculate Pearson correlation coefficient
# By default, correlation is calculated column-wise. So if we want to calculate user similarity, we need to transpose first.

# 3.1 Calculate similarity matrix between users
user_similar = df.T.corr()
print("User similarity matrix:\n", user_similar.round(2))

# 3.2 Calculate similarity matrix between items
item_similar = df.corr()
print("Item similarity matrix:\n", item_similar.round(2))

# 3.2 Calculate similarity matrix between items
item_similar = df.corr()
print("Item similarity matrix:\n", item_similar.round(2))
