# 4. Algorithm implementation: User-Based-CF rating prediction
# The above two functions provide:
# <User-movie rating matrix>
# <User similarity matrix>
# <Item similarity matrix>
# uid: User ID
# iid: Item ID
# ratings_matrix: User-movie rating matrix
# user_similar: User similarity matrix (Pearson correlation coefficient)
# :return Predicted rating value

import pandas as pd
import numpy as np
import os
from pprint import pprint

# 1. Set data and cache paths
DATA_PATH = "./data/ratings.csv"
CACHE_PATH = "./data/cache/"

# Create cache directory if it doesn't exist
os.makedirs(CACHE_PATH, exist_ok=True)


# 2. Load data function
def load_data(data_path):
    cache_path = os.path.join(CACHE_PATH, 'ratings_matrix_cache.pkl')
    print("Starting to load dataset...")
    if os.path.exists(cache_path):
        print("Loading from cache...")
        ratings_matrix = pd.read_pickle(cache_path)
        print("Dataset loaded from cache")
    else:
        print("Loading dataset from source file...")
        dtype = {'userId': np.int32, "movieId": np.int32, "rating": np.float32}
        ratings = pd.read_csv(data_path, dtype=dtype, usecols=range(3))
        ratings_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating')
        ratings_matrix.to_pickle(cache_path)
    return ratings_matrix


# 3. Calculate similarity matrix
def compute_pearson_similarity(ratings_matrix, based='user'):
    if based == 'user':
        cache_path = os.path.join(CACHE_PATH, 'user_similarity_cache.pkl')
        if os.path.exists(cache_path):
            print("Loading user similarity from cache")
            similarity = pd.read_pickle(cache_path)
        else:
            print("Calculating user similarity matrix")
            similarity = ratings_matrix.T.corr()
            similarity.to_pickle(cache_path)
    elif based == 'item':
        cache_path = os.path.join(CACHE_PATH, 'item_similarity_cache.pkl')
        if os.path.exists(cache_path):
            print("Loading item similarity from cache")
            similarity = pd.read_pickle(cache_path)
        else:
            print("Calculating item similarity matrix")
            similarity = ratings_matrix.corr()
            similarity.to_pickle(cache_path)
    else:
        raise Exception("Invalid 'based' value: %s" % based)
    print("Similarity calculation complete")
    return similarity


# 4. User-Based CF rating prediction
def predict(uid, iid, ratings_matrix, user_similar):
    print("Predicting user <%d>'s rating for movie <%d>..." % (uid, iid))

    # 4.1 Find similar users (excluding self)
    similar_users = user_similar[uid].drop([uid]).dropna()

    # 4.2 Filter for positive correlation only
    similar_users = similar_users.where(similar_users > 0).dropna()

    # 4.3 Check if similar users exist
    if similar_users.empty:
        raise Exception("User <%d> has no similar users" % uid)

    # 4.4 Find similar users who rated this item
    ids = set(ratings_matrix[iid].dropna().index) & set(similar_users.index)

    # 4.5 Get final set of similar users
    finally_similar_users = similar_users.loc[list(ids)]

    # 4.6 Calculate weighted rating prediction
    sum_up = 0
    sum_down = 0

    for sim_uid, similarity in finally_similar_users.iteritems():
        sim_user_rated_movies = ratings_matrix.loc[sim_uid].dropna()
        sim_user_rating_for_item = sim_user_rated_movies[iid]
        sum_up += similarity * sim_user_rating_for_item
        sum_down += similarity

    # 4.7 Calculate and return predicted rating
    predict_rating = sum_up / sum_down
    print("Predicted user <%d>'s rating for movie <%d>: %.2f" % (uid, iid, predict_rating))
    return round(predict_rating, 2)


# 5. Predict all ratings for a user
def predict_all(uid, ratings_matrix, user_similar):
    item_ids = ratings_matrix.columns
    for iid in item_ids:
        try:
            rating = predict(uid, iid, ratings_matrix, user_similar)
        except Exception as e:
            print(e)
        else:
            yield uid, iid, rating


# 6. Helper function for filtered predictions
def _predict_all(uid, item_ids, ratings_matrix, user_similar):
    for iid in item_ids:
        try:
            rating = predict(uid, iid, ratings_matrix, user_similar)
        except Exception as e:
            print(e)
        else:
            yield uid, iid, rating


# 7. Filtered prediction method
def predict_all_filter(uid, ratings_matrix, user_similar, filter_rule=None):
    if not filter_rule:
        item_ids = ratings_matrix.columns
    elif isinstance(filter_rule, str) and filter_rule == "unhot":
        count = ratings_matrix.count()
        item_ids = count.where(count > 10).dropna().index
    elif isinstance(filter_rule, str) and filter_rule == 'rated':
        user_ratings = ratings_matrix.loc[uid]
        outScore = user_ratings < 6
        item_ids = outScore.where(outScore == False).dropna().index
    elif isinstance(filter_rule, list) and set(filter_rule) == set(['unhot', 'rated']):
        count = ratings_matrix.count()
        ids1 = count.where(count > 10).dropna().index
        user_ratings = ratings_matrix.loc[uid]
        outScore = user_ratings < 6
        ids2 = outScore.where(outScore == False).dropna().index
        item_ids = set(ids1) & set(ids2)
    else:
        raise Exception("Invalid filter parameter")

    yield from _predict_all(uid, item_ids, ratings_matrix, user_similar)


# 8. Top-K recommendation system
def top_k_rs_result(k):
    ratings_matrix = load_data(DATA_PATH)
    user_similar = compute_pearson_similarity(ratings_matrix)
    results = predict_all_filter(1, ratings_matrix, user_similar, filter_rule=['unhot', 'rated'])
    return sorted(results, key=lambda x: x[2], reverse=True)[:k]


if __name__ == '__main__':
    # Example usage:
    print("Testing single prediction:")
    ratings_matrix = load_data(DATA_PATH)
    user_similar = compute_pearson_similarity(ratings_matrix, based='user')
    try:
        predicted = predict(1, 2, ratings_matrix, user_similar)
        print(f"Predicted rating for user 1 on movie 2: {predicted}")
    except Exception as e:
        print(f"Prediction failed: {e}")

    print("\nGenerating top 20 recommendations:")
    recommendations = top_k_rs_result(20)
    pprint(recommendations)