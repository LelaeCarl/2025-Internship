# 04 - Iris Classification using KNN

# Steps:
# 1. Load dataset
# 2. Data preprocessing
# 3. Feature engineering
# 4. Model training (Machine Learning)
# 5. Model evaluation

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # for standardization
from sklearn.neighbors import KNeighborsClassifier  # for KNN algorithm

# 1. Load dataset
iris = load_iris()

# 2. Data preprocessing
# 2.1 Split dataset into training/test sets (features and targets)
x_train, x_test, y_train, y_test = train_test_split(
    iris.data, iris.target,
    test_size=0.3, random_state=5
)

# 3. Feature engineering
# 3.1 Instantiate a scaler
transfer = StandardScaler()

# 3.2 Apply fit_transform to training set (fit and transform)
x_train = transfer.fit_transform(x_train)

# Standardize test set using the same scaler
x_test = transfer.fit_transform(x_test)

# 4. Model training (machine learning)
# 4.1 Instantiate a KNN classifier
estimator = KNeighborsClassifier(n_neighbors=3)

# 4.2 Train the model using training features and labels
estimator.fit(x_train, y_train)

# 5. Model evaluation
print(x_test)

# 5.1 Make predictions using the trained model
y_pre = estimator.predict(x_test)
print("Predicted labels:\n", y_pre)
print("Comparison with true labels:\n", y_pre == y_test)

# 5.2 Output the model's accuracy
ret = estimator.score(x_test, y_test)
print("Accuracy score:\n", ret)
