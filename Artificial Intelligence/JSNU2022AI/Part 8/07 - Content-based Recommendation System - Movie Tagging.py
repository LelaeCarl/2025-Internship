'''
07 - Content-based Recommendation System - Movie Tagging
'''

import pandas as pd
import numpy as np
from gensim.models import TfidfModel
from pprint import pprint
from gensim.corpora import Dictionary

'''
The tags.csv file contains many user-labeled keywords for movies!
This project uses TF-IDF to model movies based on tags and then builds a content-based recommendation system.
'''

# 1. Load and process the movie dataset
def get_movie_dataset():
    # 1.1 Load movie tags dataset
    tags = pd.read_csv('./data/all-tags.csv',
                       usecols=range(1, 3)).dropna()

    # 1.2 Group tags by movieId
    tags = tags.groupby('movieId').agg(list)

    # 1.3 Load movies dataset
    movies = pd.read_csv('./data/movies.csv',
                         index_col='movieId')

    # 1.4 Process genres column into list
    movies['genres'] = movies['genres'].apply(lambda x: x.split('|'))

    # 1.5 Find intersection between tags and movies
    movies_index = set(movies.index) & set(tags.index)

    # 1.6 Filter matched movies and tags
    new_tags = tags.loc[list(movies_index)]
    ret = movies.join(new_tags)

    # 1.7 Handle missing tags
    ret = pd.DataFrame(
        map(
            lambda x: (x[0], x[1], x[2], x[3]) if x[3] is not np.nan \
                else (x[0], x[1], x[2], []),
            ret.iterrows()
        ),
        columns=['movieId', 'title', 'genres', 'tags']
    )

    # 1.8 Set movieId as index
    ret.set_index('movieId', inplace=True)

    return ret

# 2. Create movie profiles using TF-IDF
def create_movie_profile(movie_dataset):
    # 2.1 Extract tags
    dataset = movie_dataset['tags'].values

    # 2.2 Create dictionary
    dict_ = Dictionary(dataset)

    # 2.3 Build corpus
    corpus = [dict.doc2bow(line) for line in dataset]

    # 2.4 Train TF-IDF model
    model = TfidfModel(corpus)

    # 2.5 Build movie profiles
    movie_profile = []
    for i, row in enumerate(movie_dataset.index):
        # 2.5.1 Get movieId
        mid = movie_dataset.index[i]
        # 2.5.2 Apply TF-IDF to the movie's tags
        vector = model[corpus[i]]
        movie_tags = sorted(vector, key=lambda x: x[1], reverse=True)

        # 2.5.3 Convert movie tags into a dictionary
        topN_tags_weights = dict(map(
            lambda x: (dict_[x[0]], x[1]),
            movie_tags
        ))

        movie_profile.append([
            mid,
            movie_dataset.loc[mid, 'title'],
            list(topN_tags_weights.keys()),
            topN_tags_weights
        ])

    # 2.6 Convert movie_profile to DataFrame
    movie_profile = pd.DataFrame(
        movie_profile,
        columns=['movieId', 'title', 'profile', 'weights']
    )

    # 2.7 Set movieId as index
    movie_profile.set_index('movieId', inplace=True)

    return movie_profile

# 3. Improved TF-IDF: Include genres into profile
def create_movie_profile2(movie_dataset):
    # 3.1 Extract tags
    dataset = movie_dataset['tags'].values

    # 3.2 Create dictionary
    dict_ = Dictionary(dataset)

    # 3.3 Build corpus
    corpus = [dict_.doc2bow(line) for line in dataset]

    # 3.4 Train TF-IDF model
    model = TfidfModel(corpus)

    # 3.5 Build movie profiles
    movie_profile = []
    for i, row in enumerate(movie_dataset.itertuples()):
        mid = row.Index
        title = row.title
        genres = row.genres
        tags = row.tags

        vector = model[corpus[i]]
        movie_tags = sorted(vector, key=lambda x: x[1], reverse=True)

        # 3.6 Convert movie tags to dictionary
        topN_tags_weights = dict(map(
            lambda x: (dict_[x[0]], x[1]),
            movie_tags
        ))

        # 3.6.4 Set genre weights to 1.0
        for gn in genres:
            topN_tags_weights[gn] = 1.0

        movie_profile.append([
            mid,
            title,
            list(topN_tags_weights.keys()),
            topN_tags_weights
        ])

    # 3.7 Convert movie_profile to DataFrame
    movie_profile = pd.DataFrame(
        movie_profile,
        columns=['movieId', 'title', 'profile', 'weights']
    )

    # 3.8 Set movieId as index
    movie_profile.set_index('movieId', inplace=True)

    return movie_profile

# 4. Build inverted index
def create_inverted_table(movie_profile):
    # 4.1 Initialize
    inverted_table = {}

    # 4.2 Iterate through movie profile weights
    for mid, weights in movie_profile['weights'].iteritems():
        # 4.3 Iterate through each tag and weight
        for tag, weight in weights.items():
            # 4.3.1 Set default empty list
            inverted_table.setdefault(tag, [])
            # 4.3.2 Append (movieId, weight) pair
            inverted_table[tag].append((mid, weight))

    # 4.4 Return inverted index
    return inverted_table

if __name__ == '__main__':
    # 1. Get processed movie dataset
    movie_dataset = get_movie_dataset()

    # 2. Create movie profiles (with genres included)
    movie_profile = create_movie_profile2(movie_dataset)

    # 3. Create inverted index
    inverted_table = create_inverted_table(movie_profile)

    # 4. Output
    pprint(inverted_table)
