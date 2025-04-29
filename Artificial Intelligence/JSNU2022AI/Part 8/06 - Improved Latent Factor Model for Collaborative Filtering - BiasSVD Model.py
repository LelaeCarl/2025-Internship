'''
06 - Improved Latent Factor Model for Collaborative Filtering - BiasSVD Model
'''

import pandas as pd
import numpy as np

'''
1. BiasSVD Model
'''

class BiasSVD(object):
    # 1.1 Initialization
    def __init__(self, alpha, reg_p, reg_q,
                 reg_bu, reg_bi, number_LatentFactors,
                 number_epochs,
                 columns=['uid', 'iid', 'rating']):
        # 1.1.1 Set hyperparameters
        self.alpha = alpha
        self.reg_p = reg_p
        self.reg_q = reg_q
        self.reg_bu = reg_bu
        self.reg_bi = reg_bi
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
        # 1.2.4 Calculate global mean rating
        self.global_mean = self.dataset[self.columns[2]].mean()
        # 1.2.5 Train P, Q, bu, bi using SGD
        self.P, self.Q, self.bu, self.bi = self.sgd()

    # 1.3 Initialize matrices P and Q
    def _init_matrix(self):
        # 1.3.1 Initialize user latent matrix P
        P = dict(zip(
            self.users_ratings.index,
            np.random.randn(len(self.users_ratings),
                            self.number_LatentFactors).astype(np.float32)
        ))

        # 1.3.2 Initialize item latent matrix Q
        Q = dict(zip(
            self.items_ratings.index,
            np.random.randn(len(self.items_ratings),
                            self.number_LatentFactors).astype(np.float32)
        ))

        return P, Q

    # 1.4 SGD Optimization
    def sgd(self):
        # 1.4.1 Initialize latent matrices
        P, Q = self._init_matrix()
        # 1.4.2 Initialize bu and bi
        bu = dict(zip(self.users_ratings.index, np.zeros(len(self.users_ratings))))
        bi = dict(zip(self.items_ratings.index, np.zeros(len(self.items_ratings))))
        # 1.4.3 Initialize error list
        error_list = []

        # 1.4.4 Loop through epochs
        for i in range(self.number_epochs):
            print(f"Epoch {i+1}/{self.number_epochs}")

            for uid, iid, r_ui in self.dataset.itertuples(index=False):
                v_pu = P[uid]
                v_qi = Q[iid]

                # 1.4.6 Calculate prediction error
                err = np.float32(
                    r_ui - self.global_mean - bu[uid] - bi[iid] - np.dot(v_pu, v_qi)
                )

                # 1.4.7 Update user latent vector
                v_pu += self.alpha * (err * v_qi - self.reg_p * v_pu)

                # 1.4.8 Update item latent vector
                v_qi += self.alpha * (err * v_pu - self.reg_q * v_qi)

                # 1.4.9 Update user and item biases
                bu[uid] += self.alpha * (err - self.reg_bu * bu[uid])
                bi[iid] += self.alpha * (err - self.reg_bi * bi[iid])

                # 1.4.10 Record squared error
                error_list.append(err ** 2)

            # 1.4.11 Print RMSE for this epoch
            print("Training RMSE:", np.sqrt(np.mean(error_list)))

        return P, Q, bu, bi

    # 1.5 Prediction function
    def predict(self, uid, iid):
        # 1.5.1 Handle unseen users or items
        if uid not in self.users_ratings.index or iid not in self.items_ratings.index:
            return self.global_mean

        # 1.5.2 Retrieve user and item latent vectors
        p_u = self.P[uid]
        q_i = self.Q[iid]

        # 1.5.3 Compute prediction
        return self.global_mean + self.bu[uid] + self.bi[iid] + np.dot(p_u, q_i)


if __name__ == '__main__':
    # 1. Define data types
    dtype = [('userId', np.int32),
             ('movieId', np.int32),
             ('rating', np.float32)]

    # 2. Load dataset
    dataset = pd.read_csv('./data/ratings.csv',
                          usecols=range(3),
                          dtype=dict(dtype))

    # 3. Initialize model
    bsvd = BiasSVD(0.02, 0.01, 0.01, 0.01, 0.01, 10, 20,
                   ['userId', 'movieId', 'rating'])

    # 4. Train model
    bsvd.fit(dataset)

    # 5. Interactive prediction
    while True:
        uid = int(input("Enter user ID: "))
        iid = int(input("Enter item ID: "))
        print(bsvd.predict(uid, iid))
