'''
01 - Tumor Classification Prediction
1. Data Collection
2. Basic Data Preprocessing
   2.1 Handling Missing Values
   2.2 Confirming Features and Labels
   2.3 Splitting the Dataset
3. Feature Engineering (Standardization)
4. Model Training (Logistic Regression)
5. Model Evaluation
'''
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression  # Logistic Regression
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score

# 1. Load the dataset
names = ['Sample code number',
         'Clump Thickness',
         'Uniformity of Cell Size',
         'Uniformity of Cell Shape',
         'Marginal Adhesion',
         'Single Epithelial Cell Size',
         'Bare Nuclei',
         'Bland Chromatin',
         'Normal Nucleoli',
         'Mitoses',
         'Class']
data = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/"
                   "breast-cancer-wisconsin/breast-cancer-wisconsin.data",
                   names=names)

# 2. Basic Data Preprocessing

# 2.1 Handle Missing Values: replace "?" with np.nan and drop rows with NaNs
data = data.replace(to_replace="?", value=np.nan)
data = data.dropna()

# View dataset summary
print(data.describe())

# 2.2 Confirm Features and Labels
# iloc: slice by row/column positions
# All rows, columns 1 to -1 (exclude first and last columns)
x = data.iloc[:, 1:-1]
# print(x.head(10))

# Confirm labels
y = data['Class']

# 2.3 Split dataset
# random_state: for reproducibility; ensures same split each time
# test_size: percentage of test data
x_train, x_test, y_train, y_test = train_test_split(
    x, y, random_state=2, test_size=0.2)

# 3. Feature Engineering (Standardization)
transfer = StandardScaler()
x_train = transfer.fit_transform(x_train)
x_test = transfer.fit_transform(x_test)

# 4. Model Training (Logistic Regression)
estimator = LogisticRegression()
estimator.fit(x_train, y_train)

# 5. Model Evaluation

# 5.1 Basic accuracy (evaluate predictions on test set)
y_pre = estimator.predict(x_test)
print("Predicted values:\n", y_pre)

# Compare predictions to ground truth
score = estimator.score(x_test, y_test)
print("Accuracy:\n", score)

# 5.2 Other metrics
ret = classification_report(y_test, y_pre, labels=[2, 4],
                            target_names=['Benign', 'Malignant'])
print("Other metrics:\n", ret)

# Additional: Handling imbalanced binary classification
y_test = np.where(y_test > 3, 1, 0)
yt = roc_auc_score(y_true=y_test, y_score=y_pre)
print("AUC Score for imbalanced binary classification:\n", yt)
