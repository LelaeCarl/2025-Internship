'''
Baseline algorithm based on Matrix Factorization - SGD Implementation
'''

import pandas as pd
import numpy as np

'''
1. Matrix Factorization - SGD Implementation
'''

class MatrixFactorizationBySGD(object):
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
        # 1.2.2 Calculate global mean rating
        self.global_mean = dataset[self.columns[2]].mean()

        # 1.2.3 Initialize parameters p, q, bu, bi
        self.p, self.q, self.bu, self.bi = self.sgd()

    '''
    1.3 SGD Optimization
    '''
    def sgd(self):
        # 1.3.1 Initialize bu, bi
        bu = dict(zip(self.dataset[self.columns[0]].unique(), np.zeros(len(self.dataset[self.columns[0]].unique()))))
        bi = dict(zip(self.dataset[self.columns[1]].unique(), np.zeros(len(self.dataset[self.columns[1]].unique()))))

        # 1.3.2 Initialize latent vectors p, q
        p = dict(zip(self.dataset[self.columns[0]].unique(), np.random.randn(len(self.dataset[self.columns[0]].unique()), 5)))
        q = dict(zip(self.dataset[self.columns[1]].unique(), np.random.randn(len(self.dataset[self.columns[1]].unique()), 5)))

        # 1.3.3 Optimize parameters
        for i in range(self.number_epochs):
            print("iter%d" % i)
            for uid, iid, real_rating in self.dataset.itertuples(index=False):
                predict_rating = self.global_mean + bu[uid] + bi[iid] + np.dot(p[uid], q[iid])

                error = real_rating - predict_rating

                bu[uid] += self.alpha * (error - self.reg * bu[uid])
                bi[iid] += self.alpha * (error - self.reg * bi[iid])

                p[uid] += self.alpha * (error * q[iid] - self.reg * p[uid])
                q[iid] += self.alpha * (error * p[uid] - self.reg * q[iid])

        return p, q, bu, bi

    # 1.4 Predict function
    def predict(self, uid, iid):
        # If uid or iid not exist, use global mean
        if uid not in self.p:
            predict_rating = self.global_mean
        elif iid not in self.q:
            predict_rating = self.global_mean
        else:
            predict_rating = self.global_mean + self.bu[uid] + self.bi[iid] + np.dot(self.p[uid], self.q[iid])
        return predict_rating

'''
2. Model Evaluation
'''

def predict_all(model, testset):
    predicts = []
    for uid, iid, real_rating in testset.itertuples(index=False):
        try:
            predict_rating = model.predict(uid, iid)
        except Exception as e:
            predict_rating = model.global_mean
        predicts.append([uid, iid, real_rating, predict_rating])
    return predicts

def RMSE(predicts):
    sum_ = 0
    n = 0
    for uid, iid, real_rating, pred_rating in predicts:
        sum_ += (real_rating - pred_rating) ** 2
        n += 1
    return np.sqrt(sum_ / n)

def MAE(predicts):
    sum_ = 0
    n = 0
    for uid, iid, real_rating, pred_rating in predicts:
        sum_ += np.abs(real_rating - pred_rating)
        n += 1
    return sum_ / n

'''
3. Plot error graph
'''

import matplotlib.pyplot as plt

def draw_rmse_mae_curve(train_losses, test_losses, metric_name='RMSE'):
    plt.plot(range(len(train_losses)), train_losses, label='train_%s' % metric_name)
    plt.plot(range(len(test_losses)), test_losses, label='test_%s' % metric_name)
    plt.xlabel('epoch')
    plt.ylabel(metric_name)
    plt.legend()
    plt.title(metric_name + ' Curve')
    plt.show()

'''
4. Main Function
'''

if __name__ == '__main__':
    # 1. Load dataset
    dataset = pd.read_csv("./data/ratings.csv", usecols=range(3))

    # 2. Split train and test set
    from sklearn.model_selection import train_test_split
    trainset, testset = train_test_split(dataset, test_size=0.25)

    # 3. Initialize matrix factorization model
    mf = MatrixFactorizationBySGD(20, 0.01, 0.01, ['userId', 'movieId', 'rating'])

    # 4. Train model
    mf.fit(trainset)

    # 5. Predict all
    predicts = predict_all(mf, testset)

    # 6. Print RMSE
    print("RMSE:", RMSE(predicts))
    print("MAE:", MAE(predicts))
