import pandas as pd
import numpy as np
import os

# 1. Set data and cache paths
DATA_PATH = "./data/ratings.csv"
CACHE_PATH = "./data/cache/"

# 2. Load data
def load_data(data_path):
    # 2.1 Get data storage area (unlock cache address)
    cache_path = os.path.join(CACHE_PATH, 'ratings_matrix_cache')

    # 2.2 Start loading dataset
    print("Starting to load dataset......")
    # 2.3 Check if storage address is allowed
    if os.path.exists(cache_path):
        print("Waiting for request while loading dataset......")
        # 2.3.1 Read buffer file from buffer pool
        ratings_matrix = pd.read_pickle(cache_path)
        # 2.3.2 Save completion of dataset loading
        print("Dataset loaded from cache complete")
    else:
        print("Loading dataset......")
        # 2.3.3 Set buffer file in buffer pool
        dtype = {'userId': np.int32,
                "movieId": np.int32,
                "rating": np.float32}
        # 2.3.4 Load data and create buffer
        ratings = pd.read_csv(data_path,
                            dtype=dtype,
                            usecols=range(3))
        # 2.3.5 Use pivot table to transform data
        ratings_matrix = ratings.pivot_table(
            index='userId',
            columns='movieId',
            values='rating')
        # 2.3.6 Ensure buffer value in buffer pool
        ratings_matrix.to_pickle(cache_path)
    return ratings_matrix

# 3. Calculate similarity coefficient
def compute_pearson_similarity(ratings_matrix, based='user'):
    # 3.1 User similarity coefficient cache path
    user_similarity_cache_path = os.path.join(CACHE_PATH, 'user_similarity_cache')

    # 3.2 Item similarity coefficient cache path
    item_similarity_cache_path = os.path.join(CACHE_PATH, 'item_similarity_cache')

    # 3.3 User similarity coefficient
    if based == 'user':
        # 3.3.1 Check if user similarity coefficient exists in buffer pool
        if os.path.exists(user_similarity_cache_path):
            print("Loading user similarity coefficient from cache")
            similarity = pd.read_pickle(user_similarity_cache_path)
        else:  # 3.3.2 Start calculating user similarity coefficient not in buffer pool
            print("Starting to calculate user similarity coefficient not in buffer pool")
            similarity = ratings_matrix.T.corr()
            similarity.to_pickle(user_similarity_cache_path)

    # 3.4 Item similarity coefficient
    elif based == 'item':
        # 3.4.1 Check item similarity coefficient
        if os.path.exists(item_similarity_cache_path):
            print("Loading user similarity coefficient from cache")
            similarity = pd.read_pickle(item_similarity_cache_path)
        else:  # 3.4.2 Start calculating item similarity coefficient not in buffer pool
            similarity = ratings_matrix.corr()
            similarity.to_pickle(item_similarity_cache_path)

    else:  # 3.5 Other similarity coefficients
        raise Exception("Unhandled 'based' Value: %s" % based)
    print("Similarity coefficient loading complete")
    return similarity

if __name__ == '__main__':
    # 1. Load dataset
    ratings_matrix = load_data(DATA_PATH)
    print("Dataset loaded: \n", ratings_matrix)
    # 2. User-based similarity coefficient
    # user_similar = compute_pearson_similarity(ratings_matrix, based='user')
    # print("User similarity: \n", user_similar)

    # 3. Item-based similarity coefficient
    item_similar = compute_pearson_similarity(ratings_matrix, based='item')
    print("Item similarity: \n", item_similar)

# 4. Algorithm Implementation: User-Based Collaborative Filtering Prediction
# This function takes in a user ID and item ID, and predicts the user's rating for the item
# Inputs:
# uid: User ID
# iid: Item ID
# ratings_matrix: User-Item Ratings Matrix
# user_similar: User Similarity Matrix (Pearson correlation coefficients)
# Returns: Predicted rating

def predict(uid, iid, ratings_matrix, user_similar):
    print("Starting prediction: User %d for Movie %d..." % (uid, iid))

    # 4.1 Get similarity scores of all users with uid (excluding uid itself)
    similar_users = user_similar[uid].drop(uid).dropna()

    # 4.2 Keep only users with a positive similarity score
    similar_users = similar_users[similar_users > 0].dropna()

    # 4.3 Check if there are any similar users
    if similar_users.empty:
        raise Exception("User %d has no similar users" % uid)

    # 4.4 Select users who have rated the item iid
    ids = set(ratings_matrix[iid].dropna().index) & set(similar_users.index)

    # 4.5 Convert the ratings of the similar users into a DataFrame
    finally_similar_users = similar_users.loc[list(ids)]

    # 4.6 Calculate the predicted rating for uid on iid
    # 4.6.1 Numerator of the prediction formula
    sum_up = 0
    # 4.6.2 Denominator of the prediction formula
    sum_down = 0

    # 4.6.3 Iterate through all similar users
    for sim_uid, similarity in finally_similar_users.iteritems():
        # 4.6.4 Get this similar user's ratings
        sim_user_rated_movies = ratings_matrix.loc[sim_uid].dropna()

        # 4.6.5 Get this user's rating for item iid
        sim_user_rating_for_item = sim_user_rated_movies[iid]

        # 4.6.6 Multiply by similarity and accumulate
        sum_up += similarity * sim_user_rating_for_item
        # 4.6.7 Accumulate similarity
        sum_down += similarity

    # 4.7 Final predicted score
    predict_rating = sum_up / sum_down
    print("Predicted rating for User %d on Movie %d: %.2f" % (uid, iid, predict_rating))

    # 4.8 Return rounded result to 2 decimal places
    return round(predict_rating, 2)


if __name__ == '__main__':
    # 1. Load the data
    ratings_matrix = load_data(DATA_PATH)

    # 2. Compute user similarity matrix using Pearson correlation
    user_similar = compute_pearson_similarity(ratings_matrix, based='user')

    # Example prediction
    predict(1, 2, ratings_matrix, user_similar)

# 5. Predict all unrated items for a user
# Inputs:
# uid: user ID
# ratings_matrix: user-item ratings matrix
# user_similar: user similarity matrix
# Returns: Generator yielding (user ID, item ID, predicted rating)

def predict_all(uid, ratings_matrix, user_similar):
    item_ids = ratings_matrix.columns

    for iid in item_ids:
        try:
            rating = predict(uid, iid, ratings_matrix, user_similar)
        except Exception as e:
            print(e)
        else:
            yield uid, iid, rating


# 6. Wrapper function to predict ratings for one user on a list of items
# Inputs:
# uid: user ID
# item_ids: list of item IDs
# ratings_matrix: user-item ratings matrix
# user_similar: user similarity matrix
# Returns: Generator yielding (user ID, item ID, predicted rating)

def _predict_all(uid, item_ids, ratings_matrix, user_similar):
    for iid in item_ids:
        try:
            rating = predict(uid, iid, ratings_matrix, user_similar)
        except Exception as e:
            print(e)
        else:
            yield uid, iid, rating


# 7. Predict function with filtering capabilities
# Inputs:
# uid: user ID
# ratings_matrix: user-item ratings matrix
# user_similar: user similarity matrix
# filter_rule: optional filter for items
# Returns: Generator yielding (user ID, item ID, predicted rating)

def predict_all_filter(uid, ratings_matrix, user_similar, filter_rule=None):
    if not filter_rule:
        item_ids = ratings_matrix.columns

    elif isinstance(filter_rule, str):
        if filter_rule == 'unhot':
            # Filter for items rated less than 20 times
            count = ratings_matrix.count()
            item_ids = count.where(count < 20).dropna().index

        elif filter_rule == 'rated':
            # Filter for items this user has already rated
            user_ratings = ratings_matrix.loc[uid]
            print("This user's rated movies:\n", user_ratings)
            outScore = user_ratings < 6
            item_ids = outScore.where(outScore == False).dropna().index

    elif isinstance(filter_rule, list) and set(filter_rule) == set(['unhot', 'rated']):
        # Filter for movies both rated by the user and are not popular
        count = ratings_matrix.count()
        ids1 = count.where(count < 20).dropna().index

        user_ratings = ratings_matrix.loc[uid]
        outScore = user_ratings < 6
        ids2 = outScore.where(outScore == False).dropna().index

        item_ids = set(ids1) & set(ids2)

    else:
        raise Exception("Invalid filter rule")

    yield from _predict_all(uid, item_ids, ratings_matrix, user_similar)


# 8. Top-K recommendation function
def top_k_rs_result(k):
    # 8.1 Load data
    ratings_matrix = load_data(DATA_PATH)

    # 8.2 Compute user similarity matrix
    user_similar = compute_pearson_similarity(ratings_matrix)

    # 8.3 Make predictions with filters
    results = predict_all_filter(
        1, ratings_matrix, user_similar, filter_rule=['unhot', 'rated']
    )

    # 8.4 Sort results by predicted rating in descending order and return top-k
    return sorted(results, key=lambda x: x[2], reverse=True)[:k]


if __name__ == '__main__':
    # 1. Load data
    ratings_matrix = load_data(DATA_PATH)

    # 2. Compute similarity matrix
    user_similar = compute_pearson_similarity(ratings_matrix)

    # 3. Predict and print results
    for result in predict_all_filter(1, ratings_matrix, user_similar, filter_rule='rated'):
        print(result)

    # 4. Print top-k recommendations
    from pprint import pprint
    result = top_k_rs_result(20)  # top-20
    pprint(result)
