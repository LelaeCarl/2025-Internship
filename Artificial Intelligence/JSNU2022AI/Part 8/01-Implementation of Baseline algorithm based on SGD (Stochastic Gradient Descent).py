"""
01-Implementation of Baseline algorithm based on SGD (Stochastic Gradient Descent)
"""

import pandas as pd
import numpy as np
from pprint import pprint

'''
1. Baseline algorithm - SGD implementation
'''

class BaseLineCFBySGD(object):
    # 1.1 Initialization
    def __init__(self, number_epochs, alpha, reg, columns=['uid', 'iid', 'rating']):
        # Initialize hyperparameters
        self.number_epochs = number_epochs
        self.alpha = alpha
        self.reg = reg
        self.columns = columns

    # 1.2 Training function
    def fit(self, dataset):
        # 1.2.1 Save dataset
        self.dataset = dataset
        # 1.2.2 Calculate user average ratings
        self.users_ratings = dataset.groupby(self.columns[0]).agg({self.columns[1]: [list], self.columns[2]: [list]})
        # 1.2.3 Calculate item average ratings
        self.items_ratings = dataset.groupby(self.columns[1]).agg({self.columns[0]: [list], self.columns[2]: [list]})
        # 1.2.4 Calculate global average rating
        self.global_mean = self.dataset[self.columns[2]].mean()

        # 1.2.5 Initialize bu, bi parameters
        self.bu, self.bi = self.sgd()

    # 1.3 Define sgd algorithm
    '''
    Use SGD to optimize bu and bi
    '''
    def sgd(self):
        # 1.3.1 Initialize bu, bi dictionaries, all initial values are 0
        bu = dict(zip(self.users_ratings.index, np.zeros(len(self.users_ratings))))
        bi = dict(zip(self.items_ratings.index, np.zeros(len(self.items_ratings))))

        # 1.3.2 Iterate to optimize parameters
        for i in range(self.number_epochs):
            print("iter%d" % i)
            for uid, iid, real_rating in self.dataset.itertuples(index=False):
                # 1.3.3 Predict rating
                predict_rating = self.global_mean + bu[uid] + bi[iid]

                # Calculate error
                error = real_rating - predict_rating
                print("error:", error)

                # 1.3.4 Update bu and bi parameters using gradient descent
                bu[uid] += self.alpha * (error - self.reg * bu[uid])
                bi[iid] += self.alpha * (error - self.reg * bi[iid])

        return bu, bi

    # 1.4 Prediction function
    def predict(self, uid, iid):
        predict_rating = self.global_mean + self.bu.get(uid, 0) + self.bi.get(iid, 0)
        return predict_rating


if __name__ == '__main__':
    # 1. Define data types for loading the dataset
    dtype = [('userId', np.int32), ('movieId', np.int32), ('rating', np.float32)]

    # 2. Load dataset and specify columns to be used
    dataset = pd.read_csv("./data/ratings.csv",
                          usecols=range(3),
                          dtype=dict(dtype))

    # 3. Initialize baseline algorithm
    bcf = BaseLineCFBySGD(20, 0.1, 0.1, ['userId', 'movieId', 'rating'])

    # 4. Train the model
    bcf.fit(dataset)

    # 5. Predict interactively
    while True:
        uid = int(input("uid:"))
        iid = int(input("iid:"))
        print(bcf.predict(uid, iid))
