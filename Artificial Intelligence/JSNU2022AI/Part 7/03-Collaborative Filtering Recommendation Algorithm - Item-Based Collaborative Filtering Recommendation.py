# 03- Collaborative Filtering Recommendation Algorithm - Item-Based Collaborative Filtering Recommendation

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 1. Construct dataset
# 1.1 Create list of users and items
users = ['User1','User2','User3','User4','User5']
items = ['Item A','Item B','Item C','Item D','Item E']

# 1.2 Create dataset (user-item interaction matrix: 1 means bought, 0 means not bought)
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

# 3. Calculate item-item similarity matrix using cosine similarity
item_similar = cosine_similarity(df.T.values)  # transpose to item-user matrix
item_similar = pd.DataFrame(item_similar,
                            columns=items,
                            index=items)
print("Item-to-item similarity matrix:\n", item_similar)

# 4. Generate recommendations for each user
# 4.1 Create dictionary to store results
rs_results = {}

# 4.2 Iterate over each user
for user in df.index:
    # 4.2.1 Get items the user has interacted with (purchased)
    user_items = df.loc[user]
    bought_items = list(user_items[user_items > 0].index)

    # 4.2.2 Initialize dictionary to score candidate items
    item_scores = {}

    for item in bought_items:
        # 4.2.3 Get similar items to the current item
        sim_items = item_similar[item].drop(index=item)  # exclude itself
        for sim_item, sim_score in sim_items.items():
            if df.loc[user, sim_item] == 0:  # recommend only unseen items
                if sim_item not in item_scores:
                    item_scores[sim_item] = 0
                # Add weighted score based on similarity
                item_scores[sim_item] += sim_score

    # 4.2.4 Sort the candidate items by their score in descending order
    sorted_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
    recommended_items = [item for item, score in sorted_items]

    # 4.2.5 Save recommendations
    rs_results[user] = set(recommended_items)

# 5. Output final recommendation results
print("Final recommendation result:\n", rs_results)
