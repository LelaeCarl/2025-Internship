'''
10 - Word vector-based content recommendation - tag vector similarity processing
'''

from gensim.models import TfidfModel, Word2Vec
import numpy as np
import pandas as pd
from gensim.corpora import Dictionary
import gensim
import logging

# 1. Load movie dataset
def get_movie_dataset():
    # 1.1 Read tag data
    _tags = pd.read_csv("./data/tags.csv",
                        usecols=range(1, 3)).dropna()

    # 1.2 Group tags by movieId
    tags = _tags.groupby("movieId").agg(list)

    # 1.3 Read movie data
    movies = pd.read_csv("./data/movies.csv",
                         index_col="movieId")

    # 1.4 Convert genres column to list
    movies['genres'] = movies['genres'].apply(lambda x: x.split('|'))

    # 1.5 Match movie IDs that exist in both datasets
    movies_index = set(movies.index) & set(tags.index)

    # 1.6 Filter and join tags to movies
    new_tags = tags.loc[list(movies_index)]
    ret = movies.join(new_tags)

    # 1.7 Ensure 'tags' column exists and is a list (not NaN)
    if 'tags' not in ret.columns:
        ret['tags'] = [[] for _ in range(len(ret))]
    else:
        ret['tags'] = ret['tags'].apply(lambda x: x if isinstance(x, list) else [])

    # 1.8 Build final movie dataset
    movie_dataset = pd.DataFrame(
        map(
            lambda x: (x[0], x[1]['title'], x[1]['genres'], x[1]['tags']),
            ret.iterrows()
        ),
        columns=['movieId', 'title', 'genres', 'tags']
    )

    # 1.9 Set movieId as index
    movie_dataset.set_index('movieId', inplace=True)

    return movie_dataset

# 2. Create movie tag profiles using TF-IDF
def create_movie_profile(movie_dataset):
    dataset = movie_dataset['tags'].values
    dct = Dictionary(dataset)
    corpus = [dct.doc2bow(line) for line in dataset]
    model = TfidfModel(corpus)

    _movie_profile = []

    for i, data in enumerate(movie_dataset.itertuples()):
        mid = data[0]
        title = data[1]
        genres = data[2]
        tags = data[3]

        vector = model[corpus[i]]
        movie_tags = sorted(vector, key=lambda x: x[1], reverse=True)[:30]

        topN_tags_weights = dict(map(
            lambda x: (dct[x[0]], x[1]), movie_tags
        ))

        for g in genres:
            topN_tags_weights[g] = 1.0

        topN_tags = list(topN_tags_weights.keys())

        _movie_profile.append([mid, title, topN_tags, topN_tags_weights])

    movie_profile = pd.DataFrame(
        _movie_profile,
        columns=['movieId', 'title', 'profile', 'weights']
    )
    movie_profile.set_index("movieId", inplace=True)

    return movie_profile

# 3. Main logic
if __name__ == '__main__':
    # Load data
    movie_dataset = get_movie_dataset()

    # Create tag profiles
    movie_profile = create_movie_profile(movie_dataset)

    # Enable gensim logging
    logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s",
                        level=logging.INFO)

    # Prepare training data: list of tag sequences per movie
    sentences = list(movie_profile['profile'].values)

    # Train Word2Vec model
    model = Word2Vec(sentences,
                     window=3,
                     min_count=1,
                     vector_size=20)

    # Interactive similarity query
    while True:
        words = input("words> ")  # enter tag
        try:
            ret = model.wv.most_similar(positive=[words], topn=10)
            print("Result:", ret)
        except KeyError:
            print(f"'{words}' not in vocabulary.")
