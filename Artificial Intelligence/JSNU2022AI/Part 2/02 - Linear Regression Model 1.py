'''
02 - Linear Regression Model 1
1. Data Collection
2. Basic Data Processing
   2.1 Dataset Splitting
3. Feature Engineering - Standardization
4. Model Training (Linear Regression)
5. Model Evaluation
'''

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge
from sklearn.metrics import mean_squared_error

# Linear Regression using LinearRegression
def linear_model1():
    # 1. Load dataset
    boston = load_boston()

    # 2. Split dataset into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(
        boston.data, boston.target, test_size=0.2
    )

    # 3. Feature scaling
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    # 4. Instantiate estimator and train
    estimator = LinearRegression()
    estimator.fit(x_train, y_train)
    print("Model intercept:\n", estimator.intercept_)

    # 5. Make predictions
    y_pre = estimator.predict(x_test)
    print("Predicted values:\n", y_pre)

    score = estimator.score(x_test, y_test)
    print("Model R² score:\n", score)

    # 6. Evaluate with Mean Squared Error
    ret = mean_squared_error(y_test, y_pre)
    print("Mean Squared Error:\n", ret)

# Linear Regression using SGDRegressor
def linear_model2():
    # 1. Load dataset
    boston = load_boston()

    # 2. Split dataset
    x_train, x_test, y_train, y_test = train_test_split(
        boston.data, boston.target, test_size=0.2
    )

    # 3. Feature scaling
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    # 4. Instantiate estimator
    estimator = SGDRegressor(max_iter=1000, learning_rate='constant', eta0=0.05)
    estimator.fit(x_train, y_train)
    print("Model intercept:\n", estimator.intercept_)

    # 5. Make predictions
    y_pre = estimator.predict(x_test)
    print("Predicted values:\n", y_pre)

    score = estimator.score(x_test, y_test)
    print("Model R² score:\n", score)

    ret = mean_squared_error(y_test, y_pre)
    print("Mean Squared Error:\n", ret)

# Linear Regression using Ridge Regularization
def linear_model3():
    # 1. Load dataset
    boston = load_boston()

    # 2. Split dataset
    x_train, x_test, y_train, y_test = train_test_split(
        boston.data, boston.target, test_size=0.2
    )

    # 3. Feature scaling
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    # 4. Instantiate estimator with alpha tuning
    estimator = Ridge(alpha=(0.001, 0.05, 0.1, 1, 10, 100))  # Accepts array for testing, will throw error if not looped
    estimator.fit(x_train, y_train)
    print("Model intercept:\n", estimator.intercept_)

    # 5. Make predictions
    y_pre = estimator.predict(x_test)
    print("Predicted values:\n", y_pre)

    score = estimator.score(x_test, y_test)
    print("Model R² score:\n", score)

    ret = mean_squared_error(y_test, y_pre)
    print("Mean Squared Error:\n", ret)

# Run the chosen model
if __name__ == "__main__":
    linear_model3()
