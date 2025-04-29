import pandas as pd
import numpy as np
from gensim.models import TfidfModel
from functools import reduce
from pprint import pprint
from gensim.corpora import Dictionary

# 1.读取电影数据集
def get_movie_dataset():
    # 1.1 读取标签数据
    _tags = pd.read_csv("./data/tags.csv",
                        usecols=range(1, 3)).dropna()

    # 1.2 按movieId分组
    tags = _tags.groupby("movieId").agg(list)

    # 1.3 读取电影数据
    movies = pd.read_csv("./data/movies.csv",
                         index_col="movieId")

    # 1.4 将genres列分割成list
    movies['genres'] = movies['genres'].apply(lambda x: x.split('|'))

    # 1.5 筛选出两者都有的movie
    movies_index = set(movies.index) & set(tags.index)

    # 1.6 筛选出符合条件的电影
    new_tags = tags.loc[list(movies_index)]

    # 1.7 合并电影和标签
    ret = movies.join(new_tags)

    # 1.8 处理缺失的tags，将NaN替换为空list
    movies_dataset = pd.DataFrame(
        map(
            lambda x: (x[0], x[1]['title'], x[1]['genres'], x[1]['tags']) if pd.notna(x[1]['tags'])
            else (x[0], x[1]['title'], x[1]['genres'], []),
            ret.iterrows()
        ),
        columns=['movieId', 'title', 'genres', 'tags']
    )

    # 1.9 设置movieId为index
    movies_dataset.set_index("movieId", inplace=True)

    return movies_dataset

# 2. 创建电影profile
def create_movie_profile(movie_dataset):
    dataset = movie_dataset['tags'].values
    dict_ = Dictionary(dataset)
    corpus = [dict_.doc2bow(line) for line in dataset]
    model = TfidfModel(corpus)

    movie_profile = []
    for i, data in enumerate(movie_dataset.itertuples()):
        mid = data[0]
        title = data[1]
        genres = data[2]
        tags = data[3]

        vector = model[corpus[i]]
        movie_tags = sorted(vector, key=lambda x: x[1], reverse=True)[:30]

        topN_tags_weights = dict(map(
            lambda x: (dict_[x[0]], x[1]),
            movie_tags
        ))

        for g in genres:
            topN_tags_weights[g] = 1.0

        topN_tags = list(topN_tags_weights.keys())

        movie_profile.append([mid, title, topN_tags, topN_tags_weights])

    movie_profile = pd.DataFrame(movie_profile,
                                 columns=['movieId', 'title', 'profile', 'weights'])
    movie_profile.set_index("movieId", inplace=True)

    return movie_profile

# 3. 创建用户profile
def create_user_profile():
    watch_record = pd.read_csv("./data/ratings.csv",
                               usecols=range(2),
                               dtype={'userId': np.int32, 'movieId': np.int32})
    watch_record = watch_record.groupby('userId').agg(list)

    movies_dataset = get_movie_dataset()
    movie_profile = create_movie_profile(movies_dataset)

    user_profile = {}

    for uid, mids in watch_record.itertuples():
        record_movie_profile = movie_profile.loc[list(mids)]

        counter = collections.Counter(reduce(
            lambda x, y: list(x) + list(y),
            record_movie_profile['profile'].values
        ))

        interest_words = counter.most_common(50)
        maxcount = interest_words[0][1]
        interest_words = [(w, round(c / maxcount, 4)) for w, c in interest_words]

        user_profile[uid] = interest_words

    return user_profile

# 4. 创建倒排表
def create_inverted_table(movie_profile):
    inverted_table = {}
    for mid, weights in movie_profile['weights'].iteritems():
        for tag, weight in weights.items():
            inverted_table.setdefault(tag, []).append((mid, weight))
    return inverted_table

if __name__ == '__main__':
    # 1. 构建用户profile
    user_profile = create_user_profile()

    # 2. 构建电影数据集和电影profile
    movie_dataset = get_movie_dataset()
    movie_profile = create_movie_profile(movie_dataset)
    inverted_table = create_inverted_table(movie_profile)

    # 3. 读取用户观看记录
    watch_record = pd.read_csv("./data/ratings.csv",
                               usecols=range(2),
                               dtype={'userId': np.int32, 'movieId': np.int32})
    watch_record = watch_record.groupby('userId').agg(list)

    # 4. 推荐电影
    for uid, record in user_profile.items():
        result_table = {}
        for interest_word, interest_weight in record:
            if interest_word in inverted_table:
                related_movies = inverted_table[interest_word]
                for mid, weight in related_movies:
                    result_table.setdefault(mid, []).append(interest_weight * weight)

        rs_result = map(lambda x: (x[0], np.sum(x[1])), result_table.items())
        rs_result = sorted(rs_result, key=lambda x: x[1], reverse=True)[:100]

        print(f"User ID: {uid}")
        pprint(rs_result)
        break  # 目前只为第一个用户推荐
