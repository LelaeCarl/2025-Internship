'''
01 - KNN Algorithm
'''

from sklearn.neighbors import KNeighborsClassifier

# Step 1: Prepare the data
x = [[1], [2], [0], [0]]  # Features
y = [1, 1, 0, 0]          # Labels

# Step 2: Machine learning
# 1. Instantiate a model
estimator = KNeighborsClassifier(n_neighbors=2)

# 2. Fit the model using training data
estimator.fit(x, y)

# 3. Use the trained model to make a prediction
ret = estimator.predict([[-1]])

print("KNN prediction result:", ret)
