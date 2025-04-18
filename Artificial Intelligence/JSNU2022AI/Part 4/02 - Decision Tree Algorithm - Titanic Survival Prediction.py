# 02 - Decision Tree Algorithm - Titanic Survival Prediction

# 1. Import libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier, export_graphviz

# 2. Load dataset
data = pd.read_csv("./data/titanic.csv")

# Optional: View data structure
# print(data.describe())

# 3. Basic data processing
# 3.1 Define feature columns and target column
# Features: 'pclass', 'age', 'sex'
# Target: 'survived'
x = data[['pclass', 'age', 'sex']]
y = data['survived']

# 3.2 Handle missing values
# Fill missing values in 'age' with the mean
x['age'].fillna(value=data['age'].mean(), inplace=True)

# 3.3 Split the dataset
x_train, x_test, y_train, y_test = train_test_split(
    x, y, random_state=22, test_size=0.2)

# 4. Feature Engineering – Dictionary-based feature extraction (One-hot encoding)
# Convert to dictionaries
x_train = x_train.to_dict(orient='records')
x_test = x_test.to_dict(orient='records')

# Apply DictVectorizer
transfer = DictVectorizer()
x_train = transfer.fit_transform(x_train)
x_test = transfer.transform(x_test)

# 5. Model training – Decision Tree
estimator = DecisionTreeClassifier(max_depth=5)
estimator.fit(x_train, y_train)

# 6. Model evaluation
# Predict
y_pred = estimator.predict(x_test)
print("Predicted values:\n", y_pred)

# Accuracy
accuracy = estimator.score(x_test, y_test)
print("Accuracy:\n", accuracy)

# 7. Visualize the decision tree
export_graphviz(
    estimator,
    out_file='./data/tree.dot',
    feature_names=[
        'age', 'pclass=1st', 'pclass=2nd', 'pclass=3rd',
        'female', 'male'
    ]
)
