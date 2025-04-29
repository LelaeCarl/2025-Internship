'''
04 - Regression Model-based Collaborative Filtering - Baseline - Alternating Least Squares (ALS) Version 2
'''

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

class BaselineALSRegressor(object):
    '''
    ALS-based Regression Model for Collaborative Filtering
    '''

    def __init__(self, number_epochs=20, reg_bu=25, reg_bi=15, columns=['uid', 'iid', 'rating']):
        # Initialize hyperparameters
        self.number_epochs = number_epochs
        self.reg_bu = reg_bu
        self.reg_bi = reg_bi
        self.columns = columns

    def fit(self, dataset):
        '''
        Train the ALS model using the training dataset
        '''
        self.dataset = dataset
        self.global_mean = dataset[self.columns[2]].mean()

        # Precompute user and item grouped ratings
        self.users_ratings = dataset.groupby(self.columns[0]).agg({self.columns[1]: [list], self.columns[2]: [list]})
        self.items_ratings = dataset.groupby(self.columns[1]).agg({self.columns[0]: [list], self.columns[2]: [list]})

        # Initialize bias terms
        self.bu = dict(zip(self.users_ratings.index, np.zeros(len(self.users_ratings))))
        self.bi = dict(zip(self.items_ratings.index, np.zeros(len(self.items_ratings))))

        # Train using ALS
        self.training_losses = []
        for epoch in range(self.number_epochs):
            print(f"Epoch {epoch + 1}/{self.number_epochs}")

            # Update item biases
            for iid, row in self.items_ratings.iterrows():
                uids = row[(self.columns[0], 'list')]
                ratings = row[(self.columns[2], 'list')]
                error_sum = 0
                for uid, rating in zip(uids, ratings):
                    error_sum += rating - self.global_mean - self.bu.get(uid, 0)
                self.bi[iid] = error_sum / (self.reg_bi + len(uids))

            # Update user biases
            for uid, row in self.users_ratings.iterrows():
                iids = row[(self.columns[1], 'list')]
                ratings = row[(self.columns[2], 'list')]
                error_sum = 0
                for iid, rating in zip(iids, ratings):
                    error_sum += rating - self.global_mean - self.bi.get(iid, 0)
                self.bu[uid] = error_sum / (self.reg_bu + len(iids))

            # Calculate training RMSE after each epoch
            rmse = self.evaluate(self.dataset)
            self.training_losses.append(rmse)
            print(f"Training RMSE after epoch {epoch + 1}: {rmse:.4f}")

    def predict_single(self, uid, iid):
        '''
        Predict a single rating
        '''
        return self.global_mean + self.bu.get(uid, 0) + self.bi.get(iid, 0)

    def predict_batch(self, dataset):
        '''
        Predict multiple ratings for a dataset
        '''
        predictions = []
        for uid, iid, _ in dataset.itertuples(index=False):
            pred = self.predict_single(uid, iid)
            predictions.append(pred)
        return np.array(predictions)

    def evaluate(self, dataset):
        '''
        Evaluate the model using RMSE
        '''
        true_ratings = dataset[self.columns[2]].values
        pred_ratings = self.predict_batch(dataset)
        rmse = np.sqrt(np.mean((true_ratings - pred_ratings) ** 2))
        return rmse

    def plot_training_curve(self):
        '''
        Plot RMSE over training epochs
        '''
        plt.plot(range(1, self.number_epochs + 1), self.training_losses, marker='o')
        plt.title('Training RMSE Over Epochs')
        plt.xlabel('Epoch')
        plt.ylabel('RMSE')
        plt.grid()
        plt.show()


if __name__ == '__main__':
    # 1. Load dataset
    dtype = [('userId', np.int32), ('movieId', np.int32), ('rating', np.float32)]
    dataset = pd.read_csv('./data/ratings.csv', usecols=range(3), dtype=dict(dtype))

    # 2. Split into training and testing sets
    trainset, testset = train_test_split(dataset, test_size=0.2, random_state=42)

    # 3. Initialize ALS model
    model = BaselineALSRegressor(number_epochs=20, reg_bu=25, reg_bi=15, columns=['userId', 'movieId', 'rating'])

    # 4. Train model
    model.fit(trainset)

    # 5. Evaluate model
    train_rmse = model.evaluate(trainset)
    test_rmse = model.evaluate(testset)
    print(f"Final Train RMSE: {train_rmse:.4f}")
    print(f"Final Test RMSE: {test_rmse:.4f}")

    # 6. Plot training curve
    model.plot_training_curve()

    # 7. Interactive prediction
    while True:
        try:
            uid = int(input("Enter user ID (uid): "))
            iid = int(input("Enter item ID (iid): "))
            prediction = model.predict_single(uid, iid)
            print(f"Predicted rating: {prediction:.2f}")
        except Exception as e:
            print("Error:", e)
            break
