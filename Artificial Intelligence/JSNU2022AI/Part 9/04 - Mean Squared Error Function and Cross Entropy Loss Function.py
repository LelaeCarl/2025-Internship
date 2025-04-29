'''
04 - Mean Squared Error Function and Cross Entropy Loss Function
'''

import numpy as np

# 1. Define Mean Squared Error (MSE) loss function
# y_true: true values
# y_pred: predicted values
def loss_mse(y_true, y_pred):
    # Calculate the mean of squared differences (true - predicted)
    mse_loss = np.mean(np.power(y_true - y_pred, 2))
    # Return loss value
    return mse_loss

# 2. Define Cross Entropy (CE) loss function
def loss_ce(y_true, y_pred):
    # Calculate the cross entropy between true and predicted values
    ce_loss = np.mean(np.sum(
        np.multiply(y_true, np.log(y_pred)), axis=1))
    return ce_loss

if __name__ == "__main__":
    '''
    1. Call Mean Squared Error Loss Function
    '''
    y_true = np.array([1, 2, 3, 4, 5])
    y_pred = np.array([1.5, 2, 3, 4.5, 5])

    # Call the MSE loss function
    mse_loss = loss_mse(y_true, y_pred)
    print("Mean Squared Error (MSE) loss value:", mse_loss)

    '''
    2. Call Cross Entropy Loss Function
    '''
    y_true = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    y_pred = np.array([[0.6, 0.2, 0.2],
                       [0.2, 0.3, 0.5],
                       [0.3, 0.3, 0.4]])

    # Call the Cross Entropy loss function
    ce_loss = loss_ce(y_true, y_pred)
    print("Cross Entropy (CE) loss value:", ce_loss)
