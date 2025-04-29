'''
03 - Single Variable Function - Perceptron Training Process
'''

import numpy as np

# 1. Define the sigmoid activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# 2. Define the cost (loss) function
def cost(x, y, w):
    '''
    np.dot returns the dot product of arrays
    np.power raises each element to the specified power
    :param x: input values
    :param y: output values (targets)
    :param w: weight parameters
    :return: sum of squared error
    '''
    return np.sum(np.power((sigmoid(np.dot(x, w)) - y), 2))

# 3. Define the linear perceptron function
def linear_perceptron(x, y, w, learning_rate, epochs):
    # 3.1 Loop through epochs
    for i in range(epochs):
        # 3.2 Calculate the dot product of x and w
        z = np.dot(x, w)
        # 3.3 Apply the activation function
        a = sigmoid(z)
        # 3.4 Calculate the error between activation and true value
        e = a - y
        # 3.5 Update the weights based on error and learning rate
        w = w - learning_rate * np.dot(x.T, e)
        # 3.6 Calculate the cost
        cost_value = cost(x, y, w)
        # 3.7 Output the result for each epoch
        print("Epoch %d, cost %f" % (i, cost_value))
    # Return the updated weights after training
    return w

if __name__ == "__main__":
    # 1. Set hyperparameters
    learning_rate = 0.01  # Learning rate
    epochs = 500          # Maximum number of iterations

    # 2. Create input and output data
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 0, 0, 1])

    # 3. Initialize weights
    w = np.array([0.1, 0.1])

    # 4. Train the perceptron
    w = linear_perceptron(x, y, w, learning_rate, epochs)

    # 5. Output final weights
    print("Final result:\n", w)
