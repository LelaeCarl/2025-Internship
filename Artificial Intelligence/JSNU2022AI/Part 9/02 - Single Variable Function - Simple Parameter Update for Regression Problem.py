'''
02 - Single Variable Function - Simple Parameter Update for Regression Problem
'''

import numpy as np

# 1. Define input X and output Y
# X are input values, Y are output values
X = np.array([[1, 2], [3, 4], [5, 6]])
Y = np.array([2, 4, 6])

# 2. Define initial weights
weights = np.array([0.5, 0.5])

# 3. Define initial bias
bias = 1

# 4. Calculate the output using the weight function
# outputs are the predicted values after calculation
outputs = np.dot(X, weights) + bias

print("The prediction results are:\n", outputs)

# 5. Calculate the error
# Y is the true value, outputs is the predicted value
error = Y - outputs

# 6. Update weights based on the error
weights = weights + 0.1 * np.dot(X.T, error)
print("The updated weights are:\n", weights)

# 7. Update bias based on the error
bias = bias + 0.1 * np.sum(error)
print("The updated bias is:\n", bias)
