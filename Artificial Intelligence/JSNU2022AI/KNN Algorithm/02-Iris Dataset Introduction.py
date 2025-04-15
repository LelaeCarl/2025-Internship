'''
02-Iris Dataset Introduction
'''

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_iris, fetch_20newsgroups
from sklearn.model_selection import train_test_split

# 1. Load dataset
# 1.1 Load small dataset
iris = load_iris()

# 1.2 Load large dataset (optional)
# news = fetch_20newsgroups()
# print(news)

# 2. View dataset
# print("Iris dataset feature values:\n", iris.data)
# print("Iris dataset target values:\n", iris['target'])
# print("Iris dataset feature names:\n", iris.feature_names)
# print("Iris dataset target names:\n", iris.target_names)
# print("Iris dataset description:\n", iris.DESCR)

# 3. Data visualization
# 3.1 Convert data to DataFrame
iris_data = pd.DataFrame(data=iris.data,
                         columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])

# 3.2 Add target to DataFrame
iris_data['target'] = iris.target
print(iris_data)

# 4. Plotting function for visualization
def iris_plot(data, col1, col2):
    # 1. Create scatterplot
    sns.lmplot(x=col1, y=col2, data=data, hue='target', fit_reg=False)

    # 2. Add plot title
    plt.title("Iris dataset visualization")

    # 3. Set axis labels
    plt.xlabel(col1)
    plt.ylabel(col2)

    # 4. Set font
    plt.rcParams['font.sans-serif'] = ['SimHei']  # For Chinese support, optional
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()

# Examples (commented out)
# iris_plot(iris_data, "sepal_length", "petal_width")
# iris_plot(iris_data, "sepal_length", "petal_length")
# iris_plot(iris_data, "sepal_width", "petal_length")

# 5. Train-test split
'''
test_size=0.2  # 20% test data
random_state=2  # Random seed
'''
x_train, x_test, y_train, y_test = \
    train_test_split(iris_data, iris.target, test_size=0.2)

print("Training features:\n", x_train)
print("Test features:\n", x_test)
print("Training labels:\n", y_train)
print("Test labels:\n", y_test)

print("Shape of training labels:\n", y_train.shape)
print("Shape of test labels:\n", y_test.shape)

# Try different random states
x_train1, x_test1, y_train1, y_test1 = \
    train_test_split(iris_data, iris.target, test_size=0.2, random_state=5)

x_train2, x_test2, y_train2, y_test2 = \
    train_test_split(iris_data, iris.target, test_size=0.2, random_state=6)

x_train2, x_test2, y_train2, y_test2 = \
    train_test_split(iris_data, iris.target, test_size=0.2, random_state=1)

print("Test labels 1:\n", y_test1)
print("Test labels 2:\n", y_test2)
