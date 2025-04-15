# 05 - Cross Validation and Grid Search

# Steps:
# 1. Load dataset
# 2. Data preprocessing
# 3. Feature engineering
# 4. Model training (with cross-validation)
# 5. Model evaluation

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# 1. Load dataset
iris = load_iris()

# 2. Data preprocessing
x_train, x_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2
)

# 3. Feature engineering
# 3.1 Instantiate a scaler
transfer = StandardScaler()

# 3.2 Standardize training and test data
x_train = transfer.fit_transform(x_train)
x_test = transfer.fit_transform(x_test)

# 4. Model training (with cross-validation and grid search)
# 4.1 Instantiate a model
estimator = KNeighborsClassifier()

# 4.2 Define grid search parameters
param_grid = {'n_neighbors': [1, 3, 5, 7, 9]}

'''
estimator: estimator object
param_grid: hyperparameter dictionary
cv: number of folds for cross-validation
fit: training data input
n_jobs: number of parallel jobs (1 means use 1 core, -1 means use all cores)
'''
estimator = GridSearchCV(
    estimator, param_grid=param_grid, cv=10, n_jobs=1
)

# 4.3 Fit model
estimator.fit(x_train, y_train)

# 5. Model evaluation
# 5.1 Predict and compare with true values
y_pre = estimator.predict(x_test)
print("Predicted values:\n", y_pre)
print("Comparison with true values:\n", y_pre == y_test)

# 5.2 Output accuracy
ret = estimator.score(x_test, y_test)
print("Accuracy score:\n", ret)

# 5.3 Other evaluation metrics
print("Best model:\n", estimator.best_estimator_)
print("Best score (from CV):\n", estimator.best_score_)
print("Grid scores for each parameter setting:\n", estimator.cv_results_)
