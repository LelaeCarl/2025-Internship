'''
05 - Latent Factor Model for Collaborative Filtering - LFM Model Implementation
'''

import numpy as np
import pandas as pd

'''
1. LFM Model Training
'''

class LFM(object):
    # 1.1 Initialization function
    def __init__(self, alpha, reg_p, reg_q,
                 number_LatentFactors=10,
                 number_epochs=10,
                 columns=['uid', 'iid', 'rating']):
        # Initialize hyperparameters
        self.alpha = alpha
        self.reg_p = reg_p
        self.reg_q = reg_q
        self.number_LatentFactors = number_LatentFactors
        self.number_epochs = number_epochs
        self.columns = columns

    # 1.2 Training function
    def fit(self, dataset):
        # 1.2.1 Save dataset
        self.dataset = pd.DataFrame(dataset)
        # 1.2.2 Group by user
        self.users_ratings = dataset.groupby(self.columns[0])\
            .agg({self.columns[1]: [list], self.columns[2]: [list]})
        # 1.2.3 Group by item
        self.items_ratings = dataset.groupby(self.columns[1])\
            .agg({self.columns[0]: [list], self.columns[2]: [list]})
        # 1.2.4 Calculate global mean
        self.global_mean = self.dataset[self.columns[2]].mean()
        # 1.2.5 Train latent factors P and Q
        self.P, self.Q = self.sgd()

    # 1.3 Initialize latent matrices
    def _init_matrix(self):
        # 1.3.1 User latent matrix P
        P = dict(zip(
            self.users_ratings.index,
            np.random.randn(len(self.users_ratings),
                            self.number_LatentFactors).astype(np.float32)
        ))

        # 1.3.2 Item latent matrix Q
        Q = dict(zip(
            self.items_ratings.index,
            np.random.randn(len(self.items_ratings),
                            self.number_LatentFactors).astype(np.float32)
        ))

        return P, Q

    # 1.4 SGD optimization
    def sgd(self):
        # 1.4.1 Initialize matrices
        P, Q = self._init_matrix()
        # 1.4.2 Initialize error list
        error_list = []

        # 1.4.3 Perform iterations
        for i in range(self.number_epochs):
            print(f"Epoch {i+1}/{self.number_epochs}")

            for uid, iid, real_rating in self.dataset.itertuples(index=False):
                v_pu = P[uid]
                v_qi = Q[iid]

                # 1.4.5 Calculate prediction error
                err = np.float32(real_rating - np.dot(v_pu, v_qi))

                # 1.4.6 Update user latent factor
                v_pu += self.alpha * (err * v_qi - self.reg_p * v_pu)

                # 1.4.7 Update item latent factor
                v_qi += self.alpha * (err * v_pu - self.reg_q * v_qi)

                # 1.4.8 Save updated factors
                P[uid] = v_pu
                Q[iid] = v_qi

                # 1.4.9 Record training error
                error_list.append(err ** 2)

            # Print RMSE at each iteration
            print("Training RMSE:", np.sqrt(np.mean(error_list)))

        return P, Q

    # 1.5 Prediction function
    def predict(self, uid, iid):
        # 1.5.1 If user or item not in training set, return global mean
        if uid not in self.users_ratings.index or iid not in self.items_ratings.index:
            return self.global_mean
        # 1.5.2 Get latent vectors
        p_u = self.P[uid]
        q_i = self.Q[iid]
        # 1.5.3 Return dot product
        return np.dot(p_u, q_i)

    # 1.6 Batch testing function
    def test(self, testset):
        for uid, iid, real_rating in testset.itertuples(index=False):
            try:
                predict_rating = self.predict(uid, iid)
            except Exception as e:
                print(e)
                predict_rating = self.global_mean
            yield uid, iid, real_rating, predict_rating


if __name__ == '__main__':
    # 1. Define the data reading format
    dtype = [('userId', np.int32),
             ('movieId', np.int32),
             ('rating', np.float32)]

    # 2. Load dataset
    dataset = pd.read_csv('./data/ratings.csv',
                          dtype=dict(dtype),
                          usecols=range(3))

    # 3. Initialize LFM model
    lfm = LFM(0.02, 0.01, 0.01, 10, 10,
              ['userId', 'movieId', 'rating'])

    # 4. Train model
    lfm.fit(dataset)

    # 5. Interactive prediction
    while True:
        uid = int(input("Enter user ID: "))
        iid = int(input("Enter item ID: "))
        print(lfm.predict(uid, iid))
