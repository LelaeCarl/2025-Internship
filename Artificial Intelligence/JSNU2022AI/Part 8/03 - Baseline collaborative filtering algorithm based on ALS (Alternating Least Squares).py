'''
03 - Baseline collaborative filtering algorithm based on ALS (Alternating Least Squares)
'''

import pandas as pd
import numpy as np

# 1. ALS Algorithm Model
class BaselineCFByALS(object):
    # 1.1 Initialization function
    def __init__(self, number_epochs, reg_bu, reg_bi, columns=['uid', 'iid', 'rating']):
        # 1.1.1 Initialize hyperparameters
        self.number_epochs = number_epochs
        # 1.1.2 Regularization parameter for bu
        self.reg_bu = reg_bu
        # 1.1.3 Regularization parameter for bi
        self.reg_bi = reg_bi
        self.columns = columns

    # 1.2 Training function
    def fit(self, dataset):
        # 1.2.1 Save dataset
        self.dataset = dataset
        # 1.2.2 Calculate user ratings
        self.users_ratings = dataset.groupby(self.columns[0]).agg({self.columns[1]: [list], self.columns[2]: [list]})
        # 1.2.3 Calculate item ratings
        self.items_ratings = dataset.groupby(self.columns[1]).agg({self.columns[0]: [list], self.columns[2]: [list]})
        # 1.2.4 Calculate global mean rating
        self.global_mean = self.dataset[self.columns[2]].mean()
        # 1.2.5 Train bu and bi using ALS method
        self.bu, self.bi = self.als()

    # 1.3 Set model parameters using ALS to optimize bu and bi
    def als(self):
        # 1.3.1 Initialize bu and bi
        bu = dict(zip(self.users_ratings.index, np.zeros(len(self.users_ratings))))
        bi = dict(zip(self.items_ratings.index, np.zeros(len(self.items_ratings))))

        # 1.3.2 Iterate
        for i in range(self.number_epochs):
            print("epoch number: %d" % i)

            # 1.3.3 Update bi by fixing bu
            for iid, row in self.items_ratings.iterrows():
                uids = row[(self.columns[0], 'list')]
                ratings = row[(self.columns[2], 'list')]
                _sum = 0
                for uid, rating in zip(uids, ratings):
                    _sum += rating - self.global_mean - bu[uid]
                bi[iid] = _sum / (self.reg_bi + len(uids))

            # 1.3.4 Update bu by fixing bi
            for uid, row in self.users_ratings.iterrows():
                iids = row[(self.columns[1], 'list')]
                ratings = row[(self.columns[2], 'list')]
                _sum = 0
                for iid, rating in zip(iids, ratings):
                    _sum += rating - self.global_mean - bi[iid]
                bu[uid] = _sum / (self.reg_bu + len(iids))

        return bu, bi

    # 1.4 Prediction function
    def predict(self, uid, iid):
        predict_rating = self.global_mean + self.bu.get(uid, 0) + self.bi.get(iid, 0)
        return predict_rating


if __name__ == '__main__':
    # 1. Define data type for reading the dataset
    dtype = [('userId', np.int32),
             ('movieId', np.int32),
             ('rating', np.float32)]

    # 2. Read dataset and select specific columns
    dataset = pd.read_csv("./data/ratings.csv",
                          usecols=range(3),
                          dtype=dict(dtype))

    # 3. Initialize ALS model
    bcf = BaselineCFByALS(20, 25, 15, ['userId', 'movieId', 'rating'])

    # 4. Train the model
    bcf.fit(dataset)

    # 5. Interactive prediction
    while True:
        uid = int(input("uid:"))
        iid = int(input("iid:"))
        print(bcf.predict(uid, iid))
