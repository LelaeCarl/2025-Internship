# 02- Collaborative Filtering Recommendation Algorithm - Based on User's Collaborative Filtering Recommendation

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

# 1. Construct dataset
# 1.1 Create list of users and items
users = ['User1','User2','User3','User4','User5']
items = ['Item A','Item B','Item C','Item D','Item E']

# 1.2 Create dataset
datasets = [
    [1,0,1,1,0],
    [1,0,0,1,1],
    [1,0,1,0,0],
    [0,1,0,1,1],
    [1,1,1,0,1]
]

# 2. Generate DataFrame structure
df = pd.DataFrame(data=datasets,
                  columns=items,
                  index=users)

# 3. Calculate user-user similarity matrix
user_similar = 1 - pairwise_distances(
    df.values, metric='jaccard')
user_similar = pd.DataFrame(user_similar,
                            columns=users,
                            index=users)
print("User similarity matrix:\n", user_similar)

# 4. Sort each user's similarity and select top-2 similar users
# 4.1 Set dictionary
topN_users = {}

# 4.2 Process similarity for each row
for i in user_similar.index:
    # 4.2.1 Drop current user’s row (remove self), then sort other users for similarity ranking
    _df = user_similar.loc[i].drop([i])
    # 4.2.2 Sort similarity values descending
    _df_sorted = _df.sort_values(ascending=False)
    # 4.2.3 Take top-2 most similar users
    top2 = list(_df_sorted.index[:2])
    # 4.2.4 Save results to dictionary
    topN_users[i] = top2
print("Top-2 similar users:\n", topN_users)

# 5. Generate recommendation results
# 5.1 Set dictionary to store recommendation results
rs_results = {}

# 5.2 Loop through topN_users items
# user ==> "User1"
# sim_users==>['User3','User2']
for user, sim_users in topN_users.items():
    # 5.2.1 Set container for recommendation results (use set to remove duplicates)
    rs_user_result = set()
    # 5.2.2 Loop through similar users and retrieve item purchase records
    for sim_user in sim_users:
        # 5.2.3 Build item recommendation set
        rs_user_result = rs_user_result.union(
            set(df.loc[sim_user].replace(0,np.nan).dropna().index)
        )
    # 5.2.4 Remove items already bought by the user

    '''
    Example:
    User1 bought: {'Item A', 'Item C', 'Item D'}
    Initial result from union: {"Item A", "Item C", "Item D", "Item E"}
    Final filtered recommendation: {"Item E"}
    '''
    rs_user_result -= set(
        df.loc[user].replace(0,np.nan).dropna().index
    )

    # 5.2.5 Save to dictionary
    '''
    Example:
    {'User1': {'Item E'}, 'User2': {...}}
    '''
    rs_results[user] = rs_user_result

print("Final recommendation result:\n", rs_results)
