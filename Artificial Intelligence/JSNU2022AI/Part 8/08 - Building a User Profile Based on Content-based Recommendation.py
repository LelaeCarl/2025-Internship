'''
08 - Building a User Profile Based on Content-based Recommendation
'''

import pandas as pd
import numpy as np
from gensim.models import TfidfModel
from functools import reduce
import collections
from pprint import pprint
from gensim.corpora import Dictionary

# 1. Load movie dataset
def get_movie_dataset():
    # 1.1 Load movie tags dataset
    _tags = pd.read_csv("./data/tags.csv",
                        usecols=range(1, 3)).dropna()

    # 1.2 Group tags by movieId
    tags = _tags.groupby("movieId").agg(list)

    # 1.3 Load movies dataset
    movies = pd.read_csv("./data/movies.csv",
                         index_col="movieId")

    # 1.4 Split genres into list
    movies['genres'] = movies['genres'].apply(lambda x: x.split('|'))

    # 1.5 Find movies with both tag and movie information
    movies_index = set(movies.index) & set(tags.index)

    # 1.6 Filter movies
    new_tags = tags.loc[list(movies_index)]

    # 1.7 Join movies and new tags
    ret = movies.join(new_tags)

    # 1.8 Handle missing tags by replacing NaN with empty list
    movies_dataset = pd.DataFrame(
        map(
            lambda x: (x[0], x[1], x[2], x[3]) if x[3] is not np.nan
            else (x[0], x[1], x[2], []),
            ret.iterrows()
        ),
        columns=['movieId', 'title', 'genres', 'tags']
    )

    # 1.9 Set movieId as index
    movies_dataset.set_index("movieId", inplace=True)

    return movies_dataset

# 2. Create movie profiles
def create_movie_profile2(movie_dataset):
    # 2.1 Extract tags
    dataset = movie_dataset['tags'].values

    # 2.2 Create dictionary
    dict_ = Dictionary(dataset)

    # 2.3 Build corpus
    corpus = [dict_.doc2bow(line) for line in dataset]

    # 2.4 Train TF-IDF model
    model = TfidfModel(corpus)

    # 2.5 Build movie profiles
    movie_profile = []
    for i, data in enumerate(movie_dataset.itertuples()):
        mid = data[0]
        title = data[1]
        genres = data[2]
        tags = data[3]

        vector = model[corpus[i]]
        movie_tags = sorted(vector, key=lambda x: x[1], reverse=True)[:30]

        # 2.6.1 Convert TF-IDF result into a dictionary
        topN_tags_weights = dict(map(
            lambda x: (dict_[x[0]], x[1]),
            movie_tags
        ))

        # 2.6.2 Add genres with a fixed weight of 1.0
        for g in genres:
            topN_tags_weights[g] = 1.0

        # 2.6.3 Create top N tags list
        topN_tags = [i[0] for i in topN_tags_weights.items()]

        # 2.6.4 Store (movieId, title, profile, weights)
        movie_profile.append([mid, title, topN_tags, topN_tags_weights])

    # 2.7 Convert movie profile into DataFrame
    movie_profile = pd.DataFrame(movie_profile,
                                 columns=['movieId', 'title', 'profile', 'weights'])

    # 2.8 Set movieId as index
    movie_profile.set_index("movieId", inplace=True)

    return movie_profile

# 3. Create user profiles
def create_user_profile():
    # 3.1 Load user watch records
    watch_record = pd.read_csv("./data/ratings.csv",
                               usecols=range(2),
                               dtype={'userId': np.int32,
                                      'movieId': np.int32})

    # 3.2 Group movies watched by each user
    watch_record = watch_record.groupby('userId').agg(list)

    # 3.3 Load movie dataset
    movies_dataset = get_movie_dataset()

    # 3.4 Create movie profiles
    movie_profile = create_movie_profile2(movies_dataset)

    # 3.5 Initialize user profile dictionary
    user_profile = {}

    # 3.6 Build user profiles
    for uid, mids in watch_record.itertuples():
        # 3.6.1 Fetch profiles for movies the user has watched
        record_movie_profile = movie_profile.loc[list(mids)]

        # 3.6.2 Merge all tags into one list
        counter = collections.Counter(reduce(
            lambda x, y: list(x) + list(y),
            record_movie_profile['profile'].values
        ))

        # 3.6.3 Select top 50 interest words
        interest_words = counter.most_common(50)

        # 3.6.4 Normalize
        maxcount = interest_words[0][1]
        interest_words = [(w, round(c / maxcount, 4)) for w, c in interest_words]

        # 3.6.5 Save user profile
        user_profile[uid] = interest_words

    return user_profile

if __name__ == '__main__':
    # 1. Build user profile
    user_profile = create_user_profile()

    # 2. Display user profiles
    pprint(user_profile)
